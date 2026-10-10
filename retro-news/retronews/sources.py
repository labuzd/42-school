import hashlib
import html
import logging
import re
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import feedparser

from retronews.config import Source

log = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (compatible; RetroNewsBot/1.0)"
SUMMARY_LIMIT = 300
TRACKING_PARAMS = ("utm_", "fbclid", "gclid", "mc_cid", "mc_eid")
YEAR_RE = re.compile(r"\b19\d\d\b")
TAG_RE = re.compile(r"<[^>]+>")
IMG_RE = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.I)


@dataclass
class Item:
    id: str
    title: str
    link: str
    source: str
    published: str
    summary: str = ""
    image: str = ""
    posted: bool = False


def normalize_link(link: str) -> str:
    parts = urlsplit(link.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query) if not k.lower().startswith(TRACKING_PARAMS)]
    return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path, urlencode(query), ""))


def clean_text(raw: str) -> str:
    text = html.unescape(TAG_RE.sub(" ", raw or ""))
    text = " ".join(text.split())
    if len(text) > SUMMARY_LIMIT:
        text = text[:SUMMARY_LIMIT].rsplit(" ", 1)[0] + "…"
    return text


def _image(entry) -> str:
    for key in ("media_content", "media_thumbnail"):
        for media in entry.get(key) or []:
            if media.get("url"):
                return media["url"]
    for enc in entry.get("enclosures") or []:
        if enc.get("type", "").startswith("image/") and enc.get("href"):
            return enc["href"]
    for content in [*(entry.get("content") or []), {"value": entry.get("summary", "")}]:
        match = IMG_RE.search(content.get("value", ""))
        if match:
            return html.unescape(match.group(1))
    return ""


def _published(entry) -> datetime:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        return datetime(*parsed[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def is_retro(title: str, summary: str, keywords: list[str]) -> bool:
    text = f"{title} {summary}".lower()
    return bool(YEAR_RE.search(text)) or any(k in text for k in keywords)


def parse_feed(data: bytes, source: Source, keywords: list[str]) -> list[Item]:
    feed = feedparser.parse(data)
    items = []
    for entry in feed.entries:
        title = clean_text(entry.get("title", ""))
        link = entry.get("link", "")
        if not title or not link:
            continue
        summary = clean_text(entry.get("summary", ""))
        if source.filter and not is_retro(title, summary, keywords):
            continue
        link = normalize_link(link)
        items.append(Item(
            id=hashlib.sha1(link.encode()).hexdigest()[:16],
            title=title,
            link=link,
            source=source.name,
            published=_published(entry).isoformat(timespec="seconds"),
            summary=summary,
            image=_image(entry),
        ))
    return items


def fetch_source(source: Source, keywords: list[str], timeout: float = 20) -> list[Item]:
    req = urllib.request.Request(source.url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    return parse_feed(data, source, keywords)


def fetch_all(sources: list[Source], keywords: list[str]) -> list[Item]:
    items = []
    for source in sources:
        try:
            found = fetch_source(source, keywords)
            log.info("%s: %d новостей", source.name, len(found))
            items.extend(found)
        except Exception as e:  # один упавший источник не должен ломать остальные
            log.warning("%s: ошибка загрузки: %s", source.name, e)
    return items
