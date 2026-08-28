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


def run(ctx):
    html = js_fetch(URL, virtual_time=15000)
    if not html:
        return {"changed": 0, "detail": "js_fetch failed (headless Chrome unavailable?)"}
    parsed = parse_stepfun(html)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    by_id = {m["id"] for m in provider["models"]}
    updates = {}
    for mid, pr in parsed.items():
        if mid not in by_id:
            continue
        updates[mid] = {
            "per_mtok": {
                "input": {"cny": pr["input"]},
                "cache_read": {"cny": pr["cache_read"]},
                "output": {"cny": pr["output"]},
            },
            "notes": (f"StepFun domestic pricing (¥/1M tokens, cache-miss/cache-hit/output): "
                      f"¥{pr['input']:g}/¥{pr['cache_read']:g}/¥{pr['output']:g}. Verified {now_iso()} (CNY). "
                      "Independent of the int'l USD list — not a currency conversion."),
        }
    changed = update_model_prices(provider, updates, ctx["now"], URL)
    return {"changed": len(changed), "detail": f"StepFun CNY parsed via headless Chrome ({len(updates)} models)"}
