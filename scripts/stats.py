"""Generate exact data statistics and update README (en + zh-CN) stats section.

Usage: python scripts/stats.py
The README section between <!-- STATS:BEGIN --> and <!-- STATS:END --> is replaced.
"""
import glob
import json
import os
import sys
from collections import Counter, defaultdict

from toolbox import has_zero_price, price_of  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

providers = []
for f in sorted(glob.glob("data/feed/providers/*.json")):
    providers.append(json.load(open(f, encoding="utf-8")))
plans = json.load(open("data/feed/plans.json", encoding="utf-8")).get("plans", [])

total_models = sum(len(p.get("models", [])) for p in providers)
chan_p = Counter(p.get("channel") for p in providers)
chan_m = defaultdict(int)
region_p = Counter(p.get("region") for p in providers)
status_m = Counter()
currency_p = Counter(p.get("currency", "USD") for p in providers)
by_provider = sorted(((len(p.get("models", [])), p["provider_id"], p.get("name", "")) for p in providers), reverse=True)
free_models = 0
sub_included = 0
no_status = 0
for p in providers:
    chan_m[p["channel"]] += len(p.get("models", []))
    for m in p.get("models", []):
        pm = (m.get("pricing") or {}).get("per_mtok") or {}
        st = m.get("status")
        if st:
            status_m[st] += 1
        else:
            no_status += 1
        if has_zero_price(pm):
            free_models += 1
        if (price_of(pm, "input") is None or price_of(pm, "output") is None) and "subscription" in str(m.get("notes", "")).lower():
            sub_included += 1

endpoints = {p.get("api_base_url") for p in providers if p.get("api_base_url")}

CHANNEL_LABEL = {"first_party": "First-party", "cloud": "Cloud-hosted", "hosted": "Inference host",
                 "aggregator": "Aggregator", "reseller": "Reseller", "subscription": "Subscription"}
CHANNEL_LABEL_ZH = {"first_party": "官方直供", "cloud": "云平台托管", "hosted": "推理托管",
                    "aggregator": "聚合站", "reseller": "中转站", "subscription": "订阅产品"}
REGION_LABEL = {"global": "Global", "cn": "China", "us": "US", "eu": "EU", "other": "Other"}
STATUS_LABEL = {"online": "online", "offline": "offline"}


def stats_block(lang):
    labels = CHANNEL_LABEL if lang == "en" else CHANNEL_LABEL_ZH
    t = []
    if lang == "en":
        t.append("## Data Statistics (exact)")
        t.append("")
        t.append(f"- **Providers**: {len(providers)}")
        t.append(f"- **Models**: {total_models}")
        t.append(f"- **Subscription plans**: {len(plans)}")
        t.append(f"- **Distinct API endpoints**: {len(endpoints)}")
        t.append(f"- **Free models**: {free_models}")
        t.append("")
        t.append("### By channel")
        t.append("")
        t.append("| Channel | Providers | Models |")
        t.append("|---|---|---|")
        for c in sorted(chan_p, key=lambda x: -chan_p[x]):
            t.append(f"| {labels.get(c, c)} | {chan_p[c]} | {chan_m.get(c, 0)} |")
        t.append("")
        t.append("### By region")
        t.append("")
        t.append("| Region | Providers |")
        t.append("|---|---|")
        for r in sorted(region_p, key=lambda x: -region_p[x]):
            t.append(f"| {REGION_LABEL.get(r, r)} | {region_p[r]} |")
        t.append("")
        t.append("### Model status")
        t.append("")
        t.append("| Status | Models |")
        t.append("|---|---|")
        for s in sorted(status_m, key=lambda x: -status_m[x]):
            t.append(f"| {STATUS_LABEL.get(s, s)} | {status_m[s]} |")
        t.append(f"| (unmarked) | {no_status} |")
        t.append("")
        t.append("### Top providers by model count")
        t.append("")
        t.append("| Provider | Models |")
        t.append("|---|---|")
        for n, pid, name in by_provider[:15]:
            t.append(f"| {name} (`{pid}`) | {n} |")
        t.append("")
        t.append("### By currency")
        t.append("")
        t.append("| Currency | Providers |")
        t.append("|---|---|")
        for c in sorted(currency_p, key=lambda x: -currency_p[x]):
            t.append(f"| {c} | {currency_p[c]} |")
    else:
        t.append("## 数据统计（精确值）")
        t.append("")
        t.append(f"- **供应商数**：{len(providers)}")
        t.append(f"- **模型数**：{total_models}")
        t.append(f"- **订阅计划数**：{len(plans)}")
        t.append(f"- **去重后的 API 端点数**：{len(endpoints)}")
        t.append(f"- **免费模型数**：{free_models}")
        t.append("")
        t.append("### 按渠道")
        t.append("")
        t.append("| 渠道 | 供应商 | 模型 |")
        t.append("|---|---|---|")
        for c in sorted(chan_p, key=lambda x: -chan_p[x]):
            t.append(f"| {labels.get(c, c)} | {chan_p[c]} | {chan_m.get(c, 0)} |")
        t.append("")
        t.append("### 按地区")
        t.append("")
        t.append("| 地区 | 供应商 |")
        t.append("|---|---|")
        for r in sorted(region_p, key=lambda x: -region_p[x]):
            t.append(f"| {REGION_LABEL.get(r, r)} | {region_p[r]} |")
        t.append("")
        t.append("### 模型状态分布")
        t.append("")
        t.append("| 状态 | 模型数 |")
        t.append("|---|---|")
        for s in sorted(status_m, key=lambda x: -status_m[x]):
            t.append(f"| {STATUS_LABEL.get(s, s)} | {status_m[s]} |")
        t.append(f"| （未标注） | {no_status} |")
        t.append("")
        t.append("### 模型数 Top 15 供应商")
        t.append("")
        t.append("| 供应商 | 模型数 |")
        t.append("|---|---|")
        for n, pid, name in by_provider[:15]:
            t.append(f"| {name}（`{pid}`） | {n} |")
        t.append("")
        t.append("### 按计价币种")
        t.append("")
        t.append("| 币种 | 供应商 |")
        t.append("|---|---|")
        for c in sorted(currency_p, key=lambda x: -currency_p[x]):
            t.append(f"| {c} | {currency_p[c]} |")
    return "\n".join(t)


STATS_BEGIN = "<!-- STATS:BEGIN -->"
STATS_END = "<!-- STATS:END -->"


def stats_section(lang):
    """Return the full STATS block (with BEGIN/END markers) for a language."""
    return f"{STATS_BEGIN}\n\n{stats_block(lang)}\n\n{STATS_END}"


def refresh_readme():
    """Regenerate the README (en + zh-CN) statistics section to match current data."""
    for readme, lang in (("README.md", "en"), ("README.zh-CN.md", "zh-CN")):
        t = open(readme, encoding="utf-8").read()
        section = stats_section(lang)
        if STATS_BEGIN in t:
            import re
            t = re.sub(rf"{re.escape(STATS_BEGIN)}.*?{re.escape(STATS_END)}", section, t, flags=re.S)
        else:
            # insert before 'Quick Start'/'快速开始' anchor
            anchor = "## Quick Start" if lang == "en" else "## 快速开始"
            t = t.replace(anchor, section + "\n\n" + anchor, 1)
        open(readme, "w", encoding="utf-8").write(t)
        print(f"README stats updated ({lang})")


if __name__ == "__main__":
    refresh_readme()
