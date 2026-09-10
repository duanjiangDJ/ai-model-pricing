"""Changelog provenance tests: diff_openrouter must report EVERY persisted field change.

main() wholesale-replaces providers/openrouter.json's models list from the remote catalog,
so ANY changed build_model() field is persisted. If diff_openrouter tracked only a subset
(pricing + context_window/max_output), the remaining fields (name/category/modalities/
notes/billing_model) landed with NO changelog entry/source — the provenance bug class fixed
for pricing in #154/#157, generalized here to every field.

Run: python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from daily_check import diff_openrouter  # noqa: E402

NOW = "2026-09-10T00:00:00Z"


def _model(**kw):
    base = {
        "id": "m",
        "name": "M",
        "category": "chat",
        "modalities": ["text"],
        "context_window": 1000,
        "max_output": None,
        "billing_model": ["pay_per_token"],
        "pricing": {"per_mtok": {"input": {"usd": 1.0}}},
        "notes": "src",
    }
    base.update(kw)
    return base


class TestDiffProvenance(unittest.TestCase):
    def _changed(self, old, new):
        _added, _removed, changed = diff_openrouter({"models": [old]}, [new], NOW)
        return changed

    def test_modalities_change_is_tracked(self):
        ch = self._changed(_model(modalities=["text"]), _model(modalities=["text", "image"]))
        self.assertIn(("m", "modalities", ["text"], ["text", "image"]), ch)

    def test_name_change_is_tracked(self):
        self.assertIn(("m", "name", "A", "B"), self._changed(_model(name="A"), _model(name="B")))

    def test_category_change_is_tracked(self):
        ch = self._changed(_model(category="chat"), _model(category="reasoning"))
        self.assertIn(("m", "category", "chat", "reasoning"), ch)

    def test_notes_change_is_tracked(self):
        self.assertIn(("m", "notes", "x", "y"), self._changed(_model(notes="x"), _model(notes="y")))

    def test_billing_model_change_is_tracked(self):
        ch = self._changed(_model(billing_model=["pay_per_token"]),
                           _model(billing_model=["free"]))
        self.assertIn(("m", "billing_model", ["pay_per_token"], ["free"]), ch)

    def test_context_window_and_pricing_still_tracked(self):
        ch = self._changed(_model(context_window=1000), _model(context_window=2000))
        self.assertIn(("m", "context_window", 1000, 2000), ch)
        ch = self._changed(_model(pricing={"per_mtok": {"input": {"usd": 1.0}}}),
                           _model(pricing={"per_mtok": {"input": {"usd": 2.0}}}))
        self.assertTrue(any(c[1] == "pricing" for c in ch))

    def test_no_change_yields_empty(self):
        self.assertEqual(self._changed(_model(), _model()), [])
    def test_pricing_change_yields_exactly_one_entry(self):
        # a pricing change must not also fire a generic dup for the same field
        ch = self._changed(_model(pricing={"per_mtok": {"input": {"usd": 1.0}}}),
                           _model(pricing={"per_mtok": {"input": {"usd": 2.0}}}))
        self.assertEqual([c for c in ch if c[1] == "pricing"], list(ch))
        self.assertEqual(len(ch), 1)

    def test_dropped_and_added_keys_are_tracked(self):
        # main() replaces the whole model dict, so a local-only key is dropped and a
        # remote-only key is added — both are persisted changes needing provenance.
        ch = self._changed(_model(legacy_field="old"),
                           _model(new_field="new"))
        self.assertIn(("m", "legacy_field", "old", None), ch)
        self.assertIn(("m", "new_field", None, "new"), ch)



if __name__ == "__main__":
    unittest.main()
