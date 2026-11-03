from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.state import InvestigationState


def build_investigation_graph(model: ChatOllama, tools: list):
    if not tools:
        raise ValueError("No MCP tools were discovered; check MCP server connectivity")
    model_with_tools = model.bind_tools(tools)

    async def call_model(state: InvestigationState):
        response = await model_with_tools.ainvoke(
            [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]
        )
        return {"messages": [response]}

    builder = StateGraph(InvestigationState)
    builder.add_node("agent", call_model)
    builder.add_node("tools", ToolNode(tools, handle_tool_errors=True))
    builder.set_entry_point("agent")
    builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    builder.add_edge("tools", "agent")
    return builder.compile()
