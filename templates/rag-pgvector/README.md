# RAG API (Postgres + pgvector)

Upload text, store embeddings in PostgreSQL with pgvector, then ask questions and get answers based on your documents.

## What you get

- POST `/v1/ingest` — add a document (source name + content)
- POST `/v1/ask` — ask a question, get an answer from your docs
- GET `/health` for Railway
- Uses OpenAI for embeddings and for generating answers

## Deploy on Railway

1. Deploy this repo from GitHub.
2. Add **PostgreSQL** with pgvector support to the project.
   - Railway's default Postgres may work. The app runs `CREATE EXTENSION vector` on startup.
   - If that fails, use a Postgres image that includes pgvector.
3. Attach a **volume** to Postgres so data survives redeploys.
4. Set variables on the API service:
   - `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`
   - `OPENAI_API_KEY` = your OpenAI key
   - `OPENAI_EMBEDDING_MODEL` = `text-embedding-3-small`
   - `OPENAI_CHAT_MODEL` = `gpt-4o-mini`
   - `API_KEY` = `${{secret(32)}}`
5. Enable public networking and deploy.

## Run locally

You need Postgres with pgvector installed locally.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Environment variables

| Variable | Required | What it does |
| --- | --- | --- |
| `DATABASE_URL` | Yes | Postgres with pgvector |
| `OPENAI_API_KEY` | Yes | OpenAI key for embeddings + chat |
| `OPENAI_EMBEDDING_MODEL` | No | Embedding model |
| `OPENAI_CHAT_MODEL` | No | Model for answers |
| `API_KEY` | No | Protects ingest/ask routes |

## Try the API

Ingest a document:

```bash
curl -X POST http://localhost:8000/v1/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d "{\"source\":\"faq\",\"content\":\"Our refund policy allows returns within 30 days of purchase.\"}"
```

Ask a question:

```bash
curl -X POST http://localhost:8000/v1/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d "{\"question\":\"What is the refund policy?\"}"
```

## Author

romeoxt — herbylegall9@gmail.com

## License

MIT
