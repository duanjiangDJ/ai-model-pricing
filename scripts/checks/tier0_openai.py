"""OpenAI official pricing check (tier 0). JS-rendered page -> Wayback snapshot,
parsed from the FIRST rows block (Standard-tier inference table).
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import (  # noqa: E402
    http_get, load_provider, to_text, update_model_prices, wayback_snapshot_candidates,
)

TIER = 0
PROVIDER_ID = "openai"
URL = "https://platform.openai.com/docs/pricing"
FALLBACK_SNAPSHOTS = ["20260812013303"]


def _extract_first_rows(text):
    start = text.find('"rows":[1,[[')
    if start < 0:
        return ""
    i = text.find("[", start + 7)
    depth = 0
    j = i
    while j < len(text):
        if text[j] == "[":
            depth += 1
        elif text[j] == "]":
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
        j += 1
    return ""


def parse(text):
    text = (text.replace("&quot;", '"').replace("&lt;", "<")
            .replace("&gt;", ">").replace("&amp;", "&"))
    seg = _extract_first_rows(text)
    rows = re.findall(
        r'\[0,"(gpt-5[\w.\-]*|gpt-4[\w.\-]*|o[1-4][\w.\-]*)"\],\[0,([\d.]+|"-")\],\[0,([\d.]+|"-")\],\[0,([\d.]+|"-")\],\[0,([\d.]+|"-")\]',
        seg,
    )

    def f(v):
        return None if v == '"-"' else float(v)

    out = {}
    seen = set()
    for name, inp, cached, cw, outp in rows:
        if name in seen:
            continue
        seen.add(name)
        out[name] = {
            "per_mtok": {"input": f(inp), "output": f(outp),
                         "cache_read": f(cached), "cache_write": f(cw)},
            "notes": "Official platform.openai.com/docs/pricing (Wayback snapshot, USD/1M, standard tier). Parsed by check openai.",
        }
    return out


def run(ctx):
    text = None
    for snap in wayback_snapshot_candidates(URL) + [
        f"http://web.archive.org/web/{ts}id_/{URL}" for ts in FALLBACK_SNAPSHOTS
    ]:
        try:
            cand = to_text(http_get(snap, timeout=90))
        except Exception:  # noqa: BLE001
            continue
        if 5000 < len(cand) < 5_000_000:
            text = cand
            break
    if text is None:
        return {"changed": 0, "detail": "no usable wayback snapshot"}
    parsed = parse(text)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = update_model_prices(provider, parsed, ctx["now"], URL)
    return {"changed": len(changed), "detail": f"parsed {len(parsed)} models"}
