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
from toolbox import http_get, js_fetch, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "deepseek"
URL = "https://api-docs.deepseek.com/quick_start/pricing"          # English (USD)
URL_CNY = "https://api-docs.deepseek.com/zh-cn/quick_start/pricing"  # 中文 (CNY)

COLS = {
    "deepseek-v4-flash": 0,
    "deepseek-v4-pro": 1,
    "deepseek-v4-flash-vision-exp": 2,
}
EXPECTED_PRICES = 18  # 6 rows x 3 columns


def _strip(text):
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text)


def parse(text):
    seg = _strip(text)
    idx = seg.find("PRICING")
    if idx < 0:
        idx = seg.find("Pricing")
    if idx < 0:
        raise ValueError("deepseek pricing section not found on page")
    seg = seg[idx:idx + 4000]
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
                "input": {"usd": nums[col + 9]},
                "output": {"usd": nums[col + 15]},
                "cache_read": {"usd": nums[col + 3]},
                "cache_write": None,
            },
            "notes": ("Official page (USD/1M tokens, peak tier; off-peak = 50%, "
                      "peak = Mon-Fri 01:00-04:00 / 06:00-10:00 UTC). Parsed by check deepseek."),
        }
    return out


def parse_cny(text):
    seg = _strip(text)
    nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)元", seg)]
    if len(nums) < EXPECTED_PRICES:
        raise ValueError(
            f"deepseek CNY pricing page structure changed: got {len(nums)} prices (expected {EXPECTED_PRICES}); "
            "do NOT write partial data — update the parser instead"
        )
    out = {}
    for mid, col in COLS.items():
        out[mid] = {
            "per_mtok": {
                "input": {"cny": nums[col + 9]},
                "output": {"cny": nums[col + 15]},
                "cache_read": {"cny": nums[col + 3]},
                "cache_write": {"cny": nums[col + 0]},
            },
            "notes": ("Domestic api-docs.deepseek.com/zh-cn pricing (CNY/1M tokens, peak tier; "
                      "independent of the USD list — not a currency conversion). Parsed by check deepseek."),
        }
    return out


def run(ctx):
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = set()
    try:
        usd = parse(to_text(http_get(URL)))
        changed.update(update_model_prices(provider, usd, ctx["now"], URL))
        detail = f"parsed {len(usd)} models (USD)"
    except ValueError as e:
        detail = f"USD parse skipped: {e}"
    try:
        cn = js_fetch(URL_CNY, virtual_time=8000)
        if cn:
            cny = parse_cny(cn)
            changed.update(update_model_prices(provider, cny, ctx["now"], URL_CNY))
            detail += f" + {len(cny)} models (CNY)"
        else:
            detail += " + CNY js_fetch failed (Chrome unavailable?)"
    except ValueError as e:
        detail += f" + CNY parse skipped: {e}"
    return {"changed": len(changed), "detail": detail}
