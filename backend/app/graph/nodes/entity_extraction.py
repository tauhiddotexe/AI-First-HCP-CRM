import json
import logging
import os
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.groq_client import get_llm, get_fallback_llm
from app.graph.state import GraphState

logger = logging.getLogger('uvicorn.error')


def _load_prompt(filename: str) -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, '..', '..', 'prompts', filename)
    with open(path) as f:
        return f.read()


async def entity_extraction_node(state: GraphState) -> dict:
    llm = get_llm()
    system_prompt = _load_prompt('system_prompt.txt')
    intent = state.get('intent', 'log_interaction')

    intent_instructions = {
        'log_interaction': 'Extract all HCP interaction details from this message',
        'edit_interaction': 'Extract the HCP name and the fields the user wants to change',
        'retrieve_history': 'Extract the HCP name the user is asking about',
        'suggest_action': 'Extract the HCP name and any context for next steps',
        'generate_summary': 'Extract the HCP name and visit context for summarization',
    }.get(intent, 'Extract any relevant HCP information from this message')

    # Inject conversation context for follow-up turns
    last_hcp = state.get('metadata', {}).get('last_hcp_name', '')
    context_hint = f' If the message refers to a previously mentioned HCP without naming them, use "{last_hcp}".' if last_hcp else ''
    prompt = f"""{intent_instructions}{context_hint}

Output ONLY a valid JSON object. Include any fields you can extract from the message. Set unknown fields to null.

ALWAYS use arrays for list fields (discussion_topics, products_discussed, etc.), never strings.

Available fields (use only those relevant):
- "hcp_name": "Full name of the doctor (extract exactly what the user says; never invent a name)"
- "hcp_hospital": "Hospital or clinic name"
- "interaction_type": "Face-to-Face, Virtual, Phone Call, Email, Group Meeting, or Conference"
- "date": "YYYY-MM-DD format"
- "time": "HH:MM in 24-hour format"
- "discussion_topics": ["array of topic strings"]
- "products_discussed": ["array of product name strings"]
- "materials_shared": [{{"material_name": "name", "quantity": number}}]
- "samples_distributed": [{{"product_name": "name", "quantity": number}}]
- "sentiment": "Positive, Neutral, Negative, Very Positive, or Concerned"
- "outcome": "Interested, Committed to Prescribe, Requested More Info, Not Interested, or Deferred Decision"
- "follow_up_actions": [{{"action": "description", "follow_up_date": "YYYY-MM-DD or null"}}]
- "summary": "A concise 2-3 sentence summary"

User message: {state['user_input']}

JSON output:"""

    response = await llm.ainvoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt),
    ])
    content = response.content.strip()

    if content.startswith('```json'):
        content = content[7:]
    if content.startswith('```'):
        content = content[3:]
    if content.endswith('```'):
        content = content[:-3]

    try:
        entities = json.loads(content)
    except json.JSONDecodeError:
        logger.error('Entity extraction JSON parse failed. Raw: %s', content[:500])
        entities = {'error': 'Failed to parse extraction', 'raw': content}

    logger.info('Extracted entities: %s', json.dumps(entities, default=str)[:500])
    return {'entities': entities}