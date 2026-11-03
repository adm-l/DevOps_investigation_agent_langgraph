import os
from mcp.server.fastmcp import FastMCP


def create_server(name: str) -> FastMCP:
    return FastMCP(name, host=os.getenv("MCP_HOST", "0.0.0.0"),
                   port=int(os.getenv("MCP_PORT", "8001")))


def run_server(server: FastMCP, default_port: int) -> None:
    # Each server instance receives its own port through MCP_PORT at construction.
    server.run(transport="streamable-http")
