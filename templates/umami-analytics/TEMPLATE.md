# Railway Template Composer Setup

## Services

| Service | Source | Notes |
| --- | --- | --- |
| PostgreSQL | Railway PostgreSQL plugin | Attach volume |
| Umami | Docker image `ghcr.io/umami-software/umami:postgresql-latest` | Public HTTP |

## Variables — Umami

| Variable | Value | Description |
| --- | --- | --- |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Postgres connection |
| `DATABASE_TYPE` | `postgresql` | Required by Umami |
| `APP_SECRET` | `${{secret(64)}}` | Session encryption secret |

## Settings — Umami

- Enable public HTTP
- Default login: admin / umami (tell users to change this)

## Publish metadata

- **Category:** Starters
- **Description:** Self-hosted Umami analytics with PostgreSQL — privacy-friendly dashboard for hobby sites.
