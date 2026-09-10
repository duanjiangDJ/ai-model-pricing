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
    if not out:
        # Fail loudly: 0 rows means the page layout changed (or we got a WAF/stub page). A
        # silent empty parse lets the manifest report check:alibaba GREEN while alibaba prices
        # drift unverified — a dead check is worse than a failing one.
        raise ValueError("alibaba pricing page: no International price rows matched (layout changed?)")
    return out


def _surge_blocked(provider, parsed, surge=5.0):
    """Corrections the official page now prices >5x away from what we store.

    update_model_prices' bidirectional surge guard correctly REFUSES such a write (it is the
    protection against a mis-parse clobbering a verified price) — but the refusal is silent, so
    a genuinely-wrong stored value stays stuck and never surfaces anywhere. Real 2026-09-10:
    qwen-vl-ocr input stayed $0.72 while the official International row read $0.07, and
    qwen3-next-80b-a3b-thinking output stayed $6 vs $1.2. The check must FIRE on these.
    """
    by_id = {m["id"]: m for m in provider.get("models", [])}
    blocked = []
    for mid, data in parsed.items():
        m = by_id.get(mid)
        if not m:
            continue
        pm = (m.get("pricing") or {}).get("per_mtok") or {}
        for k, nv in (data.get("per_mtok") or {}).items():
            ov = pm.get(k)
            ov = ov.get("usd") if isinstance(ov, dict) else ov
            if ov and nv:
                ratio = nv / ov
                if ratio > surge or ratio < (1.0 / surge):
                    blocked.append(f"{mid}.{k}: stored {ov} vs official {nv}")
    return blocked


def run(ctx):
    text = to_text(http_get(URL))
    parsed = parse(text)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    blocked = _surge_blocked(provider, parsed)
    changed = update_model_prices(provider, parsed, ctx["now"], URL)
    if blocked:
        # Apply the safe changes first, then surface the stuck ones as a FAILED check so the
        # discrepancy is recorded in the manifest instead of being swallowed by the guard.
        raise RuntimeError(
            "alibaba: official price >5x from the stored value; the surge guard blocked the "
            "correction, leaving a stale price stuck (repair it against the official page): "
            + "; ".join(blocked))
    return {"changed": len(changed), "detail": f"parsed {len(parsed)} models"}
