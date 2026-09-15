from openai import AsyncOpenAI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import DocumentChunk

client = AsyncOpenAI(api_key=settings.openai_api_key)


async def init_vector_store(session: AsyncSession) -> None:
    await session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    await session.execute(
        text(
            f"""
            CREATE TABLE IF NOT EXISTS document_chunks (
                id SERIAL PRIMARY KEY,
                source TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding vector({settings.embedding_dimensions}) NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
    )
    await session.commit()


def _chunk_text(text_value: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    if len(text_value) <= chunk_size:
        return [text_value]

    chunks: list[str] = []
    start = 0
    while start < len(text_value):
        end = start + chunk_size
        chunks.append(text_value[start:end].strip())
        if end >= len(text_value):
            break
        start = end - overlap
    return [chunk for chunk in chunks if chunk]


async def embed_texts(texts: list[str]) -> list[list[float]]:
    response = await client.embeddings.create(
        model=settings.openai_embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]


async def ingest_document(session: AsyncSession, source: str, content: str) -> int:
    chunks = _chunk_text(content)
    vectors = await embed_texts(chunks)

    for chunk, vector in zip(chunks, vectors, strict=True):
        vector_literal = "[" + ",".join(str(value) for value in vector) + "]"
        await session.execute(
            text(
                """
                INSERT INTO document_chunks (source, content, embedding)
                VALUES (:source, :content, :embedding::vector)
                """
            ),
            {"source": source, "content": chunk, "embedding": vector_literal},
        )

    await session.commit()
    return len(chunks)


async def search_chunks(session: AsyncSession, query: str, limit: int = 5) -> list[DocumentChunk]:
    query_vector = (await embed_texts([query]))[0]
    vector_literal = "[" + ",".join(str(value) for value in query_vector) + "]"

    result = await session.execute(
        text(
            """
            SELECT id, source, content, created_at
            FROM document_chunks
            ORDER BY embedding <=> :query_vector::vector
            LIMIT :limit
            """
        ),
        {"query_vector": vector_literal, "limit": limit},
    )

    return [
        DocumentChunk(
            id=row["id"],
            source=row["source"],
            content=row["content"],
            created_at=row["created_at"],
        )
        for row in result.mappings().all()
    ]


async def answer_with_context(session: AsyncSession, question: str) -> dict[str, object]:
    matches = await search_chunks(session, question, limit=5)
    context = "\n\n".join(
        f"[{match.source}] {match.content}" for match in matches
    ) or "No relevant documents found."

    response = await client.chat.completions.create(
        model=settings.openai_chat_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer using only the provided context. "
                    "If the answer is not in the context, say you do not know."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ],
    )

    return {
        "answer": response.choices[0].message.content or "",
        "sources": [match.source for match in matches],
        "model": settings.openai_chat_model,
    }
