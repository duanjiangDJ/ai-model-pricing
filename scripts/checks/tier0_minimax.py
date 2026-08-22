"""MiniMax official pricing check (tier 0). Direct fetch of the Mintlify markdown version
of the pay-as-you-go pricing page: https://platform.minimax.io/docs/guides/pricing-paygo.md

LLM table rows:
  | **MiniMax-M2.7** | $0.3 / M tokens | $1.2 / M tokens | $0.06 / M tokens | $0.375 / M tokens |
  | **MiniMax-M3**<br />≤ 512k input tokens ... | ~~$0.60~~ $0.30 / M tokens | ... |

Price cells may carry a strikethrough list price; we take the LAST $value in the cell
(the effective price, e.g. the 'Permanent 50% off' rate). The Standard tab comes first,
so the first row seen per model wins (priority 1.5x rows are ignored). M3 rows list only
input/output/cache-read; M2.x rows additionally list a cache WRITE price.
Rows priced per second / per character / per image are not matched (they lack
'/ M tokens').
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "minimax"
URL = "https://platform.minimax.io/docs/guides/pricing-paygo.md"

ROW_RE = re.compile(
    r"\|\s*\*\*(MiniMax-[^*|]+)\*\*[^|]*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|(?:\s*([^|]+)\|)?"
)
PRICE_RE = re.compile(r"\$([\d.]+)\s*/\s*M tokens")


def _prices(cell):
    vals = PRICE_RE.findall(cell)
    if not vals:
        return None
    return float(vals[-1])  # last = effective (post-discount) price


def parse(text):
    out = {}
    for mm in ROW_RE.finditer(text):
        name = mm.group(1).split("<br")[0].strip()
        cells = [mm.group(i) for i in (2, 3, 4, 5)]
        vals = []
        for c in cells:
            if c is None:
                break
            v = _prices(c)
            if v is None:
                break
            vals.append(v)
        if len(vals) < 3:
            continue
        if name != "MiniMax-M3" and len(vals) == 3:
            continue  # M2.x rows must carry the cache-write column
        if name in out:
            continue  # first (Standard) tab wins over Priority/legacy duplicates
        out[name] = {
            "per_mtok": {
                "input": vals[0], "output": vals[1],
                "cache_read": vals[2],
                "cache_write": vals[3] if len(vals) > 3 else None,
            },
            "notes": ("Official platform.minimax.io/docs/guides/pricing-paygo (USD per 1M tokens, "
                      "effective price after any promo; M3 ≤512k tier; cache-write where listed). "
                      "Parsed by check minimax."),
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
