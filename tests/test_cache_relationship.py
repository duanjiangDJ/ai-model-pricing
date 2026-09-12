"""Regression test for the cache-relationship audit rule (cache_read > input).

`cache_read` is a DISCOUNT on fresh `input`: a cache HIT can never cost more than an
uncached input token, so `cache_read > input` is impossible. It is the signature of a parser
COLUMN SWAP -- a pricing page rendering the cache cells "Write before Read" drops the write
PREMIUM into cache_read (tier0_anthropic's page once read Read-before-Write). The rule is a
WARN (not a hard-fail) because an aggregation source can itself publish an odd pair
(models.dev reports novita-ai xiaomimimo/mimo-v2-flash cache_read 0.3 > input 0.1); a check
must never block a sync for a value we cannot correctly re-derive.

Real stale case surfaced 2026-09-12: kilo openai/gpt-oss-20b cache_read 0.03 > input 0.02,
a value its declared source models.dev no longer publishes (update_model_prices only writes
non-None values and never clears a removed one -> the stale value survives every sync).
"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from toolbox import cache_read_exceeds_input  # noqa: E402


class TestCacheReadExceedsInput(unittest.TestCase):
    def test_flags_cache_read_above_input(self):
        pm = {"input": {"usd": 5}, "cache_read": {"usd": 12.5}}  # a Read/Write swap
        self.assertEqual(cache_read_exceeds_input(pm), ["usd"])

    def test_flags_per_currency_independently(self):
        pm = {"input": {"usd": 10, "cny": 70}, "cache_read": {"usd": 1, "cny": 80}}
        self.assertEqual(cache_read_exceeds_input(pm), ["cny"])

    def test_normal_cache_read_below_input_is_clean(self):
        pm = {"input": {"usd": 10}, "cache_read": {"usd": 1}}
        self.assertEqual(cache_read_exceeds_input(pm), [])

    def test_equal_is_not_flagged(self):
        self.assertEqual(cache_read_exceeds_input({"input": {"usd": 1}, "cache_read": {"usd": 1}}), [])

    def test_missing_or_null_fields_are_ignored(self):
        self.assertEqual(cache_read_exceeds_input({"input": {"usd": 5}}), [])
        self.assertEqual(cache_read_exceeds_input({"input": {"usd": 5}, "cache_read": {"usd": None}}), [])
        self.assertEqual(cache_read_exceeds_input({"input": {"usd": 5}, "cache_read": None}), [])
        self.assertEqual(cache_read_exceeds_input(None), [])

    def test_zero_input_not_flagged(self):
        self.assertEqual(cache_read_exceeds_input({"input": {"usd": 0}, "cache_read": {"usd": 0.5}}), [])


if __name__ == "__main__":
    unittest.main()
