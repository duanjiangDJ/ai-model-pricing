"""price_check.py — scheduled entry (woken by workflow / Hermes cron).

Calls router.collect() in providers.md Tier 0 -> Tier 4 order, gets STRUCTURED results, and
persists them via utils.write_prices (which wraps toolbox.update_model_prices). This module
OWNS all DB writes in the data-fetch layer — collectors only fetch+parse+return structure.

Usage:
    python scripts/collect/price_check.py [--providers a,b] [--dry-run]
    python scripts/collect/price_check.py    # normal: fetch all + persist
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
from collect.router import collect  # noqa: E402
from collect.utils import write_prices, load_provider  # noqa: E402


def run(provider_filter=None, dry_run=False):
    """Ordered fetch + persist. Returns {provider_id: {status, parsed, changed}}."""
    results = collect(provider_filter, dry_run)
    summary = {}
    for pid, res in sorted(results.items()):
        parsed = res.get("parsed") or {}
        # cross-provider collectors (e.g. models.dev) return parsed = {sub_pid: {model_id: per_mtok}}
        if res.get("cross_provider"):
            sub_changed = 0
            for spid, models in parsed.items():
                ch = write_prices(spid, models, res.get("source", ""), None) if not dry_run else len(models)
                sub_changed += ch
            summary[pid] = {"status": "ok", "cross_provider": True,
                            "providers": len(parsed), "changed": sub_changed}
            continue
        if res.get("status") != "ok" or not parsed:
            summary[pid] = {"status": res.get("status"), "parsed": 0, "changed": 0}
            continue
        # Surface collector model ids that do not resolve in the provider DB. write_prices ->
        # update_model_prices SKIPS unknown ids silently, so a stale/renamed key (or an official
        # model not yet seeded) makes the check a no-op that still looks green. Report-only:
        # count + first few ids, so the daily log flags it without aborting the sync.
        prov = load_provider(pid)
        if prov:
            db_ids = {m.get("id") for m in prov.get("models", [])}
            missing = [mid for mid in parsed if mid not in db_ids]
            if missing:
                print(f"  WARN {pid}: {len(missing)} parsed model id(s) not in DB "
                      f"(update silently skips them): {missing[:5]}")
            res["missing_ids"] = missing
        # persist (unless dry-run) — write_prices updates the provider in the DB & changelog
        changed = write_prices(pid, parsed, res.get("source", ""), None) if not dry_run else len(parsed)
        summary[pid] = {"status": "ok", "parsed": len(parsed), "changed": changed,
                        "missing_ids": len(res.get("missing_ids") or [])}
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--providers", help="comma-separated provider ids")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    s = run(set(a.providers.split(",")) if a.providers else None, a.dry_run)
    print(json.dumps(s, ensure_ascii=False, indent=0))
