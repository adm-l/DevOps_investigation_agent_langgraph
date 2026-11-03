from app.mcp_servers.common import create_server, run_server

mcp = create_server("devops-github")


@mcp.tool()
def get_recent_deployments(repository: str = "payments/api", limit: int = 5) -> list[dict]:
    """Return mock read-only deployment history for a repository."""
    if not 1 <= limit <= 20:
        raise ValueError("limit must be between 1 and 20")
    rows = [
        {"sha": "a31f9d2", "environment": "production", "status": "success", "created_at": "2026-11-03T09:20:00Z", "actor": "release-bot"},
        {"sha": "7bc22e1", "environment": "production", "status": "success", "created_at": "2026-11-03T08:05:00Z", "actor": "release-bot"},
        {"sha": "5e902ad", "environment": "staging", "status": "success", "created_at": "2026-11-02T17:30:00Z", "actor": "developer"},
    ]
    return [{"repository": repository, **item} for item in rows[:limit]]


if __name__ == "__main__":
    run_server(mcp, 8004)
