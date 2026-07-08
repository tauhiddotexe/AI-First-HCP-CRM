from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database.session import get_session
from app.graph.state import GraphState
from app.models.interaction import Interaction
from app.repositories.hcp import HCPRepository
from app.tools.log_interaction import execute_log_interaction
from app.tools.edit_interaction import execute_edit_interaction
from app.tools.retrieve_history import execute_retrieve_history
from app.tools.suggest_next_action import execute_suggest_next_action
from app.tools.generate_summary import execute_generate_summary


async def _fetch_hcp_interactions(session: AsyncSession, hcp_name: str, limit: int = 10) -> list:
    if not hcp_name or not session:
        return []
    hcp = await HCPRepository(session).find_by_name(hcp_name)
    if not hcp:
        return []
    hcp_full_name = f'{hcp.first_name} {hcp.last_name}'
    result = await session.execute(
        select(Interaction)
        .where(Interaction.hcp_id == hcp.id, Interaction.deleted_at.is_(None))
        .order_by(desc(Interaction.interaction_date), desc(Interaction.created_at))
        .limit(limit)
    )
    return [
        {
            'id': str(ix.id),
            'hcp': hcp_full_name,
            'date': ix.interaction_date.isoformat() if ix.interaction_date else '',
            'type': ix.interaction_type,
            'summary': ix.summary or '',
            'sentiment': ix.sentiment or '',
        }
        for ix in result.scalars().all()
    ]


async def tool_execution_node(
    state: GraphState,
    session: AsyncSession | None = None,
    user_id: str = 'demo-rep-001',
) -> dict:
    tool = state.get('selected_tool', '')
    entities = state.get('entities', {})
    metadata = state.get('metadata', {})
    errors = state.get('errors') or []

    if not entities.get('hcp_name'):
        last_hcp = metadata.get('last_hcp_name', '')
        if last_hcp:
            entities['hcp_name'] = last_hcp

    if not tool or tool == 'GeneralChat':
        return {'tool_result': {'message': 'General conversation - no tool needed'}}

    try:
        if tool == 'LogInteraction':
            result = await execute_log_interaction(session, entities, user_id)
        elif tool == 'EditInteraction':
            interaction_id = state.get('metadata', {}).get('interaction_id', '')
            result = await execute_edit_interaction(session, interaction_id, entities)
        elif tool == 'RetrieveHistory':
            hcp_name = entities.get('hcp_name', '')
            result = await execute_retrieve_history(session, hcp_name=hcp_name)
        elif tool == 'NextBestAction':
            hcp_name = entities.get('hcp_name', '')
            history = await _fetch_hcp_interactions(session, hcp_name)
            result = await execute_suggest_next_action(history=history)
        elif tool == 'VisitSummary':
            hcp_name = entities.get('hcp_name', '')
            history = await _fetch_hcp_interactions(session, hcp_name)
            interaction = history[0] if history else {}
            result = await execute_generate_summary(interaction=interaction, history=history)
        else:
            result = {'message': f'Unknown tool: {tool}'}

        return {'tool_result': result}

    except Exception as e:
        import logging
        logging.getLogger('uvicorn.error').exception('Tool execution error: %s', e)
        return {
            'tool_result': {'error': 'An unexpected error occurred while processing your request. Please try again.'},
            'errors': [*errors, f'Internal tool execution error: {e}'],
        }