"""Generate the provider status table (tier, models, api_base_url, check script, status)
into docs/providers.md / docs/providers.zh-CN.md (between PROVIDERS:BEGIN/END markers).

Tiers (by R&D leadership, not geography):
  T0 = the world's leading model R&D vendors (headline labs)
  T1 = other major LLM R&D vendors
  T2 = all remaining model R&D vendors (any model type)
  T3 = core inference hosts / resellers / aggregator gateways
  T4 = all other service providers (subscription products, long-tail services)
Within each tier providers are sorted alphabetically, deduplicated.

Status: 🟢 automated (has a check script) / 🟡 manual (in DB, no check) / ⚪ pending (not in DB yet).
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Tier 0: the world's leading model R&D vendors (headline labs) ---
TIER0 = ["alibaba", "anthropic", "deepseek", "google", "meta", "minimax",
         "mistral", "moonshotai", "openai", "xai", "zai"]

# --- Tier 1: other major LLM R&D vendors (incl. pending-to-add) ---
TIER1 = ["ai21", "baidu", "baichuan", "cohere", "iflytek", "lingyiwanwu",
         "nvidia", "perplexity", "stepfun", "tencent", "upstage",
         "volcengine", "xiaomi", "zhipuai", "aws"]

# --- Tier 2: all remaining model R&D vendors (any model type, incl. pending-to-add) ---
TIER2 = ["arcee", "assemblyai", "cartesia", "deepgram", "elevenlabs",
         "inception", "lilac", "morph", "nova", "playai", "poolside",
         "sakana", "sarvam", "stability", "submodel", "thinkingmachines"]

# --- Tier 3: core inference hosts / resellers / aggregator gateways ---
TIER3 = [
    # inference hosts
    "baseten", "cerebras", "cloudflare-workers-ai", "crusoe", "databricks",
    "deepinfra", "digitalocean", "fireworks-ai", "friendli", "groq",
    "hetzner", "huggingface", "modal", "nebius", "novita-ai", "ollama-cloud",
    "ovhcloud", "runinfra", "runpod", "salad-cloud", "sap-ai-core",
    "scaleway", "siliconflow", "snowflake-cortex", "stackit", "togetherai",
    "vast", "vultr", "watsonx",
    # aggregators / gateways
    "302ai", "ai-router", "aihubmix", "anyapi", "cloudflare-ai-gateway",
    "edenai", "fastrouter", "helicone", "jiekou", "kilo", "llmgateway",
    "merge-gateway", "nano-gpt", "opencode", "opencode-go", "openrouter",
    "orcarouter", "poe", "requesty", "trustedrouter", "unorouter", "vercel",
    "zenmux",
]

# --- Tier 4: other service providers (subscription products, long-tail services) ---
TIER4_SUB = ["cursor", "devin", "github", "jetbrains",
             "replit", "tabnine", "v0", "windsurf"]

# --- Pending: well-known vendors not yet in the DB (⚪ pending status, shown inside their tier) ---
PENDING = {
    "ai21": ("AI21 Labs", "https://api.ai21.com/studio/v1", 1),
    "lingyiwanwu": ("01.AI (Lingyiwanwu)", "https://api.lingyiwanwu.com/v1", 1),
    "iflytek": ("iFlytek Spark", "https://spark-api-open.xf-yun.com/v1", 1),
    "baichuan": ("Baichuan AI", "https://api.baichuan-ai.com/v1", 1),
    "stability": ("Stability AI", "https://api.stability.ai/v1", 2),
    "elevenlabs": ("ElevenLabs", "https://api.elevenlabs.io/v1", 2),
    "deepgram": ("Deepgram", "https://api.deepgram.com/v1", 2),
    "assemblyai": ("AssemblyAI", "https://api.assemblyai.com/v2", 2),
    "cartesia": ("Cartesia", "https://api.cartesia.ai/v1", 2),
    "playai": ("PlayAI", "https://api.play.ai/v1", 2),
    "runpod": ("RunPod", "https://api.runpod.ai/v2", 3),
    "vast": ("Vast.ai", "https://console.vast.ai/api/v0", 3),
}

TIER_NAMES = {
    0: "Tier 0 — World's leading model R&D vendors",
    1: "Tier 1 — Other major LLM R&D vendors",
    2: "Tier 2 — Other model R&D vendors",
    3: "Tier 3 — Core inference hosts / resellers / aggregator gateways",
    4: "Tier 4 — Other service providers (long-tail)",
}
TIER_NAMES_ZH = {
    0: "Tier 0 — 全球最头部模型研发厂商",
    1: "Tier 1 — 其他大语言模型研发大厂",
    2: "Tier 2 — 其他模型研发厂商",
    3: "Tier 3 — 核心模型中转/托管/聚合网关",
    4: "Tier 4 — 其他服务提供商（长尾）",
}

MANUAL_TIER = {}
for _t, _lst in ((0, TIER0), (1, TIER1), (2, TIER2), (3, TIER3)):
    for pid in _lst:
        MANUAL_TIER[pid] = _t
for pid in TIER4_SUB:
    MANUAL_TIER[pid] = 4


def tier_of_provider(pid):
    return MANUAL_TIER.get(pid, 4)  # anything unclassified lands in T4 (other services)


def check_for(pid):
    for f in sorted(glob.glob("scripts/checks/*.py")):
        txt = open(f, encoding="utf-8", errors="ignore").read()
        if f'PROVIDER_ID = "{pid}"' in txt:
            return os.path.basename(f)
    return ""


def table_block(lang):
    names = TIER_NAMES if lang == "en" else TIER_NAMES_ZH
    lines = []

    # group DB providers by tier
    groups = {}
    providers = []
    for f in sorted(glob.glob("data/feed/providers/*.json")):
        p = json.load(open(f, encoding="utf-8"))
        providers.append(p)
    for p in providers:
        t = tier_of_provider(p["provider_id"])
        groups.setdefault(t, []).append(p)

    for t in sorted(groups):
        lines.append(f"### {names[t]}")
        lines.append("")
        lines.append("| Provider | Name | Models | API base URL | Check script | Status | Official 1st-party |")
        lines.append("|---|---|---|---|---|---|---|")
        for p in sorted(groups[t], key=lambda x: x["provider_id"]):
            api = p.get("api_base_url") or "—"
            if api and len(api) > 40:
                api = api[:37] + "…"
            ck = check_for(p["provider_id"])
            if ck:
                st = "🟢 automated"
                # daily-check.yml only syncs aggregation sources (OpenRouter/models.dev); the
                # official check (router.py / tierN_*) is NOT auto-run by daily-check, so a new
                # first-party model (e.g. gpt-6-astra) is only added manually / by the review agent.
                off = "⚠️ manual (daily-check does NOT auto-run official source)"
            else:
                st = "🟡 manual"
                off = "— (aggregation only)"
            lines.append(f"| `{p['provider_id']}` | {p.get('name') or '—'} | {len(p.get('models', []))} | `{api}` | `{ck or '—'}` | {st} | {off} |")
        # pending vendors that belong to this tier (not in DB yet)
        pend = [(pid, info) for pid, info in sorted(PENDING.items()) if info[2] == t]
        for pid, (name, api, _t) in pend:
            lines.append(f"| `{pid}` | {name} | — | `{api}` | `—` | ⚪ pending | — |")
        lines.append("")

    # legend
    lines.append("Legend: 🟢 automated (check script) · 🟡 manual (in DB, no check) · ⚪ pending (not added yet)")
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
