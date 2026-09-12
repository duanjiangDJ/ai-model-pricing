"""Regression test for the batch-relationship audit rule (batch > standard).

A batch API is a DISCOUNT on the standard rate (OpenAI/Google/Anthropic/xAI batch is ~50-80%
of standard), so `batch.<field> > per_mtok.<field>` is impossible: it is the signature of a
stale/shared batch block copied from a SIBLING model in the same family, or of a unit error.
The rule is a WARN (not a hard-fail) because the repo mirrors its declared source and an
aggregation source could itself publish an odd pair (the same rationale as
`cache_read_exceeds_input`).

Real case 2026-09-13: openai `gpt-5.6-luna` carried batch input 2.5 against its own standard
input 0.2 (12.5x) and `gpt-5.6-terra` batch 2.5 against 2.0 -- both had inherited gpt-5.5's
batch {input 2.5, output 15}. No writer sets `batch` for openai (sync_official.parse_openai
emits batch=None and tier0_openai omits it), so the hand-written stale block survived every
3h sync and `audit.py` never inspected `batch` at all.
"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from toolbox import batch_exceeds_standard  # noqa: E402


class TestBatchExceedsStandard(unittest.TestCase):
    def test_flags_batch_input_above_standard(self):
        pricing = {
            "per_mtok": {"input": {"usd": 0.2}, "output": {"usd": 1.2}},
            "batch": {"input": {"usd": 2.5}, "output": {"usd": 15.0}},
        }
        self.assertEqual(batch_exceeds_standard(pricing), ["input", "output"])

    def test_flags_per_currency_independently(self):
        pricing = {
            "per_mtok": {"input": {"usd": 1, "cny": 7}, "output": {"usd": 3, "cny": 21}},
            "batch": {"input": {"usd": 0.5, "cny": 9}, "output": {"usd": 4, "cny": 10}},
        }
        self.assertEqual(batch_exceeds_standard(pricing), ["input", "output"])

    def test_normal_batch_below_standard_is_clean(self):
        pricing = {
            "per_mtok": {"input": {"usd": 1}, "output": {"usd": 4}},
            "batch": {"input": {"usd": 0.5}, "output": {"usd": 2}},
        }
        self.assertEqual(batch_exceeds_standard(pricing), [])

    def test_equal_is_not_flagged(self):
        pricing = {
            "per_mtok": {"input": {"usd": 1}, "output": {"usd": 4}},
            "batch": {"input": {"usd": 1}, "output": {"usd": 4}},
        }
        self.assertEqual(batch_exceeds_standard(pricing), [])

    def test_missing_or_null_fields_are_ignored(self):
        self.assertEqual(batch_exceeds_standard({"per_mtok": {"input": {"usd": 5}}}), [])
        self.assertEqual(batch_exceeds_standard({"batch": {"input": {"usd": 5}}}), [])
        self.assertEqual(batch_exceeds_standard({}), [])
        self.assertEqual(batch_exceeds_standard(None), [])

    def test_zero_standard_not_flagged(self):
        pricing = {
            "per_mtok": {"input": {"usd": 0}, "output": {"usd": 0}},
            "batch": {"input": {"usd": 0.5}, "output": {"usd": 1}},
        }
        self.assertEqual(batch_exceeds_standard(pricing), [])


if __name__ == "__main__":
    unittest.main()
