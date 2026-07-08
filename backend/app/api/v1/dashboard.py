from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.session import get_session
from app.models.interaction import Interaction
from app.models.hcp import HCP
from app.models.follow_up import FollowUp

router = APIRouter(prefix='/dashboard', tags=['Dashboard'])


@router.get('')
async def dashboard_stats(session: AsyncSession = Depends(get_session)):
    total_interactions = (
        await session.execute(
            select(func.count()).select_from(Interaction).where(Interaction.deleted_at.is_(None))
        )
    ).scalar() or 0

    pending_followups = (
        await session.execute(
            select(func.count())
            .select_from(FollowUp)
            .where(FollowUp.status == 'pending')
        )
    ).scalar() or 0

    hcp_count = (
        await session.execute(
            select(func.count()).select_from(HCP).where(HCP.deleted_at.is_(None))
        )
    ).scalar() or 0

    return {
        'total_interactions': total_interactions,
        'pending_followups': pending_followups,
        'hcp_count': hcp_count,
    }
