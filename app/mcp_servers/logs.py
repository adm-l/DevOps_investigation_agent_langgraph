from app.mcp_servers.common import create_server, run_server

mcp = create_server("devops-logs", 8001)
LOGS = [
    {"timestamp": "2026-11-03T09:41:12Z", "service": "payment-service", "level": "ERROR", "message": "PostgreSQL pool acquisition timed out after 3000ms", "trace_id": "tr-1001"},
    {"timestamp": "2026-11-03T09:41:14Z", "service": "payment-service", "level": "WARN", "message": "Request latency exceeded 2500ms", "trace_id": "tr-1002"},
    {"timestamp": "2026-11-03T09:42:02Z", "service": "payment-service", "level": "ERROR", "message": "context deadline exceeded while querying orders", "trace_id": "tr-1003"},
    {"timestamp": "2026-11-03T09:43:00Z", "service": "catalog-service", "level": "INFO", "message": "Cache hit ratio 0.94", "trace_id": "tr-2001"},
]


@mcp.tool()
def search_logs(service_name: str, keyword: str = "", level: str = "", limit: int = 20) -> list[dict]:
    """Search bundled read-only sample logs by service, keyword and level."""
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    return [row for row in LOGS if row["service"] == service_name
            and (not keyword or keyword.lower() in row["message"].lower())
            and (not level or row["level"].lower() == level.lower())][:limit]


if __name__ == "__main__":
    run_server(mcp)
