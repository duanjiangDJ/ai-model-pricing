"""router.py — core check router for the daily check.

Discovers provider check modules in scripts/checks/ and runs them in tier order.
Each check module must expose:
    TIER = int            # roadmap tier (0 = core vendors ... 6 = long tail)
    PROVIDER_ID = str     # e.g. 'openai'
    def run(ctx) -> dict  # returns {"changed": n, "status": "ok"|"error", "detail": str}

The router isolates failures per provider (one broken check never blocks others),
updates the manifest source list, and prints a summary.

Usage: python scripts/router.py [--providers openai,deepseek] [--dry-run]
"""
import argparse
import importlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toolbox import load_manifest, now_iso, save_manifest  # noqa: E402

CHECKS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checks")


def discover():
    modules = []
    if not os.path.isdir(CHECKS_DIR):
        return modules
    for f in sorted(os.listdir(CHECKS_DIR)):
        if f.endswith(".py") and not f.startswith("_"):
            name = f[:-3]
            try:
                mod = importlib.import_module(f"checks.{name}")
                tier = getattr(mod, "TIER", 9)
                pid = getattr(mod, "PROVIDER_ID", name)
                modules.append((tier, pid, mod))
            except Exception as e:  # noqa: BLE001
                print(f"WARN failed to load check {name}: {e}")
    modules.sort(key=lambda x: (x[0], x[1]))
    return modules


def run_router(provider_filter=None, dry_run=False):
    now = now_iso()
    manifest = load_manifest()
    results = []
    for tier, pid, mod in discover():
        if provider_filter and pid not in provider_filter:
            continue
        ctx = {"now": now, "dry_run": dry_run}
        try:
            res = mod.run(ctx)
            results.append({"provider": pid, "tier": tier, "status": "ok",
                            "changed": res.get("changed", 0), "detail": res.get("detail", "")})
            print(f"[tier{tier}] {pid}: ok (changed={res.get('changed', 0)})")
        except Exception as e:  # noqa: BLE001
            results.append({"provider": pid, "tier": tier, "status": "error",
                            "changed": 0, "detail": str(e)[:200]})
            print(f"[tier{tier}] {pid}: ERROR {str(e)[:160]}")

    # manifest: per-check source status
    srcs = [s for s in manifest.get("sources", []) if not s.get("check")]
    for r in results:
        srcs.append({"name": f"check:{r['provider']}", "url": f"scripts/checks/{r['provider']}.py",
                     "auto_sync": True, "official": True, "check": True,
                     "last_ok": now if r["status"] == "ok" else None,
                     "last_error": None if r["status"] == "ok" else r["detail"]})
    manifest["sources"] = srcs
    manifest["last_daily_check"] = now
    save_manifest(manifest)

    # checks may add brand-new models; keep index counts in sync so validate passes
    from toolbox import refresh_index_counts  # noqa: PLC0415
    refresh_index_counts(now)

    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"ROUTER SUMMARY: {ok}/{len(results)} checks ok")
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--providers", default=None, help="comma-separated provider ids to run")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    pf = set(args.providers.split(",")) if args.providers else None
    run_router(pf, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
