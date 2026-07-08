from app.graph.state import GraphState


TOOL_MAP = {
    'log_interaction': 'LogInteraction',
    'edit_interaction': 'EditInteraction',
    'retrieve_history': 'RetrieveHistory',
    'suggest_action': 'NextBestAction',
    'generate_summary': 'VisitSummary',
    'general': 'GeneralChat',
}


async def tool_router_node(state: GraphState) -> dict:
    intent = state.get('intent', 'general')
    tool_name = TOOL_MAP.get(intent, 'GeneralChat')
    return {'selected_tool': tool_name}
