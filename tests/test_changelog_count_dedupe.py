"""Regression: the price-sync changelog/headline must count DISTINCT models, not entries.

Two coupled defects produced a self-contradicting audit trail (real 2026-09-12, PR #219):
  - `update_model_prices()` appended the model id to `changed` once per changed
    (field, currency), so the written changelog entry carried a duplicated `item_id`
    ("pro,pro,pro,flash,flash,flash") and `new={"models":6}` for only 2 models.
  - `print_sync_summary()` summed the per-ENTRY distinct-model counts, so a model present
    in two entries of the same run (a per-model pass AND an aggregate pass) was counted
    twice: the headline read "**openrouter** (updated 4)" while listing 3 models, and
    several historical "mistral (updated 4)" lines listed only 2.
Both are user-visible counts that disagreed with the model list printed directly beside
them. This locks the count == distinct-models contract.

Run: python -m unittest discover -s tests -v
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import toolbox  # noqa: E402
import daily_check  # noqa: E402


def _model(mid, base):
    return {"id": mid, "name": mid.upper(), "category": "chat", "status": "online",
            "billing_model": ["pay_per_token"],
            "pricing": {"per_mtok": {"input": {"usd": base}, "output": {"usd": base * 2},
                                     "cache_read": {"usd": base / 10}}}}


class TestUpdateModelPricesDedupesChanged(unittest.TestCase):
    def setUp(self):
        self.saved, self.logs = [], []
        self._save, self._log, self._load = (toolbox.save_provider,
                                             toolbox.append_changelog,
                                             toolbox.load_changelog)
        toolbox.save_provider = lambda p: self.saved.append(p)
        toolbox.append_changelog = lambda e: self.logs.append(e)
        toolbox.load_changelog = lambda: {"entries": []}

    def tearDown(self):
        (toolbox.save_provider, toolbox.append_changelog,
         toolbox.load_changelog) = (self._save, self._log, self._load)

    def test_multi_field_change_lists_each_model_once(self):
        p = {"provider_id": "prov", "verified_at": "2026-01-01T00:00:00Z",
             "models": [_model("m1", 1.0), _model("m2", 3.0)]}
        updates = {
            "m1": {"per_mtok": {"input": 1.1, "output": 2.1, "cache_read": 0.11}},
            "m2": {"per_mtok": {"input": 3.1, "output": 4.1, "cache_read": 0.21}},
        }
        changed = toolbox.update_model_prices(p, updates, "2026-09-12T13:00:00Z", "test:src")
        self.assertEqual(changed, ["m1", "m2"], "return value must be a unique id list")
        entries = [e for chunk in self.logs for e in chunk]
        self.assertEqual(len(entries), 1)
        e = entries[0]
        # 3 changed fields per model must NOT repeat the id 3x
        self.assertEqual(e["item_id"], "m1,m2")
        self.assertEqual(e["new"], {"models": 2},
                         "models count must be the number of distinct models, not field-changes")


class TestSyncSummaryCountsDistinctModels(unittest.TestCase):
    def _summary(self, entries):
        orig_load, orig_start = daily_check.load_changelog, daily_check._RUN_STARTED_ISO
        try:
            daily_check.load_changelog = lambda: {"entries": entries}
            daily_check._RUN_STARTED_ISO = "2026-09-12T00:41"
            buf = io.StringIO()
            with redirect_stdout(buf):
                daily_check.print_sync_summary()
            return buf.getvalue()
        finally:
            daily_check.load_changelog, daily_check._RUN_STARTED_ISO = orig_load, orig_start

    def test_model_in_two_entries_counted_once(self):
        entries = [
            # aggregate pass (item_id already deduped by the writer fix)
            {"date": "2026-09-12T00:41:41Z", "kind": "update", "scope": "model",
             "provider_id": "openrouter", "item_id": "pro,flash", "field": "pricing",
             "new": {"models": 2}},
            # per-model pass repeating `pro`
            {"date": "2026-09-12T00:41:30Z", "kind": "update", "scope": "model",
             "provider_id": "openrouter", "item_id": "pro", "field": "pricing",
             "old": {"input": 1.0}, "new": {"input": 0.9}},
            {"date": "2026-09-12T00:41:20Z", "kind": "update", "scope": "model",
             "provider_id": "openrouter", "item_id": "m2.5", "field": "pricing",
             "old": {"input": 0.3}, "new": {"input": 0.27}},
        ]
        out = self._summary(entries)
        # distinct models across the run = {pro, flash, m2.5} = 3, not 2+1+1 = 4
        self.assertIn("**openrouter** (updated 3):", out)
        self.assertNotIn("(updated 4)", out)

    def test_duplicated_item_id_still_counted_once(self):
        # defensive: even if a legacy duplicated item_id slips through, the count dedupes
        entries = [
            {"date": "2026-09-12T00:41:41Z", "kind": "update", "scope": "model",
             "provider_id": "p", "item_id": "a,a,a,b", "field": "pricing",
             "new": {"models": 4}},
        ]
        out = self._summary(entries)
        self.assertIn("**p** (updated 2):", out)


if __name__ == "__main__":
    unittest.main()
