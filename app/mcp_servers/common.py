import os
from mcp.server.fastmcp import FastMCP


def create_server(name: str) -> FastMCP:
    return FastMCP(name)


def run_server(server: FastMCP, default_port: int) -> None:
    server.run(transport="streamable-http", host=os.getenv("MCP_HOST", "0.0.0.0"),
               port=int(os.getenv("MCP_PORT", str(default_port))))
