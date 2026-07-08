from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.interaction import Interaction
from app.repositories.base import BaseRepository


class InteractionRepository(BaseRepository[Interaction]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Interaction)

    async def list_filtered(
        self,
        user_id: str | None = None,
        hcp_id: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        interaction_type: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Interaction], int]:
        conditions = [Interaction.deleted_at.is_(None)]
        if user_id:
            conditions.append(Interaction.user_id == user_id)
        if hcp_id:
            conditions.append(Interaction.hcp_id == hcp_id)
        if date_from:
            conditions.append(Interaction.interaction_date >= date_from)
        if date_to:
            conditions.append(Interaction.interaction_date <= date_to)
        if interaction_type:
            conditions.append(Interaction.interaction_type == interaction_type)

        query = select(Interaction).where(and_(*conditions))
        count_query = select(func.count()).select_from(Interaction).where(and_(*conditions))

        total = (await self.session.execute(count_query)).scalar() or 0
        offset = (page - 1) * limit
        result = await self.session.execute(
            query.order_by(Interaction.interaction_date.desc()).offset(offset).limit(limit)
        )
        return list(result.scalars().all()), total
