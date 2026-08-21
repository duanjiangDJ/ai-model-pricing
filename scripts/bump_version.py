"""Bump version (year.content.feature) across VERSION / schema / data files, and append a CHANGELOG entry.

Usage:
  python scripts/bump_version.py --content --message "chore: daily price sync"
  python scripts/bump_version.py --feature --message "feat: new script"
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

VERSION_FILE = "VERSION"
SCHEMA = "data/machine/schema.json"
DATA_FILES = ["data/machine/index.json", "data/machine/plans.json",
              "data/meta/manifest.json", "data/meta/changelog.json"]
CHANGELOG = "CHANGELOG.md"
CHANGELOG_ZH = "CHANGELOG.zh-CN.md"


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def bump():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content", action="store_true", help="content update (pricing data) -> second segment +1")
    ap.add_argument("--feature", action="store_true", help="feature update -> third segment +1")
    ap.add_argument("--message", required=True, help="short change description for CHANGELOG")
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    args = ap.parse_args()

    old = open(VERSION_FILE, encoding="utf-8").read().strip()
    y, c, f = (int(x) for x in old.split("."))
    if args.content:
        c += 1
        f = 0
    elif args.feature:
        f += 1
        c = 0
    else:
        sys.exit("specify --content or --feature")
    new = f"{y}.{c}.{f}"
    date = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # VERSION
    open(VERSION_FILE, "w", encoding="utf-8").write(new + "\n")
    # schema
    s = json.load(open(SCHEMA, encoding="utf-8"))
    s["version"] = new
    txt = json.dumps(s, ensure_ascii=False, indent=2)
    # sync const schema_version inside the schema definition
    txt = txt.replace(f'"const": "{old}"', f'"const": "{new}"')
    s = json.loads(txt)
    json.dump(s, open(SCHEMA, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(SCHEMA, "a", encoding="utf-8").write("\n")
    # data files schema_version
    for f in DATA_FILES:
        d = json.load(open(f, encoding="utf-8"))
        if d.get("schema_version"):
            d["schema_version"] = new
            json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            open(f, "a", encoding="utf-8").write("\n")
    # CHANGELOG entries
    kind = "content update" if args.content else "feature update"
    en_entry = f"## {new} — {date} ({kind})\n\n- {args.message}\n"
    zh_entry = f"## {new} — {date}（{'内容更新' if args.content else '功能更新'}）\n\n- {args.message}\n"
    for f, entry in ((CHANGELOG, en_entry), (CHANGELOG_ZH, zh_entry)):
        t = open(f, encoding="utf-8").read()
        m = re.search(r"^(---\n\n)## \d+\.\d+\.\d+", t, re.M)
        if m:
            t = t[:m.start(1)] + "---\n\n" + entry + "\n" + t[m.end(1):]
        else:
            # fallback: insert after header
            lines = t.split("\n")
            insert_at = 0
            for i, ln in enumerate(lines):
                if ln.startswith("# "):
                    insert_at = i + 1
                    break
            lines.insert(insert_at, "\n" + entry)
            t = "\n".join(lines)
        open(f, "w", encoding="utf-8").write(t)
    print(f"bumped {old} -> {new} ({kind})")


if __name__ == "__main__":
    bump()
