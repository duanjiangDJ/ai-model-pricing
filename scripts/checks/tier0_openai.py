"""OpenAI official pricing check (tier 0).

Since 2026-08 OpenAI moved the pricing page to a Markdown-driven docs site
(developers.openai.com/api/docs/pricing). The old platform.openai.com/docs/pricing
Next.js blob and its `"rows":[1,[[...` marker no longer exist, so parse via the
`.md` version (append `.md` to the page URL) which is a plain Markdown table.
This parses the FLAGSHIP STANDARD (short context) table and maps to per_mtok.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import (  # noqa: E402
    http_get, load_provider, to_text, update_model_prices, wayback_snapshot_candidates,
)

TIER = 0
PROVIDER_ID = "openai"
URL = "https://developers.openai.com/api/docs/pricing.md"
HTML_URL = "https://developers.openai.com/api/docs/pricing"


def _val(v):
    v = (v or "").strip().replace("$", "").replace(",", "").replace(" ", "")
    return None if v in ("", "-", "—") else float(v)


def _parse_standard_table(text):
    """Extract the FIRST 'Standard pricing data' Markdown table (flagship models).

    Returns {model_id: {"per_mtok": {...}}} for rows in that table. Header columns
    (Standard, short context): Model | Input | Cached input | Cache writes | Output |
    then long-context columns follow; we take the short-context (first) group.
    """
    lines = text.splitlines()
    n = len(lines)
    i = 0
    while i < n:
        if lines[i].strip().startswith("### Standard pricing data"):
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            # j = header line; j+1 = separator line; j+2.. = data rows
            header = [c.strip() for c in lines[j].strip().strip("|").split("|")] if j < n else []
            k = j + 2
            out = {}
            while k < n and lines[k].strip().startswith("|"):
                cols = [c.strip() for c in lines[k].strip().strip("|").split("|")]
                if len(cols) >= 5:
                    model = re.sub(r"\s*\(<[^)]*\)", "", cols[0]).strip()  # strip " (<272K context length)"
                    if model and not model.startswith("Model"):
                        # Standard/Short context: Input=Cached reads=Cache writes=Output
                        out[model] = {
                            "per_mtok": {
                                "input": _val(cols[1]),
                                "cache_read": _val(cols[2]),
                                "cache_write": _val(cols[3]),
                                "output": _val(cols[4]),
                            },
                            "notes": "Official OpenAI pricing (Standard, short context, USD/1M). Parsed via developers.openai.com/api/docs/pricing.md",
                        }
                k += 1
            if out:
                return out
        i += 1
    return {}


def parse(text):
    return _parse_standard_table(text)


def _fetch(url, timeout=90):
    return to_text(http_get(url, timeout=timeout))


def run(ctx):
    # Prefer the stable Markdown version; fall back to a Wayback snapshot if it fails.
    try:
        text = _fetch(URL)
    except Exception:  # noqa: BLE001
        text = None
    if text is None or not text.strip():
        for snap in wayback_snapshot_candidates(HTML_URL):
            try:
                cand = _fetch(snap)
            except Exception:  # noqa: BLE001
                continue
            if 5000 < len(cand) < 5_000_000:
                text = cand
                break
    if text is None or not text.strip():
        return {"changed": 0, "detail": "no usable pricing source"}
    parsed = parse(text)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = update_model_prices(provider, parsed, ctx["now"], URL)
    return {"changed": len(changed), "detail": f"parsed {len(parsed)} models"}
