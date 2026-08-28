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

## 26.7.12 — 2026-08-28T08:10Z (feature update)

- **fix(test pollution)**: surge-guard unit tests only mocked `save_provider`, but `update_model_prices` also calls `append_changelog` — every test run wrote fake "test-prov" entries into the production `changelog.json`, and one such entry reached CHANGELOG.md (26.6.11). Tests now mock both; the 2 polluted changelog entries were removed and the 26.6.11 entry rewritten to explain it had no real changes.
- **fix(free notes)**: zero-price models need a "free" note (audit policy). `sync_modelsdev` / `sync_openrouter` `build_model` now append "Free model (per_mtok = 0)." to notes when classified free; backfilled the note on 90 existing zero-price models (kenari/nvidia/opencode/openrouter/orcarouter/venice/vercel). Audit warnings 34 → 2.
- **fix(audit)**: CNY-in-USD warnings now exempt notes explicitly stating "no official USD" (honest CNY-only annotations for baidu ernie-5.1/4.5-turbo, volcengine doubao — those are intentional).

## 26.7.11 — 2026-08-28T05:09Z (content update)

- price sync (341 changes):
- alibaba update x8: qwen3.7-plus,qwen3.7-plus,qwen3.6-flash,qwen3.6-flash,qwen-vl-ocr,qwen-vl-ocr,qwen3.6-35b-; qwen-vl-ocr: {'input': [0.07, 0.72], 'output': [0.16, 0.72]}->{'input': 0.72, 'output': 0.; qwen3-32b: {'input': [0.16, 0.7], 'output': [0.64, 2.8]}->{'input': 0.7, 'output': 2.8}; qwen3-next-80b-a3b-instruct: {'input': [0.15, 0.5], 'output': [1.2, 2]}->{'input': 0.5, 'o; qwen3-next-80b-a3b-thinking: {'input': [0.15, 0.5], 'output': [1.2, 6]}->{'input': 0.5, 'o
- alibaba-cn update x3: glm-5: {'input': [0.86, 0.573], 'output': [3.15, 2.58]}->{'input': 0.573, 'output': 2.58}; glm-5.1: {'input': [0.87, 0.825], 'output': [3.48, 3.301]}->{'input': 0.825, 'output': 3.3; qwen3.5-397b-a17b: {'input': [0.43, 0.172], 'output': [2.58, 1.032]}->{'input': 0.172, 'ou
- baseten add x1: zai-org/GLM-5.3-Flash: ?->zai-org/GLM-5.3-Flash
- crossmodel add x1: z-ai/glm-5.3-flash: ?->z-ai/glm-5.3-flash
- deepseek update x4: deepseek-v4-flash,deepseek-v4-flash,deepseek-v4-flash,deepseek-v4-pro,deepseek-v4-pro,deep; deepseek-v4-flash: {'input': [0.44, 0.14], 'output': [1.32, 0.28], 'cache_read': [0.014, 0; deepseek-v4-flash-vision-exp: {'input': [0.44, 0.14], 'output': [1.32, 0.28], 'cache_read'; deepseek-v4-pro: {'input': [1.32, 0.435], 'output': [3.96, 0.87], 'cache_read': [0.044, 0.
- digitalocean add x1: glm-5.3-flash: ?->glm-5.3-flash
- digitalocean update x9: deepseek-3.2: {'input': [0.25, 0.5], 'output': [0.8, 1.6], 'cache_read': [0.075, 0.15]}->{; deepseek-4-flash: {'input': [0.0679, 0.14], 'output': [0.168, 0.28], 'cache_read': [0.0168; deepseek-v4-flash-0731: {'input': [0.08, 0.14], 'output': [0.252, 0.28], 'cache_read': [0.; deepseek-v4-pro: {'input': [0.87, 1.74], 'output': [1.74, 3.48], 'cache_read': [0.174, 0.3; glm-5.2: {'input': [0.7, 1.4], 'output': [2.2, 4.4], 'cache_read': [0.105, 0.21]}->{'input
- edenai add x5: databricks/databricks-gpt-oss-120b@eu: ?->databricks/databricks-gpt-oss-120b@eu; databricks/databricks-gpt-oss-20b@eu: ?->databricks/databricks-gpt-oss-20b@eu; vertex/gemini-3.1-flash-lite: ?->vertex/gemini-3.1-flash-lite; vertex/gemini-3.1-flash-lite@eu: ?->vertex/gemini-3.1-flash-lite@eu; vertex/gemini-3.1-flash-lite@us: ?->vertex/gemini-3.1-flash-lite@us
- edenai update x5: ionos/meta-llama/Llama-3.3-70B-Instruct: {'input': [0.758485, 0.756925], 'output': [0.7584; ionos/openai/gpt-oss-120b: {'input': [0.175035, 0.174675], 'output': [0.758485, 0.756925]}; scaleway/deepseek-v4-flash-0731: {'input': [0.46676, 0.4658], 'output': [0.933521, 0.9316]; scaleway/gpt-oss-120b: {'input': [0.175035, 0.174675], 'output': [0.70014, 0.6987]}->{'inp; scaleway/llama-3.3-70b-instruct: {'input': [1.050211, 1.04805], 'output': [1.050211, 1.048
- hyper update x5: glm-5: {'input': [0.92, 0.9], 'output': [2.976, 2.804]}->{'input': 0.9, 'output': 2.804}; kimi-k2.5: {'input': [0.544, 0.5444], 'output': [2.76, 2.855]}->{'input': 0.5444, 'output'; llama-3.3-70b-instruct: {'input': [0.638, 0.6066], 'output': [0.768, 1.0386]}->{'input': 0; minimax-m2.7: {'input': [0.424, 0.408], 'output': [1.612, 1.512]}->{'input': 0.408, 'outpu; qwen3.8-flash: {'input': [0.16, 0.15]}->{'input': 0.15}
- inceptron update x2: moonshotai/Kimi-K2.6: {'cache_read': [0.13, 0.15]}->{'cache_read': 0.15}; moonshotai/Kimi-K2.7-Code: {'input': [0.67, 0.66], 'cache_read': [0.19, 0.18]}->{'input': 
- kenari add x21: claude-opus-5: ?->claude-opus-5; claude-sonnet-4-6: ?->claude-sonnet-4-6; gemini-3-1-flash-tts: ?->gemini-3-1-flash-tts; gemini-3-1-pro: ?->gemini-3-1-pro; gemini-3-5-flash: ?->gemini-3-5-flash
- kilo add x1: inclusionai/ling-3.0-flash-fin:free: ?->inclusionai/ling-3.0-flash-fin:free
- kilo update x9: google/gemma-4-31b-it: {'input': [0.09, 0.08], 'output': [0.34, 0.35], 'cache_read': [0.05; meta-llama/llama-4-maverick: {'output': [0.696, 0.8]}->{'output': 0.8}; minimax/minimax-m2.7:free: {'cache_read': [None, 0]}->{'cache_read': 0}; minimax/minimax-m3:free: {'cache_read': [None, 0]}->{'cache_read': 0}; qwen/qwen3.6-35b-a3b: {'input': [0.14, 0.1], 'output': [1, 0.9]}->{'input': 0.1, 'output':
- llmgateway add x1: deepseek-v4-flash-vision-exp: ?->deepseek-v4-flash-vision-exp
- merge-gateway update x1: zai/glm-5.3-flash: {'input': [0.075, 0.015], 'output': [0.25, 0.05], 'cache_read': [0.015,
- minimax update x2: MiniMax-M2.5-highspeed: ?->{'models': 1}; MiniMax-M2.5-highspeed: {'cache_read': [0.03, 0.06]}->{'cache_read': 0.06}
- mistral update x3: ministral-3b-latest,ministral-3b-latest,ministral-8b-latest,ministral-8b-latest: ?->{'mode; ministral-3b-latest: {'input': [0.1, 0.04], 'output': [0.1, 0.04]}->{'input': 0.04, 'outpu; ministral-8b-latest: {'input': [0.15, 0.1], 'output': [0.15, 0.1]}->{'input': 0.1, 'output
- modal add x2: Qwen/Qwen3.8-2.4T-A95B: ?->Qwen/Qwen3.8-2.4T-A95B; zai-org/GLM-5.3-Flash: ?->zai-org/GLM-5.3-Flash
- nano-gpt add x1: z-ai/glm-5.3-flash-uncensored: ?->z-ai/glm-5.3-flash-uncensored
- neuralwatt add x4: kimi-k2.7-code: ?->kimi-k2.7-code; kimi-k2.7-code-fast: ?->kimi-k2.7-code-fast; kimi-k3-flex: ?->kimi-k3-flex; qwen3.6-35b: ?->qwen3.6-35b
- neuralwatt update x10: gemma-4-31b: {'cache_read': [0.036, 0.0144]}->{'cache_read': 0.0144}; glm-5.2: {'cache_read': [0.3625, 0.145]}->{'cache_read': 0.145}; glm-5.2-fast: {'cache_read': [0.3625, 0.145]}->{'cache_read': 0.145}; glm-5.2-flex: {'input': [0.725, 0.9425], 'output': [2.25, 2.925], 'cache_read': [0.18125, ; glm-5.2-short: {'cache_read': [0.3625, 0.145]}->{'cache_read': 0.145}
- nvidia add x1: deepseek-ai/deepseek-v4-pro-0813: ?->deepseek-ai/deepseek-v4-pro-0813
- ofox add x1: z-ai/glm-5.3-flash: ?->z-ai/glm-5.3-flash

## 26.6.11 — 2026-08-27T19:41Z (content update)

- No real data changes in this run. (A transient unit-test pollution wrote two fake
  "test-prov" changelog entries that were cleaned up in 26.7.12; the version bump was
  triggered by that noise and is kept for version history continuity.)

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
