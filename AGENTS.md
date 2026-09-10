> **Language: English (en)** — This document is written in en only.
# AGENTS.md — Guide for AI Agents Working in This Repository

This file tells AI agents (and humans) everything needed to read, validate, and update
this repository correctly. Read it fully before making changes.

## ⚠️ Project Status

**This repository is a work in progress.** Data may be outdated, incomplete, or wrong;
some billing modes are hard to verify. Treat every entry as "as-of" data:
- check `verified_at` / `updated_at` and the `notes` (source) before trusting a number;
- `null` means unknown/not offered — never invent a value, never use 0 for "unknown";
- subscription-included models have `per_mtok: null` + a note (never 0);
- deprecated/retired models carry `"status"` and remain as historical entries.

Contributions are welcome via issues and PRs (see `CONTRIBUTING.md`); human changes go
through PRs checked by `.github/workflows/pr-check.yml`. Bot syncs merge straight into `main`.

**How this project is built**: maintained with
[DeepSeek Harness](https://github.com/deepseek-ai/DeepSeek-Harness) using the
**deepseek-v4-flash-0731** model.

## What This Repository Is

`ai-model-pricing` is an open database of **AI model pricing** covering every obtainable
channel: first-party vendor APIs (per-MTok, cache, batch), image/audio pricing, credit
systems, GPU-hour pricing, consumer subscriptions, and coding-tool plans.

- Machine-readable data: `data/feed/` (versioned JSON + JSON Schema)
- Human-readable pages: `data/view/` (Markdown, **generated** — never edit by hand)
- Auto-updated every 3 hours by GitHub Actions: `.github/workflows/daily-check.yml` (changes merge straight into `main`; no review needed for bot syncs)

## Repository Layout

```
data/feed/
  schema.json            # THE authoritative JSON Schema (26.0.1)
  index.json             # Entry point: providers/resellers lists, counts, timestamps
  providers/*.json       # One file per provider (provider_id.json)
  plans.json             # Subscription & coding-tool plans
data/meta/
  manifest.json          # Sync health: sources, last_ok/last_error
  changelog.json         # Every change (add/update/remove/verify), newest first
data/view/              # GENERATED (never edit): en/*.md + zh-CN/*.md
docs/                    # providers.md (landscape & status, generated), price-types.md,
                         # research-contract.md, verification.md
scripts/
  collect/router.py      # Core check router: discovers collectors/, runs in tier order
  toolbox.py             # Shared utilities (http, JSON, changelog, manifest, dedup)
  checks/                # Per-provider official-price checks (tierN_<provider>.py)
  daily_check.py         # Daily entry: collect/price_check (router) -> models.dev -> OpenRouter
  sync/sync_official.py  # Standalone official-source sync (official_sources.json registry)
  sync/sync_openrouter.py  # OpenRouter catalog sync (aggregator prices, per-token x1e6)
  sync/sync_modelsdev.py   # models.dev catalog sync
  validate.py            # Schema + consistency validation
  audit.py               # Repo-wide audit (version, counts, zero-price, docs bilingual)
  tools/
    fetch_official.py    # Official-source verification fetcher (policy §15.2 SOURCES)
  build_human.py         # Generate human pages (en + zh-CN)
  stats.py               # Exact data statistics for README
  bump_version.py        # Version bump (year.content.feature) + changelog entries
  merge_research.py      # Merge research-subagent JSON output
CONTRIBUTING.md          # contribution guide (en + zh-CN)
```

## Reading Data (for agents building tools)

1. Fetch `data/feed/index.json` first. Check `schema_version` (major bump = breaking).
2. Each `providers[]` / `resellers[]` entry has `file` (relative path), `model_count`, `updated_at`.
3. Model shape: `{id, name, category, status, modalities, context_window, max_output, billing_model, pricing, notes}`.
   `status` = **online | offline** only. Offline models keep the reason (retired/deprecated/superseded)
   in `notes` and stay as historical entries with a ❌ mark in the human pages.
   `billing_model` (required, array) = how the model is billed; one model can have several:
   `pay_per_token` (per-token API, incl. cache/batch), `pay_per_image`, `subscription_included`
   (included in a subscription/coding plan), `credits` (points-based), `free`, `unknown` (needs review).
   Use `python scripts/annotate_billing.py` to (re-)annotate; audit flags unknown/pay-per-token inconsistencies.
   `free` means the model is TRULY free: every `per_mtok` value is 0/null. A model with any
   positive `per_mtok` is `pay_per_token` — never flag it `free` (`annotate_billing.py` does
   this; a paid model stays `free`-free even when it has a zero-price dimension such as
   embedding output or free cache reads).
4. `pricing` fields (all USD per 1M tokens unless `currency` says otherwise):
   - `per_mtok.{input,output,cache_read,cache_write}` — per-token API prices
   - `batch.{input,output}` — 50% off batch APIs
   - `per_image[]` — tiers for image models
   - `promo.{list_price, ends_at}` — temporary discount; current `per_mtok` is the promo price,
     `list_price` holds the pre-promo value and `ends_at` the expiry (UTC ISO). When the promo
     expires, `per_mtok` must already hold the list price and the `promo` block MUST be removed
     (an expired promo is stale metadata that renders a misleading "🔥 promo" badge; `audit.py`
     hard-fails an expired promo whose `per_mtok` still differs from `list_price`, and warns on a
     redundant one whose `list_price` already equals `per_mtok`)
   Other billing fields (per_audio_second, per_character, per_request, credits, gpu, neuron_second,
   finetune, provisioned) were REMOVED from the schema on 2026-08-28 because nothing used them.
   **To add a billing mode back**: (a) add the field to `schema.json#/$defs/modelPricing.properties`,
   (b) add its value to `$defs.priceType.enum` and `$defs.billingModel.items.enum`, (c) populate real
   data for at least one model, (d) add a renderer in `scripts/build_human.py`, (e) add a parser test
   fixture if a page parse is involved, (f) bump VERSION as a feature update. Do not add schema fields
   speculatively — fields only exist when backed by data.
   **Dual-currency & scale gotcha**: a model's `cny`/`usd` fields across `input/output/cache_read/`
   `cache_write` must share a single FX rate. A spread >4x between fields means one field got a wrong
   unit/scale conversion (e.g. `deepseek-v4-pro` `cache_read.usd` was stored as 0.003625 when the
   official value is $0.044 = cny 0.30 / ~6.8). `audit.py` now flags this class. Note
   `update_model_prices()`'s `>5x` surge guard SKIPS any correction more than 5x from the stored value —
   so a badly-stuck wrong value (like that 12x-off cached price) can NEVER self-heal via a sync; fix it
   manually against the official page and re-run the gate. A check whose official page is >5x away
   from the stored value MUST surface it (a check parser raises rather than returning silently — see
   `tier0_alibaba._surge_blocked`); a silent skip leaves a stale price published forever. Real
   2026-09-10: `qwen-vl-ocr` input stuck at $0.72 vs the official $0.07, and
   `qwen3-next-80b-a3b-thinking` output $6 vs $1.2.
   **Mixed-currency zero (fabricated)**: `0` means *free*, so a per_mtok field that is `0` in one
   currency but `>0` in another is self-contradictory — e.g. `{"usd": 0, "cny": 0.15}` claims the
   model is free in USD while it is demonstrably paid in CNY. This happens when a CNY-only vendor's
   collector (which supplies only `cny`) inherits a stale `usd: 0` from an earlier aggregator write:
   `update_model_prices()` merges per currency and **never clears a value**, so the bad `usd: 0`
   survives every 3h sync (and even inflates the README "Free models" count). `audit.py` now
   hard-fails this class via `toolbox.mixed_currency_zero()`. The correct form for a single-currency
   vendor is the schema-blessed single-currency entry (`{"cny": 0.15}`) or `usd: null` — never `0`.
   Real 2026-09-10: zhipuai `glm-4.7-flash` (`usd: 0` vs `cny: 0.15` / `1.5`).
5. **A check parser must FAIL LOUDLY on a layout change, never return 0 rows.** `tier0_anthropic`
   was matching nothing for an unknown period (the page swapped the cache cells to
   **Read before Write** and renamed "Fable 5" → "Fable 5.1"), so `check:anthropic` stayed GREEN in
   the manifest while Anthropic prices were not verified at all. `parse()` now raises when it matches
   nothing, and the label that immediately precedes a block (nearest match, longest wins) is mapped to
   the model id so a version suffix is not absorbed by its prefix.

   **This is a whole-class rule, not an anthropic special case.** Every *real* parser — any
   check module that exposes `parse()` — must raise (ValueError) on an empty/stub page instead
   of returning an empty container, or `scripts/router.py` records `changed=0` as GREEN while
   the vendor is never verified. 2026-09-10: the guard was missing in `google` / `minimax` /
   `mistral` / `openai` / `xai` / `zai` (parser-level) and `moonshotai` / `tier1_baidu` /
   `tier1_stepfun` / `tier1_zhipuai` (run-level); they now raise too.
   `tests/test_check_fail_loud.py` sweeps every `parse()`-bearing module on empty input and
   fails if one silently returns nothing, so a future parser cannot regress. `tier0_meta` is
   the sole documented exception (its official page is a client-rendered SPA with no SSR
   prices — the check reports that honestly and never guesses a number).
6. **`null` means "not offered / unknown" — never treat as zero.** `0` means free.
7. Plans: `{id, provider_id, product, plan, category, pricing_model, billing, price_usd, limits, includes, url, verified_at}`.
   `pricing_model` (flat_monthly / flat_yearly / per_seat_monthly / per_seat_yearly / credits / free / custom) is the
   subscription pricing structure — distinct from per-token model pricing. Yearly plans store the **total yearly price**
   in `price_usd`; per-seat plans store the price per seat.
   Models included in a subscription plan have `per_mtok` = null (never 0), `billing_model: ["subscription_included"]`,
   and an explanatory note.
8. `channel` semantics: `first_party` | `cloud` | `hosted` | `aggregator` | `reseller` | `subscription`.
   - `subscription`: coding-plan / token-plan products (credits-based or flat subscription with API access)
   - `hosted`: third-party inference hosts serving models per-token
   - The same model may appear under several channels with different prices — that is correct.

## Coding Style

- **Code comments and docstrings MUST be English.** Chinese text is allowed only in:
  (a) zh-CN documentation files (explicitly declared "written in zh-CN only"),
  (b) UI/labels for the generated zh-CN pages (`scripts/build_human.py`, `scripts/stats.py`), and
  (c) Chinese-language issue/report text generated for GitHub issues (e.g. stale-plans reports).
  A mixed-language source file is a bug — fix it before committing.

## Updating Data (rules you MUST follow)

1. **Prices must come from official pricing pages / official APIs / official docs**, verified
   via at least one secondary source where possible. Record `source` URLs and `verified_at`.
2. Edit `data/feed/providers/<id>.json` or `plans.json` directly; **never edit `data/view/`**
   (run `python scripts/build_human.py` instead — it regenerates both en and zh-CN pages).
3. After any data change, run `python scripts/validate.py` (needs `pip install jsonschema`).
   It checks schema conformance, index count consistency, and duplicate model ids.
4. When prices change: update the value(s) AND `verified_at`/`updated_at`, then append a
   `changelog.json` entry (`kind: update|add|remove`, `scope: model|plan|provider`, `old`/`new`).
5. Deprecated/retired models stay in the file with `pricing` all `null` and a `notes`
   explaining retirement + replacement model. Never silently delete them.
6. Non-USD providers (CNY etc.): set `currency`/`price_currency` on the provider and explain
   the conversion in `currency_usd_note`.
7. Research-subagent output can be merged automatically:
   `python scripts/merge_research.py <research.json>` (format contract: `docs/research-contract.md`).

## Automation (daily check)

`.github/workflows/daily-check.yml` (cron `0 */3 * * *`, every 3 hours) runs `scripts/daily_check.py`:
1. Fetches OpenRouter catalog → diffs `providers/openrouter.json` → updates changed prices + changelog.
   `main()` **wholesale-replaces** the models list from the remote catalog, so `diff_openrouter`
   must emit a changelog entry for **every** persisted field (identity `id` and `pricing` are
   handled explicitly; all other keys are diffed generically). A field that changes with no
   changelog entry is lost provenance — guarded by `tests/test_changelog_provenance.py`.
2. Fetches models.dev catalog → updates `per_mtok.input/output/cache_read` where they differ
   (never touches hand-maintained fields like `batch` or `cache_write`).
3. Refreshes `index.json` counts; rebuilds human pages; updates `manifest.json`.
4. Flags plans whose `verified_at` is older than 30 days → writes `--stale-report` markdown →
   syncs the "每日价格核实提醒" GitHub issue.
5. Auto-merges changes into `main` with bot identity (bump_version.py first, `[skip ci]`), or exits cleanly if nothing changed.
6. The **unified data-fetch layer** (`collect/price_check.py` → `collect/utils.write_prices`) is the
   primary persist path. `write_prices` must return an **int count** — `toolbox.update_model_prices`
   returns a *list* of ids, and passing that list upward made price_check crash on the models.dev
   cross-provider result (`int += list`), silently aborting the whole persist loop; guarded by
   `tests/test_price_check_counts.py`.

**Truthfulness guarantees** (and their limits):
- Auto-sync sources (OpenRouter, models.dev) refresh daily; they are republished prices from
  those platforms, which are themselves aggregations — treat as "as-of" data.
- Human-verified entries carry `verified_at` + `source` URLs; stale ones surface in the
  stale-plans issue so a human can re-verify.
- The repository cannot invent or guess prices: unknown values are `null` with `notes`,
  never fabricated numbers.
- **Aggregator-channel prices can be time-of-day dependent.** OpenRouter (and some resellers)
  republish dynamic/peak prices for models with peak/off-peak billing upstream (e.g. DeepSeek
  V4: peak = 2x off-peak). A sync records whatever the API returns at run time, so the same
  model’s OpenRouter-channel value can jump by a clean 2x between runs. When a review flags a
  "surge" in an aggregator channel, cross-check against LIVE `openrouter.ai/api/v1/models` first
  — a clean 2x matching a first-party peak/off-peak tier is a timing snapshot, not corruption.

- **Official-source verification reads each source's real keys.** `scripts/tools/fetch_official.py`
  must read the key each source actually uses: models.dev `api.json` stores prices under
  `cost` (already USD per 1M tokens) — NOT `pricing`; the OpenRouter API stores per-token
  prices under `pricing` and must be scaled ×1e6. A fetcher that reads `pricing` for a
  models.dev entry silently returns no price forever (the “check that never fires” gap).
  When extending the `SOURCES` registry, verify with `python scripts/tools/fetch_official.py <model> --json`.

- **A `check:*` that is red in `manifest.json` is a bug signal, not noise.** `check:zhipuai`
  raised "no model rows matched" on EVERY run for weeks (the old JS marketing page
  `open.bigmodel.cn/pricing` was reworded) — `last_ok` stayed `null`, so the domestic CNY list was
  never verified. Retarget the parser to a stable STATIC source, don't silence it: bigmodel.cn
  publishes its canonical rate card as Mintlify Markdown at
  `https://docs.bigmodel.cn/cn/guide/start/pricing.md` (curl-able; columns `输入单价`/`输出单价`/
  `缓存命中`). A parser must RAISE when it matches nothing, so a layout change is loud. Same class
  as the free-listing trap: the domestic card marks `GLM-4.7-Flash` 免费, so a paid row landing on
  it (the old parser mis-assigned `GLM-4.6V-FlashX`'s ¥0.15/¥1.5) is a data-truth bug — fix it to
  `billing_model:["free"]` with all-zero `per_mtok`. The check RAISES on a paid/free mismatch
  (safety: `update_model_prices` cannot zero a price, so a bad paid listing would survive every sync).

- **A probe-only check is a DEAD check — it must parse the price table, not just fetch it.**
  `tier1_opencode`/`tier1_opencode_go` were auto-generated stubs that `js_fetch`ed the page and
  returned `changed: 0` ("parser TODO"), so the `opencode` provider was maintained purely from the
  models.dev aggregation — and where the aggregator diverges from the vendor's own list the repo
  published the wrong price (real 2026-09-11: `deepseek-v4-pro` output $3.84 vs the official $3.48,
  `kimi-k2.5` cache_read $0.08 vs $0.10). Both pages are SERVER-RENDERED HTML tables
  (`opencode.ai/docs/zen/`, `opencode.ai/docs/go/`): plain `http_get` suffices, no headless Chrome.
  The parser keeps ONLY the base tier of a tiered row (a `(≤ …)` / `(Off-Peak)` suffix) and skips
  `(> …)` / `(Peak)` — deterministic, never page-order dependent — and RAISES when it matches no
  rows. A check that reports GREEN while writing nothing is the bug, not the safety net.

- **Sync writers must emit every required provider field on a new provider file.**
  `sync_modelsdev.py` once built new providers without `api_base_url`: models.dev supplies
  it per-provider under `api` (e.g. `https://openrouter.ai/api/v1`). The audit gate hard-fails
  on a missing `api_base_url`, so a writer that drops it produces a file that can never merge.
  New-provider writers take `api_base_url` from the source's own base-url field, and populate
  `source`/`verified_at`; never emit a provider file without `api_base_url`.

## Contribution Workflow

1. Fork → edit machine data → `validate.py` → `build_human.py` → commit with a message
   describing which provider/prices changed and the source.
2. PRs must include the pricing-page URL used.
3. For large additions (new vendor), follow `docs/research-contract.md` and merge via
   `scripts/merge_research.py`.

## Quick Commands

```bash
pip install jsonschema
python scripts/sync_openrouter.py --write   # pull OpenRouter catalog (aggregator prices)
python scripts/sync_modelsdev.py --write    # pull models.dev (official-ish list prices)
python scripts/merge_research.py x.json     # merge subagent research output
python scripts/daily_check.py               # full daily check (network)
python scripts/build_human.py               # regenerate human pages (en + zh-CN)
python scripts/validate.py                  # schema + consistency validation
```

---

## Branch Policy

| Branch | Purpose | Rules |
|---|---|---|
| `main` | Production | Protected. Only two write paths: (1) the price-check bot (GH_PAT) auto-merges syncs; (2) PRs that pass `pr-check.yml`. Never push directly otherwise. |
| `bot/<topic>` | Automated/bot work (price syncs, scripts) | Short-lived; created by workflows, force-push allowed on same-day reruns, deleted after merge or when stale (>7 days without a PR). |
| `feat/<topic>` | New features (new provider, new script) | Created from `main`, must pass pr-check, delete after merge. |
| `fix/<topic>` | Bug/data fixes | Same as `feat/`. |
| `docs/<topic>` | Documentation only | Same as `feat/`. |

Rules: lowercase kebab-case names; always work from a fresh `main`; PRs must pass
pr-check (validate + audit + generated pages + version/CHANGELOG + security review);
delete the branch after merge. Stale branches (no PR, >7 days) are removed by maintainers.

## Related Docs

- [README.md](README.md) — overview & exact stats
- [FORMAT.md](FORMAT.md) — machine format spec
- [docs/providers.md](docs/providers.md) — provider landscape & status
- [docs/price-types.md](docs/price-types.md) — price types
- [docs/verification.md](docs/verification.md) — verification model
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute
