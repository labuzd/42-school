import json
from dataclasses import asdict
from pathlib import Path

from retronews.sources import Item

KEEP_ITEMS = 1000


def _title_key(title: str) -> str:
    return "".join(ch for ch in title.lower() if ch.isalnum())


class Store:
    """Все собранные новости; хранится в JSON и коммитится в репозиторий."""

    def __init__(self, path: Path):
        self.path = path
        self.items: dict[str, Item] = {}
        if path.exists():
            for raw in json.loads(path.read_text(encoding="utf-8")):
                item = Item(**raw)
                self.items[item.id] = item

    def merge(self, new_items: list[Item]) -> int:
        """Добавляет новые новости, пропуская дубли по ссылке и по заголовку."""
        titles = {_title_key(i.title) for i in self.items.values()}
        added = 0
        for item in new_items:
            key = _title_key(item.title)
            if item.id in self.items or key in titles:
                continue
            self.items[item.id] = item
            titles.add(key)
            added += 1
        return added

    def sorted(self) -> list[Item]:
        return sorted(self.items.values(), key=lambda i: i.published, reverse=True)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = [asdict(i) for i in self.sorted()[:KEEP_ITEMS]]
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
