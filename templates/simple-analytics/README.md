# Simple Analytics Dashboard

A lightweight analytics dashboard for side projects and MVPs. Drop a tiny script on your site, collect page views in PostgreSQL, and open a clean dashboard in your browser.

No Google Analytics. No heavy setup. Good for hobby sites, portfolios, and early products.

## What you get

- `/script.js` — embed on any website to track page views
- `/dashboard?key=YOUR_PASSWORD` — 7-day stats (views, top pages, referrers)
- PostgreSQL storage
- `/health` for Railway

## Deploy on Railway

1. Deploy this repo from GitHub.
2. Add **PostgreSQL** to the project.
3. Set variables on the app service:
   - `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`
   - `SITE_ID` = `my-site` (optional label for your project)
   - `DASHBOARD_PASSWORD` = `${{secret(32)}}`
4. Enable public HTTP and deploy.

## Track your site

Add this to your HTML:

```html
<script src="https://YOUR-RAILWAY-URL/script.js" defer></script>
```

Open your dashboard:

```
https://YOUR-RAILWAY-URL/dashboard?key=YOUR_DASHBOARD_PASSWORD
```

## Marketing site

Open `website/index.html` in a browser for the template landing page, or host the `website/` folder on any static host.

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
