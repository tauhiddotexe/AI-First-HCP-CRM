from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.interaction import Interaction
from app.repositories.hcp import HCPRepository


async def execute_retrieve_history(
    session: AsyncSession,
    hcp_name: str = '',
    limit: int = 5,
) -> dict:
    if not hcp_name:
        return {'error': 'No HCP name provided'}

    hcp = await HCPRepository(session).find_by_name(hcp_name)

    if not hcp:
        return {'error': f'HCP "{hcp_name}" not found'}

    interactions_result = await session.execute(
        select(Interaction)
        .where(
            Interaction.hcp_id == hcp.id,
            Interaction.deleted_at.is_(None),
        )
        .order_by(Interaction.interaction_date.desc(), Interaction.created_at.desc())
        .limit(limit)
    )
    interactions = interactions_result.scalars().all()

    if not interactions:
        return {'message': f'No previous interactions found for {hcp_name}', 'interactions': []}

    history = []
    for ix in interactions:
        history.append({
            'id': ix.id,
            'date': ix.interaction_date.isoformat() if ix.interaction_date else '',
            'type': ix.interaction_type,
            'summary': ix.summary or '',
            'sentiment': ix.sentiment or '',
        })

    return {
        'hcp': f'{hcp.first_name} {hcp.last_name}',
        'interaction_count': len(history),
        'interactions': history,
    }
