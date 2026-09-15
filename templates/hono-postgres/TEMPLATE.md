# Railway Template Composer Setup

## Services

| Service | Source |
| --- | --- |
| Hono Postgres API | GitHub repo (this folder) |
| PostgreSQL | Railway PostgreSQL plugin |

## Variables — Hono Postgres API

| Variable | Value | Description |
| --- | --- | --- |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Postgres connection string |
| `API_KEY` | `${{secret(32)}}` | Protects all routes except `/health` |

## Settings

- **Healthcheck path:** `/health`
- **Build command:** `npm install && npm run build`
- **Start command:** `npm start`
- Attach a **volume** to PostgreSQL.
