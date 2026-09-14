"""Regression tests for the 2026-09-10 writer-safety fixes.

Two silent writer/check gaps let a routine sync damage data:
  1. `router.collect()` passed {"now": None} to every collector, so collect_modelsdev's
     first-party-priority guard never fired and models.dev clobbered the deepseek official
     values (usd 0.44/1.32 -> 0.14/0.28 with cny unchanged -> dual-currency audit FAIL).
  2. build_model() emits no `status`, so a newly discovered OpenRouter catalog entry was
     persisted without one, regressing PR #169's explicit-status invariant, while audit.py
     only rejected a PRESENT-but-invalid value ("if st is not None") and the gate stayed green.
"""
import os
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

from collect import router as collect_router  # noqa: E402
from collect.collectors import collect_modelsdev  # noqa: E402


class TestRouterPassesRealNow(unittest.TestCase):
    """The router must hand collectors a real timestamp (a None `now` disables guards)."""

    def test_collectors_receive_a_nonempty_now(self):
        seen = {}

        class FakeCollector:
            def collect(self, ctx):
                seen.update(ctx)
                return {"provider_id": "openai", "source": "x", "status": "ok",
                        "parsed": {}, "errors": []}

        with mock.patch.object(collect_router.importlib, "import_module",
                               return_value=FakeCollector()):
            collect_router.collect(provider_filter={"openai"})
        self.assertTrue(seen.get("now"), "router passed a falsy `now` to the collector")
        # collectors compare verified_at[:10] to now[:10] -> must start with an ISO date
        self.assertRegex(str(seen["now"]), r"^\d{4}-\d{2}-\d{2}")


class TestFirstPartyGuard(unittest.TestCase):
    """models.dev must never write a provider the repo maintains from its own official source.

    2026-09-11 incident: the guard was `verified_at[:10] == now[:10]`, an exact UTC-date
    equality. deepseek was verified 2026-09-10T09:39Z and zhipuai 2026-09-10T21:28Z, but the
    next 3h sync ran at 2026-09-11T00:39Z — one UTC date later — so the guard opened and
    models.dev rewrote deepseek-flash/v4-flash/v4-pro and zhipuai glm-5.3-flash with its own
    (stale/off-peak/expired-promo) values and replaced their provenance notes.
    """

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self._orig = collect_modelsdev.PROVIDERS
        collect_modelsdev.PROVIDERS = self.tmp
        self._write_provider("deepseek", "2026-09-10T09:39:11Z")

    def tearDown(self):
        collect_modelsdev.PROVIDERS = self._orig

    def _write_provider(self, pid, verified_at):
        with open(os.path.join(self.tmp, f"{pid}.json"), "w") as f:
            f.write('{"provider_id": "%s", "verified_at": "%s", "models": []}' % (pid, verified_at))

    def test_provider_with_own_official_collector_is_never_written(self):
        # scripts/collect/collectors/collect_deepseek.py exists -> one-hand maintained
        self.assertTrue(collect_modelsdev.has_official_collector("deepseek"))
        self.assertTrue(collect_modelsdev.has_official_collector("zhipuai"))
        self.assertFalse(collect_modelsdev.has_official_collector("hyper"))

    def test_cross_midnight_verification_is_still_protected(self):
        # THE regression: ~14h old and one UTC date later -> must remain protected
        self.assertTrue(collect_modelsdev.verified_recently("deepseek", "2026-09-11T00:39:56Z"))

    def test_stale_verification_opens_the_guard(self):
        self._write_provider("deepseek", "2026-09-01T00:00:00Z")
        self.assertFalse(collect_modelsdev.verified_recently("deepseek", "2026-09-11T00:00:00Z"))

    def test_falsy_now_leaves_guard_open(self):
        # The 2026-09-10 regression: ctx {"now": None} silently disabled the guard.
        self.assertFalse(collect_modelsdev.verified_recently("deepseek", None))
        self.assertFalse(collect_modelsdev.verified_recently("deepseek", ""))

    def test_unknown_provider_is_not_skipped(self):
        self.assertFalse(collect_modelsdev.verified_recently("nope", "2026-09-10T00:00:00Z"))

    def test_collect_skips_first_party_and_keeps_third_party(self):
        """End-to-end: a first-party provider must not appear in models.dev's parsed output."""
        catalog = {
            "deepseek": {"models": {"deepseek-flash": {"cost": {"input": 0.15}}}},
            "zhipuai": {"models": {"glm-5.3-flash": {"cost": {"input": 0.075}}}},
            "some-host": {"models": {"m": {"cost": {"input": 1.0}}}},
        }
        with mock.patch.object(collect_modelsdev, "fetch_json", return_value=catalog):
            res = collect_modelsdev.collect({"now": "2026-09-11T00:39:56Z"})
        self.assertNotIn("deepseek", res["parsed"])
        self.assertNotIn("zhipuai", res["parsed"])
        self.assertIn("some-host", res["parsed"])


