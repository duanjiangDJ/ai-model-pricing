"""Fetch models.dev catalog (first-party official prices for many providers).

models.dev api.json: {provider_id: {id, name, models: {model_id: {id, name, limit{context,output}, cost{input,output,cache_read}, ...}}}}
Costs are USD per 1M tokens (official list prices, not reseller prices).

Policy:
  - If data/feed/providers/{id}.json already exists -> SKIP (keep existing richer data).
  - Otherwise write a provider file with channel inferred (first_party / hosted / aggregator).

Usage: python scripts/sync_modelsdev.py [--write] [--force]
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    PROVIDERS, SCHEMA_VERSION, append_changelog, fetch_json, load_index, load_manifest,
    now_iso, save_index, save_manifest, write_json,
)

MODELSDEV_URL = "https://models.dev/api.json"

FIRST_PARTY = {
    "openai", "anthropic", "google", "xai", "mistral", "cohere", "ai21", "deepseek",
    "alibaba", "baidu", "tencent", "zhipu", "moonshot", "minimax", "stepfun",
    "lingyiwanwu", "iflytek", "baichuan", "qwen", "gemini", "perplexity", "elevenlabs",
    "deepgram", "assemblyai", "cartesia", "playai", "nvidia", "stability", "fal",
    "kimi", "doubao", "volcengine", "spark", "hunyuan",
}
AGGREGATOR_HINTS = ("router", "aggregator", "gateway", "proxy", "relay")


def infer_channel(pid, name, api):
    low = f"{pid} {name}".lower()
    if any(h in low for h in AGGREGATOR_HINTS):
        return "aggregator"
    if pid in FIRST_PARTY:
        return "first_party"
    return "hosted"


def infer_category(mid, m):
    if m.get("reasoning"):
        return "reasoning"
    low = mid.lower()
    if "embed" in low:
        return "embedding"
    if "rerank" in low or "rank" in low:
        return "rerank"
    return "chat"


def _u(v):
    """Wrap a numeric price into a dual-currency object (usd key); None stays None."""
    return {"usd": v} if v is not None else None


def build_model(mid, m):
    cost = m.get("cost") or {}
    limit = m.get("limit") or {}
    token_vals = [cost.get("input"), cost.get("output"), cost.get("cache_read")]
    has_token_price = any(v is not None and v != 0 for v in token_vals)
    if has_token_price:
        billing = ["pay_per_token"]
    elif any(v == 0 for v in token_vals if v is not None):
        billing = ["free"]
    else:
        billing = ["unknown"]
    note = "models.dev official list price"
    if billing == ["free"]:
        note += " | Free model (per_mtok = 0)."
    return {
        "id": mid,
        "name": m.get("name", mid),
        "category": infer_category(mid, m),
        "modalities": ["text"],
        "context_window": limit.get("context") or None,
        "max_output": limit.get("output") or None,
        "billing_model": billing,
        "pricing": {
            "per_mtok": {
                "input": _u(cost.get("input")),
                "output": _u(cost.get("output")),
                "cache_read": _u(cost.get("cache_read")),
                "cache_write": None,
            },
            "batch": None,
            "per_image": None,
            "promo": None,
        },
        "notes": note,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite existing provider files")
    args = ap.parse_args()

    data = fetch_json(MODELSDEV_URL)
    now = now_iso()
    written, skipped = [], []

    for pid, pv in data.items():
        models = pv.get("models") or {}
        if not models:
            continue
        out = os.path.join(PROVIDERS, f"{pid}.json")
        if os.path.exists(out) and not args.force:
            skipped.append(pid)
            continue
        model_list = [build_model(mid, m) for mid, m in models.items()]
        model_list.sort(key=lambda x: x["id"])
        provider = {
            "provider_id": pid,
            "name": pv.get("name") or pid,
            "channel": infer_channel(pid, pv.get("name") or "", pv.get("api")),
            "category": "ai_vendor" if infer_channel(pid, pv.get("name") or "", pv.get("api")) == "first_party"
            else "aggregator" if infer_channel(pid, pv.get("name") or "", pv.get("api")) == "aggregator"
            else "inference_host",
            "region": "global",
            "homepage": pv.get("doc") or "",
            "pricing_page": pv.get("doc") or None,
            "api_base_url": pv.get("api") or None,
            "currency": "USD",
            "updated_at": now,
            "verified_at": now,
            "models": model_list,
        }
        if args.write:
            write_json(out, provider)
            written.append(pid)
        else:
            print(f"would write {pid}: {len(model_list)} models")

    if not args.write:
        print(f"models.dev: {len(written) + len(skipped)} providers scanned, dry-run (use --write)")
        return

    # update index
    index = load_index()
    existing_ids = {e["id"] for e in index["providers"]}
    for pid in written:
        if pid in existing_ids:
            continue
        p = json.load(open(os.path.join(PROVIDERS, f"{pid}.json"), encoding="utf-8"))
        index["providers"].append({
            "id": pid, "name": p["name"], "channel": p["channel"],
            "model_count": len(p["models"]), "file": f"providers/{pid}.json", "updated_at": now,
        })
    index["generated_at"] = now
    index["provider_count"] = len(index["providers"])
    index["model_count"] = sum(e["model_count"] for e in index["providers"]) + sum(
        e["model_count"] for e in index["resellers"])
    save_index(index)

    # manifest
    manifest = load_manifest()
    srcs = [s for s in manifest.get("sources", []) if s["name"] != "models.dev"]
    srcs.append({"name": "models.dev", "url": MODELSDEV_URL, "auto_sync": True, "last_ok": now, "last_error": None})
    manifest["sources"] = srcs
    save_manifest(manifest)

    append_changelog([{
        "date": now, "kind": "add", "scope": "provider", "provider_id": pid, "item_id": pid,
        "field": "catalog", "new": {"provider_count": len(written)}, "source": MODELSDEV_URL,
    } for pid in written])

    print(f"models.dev: wrote {len(written)} providers, skipped {len(skipped)} (existing).")


if __name__ == "__main__":
    main()
