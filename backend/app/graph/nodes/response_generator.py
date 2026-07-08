import json
import os
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.groq_client import ainvoke_with_fallback
from app.graph.state import GraphState


def _load_prompt(filename: str) -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, '..', '..', 'prompts', filename)
    with open(path) as f:
        return f.read()


async def response_generator_node(state: GraphState) -> dict:
    system_prompt = _load_prompt('system_prompt.txt')
    tool = state.get('selected_tool', '')
    result = state.get('tool_result', {})
    errors = state.get('errors', [])

    if tool == 'GeneralChat' or not tool:
        prompt = (
            'The user sent a general message that does not require a CRM tool.\n'
            'Respond in a friendly, helpful way as a CRM assistant.\n'
            'Keep it concise (1-2 sentences).\n\n'
            'Response:'
        )
    else:
        prompt = f"""The {tool} tool was executed with the following result:
{json.dumps(result, indent=2)}

Generate a friendly, professional confirmation message for the sales representative.
Keep it concise (2-3 sentences). Mention what was extracted or updated.
{'There were some issues. Let the user know: ' + '; '.join(errors) if errors else ''}

Response:"""

    response = await ainvoke_with_fallback([
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt),
    ])
    return {'assistant_response': response.content}