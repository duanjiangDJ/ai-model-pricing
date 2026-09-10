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
    """models.dev must skip a provider verified against its own official source today."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self._orig = collect_modelsdev.PROVIDERS
        collect_modelsdev.PROVIDERS = self.tmp
        with open(os.path.join(self.tmp, "deepseek.json"), "w") as f:
            f.write('{"provider_id": "deepseek", "verified_at": "2026-09-10T00:00:00Z", "models": []}')

    def tearDown(self):
        collect_modelsdev.PROVIDERS = self._orig

    def test_verified_today_is_skipped(self):
        self.assertTrue(collect_modelsdev.first_party_today("deepseek", "2026-09-10T09:39:11Z"))

    def test_falsy_now_leaves_guard_open(self):
        # The regression: ctx {"now": None} silently disabled the guard for every provider.
        self.assertFalse(collect_modelsdev.first_party_today("deepseek", None))
        self.assertFalse(collect_modelsdev.first_party_today("deepseek", ""))

    def test_other_day_is_not_skipped(self):
        self.assertFalse(collect_modelsdev.first_party_today("deepseek", "2026-09-11T00:00:00Z"))

    def test_unknown_provider_is_not_skipped(self):
        self.assertFalse(collect_modelsdev.first_party_today("nope", "2026-09-10T00:00:00Z"))


if __name__ == "__main__":
    unittest.main()
