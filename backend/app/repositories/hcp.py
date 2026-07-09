from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.hcp import HCP
from app.repositories.base import BaseRepository


class HCPRepository(BaseRepository[HCP]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, HCP)

    async def _parse_name(self, name: str) -> tuple[str, str]:
        cleaned = name.replace('Dr. ', '').replace('Dr ', '').strip()
        parts = cleaned.split(' ', 1)
        if len(parts) == 1:
            return '', parts[0].lower()
        return (parts[0].lower() if parts else ''), (parts[1].lower() if len(parts) > 1 else '')

    async def _load_all(self) -> list[HCP]:
        result = await self.session.execute(select(HCP).where(HCP.deleted_at.is_(None)))
        return list(result.scalars().all())

    async def find_by_name(self, name: str) -> HCP | None:
        first_name, last_name = await self._parse_name(name)
        hcps = await self._load_all()

        if first_name and last_name:
            for hcp in hcps:
                if first_name == hcp.first_name.lower() and last_name == hcp.last_name.lower():
                    return hcp
            return None

        word = last_name or first_name
        if word:
            matching = [h for h in hcps if word == h.last_name.lower()]
            if len(matching) == 1:
                return matching[0]

        return None

    async def find_all_by_name(self, name: str) -> list[HCP]:
        first_name, last_name = await self._parse_name(name)
        hcps = await self._load_all()

        if first_name and last_name:
            exact = [h for h in hcps if first_name == h.first_name.lower() and last_name == h.last_name.lower()]
            if exact:
                return exact

        if last_name:
            by_last = [h for h in hcps if last_name == h.last_name.lower()]
            if by_last:
                return by_last
            return [h for h in hcps if last_name == h.first_name.lower()]

        if first_name:
            by_first = [h for h in hcps if first_name == h.first_name.lower()]
            if by_first:
                return by_first
            return [h for h in hcps if first_name == h.last_name.lower()]

        return []

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
