"""Provenance-note persistence regression tests (2026-09-11).

update_model_prices only wrote a writer's `notes` when the price ALSO changed
(`if data.get("notes") and mid in changed`). So a check that VERIFIES an already-correct
price could never stamp its official source: nothing changed, so the note was dropped.

Real case: the retargeted opencode / opencode-go checks (#182) mapped 71 models whose
price was already identical to the official page (the aggregator had mirrored it), so
`mid in changed` was empty and none of them got a provenance note -- 71 paid models with
no source. These tests pin the fix and the anti-tug-of-war guard.

Run: python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import toolbox  # noqa: E402


class TestNotesBackfill(unittest.TestCase):
    def setUp(self):
        self.saved = []
        self._save, self._log = toolbox.save_provider, toolbox.append_changelog
        toolbox.save_provider = lambda p: self.saved.append(p)
        toolbox.append_changelog = lambda e: None

    def tearDown(self):
        toolbox.save_provider, toolbox.append_changelog = self._save, self._log

    def _provider(self, note=None, price=1.0):
        m = {"id": "m", "name": "m", "category": "chat",
             "pricing": {"per_mtok": {"input": {"usd": price}}},
             "billing_model": ["pay_per_token"], "status": "online", "notes": note}
        return {"provider_id": "acme", "verified_at": "2026-01-01T00:00:00Z", "models": [m]}

    def test_note_backfilled_when_price_unchanged(self):
        """The bug: an unchanged-price verify must still persist the official-source note."""
        p = self._provider(note=None, price=1.0)
        changed = toolbox.update_model_prices(
            p, {"m": {"per_mtok": {"input": {"usd": 1.0}}, "notes": "Official page X"}},
            "2026-09-11T00:00:00Z", "https://example.com/pricing")
        self.assertEqual(p["models"][0]["notes"], "Official page X",
                         "provenance note was dropped when the price did not change")
        self.assertIn("m", changed, "a note backfill must count as a change (bump verified_at)")
        self.assertTrue(self.saved, "provider not saved on a note backfill")

    def test_existing_note_not_clobbered_on_noop_verify(self):
        """No notes tug-of-war: an existing note survives a no-op verify from another source."""
        p = self._provider(note="Official first-party source", price=1.0)
        changed = toolbox.update_model_prices(
            p, {"m": {"per_mtok": {"input": {"usd": 1.0}}, "notes": "models.dev official list price"}},
            "2026-09-11T00:00:00Z", "https://models.dev/api.json")
        self.assertEqual(p["models"][0]["notes"], "Official first-party source")
        self.assertEqual(changed, [], "a no-op verify must not rewrite an existing note")

    def test_note_updated_when_price_changes(self):
        p = self._provider(note="stale note", price=1.0)
        changed = toolbox.update_model_prices(
            p, {"m": {"per_mtok": {"input": {"usd": 2.0}}, "notes": "fresh source"}},
            "2026-09-11T00:00:00Z", "https://example.com/pricing")
        self.assertEqual(p["models"][0]["notes"], "fresh source")
        self.assertIn("m", changed)

    def test_note_backfill_idempotent(self):
        p = self._provider(note=None, price=1.0)
        u = {"m": {"per_mtok": {"input": {"usd": 1.0}}, "notes": "Official page X"}}
        toolbox.update_model_prices(p, u, "2026-09-11T00:00:00Z", "x")
        saved_before = list(self.saved)
        changed2 = toolbox.update_model_prices(p, u, "2026-09-11T01:00:00Z", "x")
        self.assertEqual(changed2, [], "second run with identical note must be a no-op")
        self.assertEqual(self.saved, saved_before, "idempotent note must not re-save")

    def test_empty_note_not_written(self):
        p = self._provider(note=None, price=1.0)
        changed = toolbox.update_model_prices(
            p, {"m": {"per_mtok": {"input": {"usd": 1.0}}, "notes": ""}},
            "2026-09-11T00:00:00Z", "x")
        self.assertIsNone(p["models"][0]["notes"])
        self.assertEqual(changed, [])


if __name__ == "__main__":
    unittest.main()
