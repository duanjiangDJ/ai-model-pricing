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
        self.assertEqual(self.URL, "https://api-docs.deepseek.com/quick_start/pricing/",
                         "parser must target the official EN (USD) pricing page, not zh-cn")

    def test_parse_en_page(self):
        r = self.parse(load("deepseek_en.html"))
        # 2026-09-10 layout: 2 columns (deepseek-flash, deepseek-v4-pro) x 6 price rows.
        self.assertIn("deepseek-flash", r, "official name id must be the model id")
        pm = r["deepseek-flash"]["per_mtok"]
        # Official EN page peak prices (USD): flash in $0.3, out $1.2, cache-hit $0.006
        # Prices are dual-currency objects {usd, cny} since schema 26.8.
        self.assertEqual(pm["input"], {"usd": 0.3})
        self.assertEqual(pm["output"], {"usd": 1.2})
        self.assertEqual(pm["cache_read"], {"usd": 0.006})
        self.assertIsNone(pm["cache_write"], "DeepSeek publishes no cache-write price")
        # pro column
        pro = r["deepseek-v4-pro"]["per_mtok"]
        self.assertEqual(pro["input"], {"usd": 1.32})
        self.assertEqual(pro["output"], {"usd": 3.96})
        self.assertEqual(pro["cache_read"], {"usd": 0.044})

    def test_two_column_layout_index_mapping(self):
        # Regression: on the 2-column page (6 rows x 2 cols = 12 prices) the PEAK value of
        # column c lives at idx c+2 (cache-hit) / c+6 (cache-miss) / c+10 (output). A stale
        # 3-column stride would silently pull the wrong cells from the retired vision column.
        r = self.parse(load("deepseek_en.html"))
        self.assertNotIn("deepseek-v4-flash", r, "retired model must not be parsed from the 2-col page")
        self.assertNotIn("deepseek-v4-flash-vision-exp", r)
        # off-peak flash cache-hit is $0.003; the peak value we record is $0.006 (a 3-col
        # stride would have written $0.014 here).
        self.assertEqual(r["deepseek-flash"]["per_mtok"]["cache_read"], {"usd": 0.006})

    def test_parse_cny_page_2column(self):
        from checks.tier0_deepseek import parse_cny
        r = parse_cny(load("deepseek_cn.html"))
        self.assertIn("deepseek-flash", r)
        flash = r["deepseek-flash"]["per_mtok"]
        # Official EN/zh-cn page peak prices (CNY): flash in ¥2.0, out ¥8.0, cache-hit ¥0.04
        self.assertEqual(flash["input"], {"cny": 2.0})
        self.assertEqual(flash["output"], {"cny": 8.0})
        self.assertEqual(flash["cache_read"], {"cny": 0.04})
        self.assertIsNone(flash["cache_write"], "DeepSeek publishes no cache-write price")
        pro = r["deepseek-v4-pro"]["per_mtok"]
        self.assertEqual(pro["input"], {"cny": 9.0})
        self.assertEqual(pro["output"], {"cny": 27.0})
        self.assertEqual(pro["cache_read"], {"cny": 0.3})

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
        from sync.sync_official import parse_baidu
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
        with mock.patch("toolbox.save_provider"), mock.patch("toolbox.append_changelog"):
            changes = update_model_prices(p, {"m1": {"per_mtok": {"input": 0.55}}}, "2026-08-28T00:00:00Z", "test")
        # per_mtok prices are dual-currency objects {usd, cny} since schema 26.8
        self.assertEqual(p["models"][0]["pricing"]["per_mtok"]["input"], {"usd": 0.55})
        self.assertTrue(changes)

    def test_surge_skipped(self):
        from unittest import mock
        from toolbox import update_model_prices
        p = self._mk()
        with mock.patch("toolbox.save_provider"), mock.patch("toolbox.append_changelog"):
            changes = update_model_prices(p, {"m1": {"per_mtok": {"input": 5.0}}}, "2026-08-28T00:00:00Z", "test")
        self.assertEqual(p["models"][0]["pricing"]["per_mtok"]["input"], {"usd": 0.5},
                         ">5x surge must be skipped, not written")
        self.assertFalse(changes)

    def test_second_currency_preserved(self):
        from unittest import mock
        from toolbox import update_model_prices
        p = self._mk()
        p["models"][0]["pricing"]["per_mtok"]["input"] = {"usd": 0.44, "cny": 3.0}
        with mock.patch("toolbox.save_provider"), mock.patch("toolbox.append_changelog"):
            update_model_prices(p, {"m1": {"per_mtok": {"input": {"usd": 0.5, "cny": 3.5}}}}, "2026-08-28T00:00:00Z", "test")
        self.assertEqual(p["models"][0]["pricing"]["per_mtok"]["input"], {"usd": 0.5, "cny": 3.5})

