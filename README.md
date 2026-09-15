# Railway Templates

Starter projects you can deploy on [Railway](https://railway.com). Each one is a working API you can use as-is or build on top of.

Most are API backends or AI-related. Every template has its own GitHub repo so you can deploy or publish them separately.

## Templates

| Name | Repo | What it is |
| --- | --- | --- |
| FastAPI + Postgres | [railway-template-fastapi-postgres](https://github.com/romeoxt/railway-template-fastapi-postgres) | REST API with a notes example |
| Hono + Postgres | [railway-template-hono-postgres](https://github.com/romeoxt/railway-template-hono-postgres) | Lightweight TypeScript task API |
| OpenAI Chat API | [railway-template-openai-chat-api](https://github.com/romeoxt/railway-template-openai-chat-api) | Private chat endpoint with streaming |
| AI Agent API | [railway-template-ai-agent-api](https://github.com/romeoxt/railway-template-ai-agent-api) | OpenAI agent with tools |
| RAG + pgvector | [railway-template-rag-pgvector](https://github.com/romeoxt/railway-template-rag-pgvector) | Document Q&A with embeddings |

### Hobby & MVP (Reddit favorites)

| Name | Repo | What it is |
| --- | --- | --- |
| Simple Analytics | [railway-template-simple-analytics](https://github.com/romeoxt/railway-template-simple-analytics) | Lightweight analytics dashboard |
| Personal Blog | [railway-template-personal-blog](https://github.com/romeoxt/railway-template-personal-blog) | Markdown blog for side projects |
| Postgres + PgWeb | [railway-template-postgres-pgweb](https://github.com/romeoxt/railway-template-postgres-pgweb) | Database with browser UI |
| Umami Analytics | [railway-template-umami-analytics](https://github.com/romeoxt/railway-template-umami-analytics) | Self-hosted Umami setup guide |

## What's in each folder

- Source code for the app
- `railway.json` — start command and health check
- `README.md` — how to deploy and run it
- `TEMPLATE.md` — extra notes if you publish to the Railway marketplace
- `.env.example` — local dev settings

## Deploy one on Railway

1. Go to [railway.com/new](https://railway.com/new)
2. Pick "Deploy from GitHub repo"
3. Choose one of the repos above
4. Follow the README in that repo for env vars and database setup

## Publish to the Railway marketplace

See `PUBLISHING.md` for the full walkthrough. Short version:

1. Deploy the repo on Railway and make sure it works
2. Project settings → Generate Template from Project
3. Workspace → Templates → Publish

## Update the GitHub repos

After editing a template here, run:

```powershell
.\scripts\publish-github-repos.ps1
```

That copies each template to its own repo and pushes to GitHub.

## Author

romeoxt — herbylegall9@gmail.com

## License

MIT
