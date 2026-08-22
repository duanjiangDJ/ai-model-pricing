"""Z.AI official pricing check (tier 0). Direct fetch of the Mintlify markdown version of
the official pricing page: https://docs.z.ai/guides/overview/pricing.md

Text/Vision model tables:
  | GLM-5.2 | \$1.4 | \$0.26 | Limited-time Free | \$4.4 |
  -> model | input | cached input | storage | output (USD per 1M tokens).
'Free' cells map to 0; '-' / '\' cells map to None. GLM-5.3 is subscription-gated
(available to GLM Coding Plan users per its model page) and is skipped so it stays
subscription-included (per_mtok = null).
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "zai"
URL = "https://docs.z.ai/guides/overview/pricing.md"

SKIP = {"glm-5.3"}  # subscription-gated (GLM Coding Plan), not pay-as-you-go verified
ROW_RE = re.compile(
    r"\|\s*(GLM[\w.\-]*)\s*\|\s*(\\?\$?[\d.]+|Free|-|\\+)\s*\|\s*(\\?\$?[\d.]+|Free|-|\\+)\s*"
    r"\|\s*[^|]+\s*\|\s*(\\?\$?[\d.]+|Free|-|\\+)\s*\|"
)
SECTION_RE = re.compile(r"### (?:Text|Vision) Models[\s\S]*?(?=\n### |\Z)")


def _num(cell):
    cell = cell.strip().lstrip("\\$")
    if cell in ("Free", "free"):
        return 0.0
    if cell in ("-", "\\", ""):
        return None
    try:
        return float(cell)
    except ValueError:
        return None


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
                          "Free = 0). Parsed by check zai."),
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
