from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.hcp import HCP
from app.repositories.base import BaseRepository


class HCPRepository(BaseRepository[HCP]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, HCP)

    async def find_by_name(self, name: str) -> HCP | None:
        cleaned = name.replace('Dr. ', '').replace('Dr ', '').strip()
        parts = cleaned.split(' ', 1)
        first_name = parts[0] if parts else ''
        last_name = parts[1] if len(parts) > 1 else ''

        stmt = select(HCP).where(HCP.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        hcps = list(result.scalars().all())

        for hcp in hcps:
            if first_name.lower() in hcp.first_name.lower() or last_name.lower() in hcp.last_name.lower():
                return hcp
        return None

    async def search(self, query: str) -> list[HCP]:
        pattern = f'%{query}%'
        stmt = (
            select(HCP)
            .where(HCP.deleted_at.is_(None))
            .where(
                HCP.first_name.ilike(pattern) |
                HCP.last_name.ilike(pattern) |
                HCP.hospital.ilike(pattern)
            )
            .order_by(HCP.first_name)
            .limit(20)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
