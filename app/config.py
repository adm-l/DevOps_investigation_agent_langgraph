from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "DevOps Investigation Agent"
    environment: str = "local"
    log_level: str = "INFO"
    api_key: str = "change-me-to-a-long-random-secret"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:4b"
    ollama_temperature: float = 0.0
    mcp_logs_url: str = "http://localhost:8001/mcp"
    mcp_database_url: str = "http://localhost:8002/mcp"
    mcp_kubernetes_url: str = "http://localhost:8003/mcp"
    mcp_github_url: str = "http://localhost:8004/mcp"
    rate_limit: str = "30/minute"
    max_request_chars: int = 12000


@lru_cache
def get_settings() -> Settings:
    return Settings()
