# Hono + Postgres API

A lightweight TypeScript API built with Hono and PostgreSQL. Good if you want something fast and small without a heavy framework.

## What you get

- Hono server with `/health` endpoint
- Drizzle ORM + postgres.js for database access
- Example task API: create tasks, list tasks, mark done
- Optional API key via `X-API-Key` header

## Deploy on Railway

1. Deploy this repo from GitHub.
2. Add **PostgreSQL** to the project.
3. Set on the API service:
   - `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`
   - `API_KEY` = `${{secret(32)}}`
4. Enable public HTTP for the API.
5. Deploy and check `/health`.

See `TEMPLATE.md` for marketplace template setup.

## Run locally

```bash
npm install
copy .env.example .env
npm run dev
```

## Environment variables

| Variable | Required | What it does |
| --- | --- | --- |
| `DATABASE_URL` | Yes | Postgres connection string |
| `API_KEY` | No | Protects routes except `/health` |
| `PORT` | No | Defaults to 3000 |

## Try the API

```bash
curl http://localhost:3000/health

curl -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d "{\"title\":\"Buy groceries\"}"

curl http://localhost:3000/tasks -H "X-API-Key: your-api-key"
```

## Author

romeoxt — herbylegall9@gmail.com

## License

MIT
