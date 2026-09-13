"""Regression test for the "unseeded official model" silent-skip class.

`update_model_prices()` never ADDS a model: a parsed official id that is absent from the
provider file is skipped silently, so a first-party check can stay green forever while the
vendor's live models never enter the DB. Real 2026-09-13: stepfun's whole `stepaudio-*`
family — 6 token-priced models on the official pricing page, 0 in the provider file (the
check's id regex was `step-`, which silently dropped the family; a second class of 4 ids was
parsed but never seeded). Alibaba had 56 such ids, google 6.

Fix: price_check.py records each unresolved id set in the changelog as
`kind="verify"`, `field="unseeded_official:<pid>"` (deduped), and audit.py check #11 WARNs
while any recorded id is still absent — the warning drops out automatically once seeded.

Run: python -m unittest discover -s tests -v
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import toolbox  # noqa: E402

NOW = "2026-09-13T00:00:00Z"


class TestRecordUnseededOfficial(unittest.TestCase):
    def setUp(self):
        self._meta = toolbox.META
        self._tmp = tempfile.TemporaryDirectory()
        toolbox.META = self._tmp.name
        with open(os.path.join(self._tmp.name, "changelog.json"), "w", encoding="utf-8") as f:
            json.dump({"schema_version": "26.137.88", "entries": []}, f)

    def tearDown(self):
        toolbox.META = self._meta
        self._tmp.cleanup()

    def _entries(self):
        with open(os.path.join(self._tmp.name, "changelog.json"), encoding="utf-8") as f:
            return json.load(f)["entries"]

    def test_records_ids_then_dedups_identical_set(self):
        toolbox.record_unseeded_official(
            "stepfun", ["stepaudio-2.5-chat", "step-audio-2"], NOW, "tier1_stepfun:source")
        e = self._entries()
        self.assertEqual(len(e), 1)
        self.assertEqual(e[0]["field"], "unseeded_official:stepfun")
        self.assertEqual(e[0]["kind"], "verify")
        self.assertEqual(e[0]["provider_id"], "stepfun")
        self.assertEqual(e[0]["new"]["ids"], ["step-audio-2", "stepaudio-2.5-chat"])
        self.assertEqual(e[0]["new"]["count"], 2)
        # the same pending set must NOT be re-appended by every 3h sync
        toolbox.record_unseeded_official(
            "stepfun", ["step-audio-2", "stepaudio-2.5-chat"], NOW, "tier1_stepfun:source")
        self.assertEqual(len(self._entries()), 1)

    def test_changed_set_is_recorded_again(self):
        toolbox.record_unseeded_official("stepfun", ["a"], NOW, "src")
        toolbox.record_unseeded_official("stepfun", ["a", "b"], NOW, "src")
        self.assertEqual(len(self._entries()), 2)

    def test_empty_is_a_noop(self):
        toolbox.record_unseeded_official("stepfun", [], NOW, "src")
        self.assertEqual(self._entries(), [])


if __name__ == "__main__":
    unittest.main()
