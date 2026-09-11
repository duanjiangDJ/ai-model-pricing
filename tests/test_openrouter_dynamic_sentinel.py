"""OpenRouter -1 "dynamic routing price" sentinel regression tests (2026-09-12).

OpenRouter returns prompt/completion == -1 for router models that have NO fixed published
price (they forward the request to another model and bill at THAT model's rate): e.g.
openrouter/auto, auto-beta, bodybuilder, fusion, pareto-code.

`to_float_or_none()` maps a negative value to None, so the whole price set became None;
then `all(v == 0 for v in token_vals if v is not None)` evaluated True on the emptied
iterable and build_model() labelled the model "free" with a "per_mtok = 0" note --
publishing a false free price for a model that actually charges. build_model() now reads
the RAW price (sign intact) and classifies the -1 sentinel as billing_model=["unknown"]
with an explicit dynamic-price note.

Run: python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from sync.sync_openrouter import build_model  # noqa: E402


def _entry(mid, pricing):
    return {"id": mid, "name": mid, "pricing": pricing, "architecture": {}, "context_length": 1000}


class TestDynamicSentinel(unittest.TestCase):
    def test_minus_one_is_dynamic_not_free(self):
        m = build_model(_entry("openrouter/auto", {"prompt": "-1", "completion": "-1"}))
        self.assertEqual(m["billing_model"], ["unknown"])
        pm = m["pricing"]["per_mtok"]
        self.assertIsNone(pm["input"])
        self.assertIsNone(pm["output"])
        self.assertIn("Dynamic routing price", m["notes"])
        self.assertNotIn("Free model", m["notes"])

    def test_genuine_zero_is_free(self):
        m = build_model(_entry("vendor/model:free", {"prompt": "0", "completion": "0"}))
        self.assertEqual(m["billing_model"], ["free"])
        self.assertEqual(m["pricing"]["per_mtok"]["input"]["usd"], 0.0)
        self.assertIn("Free model (per_mtok = 0).", m["notes"])

    def test_paid_is_pay_per_token(self):
        m = build_model(_entry("vendor/paid", {"prompt": "0.0000002", "completion": "0.0000006"}))
        self.assertEqual(m["billing_model"], ["pay_per_token"])
        self.assertEqual(m["pricing"]["per_mtok"]["input"]["usd"], 0.2)

    def test_absent_prices_are_not_free(self):
        # no pricing keys at all -> must NOT be labelled free (only an explicit 0 is free)
        m = build_model(_entry("vendor/unknown", {}))
        self.assertNotEqual(m["billing_model"], ["free"])


if __name__ == "__main__":
    unittest.main()
