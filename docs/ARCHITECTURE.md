# Architecture

## Runtime flow

1. FastAPI accepts an authenticated investigation request.
2. LangGraph initializes an explicit InvestigationState.
3. The agent node sends conversation state and a safety-focused system prompt to Ollama.
4. The model may request one or more discovered MCP tools.
5. ToolNode executes selected MCP tools and appends results to state.
6. The graph routes back to the agent; the loop ends when the model returns a final answer.
7. FastAPI returns the answer and request metadata.

## Components

- **Agent host:** FastAPI, LangGraph state machine, Ollama client, MCP client manager.
- **LLM:** Ollama running on the host machine (default model qwen3:4b).
- **MCP servers:** four separately deployed, read-only servers for logs, database, Kubernetes and GitHub.
- **State:** LangGraph message state plus service and investigation identifiers. This starter uses per-process graph execution; it does not yet provide durable cross-restart checkpoints.

## Why LangGraph?

Nodes hold work, edges define routing, and state carries the evolving conversation. The agent/tool cycle is an explicit graph rather than handwritten nested loops. MCP remains a separate protocol boundary and can be replaced independently.
