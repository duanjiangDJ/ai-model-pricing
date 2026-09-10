"""modelStatus enum guard tests.

The schema's modelStatus enum is exactly {online, offline} (AGENTS.md: there is no
"retired" value — the reason belongs in `notes`). Two gaps existed:
  1. a live check (scripts/checks/tier1_xiaomi.py) carried `"status": "retired"`, which
     update_model_prices would have written into the data file on the next real price
     change — validate/audit then hard-fail and the 3h sync gate breaks;
  2. nothing linted the status literals in check/collector sources.
These tests close both: the source lint catches the whole bug class at the source, and
update_model_prices now refuses any schema-invalid status (defense in depth).

Run: python -m unittest discover -s tests -v
"""
import glob
import os
import re
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import toolbox  # noqa: E402

VALID = ("online", "offline")
# make_result()/router use a small closed vocabulary for *fetch* status, unrelated to the
# model-status field -- those values are legitimate and must not be flagged.
FETCH_VOCAB = ("ok", "error", "no_source")
STATUS_RE = re.compile(r'"status"\s*:\s*"([^"]+)"')


class TestStatusLiteralLint(unittest.TestCase):
    """No check/collector may hard-code a model status outside the schema enum.

    Catches the whole bug class at the source: a literal like "retired" is written into the
    provider file by update_model_prices and then hard-fails validate/audit.
    """

    def _scan(self, pattern):
        bad = []
        for path in glob.glob(os.path.join(ROOT, pattern)):
            with open(path, encoding="utf-8") as fh:
                for i, line in enumerate(fh, 1):
                    if line.lstrip().startswith("#"):   # commented-out code
                        continue
                    for val in STATUS_RE.findall(line):
                        if val not in VALID and val not in FETCH_VOCAB:
                            bad.append(f"{os.path.basename(path)}:{i} status={val!r}")
        return bad

    def test_check_scripts_use_valid_status(self):
        bad = self._scan("scripts/checks/*.py")
        self.assertEqual(bad, [], f"schema-invalid status literals: {bad}")

    def test_collectors_use_valid_status(self):
        bad = self._scan("scripts/collect/collectors/*.py")
        self.assertEqual(bad, [], f"schema-invalid status literals: {bad}")


class TestUpdateModelPricesStatusGuard(unittest.TestCase):
    """update_model_prices must reject invalid status and persist valid changes."""

    def setUp(self):
        self.saved = []
        self._save, self._log = toolbox.save_provider, toolbox.append_changelog
        toolbox.save_provider = lambda p: self.saved.append(p)
        toolbox.append_changelog = lambda e: None

    def tearDown(self):
        toolbox.save_provider, toolbox.append_changelog = self._save, self._log

    def _provider(self, status=None):
        m = {"id": "m", "name": "m", "category": "chat",
             "pricing": {"per_mtok": {"input": {"usd": 1.0}}}, "billing_model": ["pay_per_token"]}
        if status is not None:
            m["status"] = status
        return {"provider_id": "acme", "models": [m]}

    def test_invalid_status_refused(self):
        p = self._provider(status="online")
        changed = toolbox.update_model_prices(
            p, {"m": {"status": "retired"}}, "2026-09-10T00:00:00Z", "test")
        self.assertEqual(p["models"][0]["status"], "online", "invalid status was written")
        self.assertEqual(changed, [], "invalid status must not count as a change")

    def test_valid_status_change_persists(self):
        p = self._provider(status="online")
        changed = toolbox.update_model_prices(
            p, {"m": {"status": "offline"}}, "2026-09-10T00:00:00Z", "test")
        self.assertEqual(p["models"][0]["status"], "offline")
        self.assertIn("m", changed, "a status change must persist (it was silently dropped before)")
        self.assertTrue(self.saved, "provider not saved on a status change")

    def test_same_status_no_change(self):
        p = self._provider(status="offline")
        changed = toolbox.update_model_prices(
            p, {"m": {"status": "offline"}}, "2026-09-10T00:00:00Z", "test")
        self.assertEqual(changed, [])
        self.assertEqual(self.saved, [], "idempotent status must not trigger a save")


if __name__ == "__main__":
    unittest.main()
