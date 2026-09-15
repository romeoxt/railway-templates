from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel, Field
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import Base, SessionLocal, engine, get_db
from app.models import PageView

TRACKING_SCRIPT = """
(function() {
  var payload = {
    path: window.location.pathname + window.location.search,
    referrer: document.referrer || ""
  };
  navigator.sendBeacon("/api/collect", JSON.stringify(payload));
})();
""".strip()


class CollectPayload(BaseModel):
    path: str = Field(min_length=1, max_length=500)
    referrer: str = Field(default="", max_length=500)


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Simple Analytics", lifespan=lifespan)


def require_dashboard_auth(key: str | None = Query(default=None)) -> None:
    if settings.dashboard_password and key != settings.dashboard_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/script.js", response_class=PlainTextResponse)
async def tracking_script() -> str:
    return TRACKING_SCRIPT


@app.post("/api/collect", status_code=status.HTTP_204_NO_CONTENT)
async def collect(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> None:
    body = await request.body()
    payload = CollectPayload.model_validate_json(body)
    db.add(
        PageView(
            site_id=settings.site_id,
            path=payload.path,
            referrer=payload.referrer,
            user_agent=request.headers.get("user-agent", "")[:300],
        )
    )
    await db.commit()


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_dashboard_auth),
) -> str:
    since = datetime.now(timezone.utc) - timedelta(days=7)

    total = await db.scalar(
        select(func.count(PageView.id)).where(
            PageView.site_id == settings.site_id,
            PageView.created_at >= since,
        )
    )

    top_pages = await db.execute(
        select(PageView.path, func.count(PageView.id).label("views"))
        .where(PageView.site_id == settings.site_id, PageView.created_at >= since)
        .group_by(PageView.path)
        .order_by(desc("views"))
        .limit(10)
    )

    top_referrers = await db.execute(
        select(PageView.referrer, func.count(PageView.id).label("views"))
        .where(
            PageView.site_id == settings.site_id,
            PageView.created_at >= since,
            PageView.referrer != "",
        )
        .group_by(PageView.referrer)
        .order_by(desc("views"))
        .limit(10)
    )

    def rows(items: list[tuple[str, int]]) -> str:
        if not items:
            return "<tr><td colspan='2'>No data yet</td></tr>"
        return "".join(f"<tr><td>{label or '(direct)'}</td><td>{views}</td></tr>" for label, views in items)

    pages_html = rows([(r.path, r.views) for r in top_pages.all()])
    referrers_html = rows([(r.referrer, r.views) for r in top_referrers.all()])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Analytics Dashboard</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; }}
    h1 {{ margin-bottom: 0.2rem; }}
    .muted {{ color: #666; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1rem 0 2rem; }}
    th, td {{ text-align: left; padding: 0.5rem; border-bottom: 1px solid #eee; }}
    code {{ background: #f4f4f4; padding: 0.15rem 0.35rem; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>Simple Analytics</h1>
  <p class="muted">Last 7 days · site <code>{settings.site_id}</code></p>
  <h2>{total or 0} page views</h2>
  <h3>Top pages</h3>
  <table><thead><tr><th>Path</th><th>Views</th></tr></thead><tbody>{pages_html}</tbody></table>
  <h3>Top referrers</h3>
  <table><thead><tr><th>Referrer</th><th>Views</th></tr></thead><tbody>{referrers_html}</tbody></table>
  <p class="muted">Add to your site: <code>&lt;script src="/script.js" defer&gt;&lt;/script&gt;</code></p>
</body>
</html>"""
