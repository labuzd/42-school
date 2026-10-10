import argparse
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from retronews.config import load_config
from retronews.site import write_site
from retronews.sources import fetch_all
from retronews.storage import Store
from retronews.telegram import TelegramClient, TelegramError, publish_pending

ROOT = Path(__file__).resolve().parent.parent
log = logging.getLogger("retronews")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Собирает новости о ретро-авто и публикует их")
    parser.add_argument("--config", type=Path, default=ROOT / "config.toml")
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "news.json")
    parser.add_argument("--out", type=Path, default=ROOT / "site")
    parser.add_argument("--no-telegram", action="store_true", help="не публиковать в Telegram")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    cfg = load_config(args.config)
    store = Store(args.data)
    now = datetime.now(timezone.utc)

    added = store.merge(fetch_all(cfg.sources, cfg.keywords))
    log.info("Новых новостей: %d, всего: %d", added, len(store.items))

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    status = 0
    if args.no_telegram or not cfg.telegram.enabled:
        log.info("Telegram отключён")
    elif not token or not chat_id:
        log.warning("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID не заданы — пропускаю Telegram")
    else:
        try:
            publish_pending(list(store.items.values()), cfg.telegram, TelegramClient(token, chat_id), now)
        except TelegramError as e:
            log.error("Ошибка Telegram: %s", e)
            status = 1

    # Сохраняем даже после ошибки Telegram, чтобы уже отправленное не ушло повторно
    store.save()
    path = write_site(store.sorted(), cfg.site, args.out, now)
    log.info("Сайт: %s", path)
    return status
