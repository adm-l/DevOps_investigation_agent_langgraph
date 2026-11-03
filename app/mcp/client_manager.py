import logging
from langchain_mcp_adapters.client import MultiServerMCPClient
from app.config import Settings

logger = logging.getLogger(__name__)


class MCPToolManager:
    def __init__(self, settings: Settings):
        self.client = MultiServerMCPClient({
            "logs": {"transport": "streamable_http", "url": settings.mcp_logs_url},
            "database": {"transport": "streamable_http", "url": settings.mcp_database_url},
            "kubernetes": {"transport": "streamable_http", "url": settings.mcp_kubernetes_url},
            "github": {"transport": "streamable_http", "url": settings.mcp_github_url},
        })

    async def discover_tools(self):
        tools = await self.client.get_tools()
        logger.info("Discovered %d MCP tools: %s", len(tools), [tool.name for tool in tools])
        return tools
