"""Moonshot AI (Kimi) official pricing check (tier 0). The platform docs (Mintlify,
platform.kimi.ai, formerly platform.moonshot.ai) publish one pricing page per model
family with a <DocTable rows={[...]}> block:

  6-col row: ["kimi-k3", "1M tokens", <cache_hit>, <cache_miss>, <output>, "context"]
  5-col row: ["moonshot-v1-8k", "1M tokens", <input>, <output>, "context"]
  batch row: ["kimi-k2.6 (Batch)", "1M tokens", "$0.10", "$0.57", "$2.40", "context"]

Price cells are either <>{&quot;$&quot;}0.30</> or "$0.114". We fetch all pricing pages,
map cache_hit -> cache_read and cache_miss -> input, and store batch rows (60% of
standard) under the base model id. Rows for models absent from the provider file are
skipped by update_model_prices.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "moonshotai"
BASE = "https://platform.kimi.ai/docs/pricing"
PAGES = ["chat-k3", "chat-k27-code", "chat-k26", "chat-k25", "chat-v1", "batch"]

ROWS_RE = re.compile(r"rows=\{\[\s*(.*?)\s*\]\}", re.S)
ROW_RE = re.compile(r"\[\s*((?:\"(?:[^\"]|\\\")*\"|<>[^<]*</>)\s*,\s*(?:\"(?:[^\"]|\\\")*\"|<>[^<]*</>)\s*,?)+?\]")
CELL_RE = re.compile(r'<>\{[^}]*"?"?\$?"?\}?([\d.]+)</>|"\$([\d.]+)"|"([^"]*)"')


def _cells(row):
    vals = []
    for mm in CELL_RE.finditer(row):
        v = mm.group(1) or mm.group(2) or mm.group(3)
        vals.append(v)
    return vals


def parse(text):
    """Return (per_model, per_batch): {id: per_mtok dict} and {id: {input, output}}."""
    per_model, per_batch = {}, {}
    for rows_block in ROWS_RE.findall(text):
        for row in rows_block.split("],"):
            if '["' not in row:
                continue
            cells = _cells(row)
            if len(cells) < 5:
                continue
            mid = cells[0]
            if "(Batch)" in mid:
                base = mid.replace(" (Batch)", "")
                if len(cells) >= 5:
                    per_batch[base] = {"input": float(cells[3]), "output": float(cells[4])}
                continue
            if len(cells) >= 6:  # cache_hit, cache_miss, output
                per_model[mid] = {
                    "per_mtok": {
                        "input": float(cells[3]), "output": float(cells[4]),
                        "cache_read": float(cells[2]), "cache_write": None,
                    },
                    "notes": ("Official platform.kimi.ai/docs/pricing (USD per 1M tokens; "
                              "cache-hit = cache_read, cache-miss = input). Parsed by check moonshotai."),
                }
            elif len(cells) >= 5:  # input, output
                per_model[mid] = {
                    "per_mtok": {
                        "input": float(cells[2]), "output": float(cells[3]),
                        "cache_read": None, "cache_write": None,
                    },
                    "notes": ("Official platform.kimi.ai/docs/pricing (USD per 1M tokens). "
                              "Parsed by check moonshotai."),
                }
    return per_model, per_batch


def run(ctx):
    parsed, batches = {}, {}
    for slug in PAGES:
        try:
            text = to_text(http_get(f"{BASE}/{slug}.md", timeout=60))
        except Exception:  # noqa: BLE001
            continue
        pm, pb = parse(text)
        parsed.update(pm)
        batches.update(pb)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = update_model_prices(provider, parsed, ctx["now"], f"{BASE}/chat-k3.md")
    # batch rows: store as {input, output} under existing models
    by_id = {m["id"]: m for m in provider.get("models", [])}
    batch_changed = []
    for mid, b in batches.items():
        m = by_id.get(mid)
        if not m:
            continue
        cur = m.setdefault("pricing", {}).get("batch")
        if cur != b:
            m["pricing"]["batch"] = b
            batch_changed.append(mid)
    if batch_changed:
        from toolbox import append_changelog, now_iso  # noqa: PLC0415
        provider["updated_at"] = ctx["now"]
        from toolbox import save_provider  # noqa: PLC0415
        save_provider(provider)
        append_changelog([{
            "date": ctx["now"], "kind": "update", "scope": "model",
            "provider_id": PROVIDER_ID, "item_id": ",".join(batch_changed),
            "field": "pricing", "new": {"models": len(batch_changed), "batch": True},
            "source": f"{BASE}/batch.md",
        }])
    return {"changed": len(changed) + len(batch_changed),
            "detail": f"parsed {len(parsed)} models, batch {len(batches)}"}
