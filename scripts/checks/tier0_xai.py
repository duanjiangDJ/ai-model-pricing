"""xAI official pricing check (tier 0). Direct fetch of the Mintlify markdown version of
the official pricing page: https://docs.x.ai/developers/pricing.md

Text API table rows:
  | grok-4.6 (< 200k prompt tokens) | 500k | $2.00 | $0.50 | $6.00 |
  -> model id | context | input | cached input | output (USD per 1M tokens).
We record the <200k tier (the repo's list-price convention; two-tier models bill the
higher rate once the prompt threshold is crossed).

Batch API: models in the '20% off standard rates' list get batch = 0.8 x standard;
models not listed have no batch discount and keep batch = null.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, price_of, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "xai"
URL = "https://docs.x.ai/developers/pricing.md"

ROW_RE = re.compile(
    r"\|\s*([a-z0-9.\-]+) \(< 200k prompt tokens\)\s*\|\s*[\d.kM]+\s*\|\s*\$([\d.]+)\s*"
    r"\|\s*\$([\d.]+)\s*\|\s*\$([\d.]+)\s*\|"
)
BATCH_LIST_RE = re.compile(r"20% off standard rates\s*\n+\s*(-\s*\S+[\s\S]*?)(?:\n\n|\Z)")


def parse(text):
    out = {}
    for mid, inp, cached, outp in ROW_RE.findall(text):
        out[mid] = {
            "per_mtok": {
                "input": float(inp), "output": float(outp),
                "cache_read": float(cached), "cache_write": None,
            },
            "notes": ("Official docs.x.ai/developers/pricing (USD per 1M tokens, <200k tier). "
                      "Parsed by check xai."),
        }
    # batch = 20% off standard rates for the listed models
    batch_ids = []
    m = BATCH_LIST_RE.search(text)
    if m:
        batch_ids = [b.strip().lstrip("- ").strip() for b in m.group(1).splitlines() if b.strip()]
    for mid, d in out.items():
        if mid in batch_ids:
            pm = d["per_mtok"]
            # dual-currency objects: read usd value, batch is 0.8 x standard (usd key)
            inp = price_of(pm, "input", "usd") or 0.0
            outp = price_of(pm, "output", "usd") or 0.0
            d["batch"] = {"input": {"usd": round(inp * 0.8, 4)},
                          "output": {"usd": round(outp * 0.8, 4)}}
        else:
            d["batch"] = None
    return out


def run(ctx):
    text = to_text(http_get(URL))
    parsed = parse(text)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = update_model_prices(provider, parsed, ctx["now"], URL)
    return {"changed": len(changed), "detail": f"parsed {len(parsed)} models"}
