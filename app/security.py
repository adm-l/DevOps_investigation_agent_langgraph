import hmac
from fastapi import Header, HTTPException, status
from app.config import get_settings


async def require_api_key(x_api_key: str = Header(default="")) -> None:
    expected = get_settings().api_key
    if expected == "change-me-to-a-long-random-secret":
        raise HTTPException(status_code=503, detail="API_KEY must be configured")
    if not hmac.compare_digest(x_api_key, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
