"""Alibaba Cloud Model Studio (DashScope) official pricing check (tier 0). Direct fetch of
https://www.alibabacloud.com/help/en/model-studio/billing (server-rendered tables).

Row shape (raw <tr>): cells = [Model ID (+ alias note), Deployment scope, Mode?, Token
range, Input price, Output price, (cache price), unit, ...]. Scope cells are one of
Global / International / Chinese mainland / Japan / ...

To stay conservative on a page with regional scopes, promos, multimodal column layouts
and ambiguous cache columns we only:
  - take rows whose scope is exactly 'International' (alibabacloud.com USD list prices),
  - require the '1 million tokens' unit cell (excludes per-character tables),
  - require exactly 2 or 3 dollar cells (multimodal rows carry 5-6 price columns and are
    skipped; cache column is left to models.dev),
  - skip rows with 'List price' (promo listings) and rows whose model cell contains
    'Context Cache' / 'Session Cache',
  - record input/output = first two $ cells,
  - take the first row per model (doc order lists the lowest token range first).
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "alibaba"
URL = "https://www.alibabacloud.com/help/en/model-studio/billing"

TR_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
TD_RE = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S)
CELL_TEXT = lambda c: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip()  # noqa: E731
DOLLAR_RE = re.compile(r"\$([\d.]+)")
ID_RE = re.compile(r"^([a-z][a-z0-9.\-]+)")


def parse(text):
    out = {}
    for tr in TR_RE.findall(text):
        cells = [CELL_TEXT(c) for c in TD_RE.findall(tr)]
        if len(cells) < 5:
            continue
        head = cells[0]
        if "Context Cache" in head or "Session Cache" in head or "List price" in head:
            continue
        if "International" not in cells:
            continue
        if "1 million tokens" not in cells:
            continue
        prices = [float(x) for x in DOLLAR_RE.findall(" ".join(cells[1:]))]
        if len(prices) not in (2, 3):
            continue  # multimodal rows (5-6 cols) and others are skipped
        m = ID_RE.match(head)
        if not m:
            continue
        mid = m.group(1)
        if mid in out:
            continue  # first (lowest) token range wins
        out[mid] = {
            "per_mtok": {
                "input": prices[0], "output": prices[1],
                "cache_read": None, "cache_write": None,
            },
            "notes": ("Official alibabacloud.com/help/en/model-studio/billing (USD per 1M tokens, "
                      "International scope, first token range; cache left unset). "
                      "Parsed by check alibaba."),
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
