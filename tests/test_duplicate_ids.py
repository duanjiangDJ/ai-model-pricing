"""Regression test for case-variant duplicate model ids.

One logical model stored twice under different id casings is a data defect: the two rows
drift apart, so a consumer reading either id gets a divergent price. The exact-id dup check
is case-SENSITIVE and never fired on it. Real 2026-09-12: edenai
`flexai/DeepSeek-V4-Flash-0731` ($0.065/$0.18) vs `flexai/deepseek-v4-flash-0731`
($0.03/$0.1), and llmgateway `Qwen3.8-27B` ($0.2/$2) vs `qwen3.8-27b` ($0.42/$3). Only the
casing the declared source still publishes is kept; the other row is a stale ghost.
"""
import glob
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from toolbox import case_variant_duplicate_ids, duplicate_ids  # noqa: E402


class TestCaseVariantDuplicateIds(unittest.TestCase):
    def test_flags_the_real_edenai_pair(self):
        ids = ["flexai/DeepSeek-V4-Flash-0731", "flexai/deepseek-v4-flash-0731"]
        self.assertEqual(
            case_variant_duplicate_ids(ids),
            {"flexai/deepseek-v4-flash-0731": [
                "flexai/DeepSeek-V4-Flash-0731", "flexai/deepseek-v4-flash-0731"]},
        )

    def test_flags_the_real_llmgateway_pair(self):
        self.assertIn("qwen3.8-27b", case_variant_duplicate_ids(["Qwen3.8-27B", "qwen3.8-27b"]))

    def test_unique_ids_are_clean(self):
        self.assertEqual(case_variant_duplicate_ids(["a", "b", "c"]), {})

    def test_exact_dup_still_flagged_by_duplicate_ids(self):
        self.assertEqual(duplicate_ids(["a", "a", "b"]), {"a"})
        self.assertEqual(duplicate_ids(["a", "A"]), set())  # case-variant, not exact

    def test_live_dataset_has_no_case_variant_duplicates(self):
        for f in glob.glob(os.path.join(ROOT, "data", "feed", "providers", "*.json")):
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
            ids = [m["id"] for m in d.get("models", [])]
            self.assertEqual(case_variant_duplicate_ids(ids), {}, f"case-variant dup in {f}")


if __name__ == "__main__":
    unittest.main()
