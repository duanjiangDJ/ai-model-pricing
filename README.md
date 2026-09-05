> **Language: English (en)** — This document is written in en only.
# AI Model Pricing — Full Model Pricing Database

[![Daily Price Check](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/daily-check.yml/badge.svg)](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/daily-check.yml)
[![PR Check](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/pr-check.yml/badge.svg)](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/pr-check.yml)
[![GitHub Stars](https://img.shields.io/github/stars/duanjiangDJ/ai-model-pricing?style=social&label=Stars)](https://github.com/duanjiangDJ/ai-model-pricing/stargazers)

An open database collecting pricing for **every obtainable AI model** across all billing models:
per-token API (input/output/cache/batch), per-image, per-audio-second, per-request, credit
systems, GPU-second pricing, consumer subscriptions, and coding-tool plans.

- **Human-readable**: `data/view/` (Markdown tables, per provider) — English in `data/view/en/`, 中文见 `data/view/zh-CN/`
- **Machine-readable**: `data/feed/` (versioned JSON + JSON Schema, for crawlers/programs)
- **Auto-update**: GitHub Actions every 3 hours (cron `0 */3 * * *`) checks upstream prices and auto-merges changes into `main`

> Read this in Chinese? See [README.zh-CN.md](README.zh-CN.md).

## ⚠️ Project Status — Please Read

**This repository is a work in progress and NOT guaranteed to be complete or accurate.**

- Pricing changes fast; some entries may be **outdated**, **wrong**, or **missing**.
- Some billing modes (per-request, credit systems, subscription-included usage) are hard to
  verify and may be mislabeled. When in doubt, entries carry `null`/notes and a `verified_at`.
- Coverage of the long tail (CN resellers, enterprise custom pricing) is intentionally partial.
- **We welcome every contribution**: open an **issue** to report errors or suggest new
  sources/strategies, and submit a **PR** to fix prices or improve the acquisition pipeline
  (see [CONTRIBUTING.md](CONTRIBUTING.md)). Human changes go through PR + automated checks
  (`pr-check.yml`): schema validation, generated-page consistency, version consistency,
  and a security review; bot price-syncs merge directly into `main`.

**How this project is built**: the repository is maintained with
[DeepSeek Harness](https://github.com/deepseek-ai/DeepSeek-Harness) using the
**deepseek-v4-flash-0731** model. Data acquisition combines official pricing pages
(`scripts/sync_official.py`), public catalogs (models.dev, OpenRouter), and human/agent
verification.

<!-- STATS:BEGIN -->

## Data Statistics (exact)

- **Providers**: 190
- **Models**: 7579
- **Subscription plans**: 67
- **Distinct API endpoints**: 183
- **Free models**: 478

### By channel

| Channel | Providers | Models |
|---|---|---|
| Inference host | 138 | 4531 |
| First-party | 20 | 427 |
| Subscription | 18 | 176 |
| Aggregator | 13 | 2325 |
| Cloud-hosted | 1 | 120 |

### By region

| Region | Providers |
|---|---|
| Global | 175 |
| US | 9 |
| China | 6 |

### Model status

| Status | Models |
|---|---|
| offline | 43 |
| online | 18 |
| (unmarked) | 7518 |

### Top providers by model count

| Provider | Models |
|---|---|
| NanoGPT (`nano-gpt`) | 693 |
| DevPass (LLM Gateway) (`llmgateway`) | 565 |
| OpenRouter (`openrouter`) | 431 |
| Kilo Gateway (`kilo`) | 383 |
| Vercel AI Gateway (`vercel`) | 375 |
| Eden AI (`edenai`) | 255 |
| Merge Gateway (`merge-gateway`) | 179 |
| Requesty (`requesty`) | 153 |
| Poe (`poe`) | 137 |
| OrcaRouter (`orcarouter`) | 124 |
| ZenMux (`zenmux`) | 120 |
| Amazon Web Services (`aws`) | 120 |
| Ofox (`ofox`) | 114 |
| Cortecs (`cortecs`) | 112 |
| Abacus (`abacus`) | 108 |

### By currency

| Currency | Providers |
|---|---|
| USD | 186 |
| CNY | 4 |

<!-- STATS:END -->

## Documentation

| Doc | Content |
|---|---|
| [README.zh-CN.md](README.zh-CN.md) | 中文版说明 |
| [AGENTS.md](AGENTS.md) | Guide for AI agents working in this repo |
| [FORMAT.md](FORMAT.md) | Machine-readable format spec |
| [CHANGELOG.md](CHANGELOG.md) | Version history (year.content.feature) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guide |
| [docs/providers.md](docs/providers.md) | Provider landscape & status (generated table) |
| [docs/price-types.md](docs/price-types.md) | Price types & units |
| [docs/verification.md](docs/verification.md) | Daily check & truthfulness model |

## Quick Start (machine reading)

```python
import json, urllib.request

index = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/duanjiangDJ/ai-model-pricing/main/data/feed/index.json"))
print(f"{index['model_count']} models, {index['plan_count']} plans, schema v{index['schema_version']}")

# fetch the first provider
entry = index["providers"][0]
provider = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/duanjiangDJ/ai-model-pricing/main/data/feed/" + entry["file"]))
```

Format spec: [FORMAT.md](FORMAT.md). Authoritative schema: `data/feed/schema.json`.
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

**Current scale**: 190 providers, 7,465 models, 67 subscription plans. Exact numbers in the [Data Statistics](#data-statistics-exact) section above.
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

- Fix a price: edit `data/feed/providers/<id>.json` or `plans.json`, update `verified_at`
  and include the source (pricing-page URL).
- Add a provider: create `data/feed/providers/<id>.json` following `schema.json`, run `validate.py`.
- Report errors via issues (include the pricing-page link).

## Disclaimer

Prices change frequently; this repo syncs diligently but makes no guarantee of real-time accuracy.
Always treat the vendors' official pricing pages as authoritative. Data is public list pricing
before tax; actual bills depend on the vendor's settlement.
