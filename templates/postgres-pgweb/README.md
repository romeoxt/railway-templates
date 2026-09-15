# PostgreSQL + PgWeb

Spin up a Postgres database with a web UI you can open in your browser. Browse tables, run SQL, and inspect data without installing anything locally. A popular quick-start pattern for hobby projects and MVPs.

## What you get

- **PostgreSQL** — your database (with persistent volume)
- **PgWeb** — browser-based database explorer connected over Railway private networking

## Deploy on Railway

1. Create a new project.
2. Add **PostgreSQL** and attach a **volume** so data persists.
3. Deploy this repo as a second service named **PgWeb**.
4. On the PgWeb service set:
   - `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`
5. Enable public HTTP on **PgWeb** only (keep Postgres private).

Open the PgWeb URL in your browser to manage your database.

## Use the database from your app

Point any other Railway service at the same Postgres instance:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

## Marketing site

See `website/index.html` for the template landing page.

## Local development

```bash
docker build -t pgweb-local .
docker run -p 8081:8081 -e DATABASE_URL=postgres://user:pass@host:5432/db pgweb-local
```

## Author

romeoxt — herbylegall9@gmail.com

## License

MIT
