from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.repositories.hcp import HCPRepository
from app.schemas.hcp import HCPCreate, HCPUpdate


class HCPService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.repo = HCPRepository(session)

    async def list_hcps(self):
        items, total = await self.repo.list()
        return items, total

    async def get_hcp(self, hcp_id: str):
        return await self.repo.get(hcp_id)

    async def create_hcp(self, data: HCPCreate):
        return await self.repo.create(**data.model_dump())

    async def update_hcp(self, hcp_id: str, data: HCPUpdate):
        return await self.repo.update(hcp_id, **data.model_dump(exclude_none=True))

    async def search_hcps(self, query: str):
        return await self.repo.search(query)
