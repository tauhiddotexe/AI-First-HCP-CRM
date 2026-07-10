import os
import logging
import re
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.groq_client import ainvoke_with_fallback
from app.graph.state import GraphState

logger = logging.getLogger('uvicorn.error')


def _load_prompt(filename: str) -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, '..', '..', 'prompts', filename)
    with open(path) as f:
        return f.read()


def _normalize_intent(raw: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z_]', '', raw.strip().lower())
    cleaned = cleaned.replace('loginteraction', 'log_interaction')
    cleaned = cleaned.replace('editinteraction', 'edit_interaction')
    cleaned = cleaned.replace('retrievehistory', 'retrieve_history')
    cleaned = cleaned.replace('suggestaction', 'suggest_action')
    cleaned = cleaned.replace('generatesummary', 'generate_summary')
    cleaned = cleaned.replace('createhcp', 'create_hcp')
    valid = {'log_interaction', 'edit_interaction', 'retrieve_history', 'suggest_action', 'generate_summary', 'create_hcp', 'general'}
    if cleaned in valid:
        return cleaned
    return ''


_LOG_KEYWORDS = {
    'log_interaction': (
        'log a new interaction', 'log a new hcp', 'log this interaction',
        'log today\'s meeting', 'log this meeting', 'record this interaction',
        'log an interaction', 'log a meeting',
        'hcp:', 'interaction type:', 'materials shared', 'next action:',
        'met with', 'had a meeting', 'meeting with', 'we discussed',
        'shared materials', 'samples distributed',
    ),
    'edit_interaction': ('change the', 'edit the', 'update the', 'modify the'),
    'retrieve_history': ('what did we discuss', 'show me the history', 'previous interactions', 'last time with'),
    'suggest_action': ('what should i', 'next best action', 'next step', 'recommend'),
    'generate_summary': ('summarize', 'summary of', 'give me a summary'),
    'create_hcp': (
        'create a new entry for', 'create a new hcp', 'add a doctor',
        'register a new hcp', 'register a new doctor',
        'create a new entry for dr', 'add dr', 'add doctor',
        'new hcp entry', 'new doctor entry',
    ),
}


def _intent_from_keywords(message: str) -> str:
    lower = message.lower()
    scores = {}
    for intent, patterns in _LOG_KEYWORDS.items():
        scores[intent] = sum(1 for p in patterns if p in lower)
    if not any(scores.values()):
        return ''
    return max(scores, key=scores.get)


async def intent_detection_node(state: GraphState) -> dict:
    system_prompt = _load_prompt('system_prompt.txt')
    user_message = state['user_input']

    prompt = f"""You are a CRM intent classifier. Output EXACTLY ONE label. No explanation. No punctuation.

Rules (in order of priority):
1. If the user wants to CREATE, ADD, or REGISTER a new HCP/doctor/profile -> create_hcp
2. If the user says they want to LOG, RECORD, or SAVE an interaction or meeting -> log_interaction
3. If the user mentions meeting an HCP/doctor, discussing products, or sharing materials -> log_interaction
4. If the user wants to CHANGE, UPDATE, or MODIFY an existing interaction -> edit_interaction
5. If the user wants to SEE or RETRIEVE past interactions -> retrieve_history
6. If the user wants a SUGGESTION or RECOMMENDATION -> suggest_action
7. If the user wants a SUMMARY -> generate_summary
8. If the message is a general greeting or unrelated to CRM -> general

Valid labels: log_interaction, edit_interaction, retrieve_history, suggest_action, generate_summary, create_hcp, general

Examples:
"Create a new entry for Dr. Smith" -> create_hcp
"Add Dr. Jones to the CRM" -> create_hcp
"Register a new HCP named Dr. Lee" -> create_hcp
"I met with Dr. Smith today" -> log_interaction
"Log a new HCP interaction" -> log_interaction
"Change the outcome of my last meeting" -> edit_interaction
"What did we discuss with Dr. Jones last time?" -> retrieve_history
"What should I talk about with Dr. Lee next?" -> suggest_action
"Summarize my last visit with Dr. Kim" -> generate_summary
"Hello" -> general

Message: {user_message}
Label:"""

    response = await ainvoke_with_fallback([
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt),
    ])

    raw = response.content.strip()
    intent = _normalize_intent(raw)
    logger.info('IntentDetection | raw=%s normalized=%s input=%.120s', raw[:60], intent or '(empty)', user_message)

    if intent:
        return {'intent': intent}

    logger.warning('IntentDetection LLM returned invalid label, using keyword fallback. raw=%s', raw[:80])
    kw_intent = _intent_from_keywords(user_message)
    if kw_intent:
        logger.info('IntentDetection keyword fallback -> %s', kw_intent)
        return {'intent': kw_intent}

    return {'intent': 'general'}