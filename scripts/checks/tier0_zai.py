"""Z.AI official pricing check (tier 0). Direct fetch of the Mintlify markdown version of
the official pricing page: https://docs.z.ai/guides/overview/pricing.md

Model tables (Latest / Text / Vision), all "Prices per 1M tokens":
  | GLM-5.2 | \$1.4 | \$0.26 | Limited-time Free | \$4.4 |
  | GLM-5.3-Flash | ~~\$0.15~~ \$0.075 | ~~\$0.03~~ \$0.015 | Limited-time Free | ~~\$0.50~~ \$0.25 |
  -> model | input | cached input | storage | output (USD per 1M tokens).
Promo cells keep the strikethrough list price; we take the LAST $value (effective price).
'Free' cells map to 0; '-' / '\' cells map to None. GLM-5.3 is subscription-gated
(available to GLM Coding Plan users per its model page) and is skipped so it stays
subscription-included (per_mtok = null).

Brand-new official models (e.g. a fresh GLM release appearing only in the Latest table)
are added to the provider file automatically (kind: add changelog entry).
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import (  # noqa: E402
    append_changelog, http_get, load_provider, save_provider, to_text, update_model_prices,
)

TIER = 0
PROVIDER_ID = "zai"
URL = "https://docs.z.ai/guides/overview/pricing.md"

SKIP = {"glm-5.3"}  # subscription-gated (GLM Coding Plan), not pay-as-you-go verified
ROW_RE = re.compile(
    r"\|\s*(GLM[\w.\-]*)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*[^|]+\s*\|\s*([^|]+)\s*\|"
)
NUM_RE = re.compile(r"\$([\d.]+)")
SECTION_RE = re.compile(r"### (?:Latest|Text|Vision) Models[\s\S]*?(?=\n### |\Z)")


def _num(cell):
    cell = cell.strip()
    nums = NUM_RE.findall(cell)
    if nums:
        return float(nums[-1])  # last = effective (post-promo) price
    if cell.startswith("Free"):
        return 0.0
    return None  # '-' / '\' / empty cells


def parse(text):
    out = {}
    for sec in SECTION_RE.findall(text):
        if "per 1M tokens" not in sec:
            continue
        for mm in ROW_RE.finditer(sec):
            mid = mm.group(1).lower().replace(" ", "-")
            if mid in SKIP:
                continue
            inp, cached, outp = _num(mm.group(2)), _num(mm.group(3)), _num(mm.group(4))
            if inp is None or outp is None:
                continue
            out[mid] = {
                "per_mtok": {
                    "input": inp, "output": outp,
                    "cache_read": cached, "cache_write": None,
                },
                "notes": ("Official docs.z.ai/guides/overview/pricing (USD per 1M tokens; "
                          "effective price after promos; Free = 0). Parsed by check zai."),
            }
    return out


def run(ctx):
    text = to_text(http_get(URL))
    parsed = parse(text)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = update_model_prices(provider, parsed, ctx["now"], URL)
    # brand-new official models: append them (id/name/category/pricing/status/notes)
    by_id = {m["id"]: m for m in provider.get("models", [])}
    added = []
    for mid, data in parsed.items():
        if mid in by_id:
            continue
        provider["models"].append({
            "id": mid,
            "name": mid,
            "category": "chat",
            "status": "online",
            "context_window": None,
            "max_output": None,
            "pricing": {
                "per_mtok": data["per_mtok"], "batch": None, "per_image": None,
                "per_audio_second": None, "per_request": None,
            },
            "notes": data.get("notes", ""),
        })
        added.append(mid)
    if added:
        provider["updated_at"] = ctx["now"]
        provider["verified_at"] = ctx["now"]
        save_provider(provider)
        append_changelog([{
            "date": ctx["now"], "kind": "add", "scope": "model", "provider_id": PROVIDER_ID,
            "item_id": ",".join(added), "field": "catalog", "new": {"models": len(added)},
            "source": URL,
        }])
    return {"changed": len(changed) + len(added),
            "detail": f"parsed {len(parsed)} models, added {len(added)}"}
