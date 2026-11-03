import logging
import time
import uuid
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.responses import Response
from app.agent.graph import build_investigation_graph
from app.agent.state import InvestigationState
from app.config import get_settings
from app.logging_config import configure_logging
from app.mcp.client_manager import MCPToolManager
from app.security import require_api_key

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)
REQUESTS = Counter("agent_investigations_total", "Investigation requests", ["outcome"])
DURATION = Histogram("agent_investigation_duration_seconds", "Investigation duration")
limiter = Limiter(key_func=get_remote_address)


class InvestigationRequest(BaseModel):
    question: str = Field(min_length=8, max_length=12000)
    service_name: str = Field(default="payment-service", min_length=1, max_length=100)
    max_steps: int = Field(default=8, ge=1, le=20)


class InvestigationResponse(BaseModel):
    investigation_id: str
    answer: str
    tool_calls: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    manager = MCPToolManager(settings)
    try:
        tools = await manager.discover_tools()
        model = ChatOllama(model=settings.ollama_model, base_url=settings.ollama_base_url,
                           temperature=settings.ollama_temperature)
        app.state.graph = build_investigation_graph(model, tools)
        app.state.ready = True
        app.state.mcp_tool_names = [tool.name for tool in tools]
        logger.info("Agent ready with %d MCP tools", len(tools))
    except Exception:
        app.state.ready = False
        logger.exception("Agent startup failed while connecting to MCP servers")
        raise
    yield
    app.state.ready = False


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/health/live")
async def live():
    return {"status": "alive"}


@app.get("/health/ready")
async def ready(request: Request):
    if not getattr(request.app.state, "ready", False):
        raise HTTPException(status_code=503, detail="Agent is not ready")
    return {"status": "ready", "tools": request.app.state.mcp_tool_names}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/investigate", response_model=InvestigationResponse,
          dependencies=[Depends(require_api_key)])
@limiter.limit(settings.rate_limit)
async def investigate(payload: InvestigationRequest, request: Request):
    if len(payload.question) > settings.max_request_chars:
        raise HTTPException(status_code=413, detail="Question exceeds configured size limit")
    if not getattr(request.app.state, "ready", False):
        raise HTTPException(status_code=503, detail="Agent is not ready")
    investigation_id = str(uuid.uuid4())
    started = time.perf_counter()
    try:
        initial_state: InvestigationState = {
            "messages": [HumanMessage(content=f"Service: {payload.service_name}\\nIssue: {payload.question}")],
            "service_name": payload.service_name,
            "investigation_id": investigation_id,
        }
        result = await request.app.state.graph.ainvoke(
            initial_state,
            config={"recursion_limit": payload.max_steps * 2 + 1,
                    "configurable": {"thread_id": investigation_id}},
        )
        messages = result.get("messages", [])
        answer = str(messages[-1].content) if messages else "No response generated."
        tool_calls = sum(len(getattr(message, "tool_calls", [])) for message in messages)
        REQUESTS.labels(outcome="success").inc()
        return InvestigationResponse(investigation_id=investigation_id, answer=answer,
                                     tool_calls=tool_calls)
    except Exception:
        REQUESTS.labels(outcome="error").inc()
        logger.exception("Investigation %s failed", investigation_id)
        raise HTTPException(status_code=502, detail="Investigation failed; inspect service logs")
    finally:
        DURATION.observe(time.perf_counter() - started)
