import os
from mcp.server.fastmcp import FastMCP


def create_server(name: str, default_port: int) -> FastMCP:
    return FastMCP(name, host=os.getenv("MCP_HOST", "0.0.0.0"),
                   port=int(os.getenv("MCP_PORT", str(default_port))))


def run_server(server: FastMCP) -> None:
    server.run(transport="streamable-http")
