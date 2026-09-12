"""Regression: the sync-summary generator must not report a `kind="verify"` record
(a >5x surge-skip that held the stored value, or a no-change official-source check) as a
price "update", and must not count it in the headline change total.

Real 2026-09-12: PR #211 rendered "price sync (14 changes): - **merge-gateway** (updated 4)"
while all four merge-gateway entries were `kind="verify"` surge-skips -- no merge-gateway
price was updated at all.
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import daily_check  # noqa: E402


class SyncSummaryLabelTest(unittest.TestCase):
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

    def test_surge_skip_is_not_reported_as_update(self):
        entries = [
            {"date": "2026-09-12T00:41:41Z", "kind": "verify", "scope": "model",
             "provider_id": "merge-gateway", "item_id": "deepseek/deepseek-v4-flash",
             "field": "surge_skip:input.usd", "old": {"stored": 0.22},
             "new": {"official": 0.035}, "source": "models.dev:api"},
            {"date": "2026-09-12T00:41:10Z", "kind": "update", "scope": "model",
             "provider_id": "openrouter", "item_id": "qwen/qwen3.8-27b", "field": "pricing",
             "old": {"input": 0.42}, "new": {"input": 0.214}, "source": "openrouter:api"},
        ]
        out = self._summary(entries)
        # headline counts only the single real change, and flags the verification record
        self.assertIn("price sync (1 change, 1 verification record):", out)
        # the surge-skip is labelled as skipped, never as an update
        self.assertIn("**merge-gateway** (skipped 1):", out)
        self.assertIn("（校验跳过 1）", out)
        self.assertNotIn("(updated 1): `deepseek/deepseek-v4-flash`", out)
        # the real update is still rendered
        self.assertIn("**openrouter** (updated 1):", out)

    def test_plain_verify_labelled_verified(self):
        entries = [
            {"date": "2026-09-12T00:41:10Z", "kind": "verify", "scope": "provider",
             "provider_id": "deepseek", "item_id": "deepseek",
             "field": "official_sync", "new": {"verified": True}, "source": "https://x"},
        ]
        out = self._summary(entries)
        self.assertIn("price sync (0 changes, 1 verification record):", out)
        self.assertIn("**deepseek** (verified 1):", out)
        self.assertIn("（已校验 1）", out)


if __name__ == "__main__":
    unittest.main()
