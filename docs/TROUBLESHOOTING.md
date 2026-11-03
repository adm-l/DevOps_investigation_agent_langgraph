# Troubleshooting

- **API fails at startup:** confirm all four MCP endpoints are reachable and use Streamable HTTP.
- **Ollama connection refused:** run `ollama serve`, verify `ollama list`, and check OLLAMA_BASE_URL. In Compose, the default uses host.docker.internal.
- **Model not found:** run `ollama pull qwen3:4b` or change OLLAMA_MODEL.
- **No tools discovered:** check MCP server logs and the four MCP_*_URL values; the API logs discovered tool names on startup.
- **401:** send the configured X-API-Key header.
- **503 API_KEY must be configured:** replace the placeholder in .env.
- **502 investigation failed:** inspect API logs for the correlated investigation UUID and verify Ollama/MCP availability.
- **Slow responses:** reduce max_steps, use a smaller local model, or inspect /metrics.
