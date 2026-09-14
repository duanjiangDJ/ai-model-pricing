"""Regression test for the per_mtok / batch magnitude rule (BOTH ends of the scale).

per_mtok and batch values are a price PER 1M TOKENS, so either end of the scale carries a
unit-error signature that no real price can produce:
  - a non-zero value BELOW 1e-4 is a per-token value stored as per-M (~1e6x too small;
    OpenRouter's per-token API value once shipped as 2.2e-7 = $0.22/M);
  - a value ABOVE 2e3 is a per-1k table stored as per-M (~1e3x too large; several vendors
    publish a CNY-per-1k table beside their per-M one).

audit.py hard-failed only the small end, and only WARNed above 1e5 -- so probe 2026-09-14
(`per_mtok output=5000`, the per-1k signature for a $5/M model) passed validate+audit with
zero output, letting a whole per-1k bug class ship. The predicate lives in toolbox so
audit's rule is unit-testable (same convention as batch_exceeds_standard).
"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from toolbox import per_mtok_magnitude  # noqa: E402


class TestPerMtokMagnitude(unittest.TestCase):
    def test_real_prices_are_clean(self):
        for v in (0.006, 0.22, 2.1, 15.0, 600.0, 999.99):
            self.assertIsNone(per_mtok_magnitude(v), v)

    def test_per_token_stored_as_per_m_is_too_small(self):
        for v in (2.2e-7, 3e-7, 1e-5):
            self.assertEqual(per_mtok_magnitude(v), "too_small", v)

    def test_per_1k_stored_as_per_m_is_too_large(self):
        # a $5/M model read off a per-1k table -> 5000; o1-pro's $600/M mis-scaled -> 6e5
        for v in (5000.0, 2500.0, 600000.0):
            self.assertEqual(per_mtok_magnitude(v), "too_large", v)

    def test_boundaries_are_exclusive(self):
        self.assertEqual(per_mtok_magnitude(1e-4), "suspect")   # just inside the floor band
        self.assertIsNone(per_mtok_magnitude(1e-3))             # band edge is clean
        self.assertIsNone(per_mtok_magnitude(1e3))              # warn ceiling is inclusive
        self.assertEqual(per_mtok_magnitude(1000.01), "suspect")
        self.assertEqual(per_mtok_magnitude(2000.0), "suspect")      # warn band is inclusive
        self.assertEqual(per_mtok_magnitude(2000.01), "too_large")

    def test_zero_and_null_are_not_magnitude_problems(self):
        # null = unknown, 0 = free: neither is a scale error
        for v in (None, 0, 0.0, "0"):
            self.assertIsNone(per_mtok_magnitude(v), v)

    def test_non_numeric_and_bool_are_ignored(self):
        for v in ("", "free", True, False, {}, []):
            self.assertIsNone(per_mtok_magnitude(v), v)

    def test_negative_sentinel_is_not_a_magnitude_error(self):
        # OpenRouter's -1 dynamic-routing sentinel: filtered to null before storage, but
        # the predicate must not mislabel it as too_small either.
        self.assertIsNone(per_mtok_magnitude(-1))


if __name__ == "__main__":
    unittest.main()
