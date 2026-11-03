from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class InvestigationState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    service_name: str
    investigation_id: str
