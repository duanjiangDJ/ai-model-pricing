> **Language: English (en)** — This document is written in en only.

# Changelog

## Versioning Rules

Version number format: **`year.content.feature`** (e.g. `26.2.3` = the 2nd content update and the 3rd feature update of 2026).

- **Year**: the year of first release (two digits, e.g. 2026 → `26`); when the year changes, the following two segments reset to 0.
- **Content update** (second segment, +1): **pricing data ONLY** — price changes, model add/retire (status change), plan add/price change. E.g. fixing a model's input/output, adding the ChatGPT Go plan, marking a model offline.
- **Feature update** (third segment, +1): **everything else** — data structure (schema/format), scripts (router/checks/toolbox), workflows, docs, translations, directory renames, CI mechanics. E.g. adding a check script, renaming a directory, updating AGENTS.
- Boundary: when a PR mixes pricing and feature changes, bump only ONE segment by the dominant type (pricing -> content; otherwise -> feature).
- Each rule advances only its own segment; they never reset each other.
- The current version is in the `VERSION` file; `data/feed/schema.json`'s `version` and every data file's `schema_version` match it.
- Version increments are decided by maintainers/bots based on the change type and recorded in this file's entries.

---

## 26.6.11 — 2026-08-27T19:41Z (content update)

- price sync (2 changes):
- test-prov update x2: m1: ?->{'models': 1}; m1: ?->{'models': 1}

## 26.5.11 — 2026-08-27T17:38Z (feature update)

- **fix(regression, HIGH)**: `sync_openrouter.py` / `sync_modelsdev.py` did not emit the new required `billing_model` field — the next daily auto-sync would have STRIPPED billing_model from every OpenRouter/models.dev model and tripped the audit "missing billing_model" fail, breaking the auto-merge workflow. Both `build_model` functions now classify billing (pay_per_token / pay_per_image / free / unknown) and no longer write the removed `per_request`/`per_audio_second` fields (schema-dead). Verified by running a real sync: all 417 OpenRouter models annotated correctly (388 pay_per_token, 29 pay_per_image+pay_per_token).
- **fix(stats)**: "By channel" model counts were always 0 (`chan_m` was declared but never populated); README/zh-CN stats now show real counts (e.g. Inference host 4,316 / Subscription 173 / Aggregator 2,222).
- **fix(audit)**: aggregated the 235 per-model "pay_per_token but per_mtok all null" warnings into one summary line per provider (these are reseller models billed per-token whose price is simply not published); audit warnings 248 → 14.
- **feat(ui)**: view pages now mark models with a live `promo` as 🔥 promo (en) / 🔥 促销 (zh-CN); Z.ai GLM-5.3-Flash shows the badge.
- **feat(tests)**: 2 new surge-guard tests (normal change applies, >5x surge skipped) via mocked save; test suite now 7 tests.
- **refactor(schema)**: `providerFile` simplified to a pure `$ref` of `$defs.provider`.

## 26.5.10 — 2026-08-27T17:16Z (feature update)

