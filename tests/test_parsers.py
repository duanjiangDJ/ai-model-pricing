"""Parser unit tests with fixed HTML fixtures.

Fixtures are snapshots of the official pricing pages; when a page layout changes,
the parser must be updated AND the fixture re-snapshotted. A failing test here means
the parser no longer matches the page it was written for.

Run: python -m unittest discover -s tests -v   (or: python -m pytest tests/)
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8", errors="ignore") as f:
        return f.read()


class TestDeepSeekParser(unittest.TestCase):
    def setUp(self):
        from checks.tier0_deepseek import parse, URL
        self.parse = parse
        self.URL = URL
        self.assertEqual(self.URL, "https://api-docs.deepseek.com/quick_start/pricing",
                         "parser must target the official EN (USD) pricing page, not zh-cn")

    def test_parse_en_page(self):
        r = self.parse(load("deepseek_en.html"))
        self.assertIn("deepseek-v4-flash", r)
        pm = r["deepseek-v4-flash"]["per_mtok"]
        # Official EN page peak prices (USD): flash in $0.44, out $1.32, cache-hit $0.014
        self.assertEqual(pm["input"], 0.44)
        self.assertEqual(pm["output"], 1.32)
        self.assertEqual(pm["cache_read"], 0.014)
        self.assertEqual(r["deepseek-v4-pro"]["per_mtok"]["input"], 1.32)
        self.assertEqual(r["deepseek-v4-flash-vision-exp"]["per_mtok"]["output"], 1.32)

    def test_structure_change_fails_loudly(self):
        # Simulate a page layout change: only a few prices present -> must raise,
        # never return partial data.
        broken = "<html>PRICING</html>" + " $1.2 " * 10
        with self.assertRaises(ValueError):
            self.parse(broken)

    def test_missing_pricing_section_fails(self):
        with self.assertRaises(ValueError):
            self.parse("<html>no pricing section here</html>")


class TestBaiduParser(unittest.TestCase):
    def setUp(self):
        from sync_official import parse_baidu
        self.parse = parse_baidu

    def test_parse_intl_page(self):
        r = self.parse(load("baidu_intl.html"))
        self.assertIn("ernie-5.0", r)
        pm = r["ernie-5.0"]["per_mtok"]
        # Qianfan INT'L page (USD): ERNIE 5.0 input $1.4, output $5.6, no cache row
        self.assertEqual(pm["input"], 1.4)
        self.assertEqual(pm["output"], 5.6)
        self.assertIsNone(pm["cache_read"], "ERNIE 5.0 has no Cache Hit row on the INT'L page")

    def test_domestic_only_models_not_guessed(self):
        # ernie-5.1 / 4.5-turbo are NOT on the INT'L page -> parser must not invent USD prices
        r = self.parse(load("baidu_intl.html"))
        self.assertNotIn("ernie-5.1", r)
        self.assertNotIn("ernie-4.5-turbo", r)


class TestSurgeGuard(unittest.TestCase):
    """Price-surge guard: a >5x relative change must be treated as a parsing error
    and skipped, never silently written."""

    def _mk(self):
        return {"provider_id": "test-prov", "models": [{"id": "m1", "pricing": {"per_mtok": {"input": 0.5, "output": 1.0}}}]}

    def test_normal_change_applies(self):
        from unittest import mock
        from toolbox import update_model_prices
        p = self._mk()
        with mock.patch("toolbox.save_provider"):
            changes = update_model_prices(p, {"m1": {"per_mtok": {"input": 0.55}}}, "2026-08-28T00:00:00Z", "test")
        self.assertEqual(p["models"][0]["pricing"]["per_mtok"]["input"], 0.55)
        self.assertTrue(changes)

    def test_surge_skipped(self):
        from unittest import mock
        from toolbox import update_model_prices
        p = self._mk()
        with mock.patch("toolbox.save_provider"):
            changes = update_model_prices(p, {"m1": {"per_mtok": {"input": 5.0}}}, "2026-08-28T00:00:00Z", "test")
        self.assertEqual(p["models"][0]["pricing"]["per_mtok"]["input"], 0.5,
                         ">5x surge must be skipped, not written")
        self.assertFalse(changes)


if __name__ == "__main__":
    unittest.main()
