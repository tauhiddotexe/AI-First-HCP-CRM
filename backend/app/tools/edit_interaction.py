from datetime import date
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.interaction import Interaction
from app.repositories.interaction import InteractionRepository
from app.repositories.hcp import HCPRepository


async def execute_edit_interaction(
    session: AsyncSession,
    interaction_id: str,
    entities: dict,
) -> dict:
    repo = InteractionRepository(session)
    interaction = None

    if interaction_id:
        interaction = await repo.get(interaction_id)

    if not interaction:
        hcp_name = entities.get('hcp_name', '')
        if hcp_name:
            hcp = await HCPRepository(session).find_by_name(hcp_name)
            if hcp:
                stmt = (
                    select(Interaction)
                    .where(Interaction.hcp_id == hcp.id, Interaction.deleted_at.is_(None))
                    .order_by(desc(Interaction.created_at))
                    .limit(1)
                )
                result = await session.execute(stmt)
                interaction = result.scalar_one_or_none()

    if not interaction:
        return {'error': 'No interaction found to edit. Please specify an HCP name or provide an interaction ID.'}

    interaction_id = str(interaction.id)
    updates = {}

    raw_date = entities.get('date')
    if raw_date:
        try:
            updates['interaction_date'] = date.fromisoformat(raw_date)
        except (ValueError, TypeError):
            pass
    if entities.get('interaction_type'):
        updates['interaction_type'] = entities['interaction_type']
    if entities.get('sentiment'):
        updates['sentiment'] = entities['sentiment']
    if entities.get('summary'):
        updates['summary'] = entities['summary']
    if entities.get('outcome'):
        updates['outcome'] = entities['outcome']

    if updates:
        for key, value in updates.items():
            setattr(interaction, key, value)
        await session.commit()

    return {
        'interaction_id': interaction_id,
        'updated_fields': list(updates.keys()),
        'status': 'updated',
    }
