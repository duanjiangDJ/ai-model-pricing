> **Language: English (en)** — This document is written in en only.
# Machine-Readable Format Specification (FORMAT)

> Version: **1.0.0** (declared by the `version` field of `data/feed/schema.json` and the `schema_version` field of each file)
> This format is designed for crawlers / programs / toolchains: stable, versioned, validatable, and incrementally syncable.

## Directory Structure

```
data/feed/
├── schema.json          # JSON Schema（draft 2020-12），本格式的唯一权威定义
├── index.json           # 入口文件：先读它，再按需抓取
├── providers/           # 每个供应商一个文件
│   ├── openai.json
│   ├── openrouter.json  # 聚合站（转售价，channel=aggregator）
│   └── ...
├── plans.json           # 订阅/编码工具计划（月度/年度订阅、点数制）
└── (resellers.json)     # 中转站（可选，与 plans.json 同构：{schema_version, updated_at, items})

data/meta/
├── manifest.json        # 数据源健康状态、最近同步时间
└── changelog.json       # 全部变更历史（add/update/remove/verify）
```

## Reading Protocol (for Crawlers / Programs)

1. Fixed entry point: `https://raw.githubusercontent.com/duanjiangDJ/ai-model-pricing/main/data/feed/index.json`
2. `index.json` provides:
   - `schema_version` (incompatible changes bump the major version; consumers MUST check it)
   - `generated_at` (time of this full generation)
   - `providers[]` / `resellers[]`: each entry contains `id`, `model_count`, `file` (relative path), `updated_at`
   - `model_count` and `plan_count` overview
3. Fetch each provider JSON by concatenating the `file` field; when fully flattened data is needed, `models[]` already contains all fields — simply concat them.
4. Per-model price fields: see "Price Structure" below. All prices default to **USD / 1M tokens**; non-USD providers declare this at the top-level `currency` field (e.g. `"CNY"`).
5. Validation: `scripts/validate.py` (`pip install jsonschema`) can run schema + cross-consistency validation on all data.
6. Incremental sync: `data/meta/changelog.json` records every change in reverse chronological order (`kind: add|update|remove|verify`).

## Price Structure (model.pricing)

| Field | Type | Unit / Description |
|---|---|---|
| `per_mtok.input` / `.output` | number\|null | USD / 1M tokens |
| `per_mtok.cache_read` | number\|null | Cached-input price (usually 10%–25% of input) |
| `per_mtok.cache_write` | number\|null | Cache-write price (Anthropic: input × 1.25) |
| `per_mtok.reasoning_effort[]` | array | Tiered pricing by reasoning effort (e.g. OpenAI o-series) |
| `batch.input` / `.output` | number\|null | Batch API price (usually 50%) |
| `per_image[]` | array | Per-image generation: `[{name, price}]` tiers |
| `per_audio_second.input/.output` | object | TTS/STT per second/minute |
| `per_character.price` | object | Per character (with `unit: per_char\|per_1k_char`) |
| `per_request` | number\|null | Per request |
| `credits` | object | Points system: `topup{amount_usd, credits}`, `model_rate{per_mtok_input, ...}`, `convertible` |
| `gpu[]` | array | GPU billing: `[{sku, price, unit: per_second\|per_hour}]` |
| `neuron_second` | object | Cloudflare neuron seconds |
| `finetune` | object | Fine-tuning: `training_input/output/hosting` |
| `provisioned` | "contact_sales"\|null | Provisioned capacity (enterprise custom) |

**Rules**: `null` = billing method not offered or unknown; missing is **never** represented as `0`. Free models have price `0`.

## Subscription Plans (plans.json)

Each plan has: `id`, `provider_id`, `product`, `plan`, `category` (consumer/coding/team/enterprise/student/api_credits/free),
**`pricing_model`** (flat_monthly / flat_yearly / per_seat_monthly / per_seat_yearly / credits / free / custom — the subscription's independent pricing structure, strictly distinguished from model per-MTok pricing),
`billing` (monthly/yearly/one_time), `price_usd` (yearly plans record the total yearly price; per-seat plans record the per-seat price), `price_per_seat_usd`, `credits_included`, `included_models[]` (models included in the subscription with no standalone per-token pricing), `limits`, `includes[]`, `url`, `verified_at`.

**Models included in a subscription** (e.g. coding-plan / token-plan types) have `per_mtok` = `null` in the provider file plus a note stating "included in the subscription plan" — **never `0`** (`0` means a truly free API model only).

## Model Status (model.status)

`active` (on sale) / `preview` (preview/restricted) / `deprecated` (announced deprecation, still usable) / `retired` (no longer sold) / `superseded` (replaced, kept as a historical entry).
Outdated models must carry a `status`; human-readable pages mark them prominently with ❌/⚠️/🔁/🧪.

## Channel Semantics (channel)

`first_party` (official direct supply) / `cloud` (cloud-platform hosting) / `hosted` (inference-hosting platform) /
`aggregator` (aggregator resale price, e.g. OpenRouter) / `reseller` (relay/proxy station) / `subscription` (subscription product).

It is normal for the same model to have different prices across channels; each channel is recorded separately and never overwrites the others; `notes` records the price basis.

## Versioning Policy (year.content.feature)

Version number format: **`year.content.feature`** (e.g. `26.2.3`); the rules are in the repo-root `CHANGELOG.md`.

- **Content update** (second segment, +1): pricing data changes (price changes, model additions/retirements, plan changes) — the data files' `schema_version` updates in sync.
- **Feature update** (third segment, +1): non-pricing changes such as data structure / scripts / docs / mechanisms — `schema.json`'s `version` and every file's `schema_version` update in sync.
- Adding an optional field: a content update suffices; adding a required field / renaming a field / changing units: **feature update**, with the migration described in `CHANGELOG.md`.
- Consumers should check whether the `schema_version` prefix matches the version they support.

## Daily Update Mechanism

`.github/workflows/daily-check.yml` runs `scripts/daily_check.py` every day at 01:23 UTC:

1. Pull the OpenRouter catalog and diff against local data → update if changed and write a changelog entry;
2. Check `plans.json` for entries unverified for more than 30 days → generate `reports/stale-plans.md` and sync the GitHub issue「每日价格核实提醒」(Daily Price Verification Reminder);
3. Rebuild human-readable pages (`data/view/`);
4. Auto commit & push if there are changes (bot identity, `[skip ci]`).

Manual trigger: Repository Actions page → Daily Price Check → Run workflow.


---

## Related docs

- [README](README.md) — overview & exact stats
- [AGENTS.md](AGENTS.md) — guide for AI agents
- [FORMAT.md](FORMAT.md) — machine format spec
- [docs/providers.md](docs/providers.md) — provider landscape & status
- [docs/price-types.md](docs/price-types.md) — price types
- [docs/verification.md](docs/verification.md) — verification model
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute
