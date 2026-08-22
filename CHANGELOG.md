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

## 26.3.6 — 2026-08-22T12:51Z (content update)

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
