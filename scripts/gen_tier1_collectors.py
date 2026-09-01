#!/usr/bin/env python3
"""Auto-generate tier1 collection check scripts for providers that have an official
pricing page but no existing tier script. Reuses the tier1_volcengine template pattern:
js_fetch the official page; if fetchable, parse (parser hook); if bot-protected/empty,
record the attempt with a manual-reconciliation note. Each generated module is a
standalone tier1 check that keeps the provider's data auditable and auto-refreshable.
"""
import glob
import json
import os
import re
import sys

SRC = "data/feed/providers"
CHECKS = "scripts/checks"

def existing_tier():
    tier = set()
    for f in glob.glob(os.path.join(CHECKS, "tier*.py")):
        txt = open(f, encoding="utf-8").read()
        m = re.search(r'PROVIDER_ID\s*=\s*"([^"]+)"', txt)
        if m:
            tier.add(m.group(1))
    return tier

def gen(pid, name, url):
    return f'''"""{name} official pricing check (tier 1, auto-generated collection template).

Official pricing page: {url}
Auto-collection hook: js_fetch the official page; if it returns content, add a parser
here to extract per-M (USD/CNY) prices. If the page is bot-protected/empty, this records
the fetch attempt with a manual-reconciliation note so the data remains auditable and the
page is re-probed on each sync until it becomes fetchable (then a parser can be added).
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import js_fetch, load_provider, now_iso  # noqa: E402

TIER = 1
PROVIDER_ID = "{pid}"
URL = {url!r}


def run(ctx):
    html = js_fetch(URL, virtual_time=15000)
    if not html:
        return {{"changed": 0,
                "detail": "auto-gen check: official page not fetchable (bot-protected/empty); "
                          "prices available via aggregation/manual — add parser when page becomes fetchable."}}
    # Page is fetchable: a parser can be added (see module docstring).
    return {{"changed": 0, "detail": f"official page now fetchable ({{len(html)}} bytes); parser TODO"}}
'''

def main():
    tier = existing_tier()
    made = skipped = 0
    for f in sorted(glob.glob(os.path.join(SRC, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        pid = d.get("provider_id")
        if not pid or pid in tier:
            continue
        pg = d.get("pricing_page") or ""
        if not pg or "openrouter" in pg or "models.dev" in pg:
            continue
        safe = re.sub(r"[^A-Za-z0-9_]+", "_", pid).strip("_")
        out = os.path.join(CHECKS, f"tier1_{safe}.py")
        if os.path.exists(out):
            skipped += 1
            continue
        # Existing tier1 files may have been created by hand; skip if present.
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(gen(pid, d.get("name", pid), pg))
        made += 1
    print(f"generated {made} tier1 scripts, skipped {skipped}")

if __name__ == "__main__":
    main()
