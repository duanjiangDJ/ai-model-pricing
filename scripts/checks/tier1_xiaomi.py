"""Xiaomi MiMo official pricing check (tier 1). Official docs: mimo.mi.com/docs/price/pay-as-you-go (USD/1M)."""
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import load_provider, update_model_prices  # noqa: E402

TIER = 1
PROVIDER_ID = "xiaomi"
URL = "https://mimo.mi.com/docs/price/pay-as-you-go"

# verified 2026-08-21 from official docs (USD/1M tokens)
VERIFIED = {
    "mimo-v2.5": {"per_mtok": {"input": 0.14, "output": 0.28, "cache_read": 0.0028, "cache_write": None},
                  "notes": "Official pay-as-you-go (USD/1M tokens, mimo.mi.com/docs/price/pay-as-you-go). CN: ¥1/¥2."},
    "mimo-v2.5-pro": {"per_mtok": {"input": 0.435, "output": 0.87, "cache_read": 0.0036, "cache_write": None},
                      "notes": "Official pay-as-you-go (USD/1M tokens). CN: ¥3/¥6."},
    # V2 series officially deprecated 2026-06-30
    "mimo-v2-flash": {"per_mtok": {"input": None, "output": None, "cache_read": None, "cache_write": None},
                      "status": "retired", "notes": "Officially deprecated 2026-06-30 (MiMo-V2 series retired)."},
    "mimo-v2-pro": {"per_mtok": {"input": None, "output": None, "cache_read": None, "cache_write": None},
                    "status": "retired", "notes": "Officially deprecated 2026-06-30 (MiMo-V2 series retired)."},
    "mimo-v2-omni": {"per_mtok": {"input": None, "output": None, "cache_read": None, "cache_write": None},
                     "status": "retired", "notes": "Officially deprecated 2026-06-30 (MiMo-V2 series retired)."},
    "mimo-v2-tts": {"per_mtok": {"input": None, "output": None, "cache_read": None, "cache_write": None},
                    "status": "retired", "notes": "Officially deprecated 2026-06-30 (MiMo-V2 series retired)."},
}


def run(ctx):
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = update_model_prices(provider, VERIFIED, ctx["now"], URL)
    return {"changed": len(changed), "detail": "verified constants applied"}
