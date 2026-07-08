from typing import TypedDict


class GraphState(TypedDict, total=False):
    messages: list[dict]
    user_input: str
    intent: str
    selected_tool: str
    entities: dict
    interaction: dict
    tool_result: dict
    assistant_response: str
    errors: list[str]
    metadata: dict
