"""scripts/collect/dispatcher.py — the collection ROUTE.

Architecture chosen by the user (2026-09-02):
    dispatcher (route)  ->  collect_<provider>.py  ->  common.py (shared utils)

Discovers scripts/collect/collect_<provider>.py and runs each provider's collect(ctx),
isolating failures per provider and printing a summary. Target list is docs/providers.md
(196 providers); providers with a collector get independent collection, the rest fall
back to the aggregation sources (openrouter / models.dev).

Usage:
    python scripts/collect/dispatcher.py [--providers openai,deepseek] [--dry-run]
"""
import argparse
import importlib
import os
import sys

_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..")))  # scripts/

from toolbox import now_iso  # noqa: E402


def discover():
    """Return [(provider_id, module)] for every collect_<provider>.py in this dir."""
    mods = []
    for f in sorted(os.listdir(_THIS)):
        if f.startswith("collect_") and f.endswith(".py") and f != "collect_common.py" and f != "collect_dispatcher.py":
            name = f[:-3]
            try:
                mod = importlib.import_module(f"collect.{name}")
                pid = getattr(mod, "PROVIDER_ID", name.replace("collect_", ""))
                mods.append((pid, mod))
            except Exception as e:  # noqa: BLE001
                print(f"WARN failed to load collector {name}: {e}")
    return mods


def run(provider_filter=None, dry_run=False):
    now = now_iso()
    for pid, mod in discover():
        if provider_filter and pid not in provider_filter:
            continue
        ctx = {"now": now, "dry_run": dry_run}
        try:
            res = mod.collect(ctx)
            print(f'[collect] {pid}: ok changed={res.get("changed", 0)} ({res.get("detail", "")})')
        except Exception as e:  # noqa: BLE001
            print(f"[collect] {pid}: ERROR {str(e)[:160]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--providers", help="comma-separated provider ids")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    run(set(a.providers.split(",")) if a.providers else None, a.dry_run)
