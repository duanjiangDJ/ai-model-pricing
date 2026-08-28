"""Baidu Qianfan official pricing check (tier 1). Domestic CNY + int'l USD.

The Qianfan ModelBuilder pricing page (cloud.baidu.com/doc/qianfan/s/wmh4sv6ya) is
client-side rendered — fetched with headless Chrome (toolbox.js_fetch). Prices are
quoted in ¥/1k tokens; we convert to ¥/1M tokens (x1000). The int'l EUR/USD list
(ernie-5.0 $1.4/$5.6) was already captured on the int'l pricing page and is preserved;
this check adds the CNY branch (and CNY-only models like ernie-5.1/4.5-turbo that have
no int'l USD list). Domestic CN and int'l USD are independent prices — not a conversion.

Verified 2026-08-28: ernie-5.0 ¥6/¥24 (¥/1M), ernie-5.1 ¥4/¥18, ernie-4.5-turbo ¥0.8/¥3.2.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import js_fetch, load_provider, now_iso, update_model_prices  # noqa: E402

TIER = 1
PROVIDER_ID = "baidu"
URL = "https://cloud.baidu.com/doc/qianfan/s/wmh4sv6ya"

# page model name -> DB id (we only patch the models present in baidu.json)
ID_MAP = {
    "ernie-5.1": "ernie-5.1",
    "ernie-5.0": "ernie-5.0",
    "ernie-4.5-turbo": "ernie-4.5-turbo",
}


def parse_qianfan(text):
    """Extract {db_id: {cny input, cny output}} — unit ¥/1k tokens -> ¥/1M tokens (x1000).
    We match the first (<=32k) tier. Page quirks: model names are uppercase, '&lt;=32k'
    is escaped, and the price unit may repeat or carry over. so we anchor on the model
    name, then take the FIRST '输入' price and the following '输出' price, ignoring
    intermediate tier labels."""
    seg = re.sub(r"<[^>]+>", " ", text)
    seg = re.sub(r"\s+", " ", seg)
    out = {}
    for name, db_id in ID_MAP.items():
        m = re.search(
            re.escape(name)
            + r"[\s\S]{0,500}?输入(?:（[^）]*）)?\s*([\d.]+)\s*(?:[元-]+\s*元/千tokens)"
            r"[\s\S]{0,200}?输出(?:（[^）]*）)?\s*([\d.]+)",
            seg,
            re.IGNORECASE,
        )
        if m:
            out[db_id] = {"input": float(m.group(1)) * 1000, "output": float(m.group(2)) * 1000}
    return out


def run(ctx):
    html = js_fetch(URL, virtual_time=10000)
    if not html:
        return {"changed": 0, "detail": "js_fetch failed (headless Chrome unavailable?)"}
    parsed = parse_qianfan(html)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    updates = {}
    for mid, pr in parsed.items():
        updates[mid] = {
            "per_mtok": {
                "input": {"cny": pr["input"]},
                "output": {"cny": pr["output"]},
            },
            "notes": (f"Qianfan domestic pricing (¥/1M tokens): input ¥{pr['input']:g}, "
                      f"output ¥{pr['output']:g} (<=32k tier). Verified {now_iso()} (CNY). "
                      "Independent of the int'l USD list — not a currency conversion."),
        }
    changed = update_model_prices(provider, updates, ctx["now"], URL)
    return {"changed": len(changed), "detail": f"Qianfan CNY parsed via headless Chrome ({len(parsed)} models)"}
