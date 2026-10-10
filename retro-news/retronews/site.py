from datetime import datetime
from html import escape
from pathlib import Path

from retronews.config import SiteConfig
from retronews.sources import Item

MONTHS = ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]

PAGE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<style>
:root {{ --bg: #f6f1e7; --card: #fffdf8; --text: #2b2520; --muted: #7a6e62; --accent: #a4462b; --line: #e4dccd; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #1c1916; --card: #262220; --text: #eee6da; --muted: #a39686; --accent: #e08a62; --line: #3a342e; }}
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--text); font: 16px/1.5 Georgia, "Times New Roman", serif; }}
header {{ padding: 40px 16px 24px; text-align: center; border-bottom: 1px solid var(--line); }}
header h1 {{ margin: 0; font-size: clamp(28px, 6vw, 44px); letter-spacing: .02em; }}
header p {{ margin: 8px 0 0; color: var(--muted); }}
main {{ max-width: 1100px; margin: 0 auto; padding: 24px 16px 48px;
  display: grid; gap: 20px; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }}
article {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; display: flex; flex-direction: column; }}
article img {{ width: 100%; aspect-ratio: 16 / 9; object-fit: cover; display: block; background: var(--line); }}
.body {{ padding: 14px 16px 18px; }}
.meta {{ font: 13px/1.4 system-ui, sans-serif; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; }}
.meta b {{ color: var(--accent); font-weight: 600; }}
h2 {{ font-size: 19px; line-height: 1.3; margin: 6px 0 8px; }}
h2 a {{ color: inherit; text-decoration: none; }}
h2 a:hover {{ color: var(--accent); }}
.summary {{ margin: 0; color: var(--muted); font-size: 15px; }}
footer {{ text-align: center; color: var(--muted); font: 13px system-ui, sans-serif; padding: 0 16px 32px; }}
</style>
</head>
<body>
<header><h1>{title}</h1><p>{description}</p></header>
<main>
{cards}
</main>
<footer>Обновлено {updated}</footer>
</body>
</html>
"""

CARD = """<article>{image}<div class="body">
<div class="meta"><b>{source}</b> · {date}</div>
<h2><a href="{link}" target="_blank" rel="noopener">{title}</a></h2>
{summary}</div></article>"""


def format_date(iso: str) -> str:
    d = datetime.fromisoformat(iso)
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def render_card(item: Item) -> str:
    image = f'<img src="{escape(item.image)}" alt="" loading="lazy" onerror="this.remove()">' if item.image else ""
    summary = f'<p class="summary">{escape(item.summary)}</p>' if item.summary else ""
    return CARD.format(
        image=image,
        source=escape(item.source),
        date=format_date(item.published),
        link=escape(item.link),
        title=escape(item.title),
        summary=summary,
    )


def render(items: list[Item], cfg: SiteConfig, now: datetime) -> str:
    cards = "\n".join(render_card(i) for i in items[: cfg.max_items])
    return PAGE.format(
        title=escape(cfg.title),
        description=escape(cfg.description),
        cards=cards or "<p>Новостей пока нет.</p>",
        updated=f"{format_date(now.isoformat())}, {now:%H:%M} UTC",
    )


def write_site(items: list[Item], cfg: SiteConfig, out_dir: Path, now: datetime) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "index.html"
    path.write_text(render(items, cfg, now), encoding="utf-8")
    return path
