"""Merge research-subagent JSON output into the database.

Research JSON shape (see prompt contract in docs/research-contract.md):
  {"providers": [<providerFile-ish>, ...], "plans": [<plan>, ...], "sources": [...]}

Rules:
  - Provider merge: research models OVERRIDE same-id models (pricing + metadata),
    models.dev-only models are kept; provider header fields are refreshed.
  - Plans: upsert by id into plans.json; category/billing normalized to schema enums;
    verified_at filled from provider verified_at when missing.
  - index.json provider entries updated (counts + updated_at).

Usage: python scripts/merge_research.py <research.json> [--provider-only]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    FEED, PROVIDERS, SCHEMA_VERSION, append_changelog, load_index, now_iso, read_json,
    save_index, write_json,
)

PLAN_CATEGORY_MAP = {
    "developer": "coding",
    "business": "enterprise",
    "consumer": "consumer",
    "coding": "coding",
    "team": "team",
    "enterprise": "enterprise",
    "student": "student",
    "api_credits": "api_credits",
    "free": "free",
}
BILLING_MAP = {"monthly": "monthly", "yearly": "yearly", "one_time": "one_time"}


def normalize_plan(p, fallback_verified):
    out = dict(p)
    out["category"] = PLAN_CATEGORY_MAP.get(str(p.get("category")).lower(), "consumer")
    if p.get("billing") is not None:
        out["billing"] = BILLING_MAP.get(str(p.get("billing")).lower(), "monthly")
    if not out.get("verified_at"):
        out["verified_at"] = fallback_verified
    out.setdefault("provider_id", p.get("provider_id") or "")
    return out


def merge_provider(research_p):
    pid = research_p["provider_id"]
    path = os.path.join(PROVIDERS, f"{pid}.json")
    existing = read_json(path) if os.path.exists(path) else None

    if existing is None:
        merged = {
            "provider_id": pid,
            "name": research_p.get("name", pid),
            "channel": research_p.get("channel", "first_party"),
            "category": research_p.get("category", "ai_vendor"),
            "region": research_p.get("region", "global"),
            "homepage": research_p.get("homepage", ""),
            "pricing_page": research_p.get("pricing_page"),
            "currency": research_p.get("currency", "USD"),
            "updated_at": now_iso(),
            "verified_at": research_p.get("verified_at") or now_iso(),
            "models": research_p.get("models", []),
        }
        write_json(path, merged)
        return pid, len(merged["models"]), len(merged["models"]), 0

    # merge into existing
    existing_models = {m["id"]: m for m in existing["models"]}
    research_models = {m["id"]: m for m in research_p.get("models", [])}
    overridden = 0
    for mid, rm in research_models.items():
        if mid in existing_models:
            em = existing_models[mid]
            # refresh pricing + key metadata, keep existing extra fields
            em["pricing"] = rm["pricing"]
            em["name"] = rm.get("name", em.get("name"))
            em["category"] = rm.get("category", em.get("category"))
            em["context_window"] = rm.get("context_window", em.get("context_window"))
            em["max_output"] = rm.get("max_output", em.get("max_output"))
            if rm.get("notes"):
                em["notes"] = rm["notes"]
            overridden += 1
        else:
            existing["models"].append(rm)
    existing["models"].sort(key=lambda m: m["id"])
    existing["channel"] = research_p.get("channel", existing.get("channel"))
    existing["category"] = research_p.get("category", existing.get("category"))
    existing["pricing_page"] = research_p.get("pricing_page", existing.get("pricing_page"))
    existing["updated_at"] = now_iso()
    existing["verified_at"] = research_p.get("verified_at") or existing.get("verified_at")
    write_json(path, existing)
    return pid, len(existing["models"]), len(research_models), overridden


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("research_json", help="path to research output JSON")
    args = ap.parse_args()

    data = read_json(args.research_json)
    now = now_iso()
    changed = False
    entries = []

    for rp in data.get("providers", []):
        pid, total, added_or_overridden, overridden = merge_provider(rp)
        entries.append({"date": now, "kind": "update", "scope": "provider", "provider_id": pid,
                        "item_id": pid, "field": "catalog",
                        "new": {"models": total, "research_models": added_or_overridden},
                        "source": "research-subagent"})
        changed = True

    # plans upsert
    plans_path = os.path.join(FEED, "plans.json")
    plans_data = read_json(plans_path)
    existing_plans = {p["id"]: p for p in plans_data["plans"]}
    fallback = data.get("providers", [{}])[0].get("verified_at") or now
    for rp in data.get("providers", []):
        for p in rp.get("plans", []):
            p["provider_id"] = rp["provider_id"]
            p = normalize_plan(p, rp.get("verified_at") or now)
            if p["id"] in existing_plans:
                existing_plans[p["id"]].update(p)
            else:
                existing_plans[p["id"]] = p
            entries.append({"date": now, "kind": "update", "scope": "plan", "provider_id": p["provider_id"],
                            "item_id": p["id"], "field": "price", "new": p.get("price_usd"),
                            "source": "research-subagent"})
    plans_data["plans"] = sorted(existing_plans.values(), key=lambda p: p["id"])
    plans_data["updated_at"] = now
    write_json(plans_path, plans_data)
    changed = True

    # index refresh
    index = load_index()
    known = {e["id"]: e for e in index["providers"] + index["resellers"]}
    for rp in data.get("providers", []):
        pid = rp["provider_id"]
        path = os.path.join(PROVIDERS, f"{pid}.json")
        count = len(read_json(path).get("models", []))
        if pid in known:
            known[pid]["model_count"] = count
            known[pid]["updated_at"] = now
        else:
            index["providers"].append({
                "id": pid, "name": rp.get("name", pid), "channel": rp.get("channel", "first_party"),
                "model_count": count, "file": f"providers/{pid}.json", "updated_at": now,
            })
    index["generated_at"] = now
    index["provider_count"] = len(index["providers"])
    index["model_count"] = sum(e["model_count"] for e in index["providers"]) + sum(
        e["model_count"] for e in index["resellers"])
    index["plan_count"] = len(plans_data["plans"])
    save_index(index)

    if entries:
        append_changelog(entries)

    print(f"merged {args.research_json}: {len(data.get('providers', []))} providers, "
          f"{len(plans_data['plans'])} plans total")


if __name__ == "__main__":
    main()
