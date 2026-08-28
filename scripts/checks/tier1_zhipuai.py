"""Zhipu (bigmodel.cn, domestoric) official pricing check (tier 1).

The domestic pricing page (open.bigmodel.cn/pricing) is client-side rendered (JS) —
curl/urllib returns an empty shell, so this check fetches it with headless Chrome
(toolbox.js_fetch) and parses the CNY list prices. USD list prices come from the
z.ai international pricing and are left untouched (a model carries both currencies).

Verified 2026-08-28: the domestic page lists GLM-5.3 in ¥8 / ¥28 / ¥2 etc. These are
independent of the z.ai USD list (e.g. GLM-5.3 $1.4/$4.4) — NOT a currency conversion.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import js_fetch, load_provider, now_iso, update_model_prices  # noqa: E402

TIER = 1
PROVIDER_ID = "zhipuai"
URL = "https://open.bigmodel.cn/pricing"

# Model-name -> DB id. Page names are already close to DB ids; normalize by lowercase.
# Some page names need an explicit mapping (e.g. 'GLM-5-Turbo'). Unmatched names are skipped.
ID_MAP = {
    "glm-5.3": "glm-5.3",
    "glm-5.3-flash": "glm-5.3-flash",
    "glm-5.2": "glm-5.2",
    "glm-5.1": "glm-5.1",
    "glm-5-turbo": "glm-5-turbo",
    "glm-5": "glm-5",
    "glm-4.7": "glm-4.7",
    "glm-4.5-air": "glm-4.5-air",
    "glm-4.7-flashx": "glm-4.7-flashx",
    "glm-4.7-flash": "glm-4.7-flash",
}


def parse_bigmodel(text):
    """Extract {db_id: {cny input, cny output}} from the bigmodel.cn pricing text."""
    out = {}
    for m in re.finditer(
        r"(GLM-[\d.]+(?:-FlashX|-Flash|-Air|-Turbo|-5v)?)\s+(?:新品|5折[^ ]*)?\s*[^元]{0,60}?"
        r"(\d+(?:\.\d+)?)元\s+(\d+(?:\.\d+)?)元",
        text,
    ):
        name = m.group(1).lower()
        mid = ID_MAP.get(name)
        if not mid:
            continue
        out[mid] = {"input": float(m.group(2)), "output": float(m.group(3))}
    return out


def run(ctx):
    # The domestic page is JS-rendered, so use headless Chrome.
    html = js_fetch(URL, virtual_time=12000)
    if not html:
        return {"changed": 0, "detail": "js_fetch failed (headless Chrome unavailable?)"}
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    parsed = parse_bigmodel(text)

    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}

    # Build updates that set only the CNY branch (USD branch kept from the z.ai list).
    updates = {}
    for mid, pr in parsed.items():
        updates[mid] = {
            "per_mtok": {
                "input": {"cny": pr["input"]},
                "output": {"cny": pr["output"]},
            },
            "notes": (f"Domestic bigmodel.cn pricing (CNY/1M tokens): input ¥{pr['input']:g}, "
                      f"output ¥{pr['output']:g}. Official page, verified {now_iso()} (CNY). "
                      "Independent of z.ai USD list — not a currency conversion."),
        }
    changed = update_model_prices(provider, updates, ctx["now"], URL)
    return {"changed": len(changed), "detail": f"bigmodel.cn CNY parsed via headless Chrome ({len(parsed)} models)"}
