from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

from app.agent import run_agent
from app.config import settings

app = FastAPI(title="AI Agent API")


class AgentRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "model": settings.openai_model}


@app.post("/v1/agent")
async def agent(
    payload: AgentRequest,
    _: None = Depends(require_api_key),
):
    return await run_agent(payload.prompt)