class TestOneHandCheckGuard(unittest.TestCase):
    """A check-only one-hand provider must also be off-limits to models.dev.

    2026-09-14: opencode/opencode-go ship a price-fetching check
    (scripts/checks/tier1_opencode*.py) but no collect/collectors/collect_<pid>.py, so
    has_official_collector() was False for them. Their verified_at only advances when a write
    happens, so once it aged past FRESH_HOURS the guard opened: models.dev wrote its own values
    (opencode kimi-k2.5 cache_read 0.08 vs the official 0.10; gpt-5.6-terra 2.5/15 vs 2.0/12)
    and the official check reverted them in the SAME run -- collectors run before checks. Net
    price diff was zero, but every ~26h the cycle produced 4 phantom "pricing" changelog
    entries, note churn, a re-rendered view and a version bump.
    """

    def test_fetching_check_counts_as_one_hand(self):
        self.assertTrue(collect_modelsdev.has_official_check("opencode"))
        self.assertTrue(collect_modelsdev.has_official_check("opencode-go"))
        self.assertTrue(collect_modelsdev.has_official_check("moonshotai"))

    def test_static_curated_check_counts_as_one_hand(self):
        # tier1_tencent has no live parser (its page is JS-rendered) and tier1_xiaomi likewise:
        # they persist curated official constants, which is still one-hand maintenance.
        self.assertTrue(collect_modelsdev.has_official_check("tencent"))
        self.assertTrue(collect_modelsdev.has_official_check("xiaomi"))

    def test_record_only_stub_check_is_not_one_hand(self):
        # An auto-generated record/stub check (it neither fetches nor writes prices) must NOT
        # be protected, or the ~170 long-tail providers would lose their aggregator fallback.
        self.assertFalse(collect_modelsdev.has_official_check("302ai"))
        self.assertFalse(collect_modelsdev.has_official_check("hyper"))
        self.assertFalse(collect_modelsdev.has_one_hand_source("302ai"))

    def test_one_hand_source_covers_both_layers(self):
        self.assertTrue(collect_modelsdev.has_one_hand_source("deepseek"))  # collector layer
        self.assertTrue(collect_modelsdev.has_one_hand_source("opencode"))  # check layer
        self.assertFalse(collect_modelsdev.has_one_hand_source("hyper"))    # neither

    def test_stale_check_only_provider_is_still_skipped(self):
        """The regression: a check-only provider whose verified_at is older than FRESH_HOURS."""
        tmp = tempfile.mkdtemp()
        orig = collect_modelsdev.PROVIDERS
        collect_modelsdev.PROVIDERS = tmp
        try:
            with open(os.path.join(tmp, "opencode.json"), "w") as f:
                f.write('{"provider_id": "opencode", "verified_at": "2026-09-01T00:00:00Z", "models": []}')
            self.assertFalse(collect_modelsdev.verified_recently("opencode", "2026-09-14T09:44:20Z"))
            catalog = {
                "opencode": {"models": {"kimi-k2.5": {"cost": {"input": 0.6}}}},
                "some-host": {"models": {"m": {"cost": {"input": 1.0}}}},
            }
            with mock.patch.object(collect_modelsdev, "fetch_json", return_value=catalog):
                res = collect_modelsdev.collect({"now": "2026-09-14T09:44:20Z"})
            self.assertNotIn("opencode", res["parsed"])
            self.assertIn("some-host", res["parsed"])
        finally:
            collect_modelsdev.PROVIDERS = orig



if __name__ == "__main__":
    unittest.main()


class TestNewCatalogEntriesGetStatus(unittest.TestCase):
    """Both catalog writers that can ADD a model must emit an explicit status."""

    def test_openrouter_default_status_helper(self):
        from sync.sync_openrouter import default_catalog_status
        models = [{"id": "a"}, {"id": "b", "status": "offline"}]
        n = default_catalog_status(models)
        self.assertEqual(n, 1)
        self.assertEqual(models[0]["status"], "online")
        self.assertEqual(models[1]["status"], "offline")  # already-set status untouched

    def test_modelsdev_build_model_emits_status(self):
        from sync.sync_modelsdev import build_model
        m = build_model("some-model", {"name": "M", "cost": {"input": 1.0, "output": 2.0}})
        self.assertEqual(m.get("status"), "online")
