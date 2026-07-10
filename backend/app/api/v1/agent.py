import re
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.schemas.common import SuccessResponse
from app.graph.graph import agent_graph
from app.graph.state import GraphState
from app.database.session import get_session
from app.core.dependencies import get_current_user_id
from app.graph.nodes.tool_execution import tool_execution_node
from app.graph.nodes.response_generator import response_generator_node
from app.models.interaction import Interaction


async def _fetch_form_data(session: AsyncSession, interaction_id: str) -> dict:
    if not interaction_id:
        return {}
    result = await session.execute(
        select(Interaction)
        .options(
            selectinload(Interaction.discussion_topics),
            selectinload(Interaction.products_discussed),
            selectinload(Interaction.materials_shared),
            selectinload(Interaction.samples_distributed),
            selectinload(Interaction.follow_ups),
            selectinload(Interaction.hcp),
        )
        .where(Interaction.id == interaction_id, Interaction.deleted_at.is_(None))
    )
    ix = result.scalar_one_or_none()
    if not ix:
        return {}
    return {
        'hcp_name': f'{ix.hcp.first_name} {ix.hcp.last_name}' if ix.hcp else None,
        'interaction_type': ix.interaction_type,
        'date': ix.interaction_date.isoformat() if ix.interaction_date else None,
        'time': ix.interaction_time.strftime('%H:%M') if ix.interaction_time else None,
        'summary': ix.summary,
        'sentiment': ix.sentiment,
        'outcome': ix.outcome,
        'discussion_topics': [dt.topic for dt in ix.discussion_topics],
        'products_discussed': [pd.product_name for pd in ix.products_discussed],
        'materials_shared': [{'material_name': ms.material_name, 'quantity': ms.quantity} for ms in ix.materials_shared],
        'samples_distributed': [{'product_name': sd.product_name, 'quantity': sd.quantity} for sd in ix.samples_distributed],
        'follow_up_actions': [
            {
                'action': fu.action,
                'follow_up_date': fu.follow_up_date.isoformat() if fu.follow_up_date else None,
                'status': fu.status,
            }
            for fu in ix.follow_ups
        ],
    }

router = APIRouter(prefix='/agent', tags=['Agent'])

UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)


def _validate_uuid(v: str | None) -> str | None:
    if v is None:
        return None
    if not UUID_PATTERN.match(v):
        raise HTTPException(status_code=422, detail='interaction_id must be a valid UUID')
    return v


def sanitize_llm_output(text: str) -> str:
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    return text


class ChatRequest(BaseModel):
    message: str = Field(description='User message to the agent', min_length=1, max_length=4000)
    interaction_id: str | None = Field(default=None, description='Optional interaction UUID')
    last_hcp_name: str | None = Field(default=None, description='HCP name from previous turn for conversation context')


class ChatResponse(BaseModel):
    assistant_message: str
    tool_used: str | None = None
    updated_form: dict = {}
    interaction_id: str | None = None


@router.post('/chat')
async def agent_chat(
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
    user_id: str = Depends(get_current_user_id),
):
    if request.interaction_id:
        request.interaction_id = _validate_uuid(request.interaction_id)

    initial_state: GraphState = {
        'messages': [],
        'user_input': request.message,
        'intent': '',
        'selected_tool': '',
        'entities': {},
        'interaction': {},
        'tool_result': {},
        'assistant_response': '',
        'errors': [],
        'metadata': {
            'interaction_id': request.interaction_id or '',
            'last_hcp_name': request.last_hcp_name or '',
        },
    }

    result = await agent_graph.ainvoke(initial_state)

    tool_name = result.get('selected_tool', '')
    entities = result.get('entities', {})

    if tool_name and tool_name != 'GeneralChat':
        tool_result = await tool_execution_node(result, session, user_id)
        result['tool_result'] = tool_result.get('tool_result', {})
        result['errors'] = tool_result.get('errors', [])
        response_result = await response_generator_node(result)
        result['assistant_response'] = response_result.get('assistant_response', '')

    tool_data = result.get('tool_result', {})
    interaction_id = tool_data.get('interaction_id') or request.interaction_id

    updated_form = {}
    if tool_name and tool_name != 'GeneralChat' and 'error' not in tool_data:
        form_interaction_id = tool_data.get('interaction_id')
        if not form_interaction_id and tool_data.get('interactions'):
            form_interaction_id = tool_data['interactions'][0].get('id')
        hcp_name = entities.get('hcp_name') or tool_data.get('hcp_name') or tool_data.get('created_hcp_name')

        if tool_name == 'CreateHCP':
            updated_form = {'hcp_name': hcp_name}
        elif form_interaction_id:
            form_data = await _fetch_form_data(session, form_interaction_id)
            if form_data:
                updated_form = form_data
            elif hcp_name:
                updated_form = {'hcp_name': hcp_name}
        elif hcp_name:
            updated_form = {'hcp_name': hcp_name}

    raw_response = result.get('assistant_response', 'I processed your request.')
    safe_response = sanitize_llm_output(raw_response)

    return SuccessResponse(
        message='Message processed',
        data=ChatResponse(
            assistant_message=safe_response,
            tool_used=tool_name,
            updated_form=updated_form,
            interaction_id=interaction_id,
        ).model_dump(),
    )