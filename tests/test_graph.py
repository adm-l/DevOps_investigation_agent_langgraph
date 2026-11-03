import pytest
from app.agent.graph import build_investigation_graph


class FakeModel:
    def bind_tools(self, tools):
        return self


def test_graph_requires_tools():
    with pytest.raises(ValueError, match="No MCP tools"):
        build_investigation_graph(FakeModel(), [])
