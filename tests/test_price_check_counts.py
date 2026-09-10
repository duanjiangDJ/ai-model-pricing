"""price_check / write_prices contract tests.

utils.write_prices is documented to return the NUMBER of changed models and every caller
treats it as a count (price_check sums it per sub-provider, the gen_collect template prints
it as "N changed"). It previously returned the raw LIST from update_model_prices, so
price_check's cross_provider branch crashed with

    unsupported operand type(s) for +=: 'int' and 'list'

on the models.dev result — an exception swallowed by daily_check (router_pc=False) that
aborted the WHOLE unified persist path on every run. These tests lock the count contract.

Run: python -m unittest discover -s tests -v
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import collect.price_check as pc  # noqa: E402
from collect import utils  # noqa: E402


class TestWritePricesReturnsCount(unittest.TestCase):
    def test_returns_int_count_not_list(self):
        # update_model_prices returns a list of ids; write_prices must expose the count.
        with mock.patch.object(utils, "load_provider",
                               return_value={"provider_id": "x", "models": []}), \
             mock.patch.object(utils, "update_model_prices",
                               return_value=["m1", "m2", "m3"]):
            out = utils.write_prices("x", {}, "src")
        self.assertIsInstance(out, int)
        self.assertEqual(out, 3)

    def test_missing_provider_still_returns_zero(self):
        with mock.patch.object(utils, "load_provider", return_value=None):
            self.assertEqual(utils.write_prices("nope", {}, "src"), 0)


class TestPriceCheckRunCounts(unittest.TestCase):
    def test_cross_provider_counts_are_summed(self):
        fake = {
            "models.dev": {
                "provider_id": "models.dev", "cross_provider": True, "source": "s",
                "parsed": {"openai": {"a": {}}, "anthropic": {"b": {}, "c": {}}},
            },
            "deepseek": {"provider_id": "deepseek", "status": "ok",
                         "source": "s", "parsed": {"d1": {}}},
        }
        with mock.patch.object(pc, "collect", return_value=fake), \
             mock.patch.object(pc, "write_prices", return_value=2):
            summary = pc.run(dry_run=False)
        self.assertTrue(summary["models.dev"]["cross_provider"])
        self.assertEqual(summary["models.dev"]["providers"], 2)
        self.assertEqual(summary["models.dev"]["changed"], 4)   # 2 sub-providers x 2
        self.assertEqual(summary["deepseek"]["changed"], 2)

    def test_real_write_prices_integration_in_run(self):
        # Second suggestion from review: exercise the REAL write_prices inside pc.run (the
        # summation above mocks pc.write_prices, so it would not catch a list regression).
        # Mock the DB layer instead of write_prices itself.
        fake = {
            "models.dev": {
                "provider_id": "models.dev", "cross_provider": True, "source": "s",
                "parsed": {"openai": {"a": {}}, "anthropic": {"b": {}}},
            },
        }
        with mock.patch.object(pc, "collect", return_value=fake), \
             mock.patch.object(utils, "load_provider",
                               return_value={"provider_id": "x", "models": []}), \
             mock.patch.object(utils, "update_model_prices", return_value=["a", "b"]):
            summary = pc.run(dry_run=False)
        self.assertEqual(summary["models.dev"]["changed"], 4)  # 2 sub-providers x 2 events


if __name__ == "__main__":
    unittest.main()
