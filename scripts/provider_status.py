"""Generate the provider status table (tier, models, api_base_url, check script, status)
into docs/providers.md / docs/providers.zh-CN.md (between PROVIDERS:BEGIN/END markers).

Usage: python scripts/provider_status.py
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# tier assignment: from checks/ modules (TIER attr), default 6 (long tail)
tier_of = {}
for f in glob.glob("scripts/checks/tier*_*.py"):
    name = os.path.basename(f)[:-3]
    try:
        txt = open(f, encoding="utf-8").read()
        m = re.search(r"TIER\s*=\s*(\d+)", txt)
        pid_m = re.search(r'PROVIDER_ID\s*=\s*"([^"]+)"', txt)
        if m and pid_m:
            tier_of[pid_m.group(1)] = int(m.group(1))
    except Exception:  # noqa: BLE001
        pass

providers = []
for f in sorted(glob.glob("data/machine/providers/*.json")):
    p = json.load(open(f, encoding="utf-8"))
    providers.append(p)

TIER_NAMES = {
    0: "Tier 0 — Core model R&D vendors (global)",
    1: "Tier 1 — Core model R&D vendors (China)",
    2: "Tier 2 — Cloud platforms",
    3: "Tier 3 — Inference hosting",
    4: "Tier 4 — Aggregators & gateways",
    5: "Tier 5 — Subscription & coding products",
    6: "Tier 6 — Long tail",
}
TIER_NAMES_ZH = {
    0: "Tier 0 — 全球核心模型研发厂商",
    1: "Tier 1 — 中国核心模型研发厂商",
    2: "Tier 2 — 云平台托管",
    3: "Tier 3 — 推理托管平台",
    4: "Tier 4 — 聚合/网关",
    5: "Tier 5 — 订阅与编码产品",
    6: "Tier 6 — 长尾",
}

# manual tier overrides for known core providers without checks yet
MANUAL_TIER = {
    "openai": 0, "anthropic": 0, "google": 0, "xai": 0, "deepseek": 0, "meta": 0,
    "mistral": 0, "cohere": 0, "aws": 0, "nvidia": 0, "perplexity": 0,
    "alibaba": 1, "alibaba-cn": 1, "zhipuai": 1, "zai": 1, "moonshotai": 1,
    "volcengine": 1, "minimax": 1, "baidu": 1, "tencent": 1, "tencent-tokenhub": 1,
    "stepfun": 1, "xiaomi": 1,
    "azure": 2, "google-vertex": 2,
    "togetherai": 3, "groq": 3, "cerebras": 3, "deepinfra": 3, "siliconflow": 3,
    "fireworks-ai": 3, "novita-ai": 3, "nebius": 3, "baseten": 3, "modal": 3,
    "huggingface": 3, "cloudflare-workers-ai": 3, "scaleway": 3, "ovhcloud": 3,
    "vultr": 3, "digitalocean": 3, "databricks": 3, "snowflake-cortex": 3,
    "watsonx": 3, "sap-ai-core": 3,
    "openrouter": 4, "opencode": 4, "opencode-go": 4, "poe": 4, "vercel": 4,
    "llmgateway": 4, "kilo": 4, "orcarouter": 4, "cloudflare-ai-gateway": 4,
    "merge-gateway": 4, "fastrouter": 4, "unorouter": 4, "302ai": 4, "aihubmix": 4,
    "requesty": 4, "anyapi": 4, "nano-gpt": 4, "edenai": 4, "zenmux": 4,
    "github": 5, "cursor": 5, "windsurf": 5, "jetbrains": 5, "devin": 5,
    "replit": 5, "tabnine": 5, "v0": 5,
}


def tier_of_provider(pid):
    return tier_of.get(pid) or MANUAL_TIER.get(pid, 6)


def check_for(pid):
    """Return the check module filename if one exists."""
    for f in sorted(glob.glob("scripts/checks/*.py")):
        txt = open(f, encoding="utf-8", errors="ignore").read()
        if f'PROVIDER_ID = "{pid}"' in txt:
            return os.path.basename(f)
    return ""


def status_of(p):
    # a provider is 'verified' if it has a check script OR verified_at is recent
    if check_for(p["provider_id"]):
        return "🟢 automated"
    return "🟡 manual"


def table_block(lang):
    lines = []
    groups = {}
    for p in providers:
        t = tier_of_provider(p["provider_id"])
        groups.setdefault(t, []).append(p)
    names = TIER_NAMES if lang == "en" else TIER_NAMES_ZH
    for t in sorted(groups):
        lines.append(f"### {names[t]}")
        lines.append("")
        lines.append("| # | Provider | Models | API base URL | Check script | Status |")
        lines.append("|---|---|---|---|---|---|")
        for i, p in enumerate(sorted(groups[t], key=lambda x: -len(x.get("models", []))), 1):
            api = p.get("api_base_url") or "—"
            if api and len(api) > 42:
                api = api[:39] + "…"
            ck = check_for(p["provider_id"]) or "—"
            lines.append(f"| {i} | {p['provider_id']} | {len(p.get('models', []))} | `{api}` | `{ck}` | {status_of(p)} |")
        lines.append("")
    return "\n".join(lines)


for readme, lang in (("docs/providers.md", "en"), ("docs/providers.zh-CN.md", "zh-CN")):
    t = open(readme, encoding="utf-8").read()
    block = table_block(lang)
    begin = "<!-- PROVIDERS:BEGIN -->"
    end = "<!-- PROVIDERS:END -->"
    section = f"{begin}\n\n{block}\n\n{end}"
    if begin in t:
        t = re.sub(rf"{re.escape(begin)}.*?{re.escape(end)}", section, t, flags=re.S)
    else:
        t += "\n\n" + section
    open(readme, "w", encoding="utf-8").write(t)
    print(f"providers table updated ({lang})")
