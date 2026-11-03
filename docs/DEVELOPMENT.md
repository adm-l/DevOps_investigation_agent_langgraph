# Development

## Local setup

Requires Python 3.12+, Docker (optional), and Ollama installed on the host.

```bash
cp .env.example .env
# Edit API_KEY to a long random secret.
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull qwen3:4b
```

Start the four MCP servers in separate terminals:

```bash
python -m app.mcp_servers.logs
python -m app.mcp_servers.database
python -m app.mcp_servers.kubernetes
python -m app.mcp_servers.github
```

Then start the API:

```bash
uvicorn app.main:app --reload --port 8000
```

## Docker Compose

Ollama intentionally remains on the host (especially useful on Apple Silicon). Ensure Ollama is running and the model is pulled, then:

```bash
cp .env.example .env
# Set API_KEY in .env
docker compose up --build
```

## Test and lint

```bash
pytest -q
ruff check .
```

## Example request

```bash
curl -X POST http://localhost:8000/investigate \\
  -H 'Content-Type: application/json' \\
  -H 'X-API-Key: replace-this-secret' \\
  -d '{"service_name":"payment-service","question":"Why are payment requests timing out? Check logs, database and recent deployments.","max_steps":8}'
```

Endpoints: GET /health/live, GET /health/ready, GET /metrics, POST /investigate.
