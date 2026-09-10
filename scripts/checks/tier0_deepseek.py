"""DeepSeek official pricing check (tier 0). Direct fetch of the Docusaurus pricing page (English, USD).

Table layout: 2 columns (flash / pro) x 6 price rows:
  cache-hit off/peak, cache-miss off/peak, output off/peak (USD).
Records the PEAK tier as the list price; notes mention off-peak = 50%.
Parsing is position-based on the row-major flattened price list; a structure
assertion (exactly 12 prices) fails loudly instead of silently writing bad data
when the page layout changes.

Layout change (2026-09-10): the official page dropped the 3rd column
(deepseek-v4-flash-vision-exp) and now lists 2 columns — the official model name
`deepseek-flash` (= DeepSeek-V4.1-Flash) and `deepseek-v4-pro` — so the row-major
flat list is 12 prices and the peak value of column c sits at idx c+2 (cache-hit),
c+6 (cache-miss) and c+10 (output). The legacy names deepseek-v4-flash /
deepseek-v4-flash-vision-exp are retired and no longer priced on the page.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, js_fetch, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "deepseek"
URL = "https://api-docs.deepseek.com/quick_start/pricing/"  # trailing slash: avoids 302, serves static price table          # English (USD)
URL_CNY = "https://api-docs.deepseek.com/zh-cn/quick_start/pricing"  # 中文 (CNY)

COLS = {
    "deepseek-v4.1-flash": 0,  # official model name on the page is `deepseek-flash`
    "deepseek-v4-pro": 1,
}
EXPECTED_PRICES = 12  # 6 rows x 2 columns

NOTE_BASE = ("Official page (USD/1M tokens, peak tier; off-peak = 50%, "
             "peak = Mon-Fri 01:00-04:00 / 06:00-10:00 UTC).")
NOTE_EXTRA = {
    "deepseek-v4.1-flash": (" Official model name on the page is deepseek-flash "
                            "(DeepSeek-V4.1-Flash); legacy names deepseek-v4-flash and "
                            "deepseek-v4-flash-vision-exp are retired and billed at this price."),
    "deepseek-v4-pro": (" From 12:00 Beijing time 2026-09-14, deepseek-v4-pro requests are "
                        "routed to V4.1-Flash and billed at the V4.1-Flash price (until a "
                        "future V4.1 Pro release)."),
}


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
                "input": {"usd": nums[col + 6]},
                "output": {"usd": nums[col + 10]},
                "cache_read": {"usd": nums[col + 2]},
                "cache_write": None,
            },
            "notes": (NOTE_BASE + NOTE_EXTRA.get(mid, "") + " Parsed by check deepseek."),
        }
    return out


def parse_cny(text):
    seg = _strip(text)
    # The domestic page prices three rows, in order: cache-hit, cache-miss,
    # output (each row = off-peak value then peak value), across 2 model columns
    # (deepseek-flash, deepseek-v4-pro) -> 12 prices, peak value of column c at
    # idx c+2 / c+6 / c+10. DeepSeek publishes NO separate cache-write price, so
    # cache_write must stay null (same as parse()). Assert the row labels so a
    # future layout change fails loudly instead of silently grabbing an unrelated
    # number. (Fixed 2026-09-10: `nums[col + 0]` — the off-peak CACHE-HIT price —
    # had been written into cache_write, e.g. flash cache_write.cny=0.05 was really
    # the off-peak cache-hit value.)
    for _label in ("缓存命中", "缓存未命中", "输出"):
        if _label not in seg:
            raise ValueError(
                f"deepseek CNY pricing page structure changed: missing row label {_label!r}; "
                "do NOT write partial data — update the parser instead"
            )
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
                "input": {"cny": nums[col + 6]},
                "output": {"cny": nums[col + 10]},
                "cache_read": {"cny": nums[col + 2]},
                "cache_write": None,  # no cache-write row on the page (see note above)
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
