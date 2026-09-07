"""Router manifest check-source dedup tests.

A provider may expose more than one check module across tiers (e.g. tier0_minimax +
tier1_minimax). run_router's manifest writer must register that provider's check source
ONCE — otherwise data/meta/manifest.json accumulates a duplicate "check:<pid>" entry
(real bug: check:minimax appeared twice).

Run: python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from router import _merge_check_sources  # noqa: E402

NOW = "2026-09-08T00:00:00Z"


def _count(entries, name):
    return sum(1 for s in entries if s["name"] == name)


class TestRouterCheckSourceMerge(unittest.TestCase):
    def test_provider_with_two_tiers_deduped(self):
        # minimax appears at tier0 AND tier1 -> must become a single check:minimax entry
        res = [
            {"provider": "minimax", "tier": 0, "status": "ok", "changed": 1, "detail": ""},
            {"provider": "minimax", "tier": 1, "status": "ok", "changed": 0, "detail": ""},
            {"provider": "openai", "tier": 0, "status": "ok", "changed": 1, "detail": ""},
        ]
        out = _merge_check_sources([], res, NOW)
        mm = [s for s in out if s["name"] == "check:minimax"]
        self.assertEqual(len(mm), 1, "duplicate check:minimax registered")
        self.assertEqual(mm[0]["last_ok"], NOW)
        self.assertIsNone(mm[0]["last_error"])

    def test_error_on_any_tier_fails_badly(self):
        # If a provider errors on any tier, its check source must not show green.
        res = [
            {"provider": "xai", "tier": 0, "status": "ok", "changed": 1, "detail": ""},
            {"provider": "xai", "tier": 1, "status": "error", "changed": 0, "detail": "boom"},
        ]
        out = _merge_check_sources([], res, NOW)
        xai = [s for s in out if s["name"] == "check:xai"][0]
        self.assertIsNone(xai["last_ok"], "errored provider must not show green")
        self.assertEqual(xai["last_error"], "boom")

    def test_preserves_non_check_sources(self):
        res = [{"provider": "openai", "tier": 0, "status": "ok", "changed": 1, "detail": ""}]
        out = _merge_check_sources([{"name": "models.dev", "auto_sync": True}], res, NOW)
        self.assertTrue(any(s["name"] == "models.dev" for s in out))
        self.assertEqual(_count(out, "check:openai"), 1)


if __name__ == "__main__":
    unittest.main()
