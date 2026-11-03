# Security notes

- All sample MCP tools are read-only and return bundled mock data. No production systems are contacted.
- The investigation API requires X-API-Key. Replace the example key before startup; the application refuses requests while the known placeholder is configured.
- Use TLS and a secret manager at the ingress/deployment layer in real environments.
- SlowAPI applies a per-process IP rate limit. Use a shared Redis-backed limiter when running multiple API replicas.
- Containers run as non-root, with read-only root filesystems and no-new-privileges.
- Tool output is treated as untrusted evidence. The agent is instructed not to perform remediation or mutations.
- Restrict MCP network access to the agent network. Do not expose MCP ports publicly.
- Add tenant-aware authorization, audit retention, durable checkpointing, and secret rotation before production use.
