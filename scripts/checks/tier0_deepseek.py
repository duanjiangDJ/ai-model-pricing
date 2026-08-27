"""DeepSeek official pricing check (tier 0). Direct fetch of the Docusaurus pricing page (English, USD).

Table layout: 3 columns (flash / pro / vision) x 6 price rows:
  cache-hit off/peak, cache-miss off/peak, output off/peak (USD).
Records the PEAK tier as the list price; notes mention off-peak = 50%.
Parsing is position-based on the row-major flattened price list; a structure
assertion (exactly 18 prices) fails loudly instead of silently writing bad data
when the page layout changes.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "deepseek"
URL = "https://api-docs.deepseek.com/quick_start/pricing"

COLS = {
    "deepseek-v4-flash": 0,
    "deepseek-v4-pro": 1,
    "deepseek-v4-flash-vision-exp": 2,
}
EXPECTED_PRICES = 18  # 6 rows x 3 columns


def parse(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    idx = text.find("PRICING")
    if idx < 0:
        idx = text.find("Pricing")
    if idx < 0:
        raise ValueError("deepseek pricing section not found on page")
    seg = text[idx:idx + 4000]
    nums = [float(x) for x in re.findall(r"\$\s*([\d.]+)", seg)]
    if len(nums) < EXPECTED_PRICES:
        raise ValueError(
            f"deepseek pricing page structure changed: got {len(nums)} $prices (expected {EXPECTED_PRICES}); "
            "do NOT write partial data — update the parser instead"
        )
    out = {}
    for mid, col in COLS.items():
        out[mid] = {
            "per_mtok": {
                "input": nums[col + 9],      # cache-miss peak
                "output": nums[col + 15],    # output peak
                "cache_read": nums[col + 3],  # cache-hit peak
                "cache_write": None,
            },
            "notes": ("Official page (USD/1M tokens, peak tier; off-peak = 50%, "
                      "peak = Mon-Fri 01:00-04:00 / 06:00-10:00 UTC). Parsed by check deepseek."),
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
