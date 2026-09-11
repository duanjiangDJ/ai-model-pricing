"""A collector must feed make_result the {per_mtok, notes} contract shape.

Bug class (2026-09-11): a collector that reuses a check's LOW-LEVEL flat parse (e.g.
tier1_stepfun.parse_stepfun -> {input, output, cache_read}) and passes it straight to
make_result silently produced per_mtok=None for every model. make_result read
info.get("per_mtok") on a dict that had no such key, so the collector parsed the page
correctly and then wrote NOTHING — a dead collector that looks green (status ok, parsed N)
while the provider's CNY branch was never updated. collect_stepfun and collect_baidu were
both dead this way.

Two guards:
  - make_result now RAISES on that shape mismatch (fail loud, never a silent no-op);
  - each collector's build_updates produces the contract shape with the correct currency
    key (CNY for these ¥-only vendors — a scalar would be coerced to usd = a ~7x unit error).

Run: python -m unittest discover -s tests
"""
import importlib
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

from collect import utils  # noqa: E402


class TestMakeResultContract(unittest.TestCase):
    def test_accepts_contract_shape(self):
        r = utils.make_result("x", "src", {"m": {"per_mtok": {"input": {"usd": 1.0}}, "notes": "n"}})
        self.assertEqual(r["parsed"]["m"]["per_mtok"], {"input": {"usd": 1.0}})
        self.assertEqual(r["parsed"]["m"]["notes"], "n")

    def test_raises_on_flat_price_dict(self):
        with self.assertRaises(ValueError) as cm:
            utils.make_result("stepfun", "src", {"step-3.5-flash": {"input": 0.7, "output": 2.1}})
        self.assertIn("per_mtok", str(cm.exception))

    def test_notes_only_entry_is_allowed(self):
        # a note-only update (no price keys) is legitimate and must not raise
        r = utils.make_result("x", "src", {"m": {"notes": "verified"}})
        self.assertIsNone(r["parsed"]["m"]["per_mtok"])


class TestCnyCollectorsCarryContractShape(unittest.TestCase):
    def _collect(self, mod_name, parse_attr, fetch_attr, flat):
        mod = importlib.import_module(f"collect.collectors.{mod_name}")
        with mock.patch.object(mod, fetch_attr, return_value="<html/>"), \
             mock.patch.object(mod, parse_attr, return_value=flat):
            return mod.collect({"now": "2026-01-01T00:00:00Z"})

    def test_stepfun_collect_emits_cny_per_mtok(self):
        flat = {"step-3.5-flash": {"input": 0.7, "cache_read": 0.14, "output": 2.1}}
        res = self._collect("collect_stepfun", "parse_stepfun", "js_fetch", flat)
        pm = res["parsed"]["step-3.5-flash"]["per_mtok"]
        self.assertEqual(pm["input"], {"cny": 0.7})
        self.assertEqual(pm["output"], {"cny": 2.1})
        self.assertEqual(pm["cache_read"], {"cny": 0.14})
        self.assertTrue(res["parsed"]["step-3.5-flash"]["notes"])

    def test_baidu_collect_emits_cny_per_mtok(self):
        flat = {"ernie-5.0": {"input": 6000.0, "output": 24000.0}}
        res = self._collect("collect_baidu", "parse_qianfan", "js_fetch", flat)
        pm = res["parsed"]["ernie-5.0"]["per_mtok"]
        self.assertEqual(pm["input"], {"cny": 6000.0})
        self.assertEqual(pm["output"], {"cny": 24000.0})
        self.assertTrue(res["parsed"]["ernie-5.0"]["notes"])

    def test_no_collector_passes_a_flat_price_dict(self):
        """Every collector whose parse fn returns a flat price dict must wrap it first."""
        # stepfun/baidu flat objs must route through build_updates; verified indirectly by the
        # two tests above. This asserts the shared wrappers exist and are contract-shaped.
        for chk, attr in (("checks.tier1_stepfun", "build_updates"),
                          ("checks.tier1_baidu", "build_updates")):
            mod = importlib.import_module(chk)
            self.assertTrue(hasattr(mod, attr), f"{chk}.{attr} missing (the shared wrapper)")


if __name__ == "__main__":
    unittest.main()
