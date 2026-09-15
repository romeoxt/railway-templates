# Railway Template Composer Setup

## Services

| Service | Source | Public HTTP |
| --- | --- | --- |
| PostgreSQL | Railway PostgreSQL plugin | No |
| PgWeb | GitHub repo (this folder) | Yes |

## Variables — PgWeb

| Variable | Value | Description |
| --- | --- | --- |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Connects PgWeb to Postgres over private network |

## Settings

- Attach a **volume** to PostgreSQL
- Healthcheck on PgWeb: `/`

## Publish metadata

- **Category:** Starters
- **Description:** PostgreSQL with a web UI for instant browsing and SQL queries.
