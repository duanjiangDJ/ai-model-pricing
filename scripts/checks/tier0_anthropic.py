"""Anthropic official pricing check (tier 0). SSR page with
'Input $X / MTok Output $Y / MTok Prompt caching Write $W / MTok Read $R / MTok' patterns.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "anthropic"
URL = "https://www.anthropic.com/pricing"

KNOWN = {
    "Fable 5": "claude-fable-5",
    "Mythos 5": "claude-mythos-5",
    "Opus 5": "claude-opus-5",
    "Sonnet 5": "claude-sonnet-5",
    "Haiku 4.5": "claude-haiku-4-5",
}


def parse(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    out = {}
    for label, mid in KNOWN.items():
        idx = text.find(label)
        if idx < 0:
            continue
        seg = text[idx:idx + 700]
        m = re.search(
            r"Input\s+\$\s*([\d.]+)\s*/\s*MTok\s+Output\s+\$\s*([\d.]+)\s*/\s*MTok"
            r"\s+Prompt caching\s+Write\s+\$\s*([\d.]+)\s*/\s*MTok\s+Read\s+\$\s*([\d.]+)\s*/\s*MTok",
            seg,
        )
        if not m:
            continue
        out[mid] = {
            "per_mtok": {
                "input": float(m.group(1)), "output": float(m.group(2)),
                "cache_write": float(m.group(3)), "cache_read": float(m.group(4)),
            },
            "notes": "Official anthropic.com/pricing (USD/MTok, incl. cache write/read). Parsed by check anthropic.",
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
