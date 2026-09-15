from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import SessionLocal, engine, get_db
from app.rag import answer_with_context, ingest_document, init_vector_store


class IngestRequest(BaseModel):
    source: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with SessionLocal() as session:
        await init_vector_store(session)
    yield
    await engine.dispose()


app = FastAPI(title="RAG Pgvector API", lifespan=lifespan)


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "embedding_model": settings.openai_embedding_model}


@app.post("/v1/ingest")
async def ingest(
    payload: IngestRequest,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_api_key),
) -> dict[str, int | str]:
    count = await ingest_document(db, payload.source, payload.content)
    return {"source": payload.source, "chunks_ingested": count}


@app.post("/v1/ask")
async def ask(
    payload: AskRequest,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_api_key),
) -> dict[str, object]:
    return await answer_with_context(db, payload.question)
