from app.mcp_servers.common import create_server, run_server

mcp = create_server("devops-kubernetes")


@mcp.tool()
def get_workload_status(namespace: str = "production", workload: str = "payment-service") -> dict:
    """Return mock read-only Kubernetes workload and pod status."""
    return {"namespace": namespace, "workload": workload, "desired_replicas": 4,
            "ready_replicas": 4, "restarts_last_hour": 2,
            "pods": [
                {"name": "payment-service-7c8d-a1", "cpu_percent": 81, "memory_percent": 72, "restarts": 1},
                {"name": "payment-service-7c8d-b2", "cpu_percent": 77, "memory_percent": 69, "restarts": 1},
                {"name": "payment-service-7c8d-c3", "cpu_percent": 44, "memory_percent": 61, "restarts": 0},
                {"name": "payment-service-7c8d-d4", "cpu_percent": 39, "memory_percent": 58, "restarts": 0}],
            "note": "Sample data only; no Kubernetes API is contacted."}


if __name__ == "__main__":
    run_server(mcp, 8003)
