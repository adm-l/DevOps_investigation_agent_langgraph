# DevOps Investigation Agent — LangGraph

A local-first DevOps investigation agent built with **LangGraph + Ollama + FastAPI + MCP**. It demonstrates how graph state, conditional routing and tool execution can be combined into a multi-step investigation loop.

## What is included

- Explicit `InvestigationState` and a LangGraph agent/tool cycle (`agent → tools → agent`).
- Ollama integration (default: `qwen3:4b`).
- Four independent Streamable HTTP MCP servers: logs, database, Kubernetes and GitHub deployments.
- Read-only mock tools with deterministic sample data; no real infrastructure is contacted.
- FastAPI endpoint, API-key authentication, per-process rate limiting, JSON logs and Prometheus metrics.
- Docker Compose, tests, security notes and operational documentation.

## Architecture

```text
Client
  │ POST /investigate + X-API-Key
  ▼
FastAPI agent host ── LangGraph state machine ── Ollama
  │                         │
  │ MCP client              ├── agent node (LLM/tool choice)
  │                         ├── tools node (MCP execution)
  │                         └── conditional edge / loop
  ├── Logs MCP server
  ├── Database MCP server
  ├── Kubernetes MCP server
  └── GitHub MCP server
```

See [architecture](docs/ARCHITECTURE.md), [development setup](docs/DEVELOPMENT.md), [security](docs/SECURITY.md), and [troubleshooting](docs/TROUBLESHOOTING.md).

## Quick start

Requires Python 3.12+, Ollama and `qwen3:4b` (or another tool-calling model).

```bash
cp .env.example .env
# Set API_KEY to a long random value in .env
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull qwen3:4b
```

Run the four MCP servers in separate terminals:

```bash
python -m app.mcp_servers.logs
python -m app.mcp_servers.database
python -m app.mcp_servers.kubernetes
python -m app.mcp_servers.github
```

Run the API in another terminal:

```bash
uvicorn app.main:app --reload --port 8000
```

Or use Docker Compose for the API and MCP servers while keeping Ollama on the host:

```bash
cp .env.example .env
# Set API_KEY in .env, ensure Ollama is running, then:
docker compose up --build
```

## Example request

```bash
curl -X POST http://localhost:8000/investigate \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: replace-this-secret' \
  -d '{"service_name":"payment-service","question":"Why are payment requests timing out? Check logs, database and recent deployments.","max_steps":8}'
```

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health/live` | Liveness probe |
| GET | `/health/ready` | Readiness and discovered MCP tools |
| POST | `/investigate` | Run an investigation (API key required) |
| GET | `/metrics` | Prometheus metrics |

## Tests

```bash
pytest -q
ruff check .
```

## Important limitations

This is a runnable learning/reference baseline, not a claim of production certification. The MCP tools use mock data and are read-only. LangGraph currently uses in-process execution without durable cross-restart checkpoint storage. Rate limiting is per process; use a shared backend such as Redis for multi-replica deployments. See [security hardening notes](docs/SECURITY.md) before connecting real infrastructure.

**No GitHub Actions or workflow files are included.**
