"""Fetch OpenRouter model catalog (aggregator prices) into data/feed/providers/openrouter.json.

OpenRouter pricing fields (USD, string decimals):
  prompt, completion, image, request, web_search, input_cache_read, input_cache_write, internal_reasoning
All prices are RESELLER prices (aggregator channel), kept separate from first-party prices.

Usage: python scripts/sync_openrouter.py [--write]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    PROVIDERS, FEED, SCHEMA_VERSION, append_changelog, fetch_json, load_index,
    load_manifest, now_iso, save_index, save_manifest, to_float_or_none, write_json,
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/models"


def map_modalities(m):
    out = []
    for im in (m or []):
        if im == "text":
            out.append("text")
        elif im in ("image", "audio", "video"):
            out.append(f"{im}_in")
    return out


def _u(v):
    """Wrap a numeric price into a dual-currency object (usd key); None stays None."""
    return {"usd": v} if v is not None else None


def _per_m(v):
    """OpenRouter API pricing is PER TOKEN (USD decimals). per_mtok semantics is
    per-1M tokens, so multiply per-token by 1e6. Missing this conversion made every
    OpenRouter price land 1e6x too small (e.g. $0.22/M stored as 2.2e-7)."""
    if v is None:
        return None
    return round(v * 1e6, 8)


def build_model(entry):
    p = entry.get("pricing") or {}
    token_vals = [p.get("prompt"), p.get("completion"),
                  p.get("input_cache_read"), p.get("input_cache_write")]
    img = to_float_or_none(p.get("image"))
    has_token_price = any(v is not None and v != 0 for v in token_vals)
    if img is not None and has_token_price:
        billing = ["pay_per_image", "pay_per_token"]
    elif img is not None:
        billing = ["pay_per_image"]
    elif has_token_price:
        billing = ["pay_per_token"]
    elif entry["id"].lower().endswith(":free") or all(v == 0 for v in token_vals if v is not None):
        billing = ["free"]
    else:
        billing = ["unknown"]
    arch = entry.get("architecture") or {}
    tp = entry.get("top_provider")
    if isinstance(tp, dict):
        tp = tp.get("id") or tp.get("provider_id") or tp.get("name")
    note = f"OpenRouter reseller price; top provider: {tp}" if tp else "OpenRouter reseller price"
    if billing == ["free"]:
        note += " | Free model (per_mtok = 0)."
    pricing = {
        "per_mtok": {
            "input": _u(_per_m(to_float_or_none(p.get("prompt")))),
            "output": _u(_per_m(to_float_or_none(p.get("completion")))),
            "cache_read": _u(_per_m(to_float_or_none(p.get("input_cache_read")))),
            "cache_write": _u(_per_m(to_float_or_none(p.get("input_cache_write")))),
        },
        "per_image": [{"name": "default", "price": _u(img)}] if img is not None else None,
        "promo": None,
    }
    return {
        "id": entry["id"],
        "name": entry.get("name", entry["id"]),
        "category": "reasoning" if entry.get("reasoning") else "chat",
        "modalities": map_modalities(arch.get("input_modalities")),
        "context_window": entry.get("context_length") or None,
        "max_output": None,
        "billing_model": billing,
        "pricing": pricing,
        "notes": note,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="persist files (default: dry-run to stdout)")
    args = ap.parse_args()

    data = fetch_json(OPENROUTER_URL)
    models = [build_model(m) for m in data["data"]]
    models.sort(key=lambda m: m["id"])

    now = now_iso()
    provider = {
        "provider_id": "openrouter",
        "name": "OpenRouter",
        "channel": "aggregator",
        "category": "aggregator",
        "region": "global",
        "homepage": "https://openrouter.ai",
        "pricing_page": "https://openrouter.ai/models",
        "api_base_url": "https://openrouter.ai/api/v1",
        "currency": "USD",
        "updated_at": now,
        "verified_at": now,
        "models": models,
    }

    if not args.write:
        print(f"OpenRouter: {len(models)} models, dry-run only (use --write to persist)")
        return

    write_json(os.path.join(PROVIDERS, "openrouter.json"), provider)

    # update index.json
    index = load_index() or {
        "schema_version": SCHEMA_VERSION,
        "generated_at": now,
        "currency": "USD",
        "provider_count": 0,
        "model_count": 0,
        "plan_count": 0,
        "providers": [],
        "resellers": [],
    }
    for lst in (index["providers"], index["resellers"]):
        lst[:] = [e for e in lst if e["id"] != "openrouter"]
    index["resellers"].append({
        "id": "openrouter",
        "name": "OpenRouter",
        "channel": "aggregator",
        "model_count": len(models),
        "file": "providers/openrouter.json",
        "updated_at": now,
    })
    index["generated_at"] = now
    index["provider_count"] = len(index["providers"])
    index["model_count"] = sum(e["model_count"] for e in index["providers"]) + sum(
        e["model_count"] for e in index["resellers"]
    )
    save_index(index)

    # update manifest
    manifest = load_manifest() or {"schema_version": SCHEMA_VERSION, "sources": [], "coverage": {}}
    srcs = [s for s in manifest.get("sources", []) if s["name"] != "OpenRouter API"]
    srcs.append({"name": "OpenRouter API", "url": OPENROUTER_URL, "auto_sync": True, "last_ok": now, "last_error": None})
    manifest["sources"] = srcs
    manifest["last_daily_check"] = now
    save_manifest(manifest)

    append_changelog([{
        "date": now,
        "kind": "update",
        "scope": "provider",
        "provider_id": "openrouter",
        "item_id": "openrouter",
        "field": "catalog",
        "new": {"model_count": len(models)},
        "source": OPENROUTER_URL,
    }])
    print(f"OpenRouter: {len(models)} models written.")


if __name__ == "__main__":
    main()
