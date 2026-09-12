"""Regression test for the model `category` classification (speech/image/embedding rows).

history: the two aggregator writers (sync_modelsdev.build_model, sync_openrouter.build_model)
assigned "reasoning" or "chat" and nothing else, so whisper / TTS / FLUX / embedding models
were published as chat models. Real 2026-09-13: 116 such rows across 31 providers (e.g.
`whisper-large-v3`, `openai/tts-1`, `bfl/flux-2-pro`, `baai/bge-m3`, `gpt-oss-safeguard-20b`).

Fix: a single shared id-signature table (toolbox.CATEGORY_SIGNATURES + category_signature_hint)
used by BOTH writers and by audit.py's check -- so the writer's inference and the gate can
never drift apart.
"""
import glob
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from common import category_signature_hint  # noqa: E402
from sync.sync_modelsdev import infer_category as md_infer  # noqa: E402
from sync.sync_openrouter import infer_category as or_infer  # noqa: E402


class TestCategorySignatureHint(unittest.TestCase):
    def test_unambiguous_ids(self):
        cases = {
            "openai/whisper-large-v3": "audio_stt",
            "openai/whisper-1": "audio_stt",
            "fish-audio/transcribe-1": "audio_stt",
            "openai/tts-1": "audio_tts",
            "nvidia/magpie-tts-zeroshot": "audio_tts",
            "bfl/flux-2-pro": "image_gen",
            "stable-diffusion-3.5-large": "image_gen",
            "fal-ai/fast-sdxl": "image_gen",
            "BAAI/bge-m3": "embedding",
            "intfloat/e5-mistral-7b-instruct": "embedding",
            "all-mini-lm-l6-v2": "embedding",
            "nvidia/synthetic-video-detector": "moderation",  # detector wins over video
            "bfl/flux-3-video": "video_gen",                  # video wins over flux
            "openai/gpt-oss-safeguard-20b": "moderation",
        }
        for mid, want in cases.items():
            self.assertEqual(category_signature_hint(mid), want, mid)

    def test_chat_models_have_no_hint(self):
        for mid in ("openai/gpt-5", "google/gemini-3.5-flash", "x-ai/grok-4.6",
                    "meta-llama/llama-4-maverick"):
            self.assertIsNone(category_signature_hint(mid), mid)

    def test_writers_agree_with_the_shared_table(self):
        # A hinted id must classify identically in both writers (and in audit.py, which
        # consumes the same helper): no modality data needed when the id is unambiguous.
        for mid in ("openai/whisper-large-v3", "openai/tts-1", "bfl/flux-2-pro",
                    "baai/bge-m3", "bfl/flux-3-video"):
            self.assertEqual(md_infer(mid, {}), category_signature_hint(mid), mid)
            self.assertEqual(or_infer({"id": mid}), category_signature_hint(mid), mid)

    def test_output_modality_fallback(self):
        # An id with no marker still classifies by the source's OUTPUT modality.
        self.assertEqual(md_infer("gpt-image-x", {"modalities": {"output": ["image"]}}), "image_gen")
        self.assertEqual(or_infer({"id": "v/a", "architecture": {"output_modalities": ["audio"]}}),
                         "audio_tts")
        self.assertEqual(or_infer({"id": "v/a", "reasoning": True}), "reasoning")


class TestNoRepoCategoryRegression(unittest.TestCase):
    def test_no_row_contradicts_its_id(self):
        bad = []
        for f in sorted(glob.glob(os.path.join(ROOT, "data/feed/providers/*.json"))):
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
            for m in d.get("models", []):
                want = category_signature_hint(m["id"])
                if want and m.get("category") != want:
                    bad.append(f"{d['provider_id']}::{m['id']} ({m.get('category')} != {want})")
        self.assertEqual(bad, [], f"category/id contradictions: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
