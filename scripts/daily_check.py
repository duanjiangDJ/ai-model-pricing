"""Daily check & update mechanism.

Steps (run by GitHub Actions cron, also runnable locally):
  1. Pull OpenRouter catalog, diff against committed providers/openrouter.json,
     update changed entries + record changelog.
  2. Check plans.json for entries whose verified_at is older than --stale-days
     (default 30); write reports/stale-plans.md listing them.
  3. Rebuild human-readable pages (scripts/build_human.py).
  4. Update manifest.json timestamps.
  5. Print SUMMARY line; exit 0. The workflow decides whether to commit.

Usage: python scripts/daily_check.py [--stale-days 30] [--no-network]
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    FEED, META, PROVIDERS, ROOT, append_changelog, fetch_json, load_changelog,
    load_index, load_manifest, now_iso, read_json, save_index, save_manifest, write_json,
)
from sync_openrouter import build_model  # noqa: E402

# Run-start marker (UTC, minute precision) used to detect entries created by THIS run.
_RUN_STARTED_ISO = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")

OPENROUTER_URL = "https://openrouter.ai/api/v1/models"


def diff_openrouter(local, remote, now):
    """Compare local provider file with fresh fetch. Returns (changed_models, added, removed)."""
    local_models = {m["id"]: m for m in local["models"]}
    remote_models = {m["id"]: m for m in remote}
    added, removed, changed = [], [], []

    for mid in sorted(set(remote_models) - set(local_models)):
        added.append(mid)
    for mid in sorted(set(local_models) - set(remote_models)):
        removed.append(mid)

    for mid in sorted(set(local_models) & set(remote_models)):
        lp, rp = local_models[mid].get("pricing"), remote_models[mid].get("pricing")
        if lp != rp:
            changed.append((mid, lp, rp))
    return added, removed, changed


MODELSDEV_URL = "https://models.dev/api.json"

# subscription-included providers: models.dev lists their models at 0, but these are
# "included in a plan" (per_mtok must stay null, never 0)
SUB_PROVIDER_HINTS = ("coding-plan", "token-plan", "copilot", "kimi-for-coding")


def sync_modelsdev_diff(now):
    """Diff models.dev catalog against local provider files. Only updates per_mtok
    input/output/cache_read values (never touches hand-maintained fields)."""
    from sync_modelsdev import build_model  # local import to avoid heavy init
    data = fetch_json(MODELSDEV_URL)
    stats = {"added_providers": 0, "changed_models": 0, "added_models": 0}
    entries = []
    for pid, pv in data.items():
        if any(h in pid for h in SUB_PROVIDER_HINTS):
            continue  # subscription-included providers keep per_mtok = null
        models = pv.get("models") or {}
        if not models:
            continue
        path = os.path.join(PROVIDERS, f"{pid}.json")
        if not os.path.exists(path):
            continue  # do not auto-create here; run scripts/sync_modelsdev.py --write for that
        local = read_json(path)
        # If the official-price layer verified this provider today, models.dev
        # (third-party republication) must not overwrite it.
        if str(local.get("verified_at", ""))[:10] == now[:10]:
            continue
        local_by_id = {m["id"]: m for m in local["models"]}
        remote_by_id = {m["id"]: build_model(mid, m) for mid, m in models.items()}
        for mid in sorted(set(remote_by_id) - set(local_by_id)):
            local["models"].append(remote_by_id[mid])
            stats["added_models"] += 1
            entries.append({"date": now, "kind": "add", "scope": "model", "provider_id": pid,
                            "item_id": mid, "field": "catalog", "new": mid, "source": MODELSDEV_URL})
        for mid in sorted(set(remote_by_id) & set(local_by_id)):
            lp = local_by_id[mid].get("pricing", {}).get("per_mtok") or {}
            rp = remote_by_id[mid].get("pricing", {}).get("per_mtok") or {}
            changed_fields = {}
            for k in ("input", "output", "cache_read"):
                if rp.get(k) is not None and lp.get(k) != rp.get(k):
                    changed_fields[k] = (lp.get(k), rp.get(k))
            if changed_fields:
                for k, (old_v, new_v) in changed_fields.items():
                    local_by_id[mid]["pricing"]["per_mtok"][k] = new_v
                stats["changed_models"] += 1
                entries.append({"date": now, "kind": "update", "scope": "model", "provider_id": pid,
                                "item_id": mid, "field": "pricing", "old": changed_fields,
                                "new": {k: v[1] for k, v in changed_fields.items()}, "source": MODELSDEV_URL})
        if stats["added_models"] or stats["changed_models"]:
            local["updated_at"] = now
            local["verified_at"] = now
            local["models"].sort(key=lambda m: m["id"])
            write_json(path, local)
    if entries:
        append_changelog(entries)
    return stats


def refresh_index_counts(now):
    """Recompute index provider/reseller model counts from actual files."""
    index = load_index()
    changed = False
    for lst in (index["providers"], index["resellers"]):
        for entry in lst:
            path = os.path.join(PROVIDERS, entry["file"].replace("providers/", ""))
            if os.path.exists(path):
                actual = len(read_json(path).get("models", []))
                if actual != entry["model_count"]:
                    entry["model_count"] = actual
                    entry["updated_at"] = now
                    changed = True
    if changed:
        index["generated_at"] = now
        index["model_count"] = sum(e["model_count"] for e in index["providers"]) + sum(
            e["model_count"] for e in index["resellers"])
        save_index(index)
    return changed


def check_stale_plans(stale_days):
    plans = read_json(os.path.join(FEED, "plans.json")).get("plans", [])
    stale = []
    for p in plans:
        v = p.get("verified_at")
        if not v:
            stale.append(p)
            continue
        try:
            from datetime import datetime, timezone
            dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
            age = (datetime.now(timezone.utc) - dt).days
            if age > stale_days:
                stale.append(p)
        except ValueError:
            stale.append(p)
    return stale


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stale-days", type=int, default=30)
    ap.add_argument("--no-network", action="store_true", help="skip network fetches (stale check only)")
    ap.add_argument("--stale-report", default=None, help="write stale-plans markdown to this path (e.g. /tmp/stale-plans.md)")
    args = ap.parse_args()

    now = now_iso()
    summary = {"openrouter": {"added": 0, "removed": 0, "changed": 0},
               "modelsdev": {"added_models": 0, "changed_models": 0},
               "stale_plans": 0, "network_ok": True}

    if not args.no_network:
        try:
            remote = fetch_json(OPENROUTER_URL)
            local_path = os.path.join(PROVIDERS, "openrouter.json")
            local = read_json(local_path)
            remote_models = [build_model(m) for m in remote["data"]]
            # Guard: a healthy OpenRouter catalog is large. If the remote catalog
            # shrank below half the local size, treat it as an upstream anomaly and
            # do NOT rewrite the local file (prevents mass deletion on API glitches).
            if len(local["models"]) > 100 and len(remote_models) < len(local["models"]) / 2:
                raise RuntimeError(
                    f"openrouter catalog anomaly: remote {len(remote_models)} models vs local "
                    f"{len(local['models'])}; refusing to overwrite"
                )
            added, removed, changed = diff_openrouter(local, remote_models, now)

            if added or removed or changed:
                local["models"] = remote_models
                local["models"].sort(key=lambda m: m["id"])
                local["updated_at"] = now
                local["verified_at"] = now
                write_json(local_path, local)

                entries = []
                for mid in added:
                    entries.append({"date": now, "kind": "add", "scope": "model", "provider_id": "openrouter",
                                    "item_id": mid, "field": "catalog", "new": mid, "source": OPENROUTER_URL})
                for mid in removed:
                    entries.append({"date": now, "kind": "remove", "scope": "model", "provider_id": "openrouter",
                                    "item_id": mid, "field": "catalog", "old": mid, "source": OPENROUTER_URL})
                for mid, old_p, new_p in changed:
                    entries.append({"date": now, "kind": "update", "scope": "model", "provider_id": "openrouter",
                                    "item_id": mid, "field": "pricing", "old": old_p, "new": new_p,
                                    "source": OPENROUTER_URL})
                append_changelog(entries)

                # refresh index counts
                index = load_index()
                for entry in index["resellers"]:
                    if entry["id"] == "openrouter":
                        entry["model_count"] = len(local["models"])
                        entry["updated_at"] = now
                index["generated_at"] = now
                index["model_count"] = sum(e["model_count"] for e in index["providers"]) + sum(
                    e["model_count"] for e in index["resellers"])
                save_index(index)

            summary["openrouter"] = {"added": len(added), "removed": len(removed), "changed": len(changed)}
        except Exception as e:  # noqa: BLE001
            summary["network_ok"] = False
            print(f"WARN openrouter fetch failed: {e}")

        try:
            summary["modelsdev"] = sync_modelsdev_diff(now)
        except Exception as e:  # noqa: BLE001
            summary["network_ok"] = False
            print(f"WARN models.dev fetch failed: {e}")
        refresh_index_counts(now)

        # Official pricing pages via the core check router (checks/ per provider).
        # Failures are isolated per provider and recorded in manifest, not fatal.
        try:
            from router import run_router
            results = run_router()
            summary["official"] = {"ok": sum(1 for r in results if r["status"] == "ok"),
                                   "total": len(results)}
        except Exception as e:  # noqa: BLE001
            summary["official"] = False
            print(f"WARN router failed: {e}")
    else:
        print("no-network mode: skipping fetches")

    # stale plans report — written to --stale-report path if given (no reports/ dir anymore)
    stale = check_stale_plans(args.stale_days)
    summary["stale_plans"] = len(stale)
    stale_md = ""
    if stale:
        lines = ["# 待人工核实的订阅计划（超过 {} 天未核实）".format(args.stale_days), "",
                 "| 产品 | 计划 | 上次核实 | 定价页 |", "|---|---|---|---|"]
        for p in stale:
            lines.append(f"| {p['product']} {p['plan']} | {p['plan']} | {p.get('verified_at', '从未')} | {p.get('url', '—')} |")
        stale_md = "\n".join(lines) + "\n"
    else:
        stale_md = "所有订阅计划均在 {} 天内核实过。".format(args.stale_days)
    if args.stale_report:
        with open(args.stale_report, "w", encoding="utf-8") as f:
            f.write(stale_md)
    print("STALE_PLANS " + stale_md.replace("\n", " | ")[:300])

    # rebuild human pages
    import subprocess
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "build_human.py")],
        check=False, capture_output=True,
    )

    # manifest
    manifest = load_manifest()
    manifest["last_daily_check"] = now
    for s in manifest.get("sources", []):
        if s["name"] == "OpenRouter API":
            if summary["network_ok"]:
                s["last_ok"] = now
                s["last_error"] = None
            else:
                s["last_error"] = "fetch failed at " + now
    save_manifest(manifest)

    print("SUMMARY " + json.dumps(summary, ensure_ascii=False))
    print_sync_summary()
    return 0


def print_sync_summary():
    """Print a machine-extractable, human-readable summary of changes made by THIS
    run (entries prepended to changelog.json since the run started), so the CI
    workflow can use it as the CHANGELOG message instead of a bare 'chore: price sync'."""
    cl = load_changelog()
    entries = cl if isinstance(cl, list) else cl.get("entries", [])
    fresh = [e for e in entries if e.get("date", "")[:16] >= _RUN_STARTED_ISO]
    if not fresh:
        print("SYNC_SUMMARY_BEGIN")
        print("No data changes this run.")
        print("SYNC_SUMMARY_END")
        return
    lines = ["price sync ({} change{}):".format(len(fresh), "" if len(fresh) == 1 else "s")]
    by_scope = {}
    for e in fresh:
        key = f"{e.get('provider_id', '?')} {e.get('kind', '?')}"
        by_scope.setdefault(key, []).append(e)
    for key in sorted(by_scope):
        items = by_scope[key]
        detail = "; ".join(
            "{}: {}->{}".format(i.get("item_id", "?"), i.get("old", "?"), i.get("new", "?"))[:90]
            for i in items[:5]
        )
        lines.append(f"- {key} x{len(items)}: {detail}")
    if len(fresh) > 30:
        lines.append(f"- ... and {len(fresh) - 30} more")
    print("SYNC_SUMMARY_BEGIN")
    for l in lines:
        print(l)
    print("SYNC_SUMMARY_END")


if __name__ == "__main__":
    sys.exit(main())