- **feat(billing_model)**: every model now carries a required `billing_model` array (pay_per_token / pay_per_image / subscription_included / credits / free / unknown) — machine-readable "how is this billed" instead of inferring from null/0/notes. 7,239 models annotated via `scripts/annotate_billing.py` (6467 pay_per_token, 384 free, 114 subscription_included, 55 free+pay_per_token, 219 unknown needing review — those have no price in models.dev, honestly marked). Mixed billing supported (e.g. Gemini free tier + paid).
- **feat(schema)**: removed 8 unused pricing fields (per_audio_second, per_character, per_request, credits, gpu, neuron_second, finetune, provisioned — 0 usage); added `promo.{list_price, ends_at}`; `billingModel` enum added; priceType enum trimmed 17→8. Fixed `providerFile` being an empty schema (provider data was previously NOT actually validated). Re-added a billing mode procedure documented in AGENTS.md (fields exist only when backed by data).
- **feat(channel)**: coding-plan/token-plan providers unified to `channel: subscription` (was mixed hosted/subscription across 9 providers).
- **feat(promo)**: Z.ai GLM-5.3-Flash 50% promo recorded (list $0.15/$0.50/$0.03, ends 2026-09-09).
- **feat(audit)**: new checks — billing_model presence/enum/pricing-consistency, currency-vs-CNY notes detection, `:free` id suffix exemption for zero-price warnings.
- **feat(ui)**: view pages gain a "Billing" column (en + zh-CN); subscription channel labels added.
- **feat(tests)**: `tests/test_parsers.py` with HTML fixtures (deepseek EN page, baidu INT'L page); pr-check.yml now runs them.
- **feat(ci)**: daily-check now emits a detailed `SYNC_SUMMARY` (provider/model/old→new) used as the CHANGELOG message instead of bare "chore: price sync".
- **docs**: AGENTS.md (billing_model, add-a-billing-mode procedure, English-comments rule, channel semantics), FORMAT.md (en+zh-CN, incl. model.status online/offline correction), docs/price-types.md (en+zh-CN rewritten to current billing types), README stats refreshed (186 providers, 7,239 models, 67 plans).

## 26.5.9 — 2026-08-27T15:40Z (content update)

- **fix(currency)**: deepseek.json v4 series corrected from CNY values to official EN-page USD prices (flash $0.44/$1.32, pro $1.32/$3.96, peak tier). baidu.json ernie-5.0 → INT'L page USD ($1.4/$5.6); ernie-5.1/4.5-turbo → null + CNY notes (domestic-only). tencent.json currency → CNY (hunyuan ¥1/¥4, official CNY-only). volcengine.json doubao-2.1-pro/turbo → null + CNY notes (no official USD page).
- **fix(parsers)**: deepseek parser now fetches the official EN pricing page (USD) with a structure assertion (18 $prices required — fails loudly instead of writing partial data). baidu parser rewritten for the Qianfan INT'L page (USD, $/M tokens).
- **feat(guardrails)**: price-surge guard (>5x change treated as parsing error, field skipped with warning) in both toolbox.update_model_prices and sync_official.apply_to_provider. OpenRouter catalog rewrite guarded (remote < 50% of local size → refuse overwrite).
- **fix(ci)**: pr-check.yml core-file protection paths corrected from data/machine/ to data/feed/.
- **feat(data)**: new provider zai-coding-plan (GLM-5.3-Flash + GLM-5.3 + routing rules, credit multipliers, off-peak 50% rule) + 3 plan entries (Lite/Pro/Max, credits-based, $18/$72/$160).

## 26.4.9 — 2026-08-27T08:13Z (content update)

- chore: price sync

## 26.3.9 — 2026-08-27T07:56Z (feature update)

- fix: daily-check falls back to branch + alert issue when PAT push is rejected by branch protection (fine-grained PAT cannot bypass)

## 26.3.8 — 2026-08-27T07:39Z (feature update)

- fix: daily-check workflow YAML fix (issue-body indentation) + auto-merge aligns base with latest main before commit (stash/rebase/stash-pop) to avoid rebase conflicts; GH_PAT auto-merge verified working

## 26.3.7 — 2026-08-27T07:22Z (feature update)

- fix: zai check parses Latest Models section + auto-adds new official models; router refreshes index counts; daily-check PR-failure now alerts via issue and fails loudly

## 26.3.6 — 2026-08-27T00:38Z (content update)

- chore: price sync

## 26.2.6 — 2026-08-22T11:46Z (feature update)

- feature: T0 automation for alibaba/google/meta/minimax/mistral/moonshotai/xai/zai (official-page checks); 14 models price-corrected (alibaba 7, ministral 2, minimax cache-write 8, moonshot batch 3, zai cache 2, google batch 9)

## 26.2.5 — 2026-08-22T11:10Z (feature update)

- feature: ByteDance visible in provider name/status table, fix 38 broken cross-doc links, add broken-link check to audit

## 26.2.4 — 2026-08-22T10:57Z (feature update)

- feature: data dirs renamed (data/feed + data/view/en|zh-CN), branch cleanup + branch policy, changelog boundaries + zh translations, core-file update rules documented, pending vendors merged into tiers, opencode-go same tier

## 26.2.3 — 2026-08-22T10:29Z (content update)

- fix: models.dev sync skips subscription-included providers (per_mtok stays null); re-fix 96 zero prices

## 26.1.3 — 2026-08-22T09:33 (content update)

- chore: price sync

## 26.0.3 — 2026-08-22T15:30 (feature update)

- feature: status simplified to online/offline, 3-hourly auto-check with direct merge to main, version increment logic fixed (content/feature independent) with minute-precision timestamps, AGENTS zh-CN removed, docs dedup (ego removed, providers+roadmap merged into generated status doc), cross-linked documentation

## 26.0.2 — 2026-08-22 (feature update)

- feature: core check router (scripts/router.py) + toolbox (scripts/toolbox.py) + per-provider checks (scripts/checks/), CONTRIBUTING guide expanded, daily-check PR fix

## 26.0.1 — 2026-08-22 (feature update)

- feature: api_base_url + Notes column in human pages, dedup checks, pr-check enforces CHANGELOG/VERSION, bump_version.py, README star badge + exact stats, all machine notes localized to English

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
- **Strict en/zh separation**: README / human-readable pages (`data/view/` + `zh-CN/`) are bilingual; all docs gain a `Language:` header annotation; doc H1s align with file names.
- **Version management**: `VERSION` file + `year.feature.content` versioning rules; schema version upgraded to `26.0.0`.
- AGENTS.md (agent guide), docs/verification.md (truthfulness mechanism), docs/ego-browser-workflow.md (ego-lite re-verification workflow).

### Historical Background (work before 26.0.0, archived here)
- Repository establishment: schema v1, OpenRouter (419 models) + models.dev (192 providers) auto-sync, dual-version output, daily-check workflow, 51 subscription plans, comprehensive pricing review (DeepSeek / Anthropic / OpenAI / domestic vendors).


---

## Related docs

- [README](README.md) — overview & exact stats
- [AGENTS.md](AGENTS.md) — guide for AI agents
- [FORMAT.md](FORMAT.md) — machine format spec
- [docs/providers.md](docs/providers.md) — provider landscape & status
- [docs/price-types.md](docs/price-types.md) — price types
- [docs/verification.md](docs/verification.md) — verification model
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute
