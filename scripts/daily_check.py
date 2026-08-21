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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    MACHINE, META, PROVIDERS, ROOT, append_changelog, fetch_json, load_changelog,
    load_index, load_manifest, now_iso, read_json, save_index, save_manifest, write_json,
)
from sync_openrouter import build_model  # noqa: E402

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


def sync_modelsdev_diff(now):
    """Diff models.dev catalog against local provider files. Only updates per_mtok
    input/output/cache_read values (never touches hand-maintained fields)."""
    from sync_modelsdev import build_model  # local import to avoid heavy init
    data = fetch_json(MODELSDEV_URL)
    stats = {"added_providers": 0, "changed_models": 0, "added_models": 0}
    entries = []
    for pid, pv in data.items():
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
    plans = read_json(os.path.join(MACHINE, "plans.json")).get("plans", [])
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
            added, removed, changed = diff_openrouter(local, [build_model(m) for m in remote["data"]], now)

            if added or removed or changed:
                local["models"] = [build_model(m) for m in remote["data"]]
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

        # Official pricing pages (direct fetch + wayback fallback) — the
        # "official-price-first" layer. Failures are recorded in manifest, not fatal.
        import subprocess
        r = subprocess.run(
            [sys.executable, os.path.join(ROOT, "scripts", "sync_official.py")],
            capture_output=True, text=True, timeout=600,
        )
        summary["official"] = r.returncode == 0
        print(r.stdout[-2000:] if r.stdout else "")
        if r.returncode != 0:
            print("WARN sync_official failed:", r.stderr[-500:] if r.stderr else "no stderr")
    else:
        print("no-network mode: skipping fetches")

    # stale plans report
    stale = check_stale_plans(args.stale_days)
    summary["stale_plans"] = len(stale)
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    if stale:
        lines = ["# 待人工核实的订阅计划（超过 {} 天未核实）".format(args.stale_days), "",
                 "| 产品 | 计划 | 上次核实 | 定价页 |", "|---|---|---|---|"]
        for p in stale:
            lines.append(f"| {p['product']} {p['plan']} | {p['plan']} | {p.get('verified_at', '从未')} | {p.get('url', '—')} |")
        with open(os.path.join(ROOT, "reports", "stale-plans.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    else:
        with open(os.path.join(ROOT, "reports", "stale-plans.md"), "w", encoding="utf-8") as f:
            f.write("所有订阅计划均在 {} 天内核实过。".format(args.stale_days))

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
