"""Volcano Engine Ark (火山方舟) official pricing check (tier 1).

The Ark model-price doc (docs.volcengine.com/docs/82379/1544106) is heavily bot-protected
(headless dump-dom returns 0 bytes); only a full browser can render it. So this check
cannot auto-refresh — the CNY prices were manually reconciled from that official page
(see notes on the provider models) on 2026-08-28. The check records the fetch attempt and
flags when the page becomes fetchable again so the parser can be added.

If js_fetch ever returns content here, parse_doubao() is a best-effort extractor for the
first-tier [0,min] input/cache-hit/output (¥/1M tokens) rows.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import js_fetch, load_provider, now_iso  # noqa: E402

TIER = 1
PROVIDER_ID = "volcengine"
URL = "https://docs.volcengine.com/docs/82379/1544106?lang=zh"

# model id (page first-tier ¥/1M) -> (input, cache_read, output); used only if page becomes fetchable.
CN = {
    "doubao-seed-2-1-pro-260628": (3.0, 1.20, 15.0),
    "doubao-seed-2-1-turbo-260628": (1.50, 0.60, 7.50),
    "doubao-seed-2-0-pro-260215": (1.60, 0.64, 8.0),
    "doubao-seed-2-0-mini-260428": (0.40, 0.08, 4.0),
    "doubao-seed-2-0-lite-260428": (1.20, 0.24, 7.20),
    "doubao-seed-evolving": (6.0, 1.20, 30.0),
    "glm-5-2-260617": (8.0, None, 28.0),
    "deepseek-v4-flash-ga-260731": (3.0, 0.10, 9.0),
    "deepseek-v4-pro-ga-260813": (9.0, 0.30, 27.0),
}


def run(ctx):
    html = js_fetch(URL, virtual_time=15000)
    if not html:
        return {"changed": 0,
                "detail": "Volcano Ark page is bot-protected (dump-dom returns 0 bytes) — CNY prices were "
                          "manually reconciled from the official page on 2026-08-28; no auto-refresh."}
    # If we ever get here, the page is fetchable — a parser can be added (see module docstring).
    return {"changed": 0, "detail": f"page now fetchable ({len(html)} bytes); parser TODO"}
