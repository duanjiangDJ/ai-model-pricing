"""Regression test for the 2026-09-10 mixed-currency-zero audit rule.

A CNY-only vendor's collector supplies only `cny`; `update_model_prices` merges per currency
and never clears a value, so a stale/fabricated `usd: 0` (from an earlier aggregator write)
survives every 3h sync. `{"usd": 0, "cny": 0.15}` reads as "free" in USD while the model is
demonstrably paid -- a data-truth bug that passed the gate because `price_all_zero` only fires
when *every* currency value is 0 and the cache-zero rule only covered cache_read/cache_write.
Real case: zhipuai glm-4.7-flash (input usd 0 vs cny 0.15).
"""
import glob
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from toolbox import mixed_currency_zero  # noqa: E402


class TestMixedCurrencyZero(unittest.TestCase):
    def test_flags_usd_zero_with_positive_cny(self):
        pm = {"input": {"usd": 0, "cny": 0.15}, "output": {"usd": 0, "cny": 1.5}}
        self.assertEqual(mixed_currency_zero(pm), ["input", "output"])

    def test_flags_positive_usd_with_zero_cny(self):
        self.assertEqual(mixed_currency_zero({"input": {"usd": 0.6, "cny": 0}}), ["input"])

    def test_all_zero_free_model_is_not_flagged(self):
        pm = {"input": {"usd": 0}, "output": {"usd": 0}, "cache_read": {"usd": 0}}
        self.assertEqual(mixed_currency_zero(pm), [])

    def test_single_currency_cny_only_is_not_flagged(self):
        self.assertEqual(mixed_currency_zero({"input": {"cny": 0.15}}), [])

    def test_single_currency_usd_only_is_not_flagged(self):
        self.assertEqual(mixed_currency_zero({"input": {"usd": 0.6}}), [])

    def test_non_zero_dual_currency_is_not_flagged(self):
        pm = {"input": {"usd": 0.6, "cny": 2.0}, "output": {"usd": 2.2, "cny": 8.0}}
        self.assertEqual(mixed_currency_zero(pm), [])

    def test_null_currency_is_ignored(self):
        self.assertEqual(mixed_currency_zero({"input": {"usd": None, "cny": 0.15}}), [])


class TestRepoHasNoMixedCurrencyZero(unittest.TestCase):
    """The whole repo must stay free of the fabricated-zero class (audit hard-fails it)."""

    def test_no_provider_file_has_a_mixed_currency_zero(self):
        offenders = []
        for f in sorted(glob.glob(os.path.join(ROOT, "data/feed/providers/*.json"))):
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
            for m in d.get("models", []):
                pm = (m.get("pricing") or {}).get("per_mtok") or {}
                for k in mixed_currency_zero(pm):
                    offenders.append(f"{os.path.basename(f)} :: {m['id']} {k}={pm[k]}")
        self.assertEqual(offenders, [], "mixed-currency zero (fabricated) present: " + "; ".join(offenders))


if __name__ == "__main__":
    unittest.main()
