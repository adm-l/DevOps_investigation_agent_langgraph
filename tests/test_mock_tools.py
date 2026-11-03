from app.mcp_servers.logs import search_logs
from app.mcp_servers.database import get_database_health
from app.mcp_servers.kubernetes import get_workload_status
from app.mcp_servers.github import get_recent_deployments


def test_search_logs_filters_service_and_keyword():
    rows = search_logs("payment-service", keyword="pool", level="ERROR")
    assert len(rows) == 1
    assert rows[0]["trace_id"] == "tr-1001"


def test_search_logs_rejects_unbounded_limit():
    try:
        search_logs("payment-service", limit=1000)
    except ValueError as exc:
        assert "limit" in str(exc)
    else:
        raise AssertionError("Expected limit validation")


def test_database_health_exposes_pool_pressure():
    result = get_database_health()
    assert result["active_connections"] == 48
    assert result["max_connections"] == 50


def test_kubernetes_workload_returns_pod_evidence():
    result = get_workload_status()
    assert result["ready_replicas"] == result["desired_replicas"]
    assert result["restarts_last_hour"] == 2


def test_deployment_history_is_bounded():
    assert len(get_recent_deployments(limit=2)) == 2
