> **Language: English (en)** — This document is written in en only.

# Changelog

## Versioning Rules

Version number format: **`year.content.feature`** (e.g. `26.2.3` = the 2nd content update and the 3rd feature update of 2026).

- **Year**: the year of first release (two digits, e.g. 2026 → `26`); when the year changes, the following two segments reset to 0.
- **Content update** (second segment): **pricing data updates** (price changes, model additions/retirements, plan changes), each +1.
- **Feature update** (third segment): every repository update other than pricing updates (data structure, scripts, docs, mechanisms, etc.), each +1.
- The current version is in the `VERSION` file; `data/machine/schema.json`'s `version` and every data file's `schema_version` match it.
- Version increments are decided by maintainers/bots based on the change type and recorded in this file's entries.

---

## 26.1.0 — 2026-08-21 (feature update)

- **Billing-mode fixes** (content): OpenCode Go recorded as subscription (USD-allowance
  based; plan added: $5 first month / $10 mo, $60 usage); ChatGPT Go plan added ($8/mo,
  ad-supported); 436 genuinely-free models explicitly flagged; ChatGPT plan limits marked
  "not publicly specified".
- **Versioning**: scheme reversed to `year.content.feature` (content = pricing updates).
- **Bilingual docs**: every prose document now has English (default) + `*.zh-CN.md`.
- **Repo hardening**: `main` branch protected (PR-only, no force push); `pr-check.yml`
  (validate + audit + generated-page consistency + version consistency); `daily-check.yml`
  now opens a PR instead of pushing directly; `reports/` removed (stale report via
  `--stale-report`); `CONTRIBUTING` + issue/PR templates; `scripts/audit.py` added.
- Project status disclosure (work-in-progress, data may be inaccurate) and tech-stack note
  (DeepSeek Harness + deepseek-v4-flash-0731) added to README/AGENTS.

## 26.0.0 — 2026-08-21 (Initial Normalized Version)

The first version to adopt the new versioning rules (content covers all work completed on 2026-08-21).

### Content Updates (pricing data)
- **Independent pricing structure for subscription plans**: each plan in `plans.json` gains a `pricing_model` field (flat_monthly / flat_yearly / per_seat_monthly / per_seat_yearly / credits / free / custom), clearly distinguished from model per-MTok pricing; all 51 plans are tagged.
- **Fixed the 0-price ambiguity**: 155 "included in subscription/plan" models (coding-plan / token-plan / Copilot / Duo / Kimi-for-Coding, etc. providers) changed their per-MTok price from `0` to `null` + a notes entry stating "included in the subscription plan, no standalone per-token pricing", eliminating the "0 = free" misreading.
- **Structured model status**: new `model.status` field (active / preview / deprecated / retired / superseded); 41 models tagged (OpenAI retired series, xAI retired series, DeepSeek V3 old series, Anthropic Mythos preview, etc.); human-readable pages gain a status column (prominent ❌/⚠️/🔁/🧪 marks).
- Pricing-review results (DeepSeek V4, Anthropic Sonnet 5 permanent pricing, OpenAI 5.6 series, domestic vendors' official prices) are archived together with 26.0.0.

### Feature Updates (repository)
- **Official-price direct-sync layer**: `scripts/sync_official.py` + `scripts/official_sources.json` (direct scraping of DeepSeek / Baidu / Anthropic official pages, OpenAI Wayback snapshot as fallback); the daily check runs in "official → models.dev → OpenRouter" order, and providers already verified officially that day are exempt from third-party overwrites.
- **Strict en/zh separation**: README / human-readable pages (`data/human/` + `zh-CN/`) are bilingual; all docs gain a `Language:` header annotation; doc H1s align with file names.
- **Version management**: `VERSION` file + `year.feature.content` versioning rules; schema version upgraded to `26.0.0`.
- AGENTS.md (agent guide), docs/verification.md (truthfulness mechanism), docs/ego-browser-workflow.md (ego-lite re-verification workflow).

### Historical Background (work before 26.0.0, archived here)
- Repository establishment: schema v1, OpenRouter (419 models) + models.dev (192 providers) auto-sync, dual-version output, daily-check workflow, 51 subscription plans, comprehensive pricing review (DeepSeek / Anthropic / OpenAI / domestic vendors).
