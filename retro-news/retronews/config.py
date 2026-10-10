import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Source:
    name: str
    url: str
    filter: bool = False


@dataclass
class SiteConfig:
    title: str = "Ретро Авто Новости"
    description: str = ""
    max_items: int = 200


@dataclass
class TelegramConfig:
    enabled: bool = True
    max_posts_per_run: int = 5
    delay_seconds: float = 3
    max_age_days: int = 3


@dataclass
class Config:
    site: SiteConfig
    telegram: TelegramConfig
    keywords: list[str]
    sources: list[Source] = field(default_factory=list)


def load_config(path: Path) -> Config:
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    return Config(
        site=SiteConfig(**raw.get("site", {})),
        telegram=TelegramConfig(**raw.get("telegram", {})),
        keywords=[k.lower() for k in raw.get("filter", {}).get("keywords", [])],
        sources=[Source(**s) for s in raw.get("sources", [])],
    )
