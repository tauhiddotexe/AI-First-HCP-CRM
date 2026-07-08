import os
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.groq_client import get_llm
from app.graph.state import GraphState


def _load_prompt(filename: str) -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, '..', '..', 'prompts', filename)
    with open(path) as f:
        return f.read()


async def intent_detection_node(state: GraphState) -> dict:
    llm = get_llm()
    system_prompt = _load_prompt('system_prompt.txt')

    examples = (
        'Examples:\n'
        '- "I met with Dr. Smith today" -> log_interaction\n'
        '- "Change the outcome of my last meeting" -> edit_interaction\n'
        '- "What did we discuss with Dr. Jones last time?" -> retrieve_history\n'
        '- "What should I talk about with Dr. Lee next?" -> suggest_action\n'
        '- "Summarize my last visit with Dr. Kim" -> generate_summary\n'
        '- "Hello" or "Thanks" -> general'
    )

    prompt = f"""Classify the intent of this CRM message to ONE of these labels:
log_interaction, edit_interaction, retrieve_history, suggest_action, generate_summary, general

{examples}

Message: {state['user_input']}

Intent:"""

    response = await llm.ainvoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt),
    ])
    intent = response.content.strip().lower()

    valid_intents = {'log_interaction', 'edit_interaction', 'retrieve_history', 'suggest_action', 'generate_summary', 'general'}
    if intent not in valid_intents:
        intent = 'general'

    return {'intent': intent}