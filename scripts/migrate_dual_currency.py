"""Migrate per_mtok/batch/per_image/promo prices from scalar numbers to dual-currency
objects {usd, cny} (schema 26.x, dualPrice). Idempotent: already-wrapped values are
left untouched. The wrapping currency is derived from each provider's `currency` field
(USD -> usd, CNY -> cny), assuming existing scalar prices are expressed in that currency.

Usage:
  python scripts/migrate_dual_currency.py            # dry-run: report counts
  python scripts/migrate_dual_currency.py --write    # apply
"""
import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toolbox import PROVIDERS, now_iso  # noqa: E402

PRICE_KEYS = ("input", "output", "cache_read", "cache_write")


def currency_key(cur):
    c = (cur or "USD").lower()
    return "cny" if c in ("cny", "cn", "人民币") else "usd"


def wrap(v, key):
    if v is None or isinstance(v, dict):
        return v
    return {key: v}


def migrate_provider(d, key):
    changed = 0
    for m in d.get("models", []):
        p = m.get("pricing") or {}
        pm = p.get("per_mtok")
        if isinstance(pm, dict):
            for k in PRICE_KEYS:
                if k in pm:
                    nv = wrap(pm[k], key)
                    if nv != pm[k]:
                        pm[k] = nv
                        changed += 1
            re = pm.get("reasoning_effort")
            if isinstance(re, list):
                for item in re:
                    if isinstance(item, dict):
                        for k in ("input", "output"):
                            if k in item:
                                nv = wrap(item[k], key)
                                if nv != item[k]:
                                    item[k] = nv
                                    changed += 1
        batch = p.get("batch")
        if isinstance(batch, dict):
            for k in ("input", "output"):
                if k in batch:
                    nv = wrap(batch[k], key)
                    if nv != batch[k]:
                        batch[k] = nv
                        changed += 1
        pi = p.get("per_image")
        if isinstance(pi, list):
            for tier in pi:
                if isinstance(tier, dict) and "price" in tier:
                    nv = wrap(tier["price"], key)
                    if nv != tier["price"]:
                        tier["price"] = nv
                        changed += 1
        promo = p.get("promo")
        if isinstance(promo, dict) and isinstance(promo.get("list_price"), dict):
            for k in PRICE_KEYS:
                if k in promo["list_price"]:
                    nv = wrap(promo["list_price"][k], key)
                    if nv != promo["list_price"][k]:
                        promo["list_price"][k] = nv
                        changed += 1
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    total_files = 0
    total_changed = 0
    per_file = {}
    for f in sorted(glob.glob(os.path.join(PROVIDERS, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        key = currency_key(d.get("currency"))
        n = migrate_provider(d, key)
        if n:
            per_file[os.path.basename(f)] = n
            total_changed += n
            if args.write:
                d["updated_at"] = now_iso()
                json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
                open(f, "a", encoding="utf-8").write("\n")
        total_files += 1

    print(f"扫描 {total_files} 个 provider 文件，需迁移的价格字段：{total_changed}")
    if not args.write:
        print("\n最需迁移的 10 个文件：")
        for fn, n in sorted(per_file.items(), key=lambda x: -x[1])[:10]:
            print(f"  {fn}: {n}")
        print("\n(以 --write 应用)")


if __name__ == "__main__":
    main()
