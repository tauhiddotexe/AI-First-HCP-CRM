from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_session
from app.models.follow_up import FollowUp
from app.schemas.common import SuccessResponse
from app.core.exceptions import NotFoundError
from pydantic import BaseModel

router = APIRouter(prefix='/followups', tags=['Follow-ups'])


class FollowUpCreate(BaseModel):
    interaction_id: str
    action: str
    follow_up_date: str | None = None
    status: str = 'pending'


class FollowUpUpdate(BaseModel):
    action: str | None = None
    follow_up_date: str | None = None
    status: str | None = None


@router.get('')
async def list_followups(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(FollowUp).where(FollowUp.deleted_at.is_(None)).order_by(FollowUp.created_at.desc())
    )
    return result.scalars().all()


@router.post('', status_code=201)
async def create_followup(data: FollowUpCreate, session: AsyncSession = Depends(get_session)):
    fu = FollowUp(**data.model_dump())
    session.add(fu)
    await session.commit()
    await session.refresh(fu)
    return fu


@router.patch('/{followup_id}')
async def update_followup(
    followup_id: str,
    data: FollowUpUpdate,
    session: AsyncSession = Depends(get_session),
):
    fu = await session.get(FollowUp, followup_id)
    if not fu or fu.deleted_at:
        raise NotFoundError('Follow-up not found')
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(fu, key, value)
    await session.commit()
    await session.refresh(fu)
    return fu
