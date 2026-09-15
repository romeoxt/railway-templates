# Personal Blog

A minimal markdown blog you can deploy in one click. Write posts with the admin API, readers get a clean public site. Perfect for a personal site, dev log, or MVP content page.

## What you get

- Public homepage with post list
- `/post/your-slug` pages rendered from Markdown
- Admin endpoint to publish posts (API key protected)
- PostgreSQL storage
- `/health` for Railway

## Deploy on Railway

1. Deploy this repo from GitHub.
2. Add **PostgreSQL** to the project.
3. Set variables:
   - `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`
   - `BLOG_TITLE` = `My Blog`
   - `BLOG_TAGLINE` = whatever you want
   - `ADMIN_API_KEY` = `${{secret(32)}}`
4. Enable public HTTP and deploy.

## Publish your first post

```bash
curl -X POST https://YOUR-RAILWAY-URL/admin/posts \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_ADMIN_API_KEY" \
  -d "{\"title\":\"Hello world\",\"summary\":\"First post\",\"body_markdown\":\"# Hello\\n\\nThis is my blog.\"}"
```

Visit your Railway URL to see it live.

## Marketing site

See `website/index.html` for the template landing page.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Author

romeoxt — herbylegall9@gmail.com

## License

MIT
