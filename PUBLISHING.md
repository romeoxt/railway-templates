# Publishing These Templates on Railway

All five templates are live on GitHub under [@romeoxt](https://github.com/romeoxt):

| Template | GitHub repo | Railway category |
| --- | --- | --- |
| FastAPI Postgres API | [railway-template-fastapi-postgres](https://github.com/romeoxt/railway-template-fastapi-postgres) | Starters |
| Hono Postgres API | [railway-template-hono-postgres](https://github.com/romeoxt/railway-template-hono-postgres) | Starters |
| OpenAI Chat API | [railway-template-openai-chat-api](https://github.com/romeoxt/railway-template-openai-chat-api) | AI |
| AI Agent API | [railway-template-ai-agent-api](https://github.com/romeoxt/railway-template-ai-agent-api) | AI |
| RAG Pgvector API | [railway-template-rag-pgvector](https://github.com/romeoxt/railway-template-rag-pgvector) | AI |

## One-time setup (5 minutes per template)

### 1. Create a Railway project from GitHub

1. Open [Railway](https://railway.com/new) → **Deploy from GitHub repo**.
2. Select the template repo (e.g. `romeoxt/railway-template-openai-chat-api`).
3. For **Postgres templates**, also add **PostgreSQL** from the canvas (`+ New` → **Database** → **PostgreSQL**) and attach a **volume** to Postgres.

### 2. Configure variables

Use each repo's `TEMPLATE.md`. Example for FastAPI Postgres:

| Variable | Value |
| --- | --- |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` |
| `API_KEY` | `${{secret(32)}}` |

For AI templates, mark `OPENAI_API_KEY` as **required** (user-supplied at deploy time).

### 3. Service settings

- Enable **public HTTP** on the API service.
- Set **healthcheck path** to `/health` (already in each `railway.json`).
- Confirm deploy succeeds (green healthcheck).

### 4. Generate the template

1. Project canvas → **Settings** (top right).
2. Scroll to **Generate Template from Project**.
3. Click **Create Template**.
4. Rename services to match marketplace naming (e.g. `FastAPI Postgres API`, `PostgreSQL`).
5. Verify variable descriptions and reference variables survived the conversion.

### 5. Publish to marketplace

1. Workspace → **Templates** → select your new template → **Publish**.
2. Fill in:
   - **Category** (see table above)
   - **Short description** (from `TEMPLATE.md`)
   - **Overview** — paste the repo's `README.md`
3. Add a square **template icon** (1:1, transparent PNG).

After publishing, copy the template URL and add a Deploy button to the GitHub README:

```markdown
[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template/YOUR_TEMPLATE_ID)
```

Re-run `scripts/publish-github-repos.ps1` after editing READMEs if you want the button pushed to GitHub.

## CLI helpers (optional)

Your Railway CLI is logged in as **herbylegall9@gmail.com** on workspace **romeoxt's Projects**.

Create a demo project locally:

```powershell
cd path\to\cloned\repo
railway init -n "OpenAI Chat API Template" -w "28e6f57d-85df-4589-9536-b1c99a8081f5"
railway add --repo romeoxt/railway-template-openai-chat-api --service "OpenAI Chat API"
```

Marketplace **publish** still requires the dashboard steps above (template composer + Publish form).

## Kickback program

Open-source templates with community support can earn up to **25% usage kickback**. See [Railway template kickbacks](https://docs.railway.com/templates/create).
