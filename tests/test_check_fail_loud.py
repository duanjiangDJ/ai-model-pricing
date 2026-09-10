"""Every real price-parser check must FAIL LOUDLY on an empty/stub page.

Bug class (2026-09): `tier0_anthropic` matched nothing for an unknown period (the page
swapped its cache cells and renamed a model) yet the manifest kept `check:anthropic` GREEN
because `parse()` silently returned `{}` — so the router recorded `changed=0` as ok and the
vendor's prices were never verified. The same latent hole existed in every real parser that
lacked a guard (google/minimax/mistral/openai/xai/zai/moonshotai + the headless-Chrome
tier1 baidu/stepfun/zhipuai).

Convention: a parser that matches nothing must raise ValueError rather than return an empty
container. This test sweeps every check module that exposes `parse(text)` and asserts that;
module-level guards (for parsers that return a tuple or live in run()) are asserted
explicitly. Adding a new check parser without a guard fails here.

Run: python -m unittest discover -s tests
"""
import importlib
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

CHECKS_DIR = os.path.join(ROOT, "scripts", "checks")

# Documents / intentional exceptions to the "parse('') must raise" rule:
#   meta      -> official dev.meta.ai/docs is a client-rendered SPA with no SSR prices;
#                parse() returning {} is by design and run() reports that honestly.
#   moonshotai-> parse() returns a (per_model, per_batch) TUPLE and is called per page, so
#                the guard lives in run() (asserted below).
EMPTY_PARSE_EXEMPT = {"tier0_meta", "tier0_moonshotai"}


def _modules_with_parse():
    for f in sorted(os.listdir(CHECKS_DIR)):
        if not f.startswith("tier") or not f.endswith(".py"):
            continue
        name = f[:-3]
        mod = importlib.import_module("checks." + name)
        if callable(getattr(mod, "parse", None)):
            yield name, mod


class TestCheckFailLoud(unittest.TestCase):
    def test_parse_raises_on_empty_page(self):
        checked = []
        for name, mod in _modules_with_parse():
            if name in EMPTY_PARSE_EXEMPT:
                continue
            with self.subTest(check=name):
                try:
                    r = mod.parse("")
                except Exception:
                    checked.append(name)
                    continue
                # No exception: the parser must NOT have silently matched nothing.
                empty = r is None or r == {} or r == [] or r == () or r == ({}, {})
                self.assertFalse(
                    empty,
                    f"{name}.parse('') returned an empty container instead of raising — "
                    f"a layout change would silently no-op the check (anthropic bug class).",
                )
                checked.append(name)
        # Guard against the sweep silently doing nothing (dir/import drift).
        self.assertGreaterEqual(len(checked), 6, f"sweep covered too few checks: {checked}")

    def test_tier0_parsers_that_have_guards(self):
        for name in ("tier0_google", "tier0_minimax", "tier0_mistral", "tier0_openai",
                     "tier0_xai", "tier0_zai", "tier0_deepseek", "tier0_anthropic",
                     "tier0_alibaba"):
            with self.subTest(check=name):
                mod = importlib.import_module("checks." + name)
                with self.assertRaises(ValueError):
                    mod.parse("")

    def test_run_guards_for_tuple_and_chrome_parsers(self):
        now = "2026-09-10T00:00:00Z"
        # moonshotai: every pricing page returns 0 rows -> run() must raise, not report ok.
        ms = importlib.import_module("checks.tier0_moonshotai")
        orig = ms.http_get
        ms.http_get = lambda *a, **k: b"<html>no rows here</html>"
        try:
            with self.assertRaises(ValueError):
                ms.run({"now": now})
        finally:
            ms.http_get = orig

        # openai: fetched text is non-empty but holds no pricing table -> run() must raise.
        op = importlib.import_module("checks.tier0_openai")
        orig_fetch = op._fetch
        op._fetch = lambda *a, **k: "no pricing table on this page"
        try:
            with self.assertRaises(ValueError):
                op.run({"now": now})
        finally:
            op._fetch = orig_fetch

    def test_meta_is_the_only_documented_empty_parser(self):
        # meta must keep returning {} on its SPA shell WITHOUT raising (it cannot parse it);
        # assert the exemption is real so it can't be silently dropped.
        meta = importlib.import_module("checks.tier0_meta")
        self.assertEqual(meta.parse("<html><body>client shell</body></html>"), {})


if __name__ == "__main__":
    unittest.main()
