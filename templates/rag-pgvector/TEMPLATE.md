# Railway Template Composer Setup

## Services

| Service | Source | Notes |
| --- | --- | --- |
| RAG Pgvector API | GitHub repo (this folder) | Public HTTP |
| PostgreSQL | Railway PostgreSQL (pgvector) | Must support `CREATE EXTENSION vector` |

Use a Postgres image or plugin that includes pgvector. If the default plugin lacks it, use the [pgvector Postgres template](https://railway.com/template) or `pgvector/pgvector:pg16` as a Docker service.

## Variables — RAG Pgvector API

| Variable | Value | Description |
| --- | --- | --- |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Postgres connection over private network |
| `OPENAI_API_KEY` | *(user provided)* | OpenAI API key |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `OPENAI_CHAT_MODEL` | `gpt-4o-mini` | Chat model for answers |
| `API_KEY` | `${{secret(32)}}` | Protects ingest/ask routes |

## Settings

- **Healthcheck path:** `/health`
- Attach a **volume** to PostgreSQL.

## Publish metadata

- **Category:** AI
- **Description:** RAG API with OpenAI embeddings stored in PostgreSQL pgvector.
