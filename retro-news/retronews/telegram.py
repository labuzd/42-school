import html
import json
import logging
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta

from retronews.config import TelegramConfig
from retronews.sources import Item

log = logging.getLogger(__name__)


class TelegramError(Exception):
    pass


class TelegramClient:
    def __init__(self, token: str, chat_id: str, timeout: float = 20):
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.chat_id = chat_id
        self.timeout = timeout

    def send(self, text: str) -> None:
        body = json.dumps({"chat_id": self.chat_id, "text": text, "parse_mode": "HTML"}).encode()
        for attempt in range(2):
            req = urllib.request.Request(self.url, data=body, headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=self.timeout):
                    return
            except urllib.error.HTTPError as e:
                payload = json.loads(e.read() or b"{}")
                retry = payload.get("parameters", {}).get("retry_after")
                if e.code == 429 and retry and attempt == 0:
                    time.sleep(retry)
                    continue
                raise TelegramError(f"{e.code}: {payload.get('description', e.reason)}") from e


def format_message(item: Item) -> str:
    esc = html.escape
    parts = [f"<b>{esc(item.title)}</b>"]
    if item.summary:
        parts.append(esc(item.summary))
    parts.append(f'<a href="{esc(item.link)}">Читать на {esc(item.source)}</a>')
    return "\n\n".join(parts)


def publish_pending(items: list[Item], cfg: TelegramConfig, client, now: datetime, sleep=time.sleep) -> int:
    """Публикует неопубликованные свежие новости, от старых к новым. Помечает их posted."""
    cutoff = (now - timedelta(days=cfg.max_age_days)).isoformat(timespec="seconds")
    pending = sorted((i for i in items if not i.posted and i.published >= cutoff), key=lambda i: i.published)
    sent = 0
    for item in pending[: cfg.max_posts_per_run]:
        if sent:
            sleep(cfg.delay_seconds)
        client.send(format_message(item))
        item.posted = True
        sent += 1
        log.info("Опубликовано в Telegram: %s", item.title)
    return sent
