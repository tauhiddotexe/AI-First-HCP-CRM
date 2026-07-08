from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_session
from app.models.chat_message import ChatMessage

router = APIRouter(prefix='/chat', tags=['Chat'])


@router.get('/{interaction_id}')
async def get_chat_history(
    interaction_id: str,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(ChatMessage)
        .where(
            ChatMessage.interaction_id == interaction_id,
            ChatMessage.deleted_at.is_(None),
        )
        .order_by(ChatMessage.created_at.asc())
    )
    return result.scalars().all()
