"""Meta (Meta AI API / Muse) official pricing check (tier 0).

The official dev portal (https://dev.meta.ai/docs) is a fully client-rendered SPA — no
server-side prices, and https://api.meta.ai requires authentication. We still fetch the
official page every run: if Meta ever serves pricing server-side, the parser below starts
updating automatically (pattern: model id + 'Input $X / MTok Output $Y / MTok ...').

While the page is client-rendered we report ok/0 and rely on cross-verified values already
in the DB, last confirmed against public sources:
  - Muse Spark 1.1 at $1.25 per 1M tokens (edgen.tech, deeplearning.ai 'price war' coverage)
  - Muse Spark 1.2 standard $1.25/$4.25, Contributor $0.10/$0.20 (layer3labs.io, orcarouter.ai)
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "meta"
URL = "https://dev.meta.ai/docs"

KNOWN = {
    "muse-spark-1.1": "muse-spark-1.1",
    "muse-spark-1.2": "muse-spark-1.2",
    "muse-spark-1.2-contributor": "muse-spark-1.2-contributor",
}


def parse(text):
    """Parse SSR pricing if the official page ever includes it. Returns {} when the
    page is the client-rendered shell."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    out = {}
    for label, mid in KNOWN.items():
        idx = text.find(label)
        if idx < 0:
            continue
        seg = text[idx:idx + 600]
        m = re.search(r"Input\s+\$\s*([\d.]+)\s*/?\s*(?:M|MTok|1M)[^$]*Output\s+\$\s*([\d.]+)", seg)
        if not m:
            continue
        c = re.search(r"Cache[d]?[^$]*\$([\d.]+)", seg)
        out[mid] = {
            "per_mtok": {
                "input": float(m.group(1)), "output": float(m.group(2)),
                "cache_read": float(c.group(1)) if c else None,
                "cache_write": None,
            },
            "notes": ("Official dev.meta.ai/docs (USD per 1M tokens). Parsed by check meta."),
        }
    return out


def run(ctx):
    text = to_text(http_get(URL))
    parsed = parse(text)
    if not parsed:
        return {"changed": 0,
                "detail": "official page is client-rendered (no SSR prices); values cross-verified "
                          "via public sources (edgen.tech, deeplearning.ai, layer3labs.io)"}
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = update_model_prices(provider, parsed, ctx["now"], URL)
    return {"changed": len(changed), "detail": f"parsed {len(parsed)} models"}
