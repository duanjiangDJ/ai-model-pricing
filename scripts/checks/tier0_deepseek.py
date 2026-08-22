"""DeepSeek official pricing check (tier 0). Direct fetch of the Docusaurus pricing page.

Table layout: 3 columns (flash / pro / vision) x 6 price rows:
  cache-hit off/peak, cache-miss off/peak, output off/peak (CNY).
Records the PEAK tier as the list price; notes mention off-peak = 50%.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "deepseek"
URL = "https://api-docs.deepseek.com/zh-cn/quick_start/pricing"

COLS = {
    "deepseek-v4-flash": 0,
    "deepseek-v4-pro": 1,
    "deepseek-v4-flash-vision-exp": 2,
}


def parse(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    idx = text.find("价格")
    if idx < 0:
        idx = 0
    seg = text[idx:idx + 4000]
    nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*元", seg)]
    out = {}
    for mid, col in COLS.items():
        if len(nums) <= col + 15:
            continue
        out[mid] = {
            "per_mtok": {
                "input": nums[col + 9],      # cache-miss peak
                "output": nums[col + 15],    # output peak
                "cache_read": nums[col + 3],  # cache-hit peak
                "cache_write": None,
            },
            "notes": ("Official page (CNY/1M tokens, peak tier; off-peak = 50%, "
                      "peak = Beijing 9:00-12:00 / 14:00-18:00). Parsed by check deepseek."),
        }
    return out


def run(ctx):
    text = to_text(http_get(URL))
    parsed = parse(text)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = update_model_prices(provider, parsed, ctx["now"], URL)
    return {"changed": len(changed), "detail": f"parsed {len(parsed)} models"}
