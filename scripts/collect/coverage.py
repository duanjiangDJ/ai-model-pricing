"""coverage.py — report collection status for every provider in docs/providers.md.

Shows which providers have an independent collector (collect_<pid>.py) vs which fall
back to aggregation (openrouter/models.dev), grouped by tier. This is the "structure
complete" view after the P1 refactor.
"""
import os
import re
from collections import Counter

c = os.path.dirname(os.path.abspath(__file__))
docs = os.path.abspath(os.path.join(c, "..", "..", "docs", "providers.md"))
txt = open(docs, encoding="utf-8").read()

tier = None
rows = []
for line in txt.splitlines():
    m = re.match(r"### Tier (\d+)", line)
    if m:
        tier = int(m.group(1))
        continue
    m = re.match(r"\|\s*`([a-z0-9_.-]+)`\s*\|\s*([^|]+)\|\s*(\d+)\s*\|", line)
    if m:
        pid, name = m.group(1), m.group(2).strip()
        collect = os.path.exists(os.path.join(c, f"collect_{pid}.py"))
        rows.append((tier, pid, name, collect))

print(f"providers.md total: {len(rows)}")
stats = Counter()
for t in range(5):
    sub = [r for r in rows if r[0] == t]
    if not sub:
        continue
    auto = sum(1 for r in sub if r[3])
    stats[t] = (len(sub), auto)
    print(f"  Tier{t}: {len(sub)} (独立collect {auto} / 聚合兜底 {len(sub)-auto})")

print("\n--- 有独立 collect 的供应商 ---")
for t, pid, name, has in sorted(rows):
    if has:
        print(f"  T{t} {pid}")
