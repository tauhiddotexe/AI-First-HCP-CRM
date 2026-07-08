import re
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.common import SuccessResponse
from app.graph.graph import agent_graph
from app.graph.state import GraphState
from app.database.session import get_session
from app.core.dependencies import get_current_user_id
from app.graph.nodes.tool_execution import tool_execution_node
from app.graph.nodes.response_generator import response_generator_node

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
        'metadata': {'interaction_id': request.interaction_id or ''},
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
        if tool_name == 'LogInteraction':
            updated_form = {
                'hcp_name': entities.get('hcp_name'),
                'interaction_type': entities.get('interaction_type'),
                'date': entities.get('date'),
                'sentiment': entities.get('sentiment'),
                'summary': entities.get('summary'),
                'discussion_topics': entities.get('discussion_topics'),
                'products_discussed': entities.get('products_discussed'),
            }

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