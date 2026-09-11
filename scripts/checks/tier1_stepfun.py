"""StepFun (阶跃星辰) official pricing check (tier 1). Domestic CNY list.

The pricing page (platform.stepfun.com/docs/zh/guides/pricing/details) is JS-rendered —
fetched with headless Chrome (toolbox.js_fetch). Prices are ¥/1M tokens in three columns:
input (cache miss), input (cache hit), output. The DB also carries an int'l USD list
(from the int'l site); this check adds the CNY branch. Domestic CNY is independent of the
USD list (not a conversion).

Verified 2026-08-28: step-3.5-flash ¥0.7/¥2.1, step-3.5-flash-2603 ¥0.7/¥2.1, step-3.7-flash ¥1.35/¥8.1.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import js_fetch, load_provider, now_iso, update_model_prices  # noqa: E402

TIER = 1
PROVIDER_ID = "stepfun"
URL = "https://platform.stepfun.com/docs/zh/guides/pricing/details"


def parse_stepfun(text):
    """Extract {db_id: {cny input(cache-miss), cny cache_read, cny output}}.

    Row shape: '<model> 1M tokens <in-miss>元 <in-hit>元 <out>元'. Only models actually
    present in the DB are kept (matched by page name)."""
    seg = re.sub(r"<[^>]+>", " ", text)
    seg = re.sub(r"\s+", " ", seg)
    out = {}
    for m in re.finditer(
        r"(step-[\w.\-]+)\s+1M tokens\s+([\d.]+)元\s+([\d.]+)元\s+([\d.]+)元", seg
    ):
        mid = m.group(1)
        out[mid] = {
            "input": float(m.group(2)),
            "cache_read": float(m.group(3)),
            "output": float(m.group(4)),
        }
    return out


def build_updates(parsed, now=None):
    """Wrap parse_stepfun's flat ¥/1M output into the collector contract shape.

    Returns {model_id: {"per_mtok": {"input": {"cny": ..}, "cache_read": {"cny": ..},
    "output": {"cny": ..}}, "notes": str}} — the shape make_result / price_check expect.

    CNY-only vendor: the values MUST carry the "cny" currency key. A bare scalar is coerced
    to {"usd": ...} by update_model_prices, which would store ¥ as $ (a ~7x unit error).

    Shared by run() and scripts/collect/collectors/collect_stepfun.py so the two write paths
    can never drift: the collect layer previously passed the raw flat dict straight to
    make_result, which silently produced per_mtok=None for every model -> a DEAD collector
    that parsed correctly but wrote NOTHING (2026-09-11)."""
    now = now or now_iso()
    updates = {}
    for mid, pr in parsed.items():
        updates[mid] = {
            "per_mtok": {
                "input": {"cny": pr["input"]},
                "cache_read": {"cny": pr["cache_read"]},
                "output": {"cny": pr["output"]},
            },
            "notes": (f"StepFun domestic pricing (¥/1M tokens, cache-miss/cache-hit/output): "
                      f"¥{pr['input']:g}/¥{pr['cache_read']:g}/¥{pr['output']:g}. Verified {now} (CNY). "
                      "Independent of the int'l USD list — not a currency conversion."),
        }
    return updates


def run(ctx):
    html = js_fetch(URL, virtual_time=15000)
    if not html:
        return {"changed": 0, "detail": "js_fetch failed (headless Chrome unavailable?)"}
    parsed = parse_stepfun(html)
    if not parsed:
        # Fail loudly: headless Chrome fetched a page but no price rows matched.
        raise ValueError("StepFun pricing page: no model rows matched (layout changed?)")
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    by_id = {m["id"] for m in provider["models"]}
    updates = {mid: u for mid, u in build_updates(parsed, ctx["now"]).items() if mid in by_id}
    changed = update_model_prices(provider, updates, ctx["now"], URL)
    return {"changed": len(changed), "detail": f"StepFun CNY parsed via headless Chrome ({len(updates)} models)"}
