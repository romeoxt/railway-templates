import json
from typing import AsyncIterator

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI

from app.config import settings
from app.schemas import ChatRequest

app = FastAPI(title="OpenAI Chat API")
client = AsyncOpenAI(api_key=settings.openai_api_key)


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "model": settings.openai_model}


async def _stream_chat(payload: ChatRequest) -> AsyncIterator[str]:
    stream = await client.chat.completions.create(
        model=settings.openai_model,
        messages=[message.model_dump() for message in payload.messages],
        stream=True,
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield f"data: {json.dumps({'content': delta})}\n\n"

    yield "data: [DONE]\n\n"


@app.post("/v1/chat")
async def chat(
    payload: ChatRequest,
    _: None = Depends(require_api_key),
):
    if payload.stream:
        return StreamingResponse(_stream_chat(payload), media_type="text/event-stream")

    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=[message.model_dump() for message in payload.messages],
    )

    message = response.choices[0].message
    return {
        "model": settings.openai_model,
        "content": message.content,
        "usage": response.usage.model_dump() if response.usage else None,
    }
