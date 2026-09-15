# Railway Template Composer Setup

Use this checklist when building the marketplace template in Railway.

## Services

| Service | Source | Notes |
| --- | --- | --- |
| FastAPI Postgres API | GitHub repo (this folder) | Enable public HTTP networking |
| PostgreSQL | Railway PostgreSQL plugin | Attach volume for persistence |

## Variables — FastAPI Postgres API

| Variable | Value | Description |
| --- | --- | --- |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Postgres connection string over private network |
| `API_KEY` | `${{secret(32)}}` | Required for write/list routes; send as `X-API-Key` header |

## Settings — FastAPI Postgres API

- **Healthcheck path:** `/health`
- **Start command:** (from `railway.json`) `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Settings — PostgreSQL

- Attach a **volume** at the default Postgres data path so data survives redeploys.

## Private networking

Reference `${{Postgres.DATABASE_URL}}` (or `${{Postgres.RAILWAY_PRIVATE_DOMAIN}}` for host-only configs) so the API talks to Postgres on the private network, not the public internet.

## Publish metadata

- **Category:** Starters (or Backend)
- **Description:** Production-ready FastAPI REST API with PostgreSQL, health checks, and API-key auth.
- **Overview:** Use `README.md` as the marketplace readme.
