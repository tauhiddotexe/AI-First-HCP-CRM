from typing import Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.base import BaseModel

ModelType = TypeVar('ModelType', bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get(self, id: str) -> ModelType | None:
        result = await self.session.execute(
            select(self.model).where(
                self.model.id == id,
                self.model.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def list(self, offset: int = 0, limit: int = 20, **filters) -> tuple[list[ModelType], int]:
        query = select(self.model).where(self.model.deleted_at.is_(None))
        count_query = select(func.count()).select_from(self.model).where(self.model.deleted_at.is_(None))

        for field, value in filters.items():
            if value is not None and hasattr(self.model, field):
                query = query.where(getattr(self.model, field) == value)
                count_query = count_query.where(getattr(self.model, field) == value)

        total = (await self.session.execute(count_query)).scalar() or 0
        result = await self.session.execute(
            query.order_by(self.model.created_at.desc()).offset(offset).limit(limit)
        )
        return list(result.scalars().all()), total

    async def update(self, id: str, **kwargs) -> ModelType | None:
        instance = await self.get(id)
        if not instance:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(instance, key):
                setattr(instance, key, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id: str) -> bool:
        from datetime import datetime, timezone
        instance = await self.get(id)
        if not instance:
            return False
        instance.deleted_at = datetime.now(timezone.utc)
        await self.session.commit()
        return True
