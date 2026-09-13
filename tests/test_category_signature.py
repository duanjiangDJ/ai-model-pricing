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
            # video-generator families whose ids carry no literal "video" (2026-09-13: the
            # writers re-defaulted 54 such rows to "chat" every 3h sync)
            "google/veo-3.1-fast-generate-001": "video_gen",
            "veo-3.1-generate-preview": "video_gen",
            "openai/sora-2": "video_gen",
            "klingai/kling-v2.6-t2v": "video_gen",
            "qiniu-ai/kling-v2-6": "video_gen",
            "bytedance/seedance-2.0": "video_gen",
            "runwayml/runway-gen-4-turbo": "video_gen",
            "lumalabs/ray2": "video_gen",
            "alibaba/wan-v2.6-t2v": "video_gen",
            "wanx/wan-v2-6": "video_gen",
            "wan2-2-t2v-a14b": "video_gen",
            "happyhorse-1.1-i2v": "video_gen",
            # image generators (2026-09-13: 97 such rows were chat/reasoning)
            "google/imagen-4-fast": "image_gen",
            "google/gemini-3-pro-image-preview": "image_gen",
            "openai/gpt-image-2": "image_gen",
            "chatgpt-image-latest": "image_gen",
            "nvidia/qwen/qwen-image-edit": "image_gen",
            "wan2.7-image": "image_gen",
            "wan2.7-image-pro": "image_gen",
            "xai/grok-imagine-image-2.0": "image_gen",
            "meta/muse-image-1.0": "image_gen",
            # round 3 (2026-09-14): whole families the table still missed, each found by a
            # proactive audit sweep -- every one of these rows was published as "chat".
            "stepfun/stepaudio-2.5-asr": "audio_stt",        # `asr` was not a marker at all
            "qwen3-asr-flash": "audio_stt",
            "fal-ai/stable-audio-25/text-to-audio": "audio_tts",  # only text-to-SPEECH was known
            "stabilityai/stablediffusionxl": "image_gen",    # `stable-diffusion` was hyphen-literal
            "google/nano-banana": "image_gen",               # Google Gemini image alias
            "google/nano-banana-pro": "image_gen",
            "fish-audio/s1": "audio_tts",                    # Fish Audio TTS family
            "fish-audio/s2.1-pro-free": "audio_tts",
        }
        for mid, want in cases.items():
            self.assertEqual(category_signature_hint(mid), want, mid)

    def test_chat_models_have_no_hint(self):
        for mid in ("openai/gpt-5", "google/gemini-3.5-flash", "x-ai/grok-4.6",
                    "meta-llama/llama-4-maverick",
                    # the `kling`/`wan` markers are boundary-anchored, so these stay chat
                    "nano-gpt/thinkingmachines/Inkling-Small", "thinkingmachines/inkling"):
            self.assertIsNone(category_signature_hint(mid), mid)

    def test_asr_does_not_steal_the_tts_rows(self):
        # `fish-audio` is a TTS family marker but it must NOT outrank the stt rule: Fish Audio
        # also ships `transcribe-1`, which stays audio_stt (the ordering is load-bearing).
        self.assertEqual(category_signature_hint("fish-audio/transcribe-1"), "audio_stt")
        self.assertEqual(category_signature_hint("fish-audio/transcribe-1-free"), "audio_stt")
        self.assertEqual(category_signature_hint("fish-audio/s1"), "audio_tts")
        # `asr` is boundary-anchored: a bare substring must not match.
        self.assertIsNone(category_signature_hint("openai/gpt-5"))

    def test_ambiguous_voice_models_stay_unclassified(self):
        # Deliberately NOT in the table: gpt-audio / grok-voice-* / nemotron-voicechat / studiovoice
        # are conversational or enhancement models whose correct bucket (audio_tts vs
        # audio_understanding vs realtime) is not derivable from the id -- guessing would trade one
        # wrong category for another, so they stay as the source classifies them.
        for mid in ("openai/gpt-audio", "openai/gpt-audio-mini",
                    "vercel/spacexai/grok-voice-think-fast-1.0",
                    "nvidia/nemotron-voicechat", "nvidia/studiovoice",
                    "poe/elevenlabs/elevenlabs-music"):
            self.assertIsNone(category_signature_hint(mid), mid)

    def test_image_before_video_precedence(self):
        # `wan2.7-image` is an IMAGE generator and `wan-v2.6-t2v` a VIDEO one, even though both
        # carry the `wan` marker -- the image rule must be evaluated first.
        self.assertEqual(category_signature_hint("wan2.7-image"), "image_gen")
        self.assertEqual(category_signature_hint("alibaba/wan-v2.6-t2v"), "video_gen")
        self.assertEqual(category_signature_hint("bfl/flux-3-video"), "video_gen")

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
