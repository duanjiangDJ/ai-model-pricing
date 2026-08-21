# AI Model Pricing — Full Model Pricing Database

[![Daily Price Check](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/daily-check.yml/badge.svg)](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/daily-check.yml)

An open database collecting pricing for **every obtainable AI model** across all billing models:
per-token API (input/output/cache/batch), per-image, per-audio-second, per-request, credit
systems, GPU-second pricing, consumer subscriptions, and coding-tool plans.

- **Human-readable**: `data/human/` (Markdown tables, per provider) — English by default, 中文见 `data/human/zh-CN/`
- **Machine-readable**: `data/machine/` (versioned JSON + JSON Schema, for crawlers/programs)
- **Daily auto-update**: GitHub Actions at 01:23 UTC checks upstream prices and commits changes

> Read this in Chinese? See [README.zh-CN.md](README.zh-CN.md).

## Quick Start (machine reading)

```python
import json, urllib.request

index = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/duanjiangDJ/ai-model-pricing/main/data/machine/index.json"))
print(f"{index['model_count']} models, {index['plan_count']} plans, schema v{index['schema_version']}")

# fetch the first provider
entry = index["providers"][0]
provider = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/duanjiangDJ/ai-model-pricing/main/data/machine/" + entry["file"]))
```

Format spec: [FORMAT.md](FORMAT.md). Authoritative schema: `data/machine/schema.json`.
Reading/updating rules for AI agents: [AGENTS.md](AGENTS.md).

## Coverage

| Channel | Description | Status |
|---|---|---|
| First-party vendors (global) | OpenAI (full GPT-5.6 family, 47 models), Anthropic (Fable/Opus/Sonnet/Haiku, 13 models), Google Gemini 3.x/2.5, xAI Grok 4.x, Mistral, Cohere etc. | ✅ in DB |
| First-party vendors (CN) | DeepSeek, Qwen/Alibaba, Doubao 2.1, GLM/Zhipu, Kimi, MiniMax, StepFun, Baidu ERNIE 5.x, Tencent Hunyuan Hy3 etc. | ✅ mostly in DB |
| Cloud platforms | AWS Bedrock, Azure, Vertex etc. (partial via models.dev) | partial |
| Inference hosts | OpenRouter (419 models, auto-synced), Together, Groq, Cerebras, SiliconFlow, DeepInfra, Novita, Nebius etc. | ✅ in DB |
| Aggregators / resellers | OpenRouter (auto), Poe, orcarouter, aihubmix etc.; long-tail CN resellers per documented policy | partial |
| Consumer subscriptions | ChatGPT Plus/Pro, Claude Pro/Max, Gemini AI, Perplexity, SuperGrok, Poe etc. | ✅ in DB |
| Coding plans | Copilot, Cursor, Windsurf, Claude Code, JetBrains AI, Devin, Amazon Q, Replit, Tabnine etc. | ✅ in DB |

**Current scale**: 204 providers, 7,700+ models (incl. 419 OpenRouter reseller prices), 51 plans.
Data is auto-synced daily (OpenRouter + models.dev); human-verified entries carry `verified_at` + source URLs.

> Honest scope statement: **no single source covers all pricing** (verified: OpenRouter / models.dev /
> LiteLLM only cover API token pricing). This repo combines "official pricing pages + public-API
> auto-sync + human verification" to get as close to the full set as feasible. Long-tail CN
> resellers number in the thousands and change constantly; we track representative samples with
> public pricing pages and do not promise exhaustive coverage.

## Provider Landscape & Price Types

- [Provider landscape (7 categories)](docs/providers.md)
- [Price types & units (17 types)](docs/price-types.md)

## Repository Layout

```
data/
├── machine/            # machine-readable JSON (schema-validated)
│   ├── schema.json     # JSON Schema 1.0.0 (authoritative)
│   ├── index.json      # entry index
│   ├── providers/      # one file per provider
│   └── plans.json      # subscription/coding plans
├── human/              # human-readable Markdown (generated; en + zh-CN/)
└── meta/               # manifest + changelog
scripts/                # sync/validate/build/merge (stdlib + jsonschema)
.github/workflows/      # daily-check.yml (daily auto check)
docs/                   # landscape, price types, research contract
reports/                # daily check artifacts (e.g. stale-plans.md)
AGENTS.md               # guide for AI agents working in this repo
```

## Daily Update Mechanism

1. `scripts/sync_openrouter.py` — pull OpenRouter catalog (reseller prices, 419+ models);
2. `scripts/daily_check.py` — daily diff (OpenRouter + models.dev), update + changelog,
   flag plans unverified for >30 days, rebuild human pages;
3. `scripts/validate.py` — schema + cross-consistency validation (also in CI);
4. Stale plans auto-sync to a GitHub issue ("每日价格核实提醒").

Manual trigger: repo Actions → **Daily Price Check** → Run workflow.

## Development

```bash
pip install jsonschema
python scripts/sync_openrouter.py --write   # sync OpenRouter
python scripts/sync_modelsdev.py --write    # sync models.dev providers
python scripts/merge_research.py x.json     # merge subagent research output
python scripts/build_human.py               # rebuild human pages (en + zh-CN)
python scripts/daily_check.py               # full daily check (network)
python scripts/validate.py                  # full validation
```

## Contributing

- Fix a price: edit `data/machine/providers/<id>.json` or `plans.json`, update `verified_at`
  and include the source (pricing-page URL).
- Add a provider: create `data/machine/providers/<id>.json` following `schema.json`, run `validate.py`.
- Report errors via issues (include the pricing-page link).

## Disclaimer

Prices change frequently; this repo syncs diligently but makes no guarantee of real-time accuracy.
Always treat the vendors' official pricing pages as authoritative. Data is public list pricing
before tax; actual bills depend on the vendor's settlement.
