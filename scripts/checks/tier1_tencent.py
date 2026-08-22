"""Tencent Hunyuan official pricing check (tier 1). TokenHub billing doc (CNY/1M tokens)."""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 1
PROVIDER_ID = "tencent"
URL = "https://cloud.tencent.com/document/product/1759/127342"

# verified 2026-08: hy3 input ¥1 / output ¥4 / cache-hit ¥0.25 per 1M tokens (CNY)
VERIFIED = {
    "hy3": {"per_mtok": {"input": 1.0, "output": 4.0, "cache_read": 0.25, "cache_write": None},
            "notes": "Official TokenHub billing (CNY/1M tokens): input ¥1, output ¥4, cache-hit ¥0.25. Verified 2026-08-21."},
    "hunyuan-hy3": {"per_mtok": {"input": 1.0, "output": 4.0, "cache_read": 0.25, "cache_write": None},
                    "notes": "Official TokenHub billing (CNY/1M tokens): input ¥1, output ¥4, cache-hit ¥0.25. Verified 2026-08-21."},
}


def run(ctx):
    # The TokenHub doc page is JS-rendered; rely on verified values until a parser lands.
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = update_model_prices(provider, VERIFIED, ctx["now"], URL)
    return {"changed": len(changed), "detail": "verified constants applied (page JS-rendered)"}
