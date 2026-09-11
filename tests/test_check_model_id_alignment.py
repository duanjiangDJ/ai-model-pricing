"""A price check must only target model ids that actually exist in the provider DB.

Bug class (2026-09): PR #166 renamed the DeepSeek DB model id `deepseek-v4.1-flash` ->
`deepseek-flash` (the official /models id) but left the old key in
`scripts/checks/tier0_deepseek.py`'s `COLS` map. `update_model_prices()` skips ids it
cannot resolve (`if not m: continue`), so the tier0 deepseek check parsed the live flash
column correctly (USD + CNY) yet silently wrote NOTHING for it — the model was never
verified and never got its official note. A check whose model key does not resolve is a
dead check: it looks green (parse succeeded, changed=0) while a live price goes
unmonitored forever.

This test is deterministic (no network): it reads the committed provider files and the
fixtures, so it catches a stale key at review time instead of after a silent no-op.

Run: python -m unittest discover -s tests
"""
import importlib
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

CHECKS_DIR = os.path.join(ROOT, "scripts", "checks")
PROVIDERS_DIR = os.path.join(ROOT, "data", "feed", "providers")
FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _provider_ids(provider_id):
    p = os.path.join(PROVIDERS_DIR, provider_id + ".json")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return {m["id"] for m in json.load(fh)["models"]}


def _check_modules():
    for f in sorted(os.listdir(CHECKS_DIR)):
        if not f.startswith("tier") or not f.endswith(".py"):
            continue
        name = f[:-3]
        yield name, importlib.import_module("checks." + name)


class TestCheckModelIdAlignment(unittest.TestCase):
    def test_cols_keys_exist_in_provider_db(self):
        """Any check that declares a COLS model->column map must key it on real DB ids."""
        swept = []
        for name, mod in _check_modules():
            cols = getattr(mod, "COLS", None)
            pid = getattr(mod, "PROVIDER_ID", None)
            if not isinstance(cols, dict) or not pid:
                continue
            # only treat it as a model-id map if every value is an int column index
            if not all(isinstance(v, int) for v in cols.values()):
                continue
            ids = _provider_ids(pid)
            self.assertIsNotNone(ids, f"{name}: provider file {pid}.json is missing")
            dead = [k for k in cols if k not in ids]
            self.assertEqual(
                dead, [],
                f"{name}: COLS keys {dead} are not model ids in providers/{pid}.json — "
                f"update_model_prices would silently skip them (dead check).",
            )
            swept.append(name)
        # the sweep must actually cover the known COLS-based check (guard against drift)
        self.assertIn("tier0_deepseek", swept, f"sweep missed tier0_deepseek: {swept}")

    def test_deepseek_parse_ids_match_db(self):
        """Tier0 deepseek parses ids that resolve in the DB (both EN/USD and zh-CN/CNY)."""
        from checks.tier0_deepseek import parse, parse_cny, COLS
        ids = _provider_ids("deepseek")
        with open(os.path.join(FIXTURES, "deepseek_en.html"), encoding="utf-8") as fh:
            en = fh.read()
        with open(os.path.join(FIXTURES, "deepseek_cn.html"), encoding="utf-8") as fh:
            cn = fh.read()
        for label, parsed in (("en", parse(en)), ("cn", parse_cny(cn))):
            self.assertTrue(parsed, f"{label} parse returned nothing")
            for mid in parsed:
                self.assertIn(
                    mid, ids,
                    f"deepseek {label} parser emits model id {mid!r} that is not in "
                    f"providers/deepseek.json — the update would silently no-op.",
                )
        # COLS and parse() must stay aligned, or one column gets mislabeled.
        self.assertEqual(set(COLS), set(parse(en)),
                         "COLS keys drifted from the parsed model ids")


if __name__ == "__main__":
    unittest.main()
