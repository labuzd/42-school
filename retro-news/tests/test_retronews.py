import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from retronews.config import SiteConfig, Source, TelegramConfig, load_config
from retronews.site import render
from retronews.sources import Item, is_retro, normalize_link, parse_feed
from retronews.storage import Store
from retronews.telegram import format_message, publish_pending

RSS = b"""<?xml version="1.0"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
<channel><title>Test</title>
<item>
  <title>1967 Ford Mustang barn find &amp; restored</title>
  <link>https://example.com/mustang?utm_source=rss&amp;id=5#top</link>
  <pubDate>Fri, 09 Oct 2026 10:00:00 GMT</pubDate>
  <description><![CDATA[<p>A <b>great</b> car.</p><img src="https://example.com/a.jpg">]]></description>
</item>
<item>
  <title>New electric SUV revealed</title>
  <link>https://example.com/suv</link>
  <pubDate>Fri, 09 Oct 2026 11:00:00 GMT</pubDate>
  <media:content url="https://example.com/suv.jpg" medium="image"/>
  <description>Modern crossover.</description>
</item>
</channel></rss>"""

KEYWORDS = ["classic", "barn find"]


def item(id, published, title=None, posted=False):
    return Item(id=id, title=title or f"Title {id}", link=f"https://e.com/{id}",
                source="S", published=published, posted=posted)


class ParseTest(unittest.TestCase):
    def test_parse_all(self):
        items = parse_feed(RSS, Source("T", "u"), KEYWORDS)
        self.assertEqual(len(items), 2)
        first = items[0]
        self.assertEqual(first.title, "1967 Ford Mustang barn find & restored")
        self.assertEqual(first.link, "https://example.com/mustang?id=5")
        self.assertEqual(first.summary, "A great car.")
        self.assertEqual(first.image, "https://example.com/a.jpg")
        self.assertEqual(first.published, "2026-10-09T10:00:00+00:00")
        self.assertEqual(items[1].image, "https://example.com/suv.jpg")

    def test_filter(self):
        items = parse_feed(RSS, Source("T", "u", filter=True), KEYWORDS)
        self.assertEqual([i.link for i in items], ["https://example.com/mustang?id=5"])

    def test_is_retro(self):
        self.assertTrue(is_retro("1972 Porsche 911", "", []))
        self.assertTrue(is_retro("Classic Mini", "", ["classic"]))
        self.assertFalse(is_retro("2026 Tesla", "", ["classic"]))

    def test_normalize_link(self):
        self.assertEqual(normalize_link("https://A.com/x?fbclid=1&q=2"), "https://a.com/x?q=2")


class StoreTest(unittest.TestCase):
    def test_merge_dedupe_and_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "news.json"
            store = Store(path)
            a = item("a", "2026-10-01T00:00:00+00:00", title="Same Title")
            b = item("b", "2026-10-02T00:00:00+00:00", title="same title!")  # дубль по заголовку
            c = item("c", "2026-10-03T00:00:00+00:00")
            self.assertEqual(store.merge([a, b, c, a]), 2)
            store.save()
            loaded = Store(path)
            self.assertEqual([i.id for i in loaded.sorted()], ["c", "a"])


class FakeClient:
    def __init__(self):
        self.sent = []

    def send(self, text):
        self.sent.append(text)


class TelegramTest(unittest.TestCase):
    def test_format_escapes(self):
        msg = format_message(Item("x", "A <b> & C", "https://e.com/?a=1&b=2", "Src", "2026-10-01"))
        self.assertIn("<b>A &lt;b&gt; &amp; C</b>", msg)
        self.assertIn('href="https://e.com/?a=1&amp;b=2"', msg)

    def test_publish_pending(self):
        now = datetime(2026, 10, 10, tzinfo=timezone.utc)
        items = [
            item("old", "2026-09-01T00:00:00+00:00"),
            item("done", "2026-10-09T00:00:00+00:00", posted=True),
            item("n2", "2026-10-09T12:00:00+00:00"),
            item("n1", "2026-10-09T06:00:00+00:00"),
            item("n3", "2026-10-09T18:00:00+00:00"),
        ]
        cfg = TelegramConfig(max_posts_per_run=2, max_age_days=3)
        client = FakeClient()
        self.assertEqual(publish_pending(items, cfg, client, now, sleep=lambda s: None), 2)
        self.assertIn("Title n1", client.sent[0])
        self.assertIn("Title n2", client.sent[1])
        self.assertEqual({i.id for i in items if i.posted}, {"done", "n1", "n2"})


class SiteTest(unittest.TestCase):
    def test_render(self):
        now = datetime(2026, 10, 10, 8, 5, tzinfo=timezone.utc)
        page = render([item("a", "2026-10-09T00:00:00+00:00", title="<script>")], SiteConfig(), now)
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn("<script>", page)
        self.assertIn("9 окт 2026", page)


class ConfigTest(unittest.TestCase):
    def test_default_config_loads(self):
        cfg = load_config(Path(__file__).resolve().parent.parent / "config.toml")
        self.assertTrue(cfg.sources)
        self.assertTrue(all(k == k.lower() for k in cfg.keywords))


if __name__ == "__main__":
    unittest.main()
