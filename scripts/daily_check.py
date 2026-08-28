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
    load_index, load_manifest, now_iso, price_of, read_json, save_index, save_manifest,
    set_price, write_json,
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
                rpv = rp.get(k) or {}
                if not isinstance(rpv, dict):
                    rpv = {"usd": rpv} if rpv is not None else {}
                for currency, rv in rpv.items():
                    if rv is None:
                        continue
                    lv = price_of(lp, k, currency)
                    if lv != rv:
                        changed_fields[f"{k}.{currency}"] = (lv, rv)
            if changed_fields:
                for fk, (old_v, new_v) in changed_fields.items():
                    key, currency = fk.split(".", 1)
                    # update only this currency, preserving any others (e.g. cny added by official sync)
                    set_price(local_by_id[mid].setdefault("pricing", {}).setdefault("per_mtok", {}), key, currency, new_v)
                stats["changed_models"] += 1
                new_shape = {}
                for fk, (old_v, new_v) in changed_fields.items():
                    key, currency = fk.split(".", 1)
                    new_shape.setdefault(key, {})[currency] = new_v
                entries.append({"date": now, "kind": "update", "scope": "model", "provider_id": pid,
                                "item_id": mid, "field": "pricing", "old": changed_fields,
                                "new": new_shape, "source": MODELSDEV_URL})
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


def _fmt_prices(v, labels=None):
    """Human-readable price summary from a changelog old/new value.

    Handles dict shapes like {'input': 0.44, 'output': 1.32, 'cache_read': 0.014}
    or lists like {'input': [0.44, 0.14]} (tiered). Falls back to '' for anything
    that isn't a simple price dict. `labels` localizes the field names (default EN).
    """
    if not isinstance(v, dict):
        return ""
    labels = labels or (("input", "in"), ("output", "out"), ("cache_read", "cache"))
    parts = []
    for k, label in labels:
        val = v.get(k)
        if isinstance(val, dict):
            # dual-currency object {usd, cny}: pick a representative value (usd preferred)
            uv = val.get("usd") if val.get("usd") is not None else val.get("cny")
            if uv is None or not isinstance(uv, (int, float)):
                continue
            val = uv
        elif isinstance(val, list):
            val = val[0] if val else None
        if isinstance(val, (int, float)):
            parts.append(f"{label} ${val:g}")
    return " ".join(parts)


def _model_list(item_id, limit=None):
    ids = [x for x in dict.fromkeys(str(item_id or "?").split(",")) if x]
    # Print the FULL model list — no truncation (asked by user; content updates must
    # list every model even when there are many).
    shown = ", ".join(f"`{x}`" for x in ids)
    return shown, len(ids)


def print_sync_summary():
    """Print a machine-extractable, HUMAN-READABLE, bilingual summary of the changes
    made by THIS run (entries prepended to changelog.json since the run started).
    Emits two blocks: SYNC_SUMMARY_EN_BEGIN/END and SYNC_SUMMARY_ZH_BEGIN/END, used by
    daily-check.yml as the CHANGELOG message for CHANGELOG.md / CHANGELOG.zh-CN.md.
    """
    cl = load_changelog()
    entries = cl if isinstance(cl, list) else cl.get("entries", [])
    fresh = [e for e in entries if e.get("date", "")[:16] >= _RUN_STARTED_ISO]
    if not fresh:
        print("SYNC_SUMMARY_EN_BEGIN\nNo data changes this run.\nSYNC_SUMMARY_EN_END")
        print("SYNC_SUMMARY_ZH_BEGIN\n本次运行无数据变更。\nSYNC_SUMMARY_ZH_END")
        return

    groups = {}
    for e in fresh:
        key = (e.get("provider_id", "?"), e.get("kind", "?"))
        groups.setdefault(key, []).append(e)

    en = ["price sync ({} change{}):".format(len(fresh), "" if len(fresh) == 1 else "s")]
    zh = ["价格同步（{} 处变更）：".format(len(fresh))]
    labels = (("input", "in"), ("output", "out"), ("cache_read", "cache"))
    labels_zh = (("input", "入"), ("output", "出"), ("cache_read", "缓存"))
    for (pid, kind) in sorted(groups):
        items = groups[(pid, kind)]
        n = sum(_model_list(i.get("item_id", "?"))[1] for i in items)
        # merge model names across entries of the same provider+kind
        merged = []
        for i in items:
            merged += [x for x in dict.fromkeys(str(i.get("item_id", "?")).split(",")) if x]
        shown, _ = _model_list(",".join(merged))
        if kind == "add":
            en.append(f"- **{pid}** (+{n}): {shown}")
            zh.append(f"- **{pid}**（新增 {n}）：{shown}")
        elif kind == "remove":
            en.append(f"- **{pid}** (-{n}): {shown}")
            zh.append(f"- **{pid}**（下架 {n}）：{shown}")
        else:  # update — always show price detail, no count-based truncation
            detail = ""
            dparts = []
            for i in items:
                old, new = i.get("old"), i.get("new")
                fo, fn_ = _fmt_prices(old, labels), _fmt_prices(new, labels)
                if fo and fn_:
                    dparts.append(f"{fo} → {fn_}")
                elif fn_:
                    dparts.append(fn_)
            if dparts:
                detail = " — " + "; ".join(dict.fromkeys(dparts))
            en.append(f"- **{pid}** (updated {n}): {shown}{detail}")
            zh_detail = detail
            if detail:
                zh_detail = " — " + "; ".join(
                    _fmt_prices(i.get("new"), labels_zh) or ""
                    for i in items if _fmt_prices(i.get("new"), labels_zh)
                )
                if not zh_detail:
                    zh_detail = ""
            zh.append(f"- **{pid}**（更新 {n}）：{shown}{zh_detail}")

    en_lines, zh_lines = [], []
    for l in en:
        en_lines.append(l)  # full line, no truncation (user asked to lift the limit)
    for l in zh:
        zh_lines.append(l)
    print("SYNC_SUMMARY_EN_BEGIN")
    for l in en_lines:
        print(l)
    print("SYNC_SUMMARY_EN_END")
    print("SYNC_SUMMARY_ZH_BEGIN")
    for l in zh_lines:
        print(l)
    print("SYNC_SUMMARY_ZH_END")


if __name__ == "__main__":
    sys.exit(main())