class TestAnthropicParser(unittest.TestCase):
    """2026-09-10 retarget: the page swapped the cache cells to Read-before-Write and renamed
    "Fable 5" -> "Fable 5.1"; the old parser matched 0 blocks and the check reported GREEN
    with 0 models (a dead check). These fixtures lock the current shape and the fail-loud rule."""

    def setUp(self):
        from checks.tier0_anthropic import parse
        self.parse = parse

    def test_current_layout_parses_all_blocks(self):
        r = self.parse(load("anthropic_pricing.html"))
        self.assertEqual(len(r), 12)
        # cache READ is the 3rd cell, WRITE the 4th (the pre-2026-09 order was reversed)
        self.assertEqual(r["claude-fable-5-1"]["per_mtok"],
                         {"input": 10.0, "output": 50.0, "cache_read": 0.25, "cache_write": 12.5})
        self.assertEqual(r["claude-opus-5"]["per_mtok"],
                         {"input": 5.0, "output": 25.0, "cache_read": 0.5, "cache_write": 6.25})
        self.assertEqual(r["claude-sonnet-5"]["per_mtok"],
                         {"input": 2.0, "output": 10.0, "cache_read": 0.2, "cache_write": 2.5})
        self.assertEqual(r["claude-haiku-4-5"]["per_mtok"],
                         {"input": 1.0, "output": 5.0, "cache_read": 0.1, "cache_write": 1.25})

    def test_versioned_label_maps_to_its_own_id(self):
        # "Fable 5.1" must not be absorbed by the "Fable 5" prefix (which would reuse the
        # older row and record the wrong cache_read: 0.25 vs 1).
        r = self.parse(load("anthropic_pricing.html"))
        self.assertEqual(r["claude-fable-5"]["per_mtok"]["cache_read"], 1.0)
        self.assertEqual(r["claude-fable-5-1"]["per_mtok"]["cache_read"], 0.25)

    def test_empty_parse_fails_loudly(self):
        # No price blocks -> raise, never return {} (a silent 0-model check is the bug).
        with self.assertRaises(ValueError):
            self.parse("<html><body>pricing unavailable</body></html>")
        # The pre-2026-09 Write-before-Read shape must not silently match either.
        legacy = ("Fable 5 Input $10 / MTok Output $50 / MTok "
                  "Prompt caching Write $12.5 / MTok Read $1 / MTok")
        with self.assertRaises(ValueError):
            self.parse(legacy)


class TestAlibabaSurgeBlockedGuard(unittest.TestCase):
    """The surge guard silently refuses a >5x correction; the check must surface it instead.

    2026-09-10: qwen-vl-ocr input stayed $0.72 while the official International row read
    $0.07 (and qwen3-next-80b-a3b-thinking output $6 vs $1.2) — update_model_prices skipped
    both, so main published a stale price with no signal anywhere.
    """

    def setUp(self):
        from checks import tier0_alibaba as A
        self.A = A

    def _prov(self, usd):
        return {"provider_id": "alibaba", "models": [
            {"id": "m1", "pricing": {"per_mtok": {"input": {"usd": usd}, "output": None}}}]}

    def test_empty_parse_fails_loudly(self):
        with self.assertRaises(ValueError):
            self.A.parse("<html><body>no price table</body></html>")

    def test_detects_a_stuck_value(self):
        parsed = {"m1": {"per_mtok": {"input": 0.07, "output": None}}}
        blocked = self.A._surge_blocked(self._prov(0.72), parsed)  # 0.72 -> 0.07 = 10.3x
        self.assertEqual(len(blocked), 1)
        self.assertIn("m1.input", blocked[0])

    def test_no_false_positive_on_a_matching_value(self):
        parsed = {"m1": {"per_mtok": {"input": 0.07, "output": None}}}
        self.assertEqual(self.A._surge_blocked(self._prov(0.07), parsed), [])

    def test_small_change_is_not_blocked(self):
        parsed = {"m1": {"per_mtok": {"input": 0.5, "output": None}}}
        self.assertEqual(self.A._surge_blocked(self._prov(0.5), parsed), [])



