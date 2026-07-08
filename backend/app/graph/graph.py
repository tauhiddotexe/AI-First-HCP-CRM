from langgraph.graph import StateGraph, END
from app.graph.state import GraphState
from app.graph.nodes.intent_detection import intent_detection_node
from app.graph.nodes.entity_extraction import entity_extraction_node
from app.graph.nodes.tool_router import tool_router_node
from app.graph.nodes.response_generator import response_generator_node


CRM_INTENTS = {'log_interaction', 'edit_interaction', 'retrieve_history', 'suggest_action', 'generate_summary'}


def should_extract(state: GraphState) -> str:
    intent = state.get('intent', 'general')
    if intent in CRM_INTENTS:
        return 'entity_extraction'
    return 'response_generator'


def build_graph() -> StateGraph:
    workflow = StateGraph(GraphState)

    workflow.add_node('intent_detection', intent_detection_node)
    workflow.add_node('entity_extraction', entity_extraction_node)
    workflow.add_node('tool_router', tool_router_node)
    workflow.add_node('response_generator', response_generator_node)

    workflow.set_entry_point('intent_detection')

    workflow.add_conditional_edges(
        'intent_detection',
        should_extract,
        {'entity_extraction': 'entity_extraction', 'response_generator': 'response_generator'},
    )

    workflow.add_edge('entity_extraction', 'tool_router')
    workflow.add_edge('tool_router', 'response_generator')
    workflow.add_edge('response_generator', END)

    return workflow.compile()


agent_graph = build_graph()