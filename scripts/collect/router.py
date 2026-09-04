"""router.py — the collection ROUTE (routing center).

Unified entry point for the data-fetch layer. `collect()` calls every provider collector
(scripts/collect/collect_<provider>.py) in docs/providers.md Tier 0 -> Tier 4 order
(alphabetical within tier) and returns STRUCTURED results:

    {provider_id: {"provider_id": ..., "source": ..., "status": "ok|error|no_source",
                   "parsed": {model_id: <model-structure update block>}, "errors": [...]}}

The router NEVER writes to the DB. Persistence is owned by price_check.py (which calls this
router in order, then persists via utils.write_prices). This keeps the data-fetch layer
decoupled: collectors only fetch+parse+return structure.

Contract for a collector module (collect_<provider>.py):
    from collect.utils import fetch_markdown, ...   # shared tools
    def collect(ctx):                                # ctx: {"now", "dry_run"}
        ...fetch + parse official/aggregation source...
        return {"provider_id": <pid>, "source": <src>, "status": "ok",
                "parsed": {model_id: {"pricing": {...}, "notes": ...}}, "errors": []}
"""
import importlib
import os
import sys

_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..")))  # scripts/ so toolbox is importable

# modules in collect/ that are NOT provider collectors
_SKIP = {
    "__init__.py", "utils.py", "router.py", "price_check.py",
    "dispatcher.py", "coverage.py", "gen_collect.py",
}


def _collector_ids():
    """Return every provider id that has a collect_<pid>.py module in collectors/."""
    cdir = os.path.join(_THIS, "collectors")
    for f in sorted(os.listdir(cdir)):
        if not f.startswith("collect_") or not f.endswith(".py"):
            continue
        yield f[len("collect_"):-3]


def _tier_order(pid):
    """Tier for ordering (0..4), from provider_status. Falls back to 4 (long-tail)."""
    try:
        from provider_status import tier_of_provider
        return tier_of_provider(pid)
    except Exception:  # noqa: BLE001
        return 4


def collect(provider_filter=None, dry_run=False):
    """Call every collector in providers.md Tier 0 -> Tier 4 order.
    Returns {provider_id: structured_result}; never writes the DB."""
    ids = [pid for pid in _collector_ids()]
    ids.sort(key=lambda pid: (_tier_order(pid), pid))
    if provider_filter:
        ids = [p for p in ids if p in provider_filter]

    results = {}
    for pid in ids:
        mod_name = "collect_" + pid
        try:
            mod = importlib.import_module(f"collect.collectors.{mod_name}")
            res = mod.collect({"now": None, "dry_run": dry_run})
            # normalize: guarantee the structured shape
            res = res or {}
            results[pid] = {
                "provider_id": res.get("provider_id", pid),
                "source": res.get("source", ""),
                "status": res.get("status", "no_source"),
                "parsed": res.get("parsed") or {},
                "errors": res.get("errors") or [],
                "cross_provider": res.get("cross_provider", False),
            }
        except Exception as e:  # noqa: BLE001
            results[pid] = {
                "provider_id": pid, "source": "", "status": "error",
                "parsed": {}, "errors": [str(e)[:200]],
            }
    return results


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--providers", help="comma-separated provider ids")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    r = collect(set(a.providers.split(",")) if a.providers else None, a.dry_run)
    for pid, res in sorted(r.items()):
        print(f"[router] {pid}: {res['status']} parsed={len(res['parsed'])}")
        if res["errors"]:
            print(f"    error: {res['errors'][0]}")
