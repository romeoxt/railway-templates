# FastAPI + Postgres API

A simple REST API you can deploy on Railway. It uses FastAPI, stores data in PostgreSQL, and includes a small "notes" example so you have something working right away.

## What you get

- FastAPI app with `/health` for Railway health checks
- PostgreSQL connection (async SQLAlchemy)
- Example endpoints: list notes, create notes
- Optional API key protection via the `X-API-Key` header

## Deploy on Railway

1. Click "Deploy from GitHub" and select this repo.
2. Add a **PostgreSQL** database to the same project.
3. On the API service, set these variables:
   - `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`
   - `API_KEY` = `${{secret(32)}}` (or any secret string you choose)
4. Turn on public networking for the API service.
5. Deploy. When it is green, visit `/health` to confirm it works.

See `TEMPLATE.md` if you are turning this into a Railway marketplace template.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate        # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env        # Mac/Linux: cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

You need Postgres running locally and a matching `DATABASE_URL` in your `.env` file.

## Environment variables

| Variable | Required | What it does |
| --- | --- | --- |
| `DATABASE_URL` | Yes | Postgres connection string |
| `API_KEY` | No | If set, requests need `X-API-Key` header |

## Try the API

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d "{\"title\":\"My first note\",\"body\":\"Hello world\"}"

curl http://localhost:8000/notes -H "X-API-Key: your-api-key"
```

## Author

romeoxt — herbylegall9@gmail.com

## License

MIT