class TestOpencodeParser(unittest.TestCase):
    """2026-09-11 retarget: the auto-generated opencode check only probed the page with
    js_fetch and never parsed it, so `opencode` prices were maintained from the models.dev
    aggregation and drifted from the vendor list (deepseek-v4-pro output 3.84 vs 3.48,
    kimi-k2.5 cache_read 0.08 vs 0.10). Fixtures lock the current HTML-table shape, the
    base-tier rule and the fail-loud contract."""

    def setUp(self):
        from checks.tier1_opencode import parse as zparse, PROVIDER_ID, URL
        from checks.tier1_opencode_go import parse as gparse
        self.zparse, self.gparse = zparse, gparse
        self.assertEqual(PROVIDER_ID, "opencode")
        self.assertEqual(URL, "https://opencode.ai/docs/zen/")

    def test_zen_page_official_prices(self):
        r = self.zparse(load("opencode_zen.html"))
        # official Zen rows (USD/1M): DeepSeek V4 Pro out $3.48, Kimi K2.5 cache-read $0.10,
        # Claude Fable 5.1 cache-write $12.50.
        self.assertEqual(r["deepseek-v4-pro"]["output"], 3.48)
        self.assertEqual(r["kimi-k2-5"]["cache_read"], 0.10)
        self.assertEqual(r["claude-fable-5-1"]["cache_write"], 12.5)

    def test_zen_higher_tier_rows_are_ignored(self):
        # GPT 5.6 Sol is listed as (<= 272K) then (> 272K); the base row must win regardless
        # of page order -> output 10.0, never the 15.0 of the higher range.
        r = self.zparse(load("opencode_zen.html"))
        self.assertEqual(r["gpt-5-6-sol"]["output"], 10.0)
        self.assertEqual(r["gpt-5-6-terra"]["input"], 2.0)

    def test_go_offpeak_row_is_the_base(self):
        # opencode-go lists DeepSeek rows as (Off-Peak) and (Peak); the repo stores the
        # off-peak rate, so the off-peak row is the one kept.
        r = self.gparse(load("opencode_go.html"))
        self.assertEqual(r["deepseek-v4-pro"]["output"], 1.98)

    def test_free_rows_are_skipped(self):
        # "Big Pickle / Free Free Free -" carries no price -> not returned (never write 0).
        r = self.zparse(load("opencode_zen.html"))
        self.assertNotIn("big-pickle", r)

    def test_empty_parse_fails_loudly(self):
        with self.assertRaises(ValueError):
            self.zparse("<html><body>no pricing table here</body></html>")
        with self.assertRaises(ValueError):
            self.gparse("<html><body>no pricing table here</body></html>")


if __name__ == "__main__":
    unittest.main()


class TestZhipuaiCheck(unittest.TestCase):
    """tier1_zhipuai must persist every dimension its parser extracts.

    Regression (2026-09-11): the bigmodel.cn retarget parsed the 缓存命中 column into
    pr["cache"], but build_updates() only wrote input/output — so all 9 tracked models
    kept a USD-only cache_read (glm-5.3 usd 0.26, cny absent) while the official CNY
    cache-hit price (¥2) was already known. A parsed price dimension that never
    reaches build_updates() is a silent half-fill; assert it here so the next
    retarget cannot re-drop it.
    """

    def setUp(self):
        from checks.tier1_zhipuai import parse, build_updates, URL
        self.parse, self.build_updates = parse, build_updates
        self.assertEqual(URL, "https://docs.bigmodel.cn/cn/guide/start/pricing.md")

    def test_cache_hit_price_is_written(self):
        rows = self.parse(load("bigmodel_pricing.md"))
        self.assertEqual(rows["glm-5.3"]["cache"], 2.0)
        self.assertEqual(rows["glm-5.3-flash"]["cache"], 0.23)
        up, _free = self.build_updates(rows, now="2026-09-11T00:00:00Z")
        # parsed cache-hit (缓存命中) must survive into per_mtok.cache_read.cny
        self.assertEqual(up["glm-5.3"]["per_mtok"]["cache_read"], {"cny": 2.0})
        self.assertEqual(up["glm-5.3-flash"]["per_mtok"]["cache_read"], {"cny": 0.23})
        self.assertEqual(up["glm-5.3"]["per_mtok"]["input"], {"cny": 8.0})
        self.assertEqual(up["glm-5.3"]["per_mtok"]["output"], {"cny": 28.0})

    def test_free_model_is_not_priced(self):
        rows = self.parse(load("bigmodel_pricing.md"))
        up, free = self.build_updates(rows, now="2026-09-11T00:00:00Z")
        self.assertIn("glm-4.7-flash", free)
        self.assertNotIn("glm-4.7-flash", up)

    def test_zero_rows_raises(self):
        # a header without the price columns must fail loud, never no-op silently
        with self.assertRaises(ValueError):
            self.parse("| 模型名称 | 输入单价 |\n| --- | --- |\n")
