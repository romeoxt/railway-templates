import re
from contextlib import asynccontextmanager
from datetime import datetime

import markdown
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import Base, engine, get_db
from app.models import Post

PAGE_STYLE = """
body { font-family: Georgia, serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; color: #222; }
h1, h2, h3 { line-height: 1.2; }
a { color: #0b57d0; }
.muted { color: #666; }
.post-list { list-style: none; padding: 0; }
.post-list li { margin: 1.25rem 0; padding-bottom: 1rem; border-bottom: 1px solid #eee; }
pre { background: #f6f6f6; padding: 1rem; overflow-x: auto; }
code { background: #f6f6f6; padding: 0.1rem 0.25rem; }
"""


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:200] or "post"


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(default="", max_length=400)
    body_markdown: str = Field(min_length=1)
    slug: str | None = Field(default=None, max_length=200)
    published: bool = True


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Personal Blog", lifespan=lifespan)


def require_admin(x_api_key: str | None = Header(default=None)) -> None:
    if settings.admin_api_key and x_api_key != settings.admin_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


def layout(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8" /><title>{title}</title><style>{PAGE_STYLE}</style></head>
<body>{body}</body></html>"""


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def home(db: AsyncSession = Depends(get_db)) -> str:
    result = await db.execute(
        select(Post).where(Post.published.is_(True)).order_by(desc(Post.created_at))
    )
    posts = result.scalars().all()
    items = "".join(
        f"<li><a href='/post/{p.slug}'><strong>{p.title}</strong></a>"
        f"<div class='muted'>{p.created_at.date()} · {p.summary or 'No summary'}</div></li>"
        for p in posts
    ) or "<li>No posts yet. Publish one with the admin API.</li>"
    body = f"<h1>{settings.blog_title}</h1><p class='muted'>{settings.blog_tagline}</p><ul class='post-list'>{items}</ul>"
    return layout(settings.blog_title, body)


@app.get("/post/{slug}", response_class=HTMLResponse)
async def post_page(slug: str, db: AsyncSession = Depends(get_db)) -> str:
    result = await db.execute(select(Post).where(Post.slug == slug, Post.published.is_(True)))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    html = markdown.markdown(post.body_markdown, extensions=["fenced_code", "tables"])
    body = f"<p><a href='/'>← Back</a></p><h1>{post.title}</h1><p class='muted'>{post.created_at.date()}</p>{html}"
    return layout(post.title, body)


@app.post("/admin/posts", status_code=status.HTTP_201_CREATED)
async def create_post(
    payload: PostCreate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_admin),
) -> dict[str, str | datetime]:
    slug = slugify(payload.slug or payload.title)
    post = Post(
        slug=slug,
        title=payload.title,
        summary=payload.summary,
        body_markdown=payload.body_markdown,
        published=payload.published,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return {"slug": post.slug, "title": post.title, "created_at": post.created_at}
