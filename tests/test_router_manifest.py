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
from router import _merge_check_sources, discover  # noqa: E402

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


class TestCheckSourceUrl(unittest.TestCase):
    """A check source's manifest `url` must resolve to the REAL module file.

    A provider id is not a filename: `io-net` -> tier1_io_net.py, `wafer.ai` ->
    tier1_wafer_ai.py. Building the url as `scripts/checks/<pid>.py` (the old bug)
    produced a path that resolved for 0 of the ~190 check sources, so the manifest
    lied about where its own checks live. Pin the real module mapping.
    """

    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def test_every_check_url_resolves(self):
        mods = discover()
        self.assertGreater(len(mods), 0, "no check modules discovered")
        res = [{"provider": pid, "module": name, "tier": tier,
                "status": "ok", "changed": 0, "detail": ""}
               for tier, pid, _mod, name in mods]
        out = _merge_check_sources([], res, NOW)
        self.assertTrue(all(s["name"].startswith("check:") for s in out))
        bad = [s["url"] for s in out
               if not os.path.exists(os.path.join(self.ROOT, s["url"]))]
        self.assertEqual(bad, [], f"check-source url(s) do not resolve: {bad[:5]}")

    def test_committed_manifest_check_urls_resolve(self):
        # guard the OTHER direction: the committed data/meta/manifest.json must not
        # carry a check-source url that points at a nonexistent file.
        import json
        mp = json.load(open(os.path.join(self.ROOT, "data", "meta", "manifest.json"),
                            encoding="utf-8"))
        bad = [s["url"] for s in mp["sources"]
               if s.get("check") and
               not os.path.exists(os.path.join(self.ROOT, s["url"]))]
        self.assertEqual(bad, [], f"committed manifest check urls do not resolve: {bad[:5]}")

    def test_url_uses_module_name_not_provider_id(self):
        # a provider whose id is NOT its module name must still get a real path
        res = [{"provider": "io-net", "module": "tier1_io_net", "tier": 1,
                "status": "ok", "changed": 0, "detail": ""}]
        out = _merge_check_sources([], res, NOW)
        self.assertEqual(out[0]["url"], "scripts/checks/tier1_io_net.py")


if __name__ == "__main__":
    unittest.main()
