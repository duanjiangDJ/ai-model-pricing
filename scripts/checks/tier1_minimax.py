"""MiniMax official pricing check (tier 1). Domestic CNY via the MiniMax open-platform
billing doc (platform.minimaxi.com/docs/guides/pricing-paygo) — fetched with headless
Chrome (browser-rendered; a plain js_fetch may not render it). CNY prices are ¥/1M tokens
(standard tier). Domestic CNY is independent of the int'l USD list. The current CNY branch
was reconciled from that page on 2026-08-28; this check records the fetch status.

Verified 2026-08-28: MiniMax-M3 ¥4.2/¥16.8 (≤512k; 50% promo -> 2.10/8.40), M2.7 ¥2.1/¥8.4,
M2.7-highspeed ¥4.2/¥16.8. M2/M2.1/M2.5 are legacy (historical section, no current list).
"""
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import js_fetch, load_provider  # noqa: E402

TIER = 1
PROVIDER_ID = "minimax"
URL = "https://platform.minimaxi.com/docs/guides/pricing-paygo"

# model id -> (input ¥/1M, output ¥/1M) standard tier (used if page becomes parseable)
CN = {
    "MiniMax-M3": (4.2, 16.8),
    "MiniMax-M2.7": (2.1, 8.4),
    "MiniMax-M2.7-highspeed": (4.2, 16.8),
}


def run(ctx):
    html = js_fetch(URL, virtual_time=15000)
    if not html:
        return {"changed": 0,
                "detail": "page not auto-fetchable — CNY reconciled from official Minimax billing"
                          " doc (platform.minimaxi.com) on 2026-08-28; parser TODO"}
    return {"changed": 0, "detail": f"page fetched ({len(html)} bytes); parser TODO"}
