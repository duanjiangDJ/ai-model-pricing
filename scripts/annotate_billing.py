"""Annotate every model with a machine-readable `billing_model` (array).

Rules (order matters, first match wins for the primary billing method):
  1. per_mtok has any value > 0      -> pay_per_token (plus "free" if any price is 0:
                                        free tier + paid tier, e.g. Gemini)
  2. per_mtok all 0 (not null)       -> free
  3. per_image has values            -> pay_per_image
  4. notes mention subscription/coding plan -> subscription_included
  5. otherwise                       -> unknown (needs human review)

Usage:
  python scripts/annotate_billing.py            # dry-run: stats + pending list
  python scripts/annotate_billing.py --write    # write billing_model + changelog entries
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROVIDERS = os.path.join(ROOT, "data", "feed", "providers")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from toolbox import append_changelog, now_iso  # noqa: E402

SUB_HINTS = ("included in a subscription", "coding plan", "token plan", "subscription/coding")


def classify(m):
    p = m.get("pricing") or {}
    pm = p.get("per_mtok") or {}
    vals = [pm.get(k) for k in ("input", "output", "cache_read") if pm.get(k) is not None]
    note = (m.get("notes") or "").lower()
    if any((v or 0) > 0 for v in vals):
        billing = ["pay_per_token"]
        if any(v == 0 for v in vals):
            billing.append("free")
        return billing
    if vals and all(v == 0 for v in vals):
        return ["free"]
    if p.get("per_image"):
        return ["pay_per_image"]
    if any(h in note for h in SUB_HINTS):
        return ["subscription_included"]
    return ["unknown"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    # Pass 1: classify without provider context, collect per-provider stats
    stats = {}
    provider_pay = {}   # provider_id -> count of pay_per_token (incl. mixed)
    provider_total = {}
    pending = []
    for fn in sorted(os.listdir(PROVIDERS)):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(PROVIDERS, fn)
        d = json.load(open(path, encoding="utf-8"))
        pid = d["provider_id"]
        provider_total[pid] = len(d.get("models", []))
        for m in d.get("models", []):
            billing = classify(m)
            if billing[0] == "pay_per_token":
                provider_pay[pid] = provider_pay.get(pid, 0) + 1
            if "unknown" in billing:
                pending.append((pid, m["id"], (m.get("notes") or "")[:80]))

    # Pass 2: resolve "unknown" using provider context — resellers/aggregators whose
    # catalog is predominantly pay-per-token almost certainly resell those models per-token.
    # A model with no price info inside such a provider is most likely a missing-price
    # catalog entry, not a different billing method.
    def resolve(pid, billing):
        if "unknown" in billing:
            total = provider_total.get(pid, 0)
            if total >= 5 and provider_pay.get(pid, 0) / total > 0.5:
                return ["pay_per_token"]
        return billing

    changed = 0
    for fn in sorted(os.listdir(PROVIDERS)):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(PROVIDERS, fn)
        d = json.load(open(path, encoding="utf-8"))
        pid = d["provider_id"]
        for m in d.get("models", []):
            billing = resolve(pid, classify(m))
            key = ",".join(billing)
            stats[key] = stats.get(key, 0) + 1
            old = m.get("billing_model")
            if old != billing:
                changed += 1
                if args.write:
                    m["billing_model"] = billing
        if args.write:
            d["updated_at"] = now_iso()
            json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("=== billing_model 分布 ===")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    print(f"\n需标注/更新的模型数: {changed}")
    # remaining unknowns after provider-context resolution
    unknown_left = sum(1 for p, m, n in pending
                       if "unknown" in resolve(p, classify({"id": m, "notes": n}))[0] or
                       resolve(p, classify({"id": m, "notes": n}))[0] == "unknown")
    if unknown_left:
        print(f"剩余 unknown（provider 兜底未覆盖）: {unknown_left}")
    if args.write:
        if changed:
            append_changelog([{
                "date": now_iso(), "kind": "update", "scope": "model", "provider_id": "all",
                "item_id": f"{changed} models", "field": "billing_model",
                "new": "annotated billing_model across all providers", "source": "scripts/annotate_billing.py",
            }])
        print(f"\n已写入 {changed} 个模型的 billing_model")


if __name__ == "__main__":
    main()
