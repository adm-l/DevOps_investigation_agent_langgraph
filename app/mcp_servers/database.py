from app.mcp_servers.common import create_server, run_server

mcp = create_server("devops-database")


@mcp.tool()
def get_database_health(database_name: str = "orders") -> dict:
    """Return mock read-only database health and connection-pool metrics."""
    return {"database": database_name, "status": "degraded", "active_connections": 48,
            "max_connections": 50, "pool_wait_ms_p95": 2870, "query_latency_ms_p95": 940,
            "slow_queries": [
                {"query": "SELECT * FROM orders WHERE customer_id = $1", "duration_ms": 1820},
                {"query": "SELECT status, count(*) FROM payments GROUP BY status", "duration_ms": 1260}],
            "note": "Sample data only; no database connection is made."}


if __name__ == "__main__":
    run_server(mcp, 8002)
