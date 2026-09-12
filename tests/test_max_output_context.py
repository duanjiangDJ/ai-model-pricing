"""Regression test for the limit-pair audit rule (max_output > context_window).

Every token a model GENERATES occupies a slot in its own context window (input + output share
one bounded budget), so `max_output > context_window` is self-contradictory: one of the two
specs is wrong. The signature is an INVERTED limit block from an aggregation source, or a
stale spec kept after a context-window shrink (update_model_prices never clears a value its
source stopped publishing).

The rule is a WARN, not a hard-fail: the repo mirrors its declared source and models.dev DOES
publish inverted pairs. Real case 2026-09-12: models.dev `limit: {context: 524288,
output: 1048576}` for deepinfra `thinkingmachines/Inkling`, while DeepInfra's own first-party
API (https://api.deepinfra.com/v1/openai/models) reports `context_length` 524288 /
`max_tokens` 524288 -- the vendor endpoint is the anchor that corrects the pair. 99 models /
28 providers were silently publishing such a pair before this check existed.
"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from toolbox import max_output_exceeds_context  # noqa: E402


class TestMaxOutputExceedsContext(unittest.TestCase):
    def test_flags_inverted_pair(self):
        # models.dev publishes this pair for deepinfra thinkingmachines/Inkling
        self.assertEqual(
            max_output_exceeds_context({"context_window": 524288, "max_output": 1048576}),
            (524288, 1048576),
        )

    def test_flags_close_inversion(self):
        # nebius "fast" rows: 8000 context with an 8192 output cap
        self.assertEqual(
            max_output_exceeds_context({"context_window": 8000, "max_output": 8192}),
            (8000, 8192),
        )

    def test_equal_is_not_flagged(self):
        self.assertIsNone(
            max_output_exceeds_context({"context_window": 8192, "max_output": 8192})
        )

    def test_output_below_context_is_clean(self):
        self.assertIsNone(
            max_output_exceeds_context({"context_window": 1_000_000, "max_output": 384_000})
        )

    def test_missing_or_null_fields_are_ignored(self):
        self.assertIsNone(max_output_exceeds_context({"context_window": None, "max_output": 8192}))
        self.assertIsNone(max_output_exceeds_context({"context_window": 8192}))
        self.assertIsNone(max_output_exceeds_context({"max_output": 8192}))
        self.assertIsNone(max_output_exceeds_context({}))
        self.assertIsNone(max_output_exceeds_context(None))

    def test_zero_or_negative_context_not_flagged(self):
        self.assertIsNone(max_output_exceeds_context({"context_window": 0, "max_output": 8192}))
        self.assertIsNone(max_output_exceeds_context({"context_window": -1, "max_output": 8192}))

    def test_non_numeric_values_ignored(self):
        self.assertIsNone(
            max_output_exceeds_context({"context_window": True, "max_output": 8192})
        )
        self.assertIsNone(
            max_output_exceeds_context({"context_window": "8192", "max_output": 65536})
        )


if __name__ == "__main__":
    unittest.main()
