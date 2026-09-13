"""Regression test for the input/output zero-price audit rule.

Schema / docs/price-types.md invariant: `null` = not offered / unknown, `0` = genuinely free.
A model that is NOT labelled free (or subscription_included) and publishes `usd: 0` on
`input`/`output` while another field is positive therefore claims "free tokens" -- the real
meaning of that 0 is "the source publishes no price" (models.dev's sentinel), so it must be
`null`. audit.py already hard-failed this class for `cache_read`/`cache_write` (PR #147);
the two TOKEN fields were never checked, so 4 chat rows slipped through silently.

Real case 2026-09-14: greenpt `green-s`/`green-s-pro`, azure `model-router`,
privatemode-ai `voxtral-mini-3b` all carried `output: {"usd": 0}` next to a positive input,
sourced from models.dev `cost.output = 0`. They were written BEFORE sync_modelsdev's
`_u()` 0->None guard and are UNCLEARABLE by the writer afterwards (the source's 0 now maps to
None and update_model_prices skips None), so only a hand repair + this check can catch them.

`output` is exempted for structurally-zero-output categories (embedding / rerank /
audio_stt / audio_tts / image_gen / video_gen) -- those genuinely have no output tokens to
bill. `input` is never exempted.
"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from toolbox import zero_token_price_fields  # noqa: E402


class TestZeroTokenPriceFields(unittest.TestCase):
    def test_flags_zero_output_on_paid_chat_model(self):
        pm = {"input": {"usd": 0.00437}, "output": {"usd": 0}, "cache_read": None}
        self.assertEqual(zero_token_price_fields(pm, ["pay_per_token"], "chat"), ["output"])

    def test_flags_zero_input_on_paid_model(self):
        pm = {"input": {"usd": 0}, "output": {"usd": 0.66}}
        self.assertEqual(zero_token_price_fields(pm, ["pay_per_token"], "chat"), ["input"])

    def test_embedding_output_zero_is_structural(self):
        # An embedding model generates no tokens: output 0 is legitimate, input is not.
        pm = {"input": {"usd": 0.02}, "output": {"usd": 0}}
        self.assertEqual(zero_token_price_fields(pm, ["pay_per_token"], "embedding"), [])
        self.assertEqual(zero_token_price_fields(pm, ["pay_per_token"], "rerank"), [])
        self.assertEqual(zero_token_price_fields(pm, ["pay_per_token"], "audio_stt"), [])

    def test_embedding_zero_input_still_flagged(self):
        pm = {"input": {"usd": 0}, "output": {"usd": 0.02}}
        self.assertEqual(zero_token_price_fields(pm, ["pay_per_token"], "embedding"), ["input"])

    def test_free_labelled_model_not_flagged(self):
        pm = {"input": {"usd": 0}, "output": {"usd": 0}}
        self.assertEqual(zero_token_price_fields(pm, ["free"], "chat"), [])
        self.assertEqual(zero_token_price_fields(pm, ["subscription_included"], "chat"), [])

    def test_all_null_price_not_flagged(self):
        pm = {"input": None, "output": None, "cache_read": None}
        self.assertEqual(zero_token_price_fields(pm, ["unknown"], "chat"), [])

    def test_healthy_model_not_flagged(self):
        pm = {"input": {"usd": 0.3, "cny": 2.0}, "output": {"usd": 1.2, "cny": 8.0}}
        self.assertEqual(zero_token_price_fields(pm, ["pay_per_token"], "chat"), [])

    def test_scalar_billing_model_accepted(self):
        pm = {"input": {"usd": 0.1}, "output": {"usd": 0}}
        self.assertEqual(zero_token_price_fields(pm, "pay_per_token", "chat"), ["output"])
        self.assertEqual(zero_token_price_fields(pm, None, "chat"), ["output"])


if __name__ == "__main__":
    unittest.main()
