# Railway Template Composer Setup

## Services

| Service | Source |
| --- | --- |
| Personal Blog | GitHub repo (this folder) |
| PostgreSQL | Railway PostgreSQL plugin |

## Variables

| Variable | Value | Description |
| --- | --- | --- |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Postgres connection |
| `BLOG_TITLE` | `My Blog` | Site title |
| `BLOG_TAGLINE` | `Notes and updates` | Subtitle on homepage |
| `ADMIN_API_KEY` | `${{secret(32)}}` | Protects `/admin/posts` |

## Settings

- Healthcheck: `/health`
- Attach a **volume** to PostgreSQL

## Publish metadata

- **Category:** Starters
- **Description:** Minimal markdown personal blog for hobby projects and quick MVPs.
