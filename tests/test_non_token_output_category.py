"""Regression test for the non-token-output `max_output` audit rule.

`max_output` is the maximum number of tokens a model GENERATES. An embedding or rerank model
generates no tokens at all -- it returns a vector / a score -- so the field does not apply and
must be null.

Real case 2026-09-14: models.dev stores the embedding DIMENSION in `limit.output`
(text-embedding-3-large 3072, ada-002 / 3-small 1536, bge-m3 1024, all-mini-lm-l6-v2 384,
rerankers 1) and `sync_modelsdev.build_model` copied it verbatim into `max_output`, so 68
embedding/rerank rows published a vector size as a token limit. The pre-existing pair check
(`max_output > context_window`) saw only the 7 whose dimension happened to exceed the context
window; the other 61 -- e.g. azure/openai `text-embedding-3-large` with context 8191 and
"max_output" 3072 -- passed silently. A check that fires on only part of a bug class is itself
the bug (policy §15.1). The rule is a hard FAIL: unlike a token pair (which only the vendor can
re-derive), "an embedding model has an output-token limit" is impossible, so the stored value is
provably wrong. `sync_modelsdev.build_model` now leaves these categories null.
"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from toolbox import NON_TOKEN_OUTPUT_CATEGORIES, max_output_on_non_token_category  # noqa: E402


class TestMaxOutputNonTokenCategory(unittest.TestCase):
    def test_flags_embedding_with_dimension(self):
        # models.dev limit.output for text-embedding-3-large IS the 3072-dim vector size
        self.assertEqual(
            max_output_on_non_token_category({"category": "embedding", "max_output": 3072}),
            ("embedding", 3072),
        )

    def test_flags_rerank(self):
        self.assertEqual(
            max_output_on_non_token_category({"category": "rerank", "max_output": 1}),
            ("rerank", 1),
        )

    def test_case_insensitive_category(self):
        self.assertEqual(
            max_output_on_non_token_category({"category": "Embedding", "max_output": 1536}),
            ("embedding", 1536),
        )

    def test_null_max_output_is_clean(self):
        self.assertIsNone(
            max_output_on_non_token_category({"category": "embedding", "max_output": None})
        )
        self.assertIsNone(max_output_on_non_token_category({"category": "embedding"}))

    def test_chat_with_max_output_is_clean(self):
        # a generative model legitimately carries a generated-token limit
        self.assertIsNone(
            max_output_on_non_token_category({"category": "chat", "max_output": 384000})
        )

    def test_other_non_generative_categories_not_flagged(self):
        # audio_stt / image_gen etc. are out of scope: only embedding/rerank are asserted here
        for cat in ("audio_stt", "audio_tts", "image_gen", "video_gen"):
            self.assertIsNone(
                max_output_on_non_token_category({"category": cat, "max_output": 1024})
            )

    def test_missing_category_is_clean(self):
        self.assertIsNone(max_output_on_non_token_category({"max_output": 3072}))
        self.assertIsNone(max_output_on_non_token_category({}))

    def test_non_dict_is_clean(self):
        self.assertIsNone(max_output_on_non_token_category(None))
        self.assertIsNone(max_output_on_non_token_category("embedding"))

    def test_category_tuple_matches_audit_scope(self):
        self.assertEqual(NON_TOKEN_OUTPUT_CATEGORIES, ("embedding", "rerank"))


class TestNoViolationInRepoData(unittest.TestCase):
    """The rule must be GREEN on the repaired tree (68 rows were nulled on 2026-09-14)."""

    def test_repo_has_no_embedding_or_rerank_max_output(self):
        import glob
        import json
        bad = []
        for f in sorted(glob.glob(os.path.join(ROOT, "data/feed/providers/*.json"))):
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
            for m in d.get("models", []):
                if max_output_on_non_token_category(m):
                    bad.append(f"{d['provider_id']}::{m['id']}")
        self.assertEqual(bad, [], f"embedding/rerank rows still carrying max_output: {bad}")


if __name__ == "__main__":
    unittest.main()
