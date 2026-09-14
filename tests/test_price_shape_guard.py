"""Regression test for the price-object SHAPE guard (`toolbox.price_shape_errors`).

Every price is a dual-currency object (`{usd, cny}`). The JSON Schema types `usd`/`cny`
but does NOT set `additionalProperties: false`, so an EXTRA key is schema-legal -- and the
numeric helpers (`any_price_positive` / `price_all_zero` / the dual-currency audit rules)
read only the known keys, so a price stored under a typo/foreign key ("USD", "usd ", "eur")
passed `validate.py` AND every audit check with ZERO output: a real, unverifiable price
silently invisible to the whole pipeline.

A non-numeric value is worse than silent: `any((x or 0) > 0 for x in v.values())` raises
`TypeError: '>' not supported between instances of 'str' and 'int'`, which aborts the ENTIRE
audit (exit 1, traceback) so a single malformed field masks every later finding.

Real probe 2026-09-14 (scratch copy of the repo, `deepseek :: deepseek-flash`):
  per_mtok.input = {"usd": 0.3, "eur": "0.28"}  -> validate OK, audit OK (price dropped)
  per_mtok.input = {"eur": "0.28", ...}         -> audit TypeError (audit destroyed)
This test pins both halves: the guard REPORTS the extra key (not fatal) and flags a
non-numeric value as FATAL so the caller can fail closed instead of crashing.
"""
import glob
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from toolbox import price_shape_errors  # noqa: E402


def _model(pricing):
    return {"id": "m", "pricing": pricing}


class PriceShapeGuard(unittest.TestCase):
    def test_clean_pricing_is_clean(self):
        m = _model({
            "per_mtok": {"input": {"usd": 0.3, "cny": 2.0},
                         "output": {"usd": 1.2},
                         "cache_read": {"usd": 0.006},
                         "cache_write": None},
            "batch": {"input": {"usd": 0.15}, "output": {"usd": 0.6}},
            "per_image": [{"name": "1024", "price": {"usd": 0.04}}],
            "promo": {"list_price": {"usd": 0.5}, "ends_at": None},
        })
        self.assertEqual(price_shape_errors(m), ([], False))

    def test_null_prices_ok(self):
        self.assertEqual(price_shape_errors(_model({"per_mtok": {"input": None}})), ([], False))
        self.assertEqual(price_shape_errors(_model(None)), ([], False))

    def test_unknown_currency_key_reported_not_fatal(self):
        # the silent-pass hole: a numeric price under an unreadable key
        errs, fatal = price_shape_errors(_model({"per_mtok": {"input": {"usd": 0.3, "eur": 0.28}}}))
        self.assertFalse(fatal)
        self.assertTrue(any("eur" in e for e in errs), errs)
        self.assertTrue(any("invisible" in e for e in errs), errs)

    def test_non_numeric_value_is_fatal(self):
        errs, fatal = price_shape_errors(_model({"per_mtok": {"input": {"usd": "0.3"}}}))
        self.assertTrue(fatal)
        self.assertTrue(any("not a number" in e for e in errs), errs)

    def test_unknown_key_with_string_is_fatal(self):
        # order matters for the crash: an unreadable string feeds the `> 0` comparison
        errs, fatal = price_shape_errors(_model({"per_mtok": {"input": {"eur": "0.28", "usd": 0.3}}}))
        self.assertTrue(fatal)
        self.assertTrue(any("eur" in e for e in errs), errs)

    def test_bool_is_not_a_number(self):
        errs, fatal = price_shape_errors(_model({"per_mtok": {"input": {"usd": True}}}))
        self.assertTrue(fatal)

    def test_scalar_price_is_fatal(self):
        errs, fatal = price_shape_errors(_model({"per_mtok": {"input": 0.3}}))
        self.assertTrue(fatal)
        self.assertTrue(any("per_mtok.input" in e for e in errs), errs)

    def test_batch_and_per_image_and_promo_are_scanned(self):
        errs, fatal = price_shape_errors(_model({
            "batch": {"input": {"eur": 0.1}},
            "per_image": [{"name": "x", "price": {"usd": "nope"}}],
            "promo": {"list_price": {"gbp": 1.0}},
        }))
        self.assertTrue(fatal)
        self.assertTrue(any("batch.input.eur" in e for e in errs), errs)
        self.assertTrue(any("per_image[0].price.usd" in e for e in errs), errs)
        self.assertTrue(any("promo.list_price.gbp" in e for e in errs), errs)

    def test_current_provider_files_are_shape_clean(self):
        # Guards against the guard: every committed provider file must pass, otherwise the
        # new audit FAIL would block the 3h bot sync.
        checked = 0
        for f in glob.glob(os.path.join(ROOT, "data", "feed", "providers", "*.json")):
            with open(f, encoding="utf-8") as fh:
                prov = json.load(fh)
            for m in prov.get("models", []):
                errs, fatal = price_shape_errors(m)
                self.assertEqual((errs, fatal), ([], False),
                                 f"{prov.get('provider_id')} :: {m.get('id')} -> {errs}")
                checked += 1
        self.assertGreater(checked, 1000, "provider fixtures drifted")


if __name__ == "__main__":
    unittest.main()
