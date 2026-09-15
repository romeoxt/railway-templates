# Railway Template Composer Setup

## Services

| Service | Source |
| --- | --- |
| Simple Analytics | GitHub repo (this folder) |
| PostgreSQL | Railway PostgreSQL plugin |

## Variables

| Variable | Value | Description |
| --- | --- | --- |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Postgres connection |
| `SITE_ID` | `my-site` | Label for this site's traffic |
| `DASHBOARD_PASSWORD` | `${{secret(32)}}` | Opens `/dashboard?key=...` |

## Settings

- Healthcheck: `/health`
- Attach a **volume** to PostgreSQL

## Publish metadata

- **Category:** Starters
- **Description:** Lightweight self-hosted analytics dashboard for hobby projects and MVPs.
