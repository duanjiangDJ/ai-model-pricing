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
from collect.utils import write_prices  # noqa: E402


def run(provider_filter=None, dry_run=False):
    """Ordered fetch + persist. Returns {provider_id: {status, parsed, changed}}."""
    results = collect(provider_filter, dry_run)
    summary = {}
    for pid, res in sorted(results.items()):
        parsed = res.get("parsed") or {}
        if res.get("status") != "ok" or not parsed:
            summary[pid] = {"status": res.get("status"), "parsed": 0, "changed": 0}
            continue
        # persist (unless dry-run) — write_prices updates the provider in the DB & changelog
        changed = write_prices(pid, parsed, res.get("source", ""), None) if not dry_run else len(parsed)
        summary[pid] = {"status": "ok", "parsed": len(parsed), "changed": changed}
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--providers", help="comma-separated provider ids")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    s = run(set(a.providers.split(",")) if a.providers else None, a.dry_run)
    print(json.dumps(s, ensure_ascii=False, indent=0))
