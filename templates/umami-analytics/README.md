# Umami Analytics

Deploy [Umami](https://umami.is/) — a privacy-friendly, self-hosted analytics tool Reddit often recommends for hobby sites and side projects. No cookies, lightweight, and easy to embed.

This template repo is a Railway setup guide. Umami runs from the official Docker image plus PostgreSQL.

## What you get

- Umami dashboard for page views, referrers, and devices
- PostgreSQL backend
- One script tag on your site — no cookie banner needed for basic use

## Deploy on Railway

### 1. Create the project

1. New Railway project.
2. Add **PostgreSQL** and attach a **volume**.

### 2. Add Umami (Docker service)

1. Add a new service → **Docker Image**
2. Image: `ghcr.io/umami-software/umami:postgresql-latest`
3. Set variables:

| Variable | Value |
| --- | --- |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` |
| `DATABASE_TYPE` | `postgresql` |
| `APP_SECRET` | `${{secret(64)}}` |
| `TRACKER_SCRIPT_NAME` | `umami` (optional) |

4. Enable **public HTTP** on Umami.
5. Deploy and open the Umami URL.

### 3. First login

Default credentials (change immediately after login):

- Email: `admin`
- Password: `umami`

### 4. Track your site

In Umami, add your website, then paste the tracking script into your HTML.

## Marketing site

See `website/index.html` for the template landing page.

## Why this template?

Railway is one of the easiest ways to launch Umami from a template: Postgres + Docker image, no server management. Great for portfolios, blogs, and MVPs.

## Author

romeoxt — herbylegall9@gmail.com

## License

MIT (this template guide). Umami is MIT-licensed separately.
