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
  router.py              # Core check router: discovers checks/, runs in tier order
  toolbox.py             # Shared utilities (http, JSON, changelog, manifest, dedup)
  checks/                # Per-provider official-price checks (tierN_<provider>.py)
  daily_check.py         # Daily entry: router (official) -> models.dev -> OpenRouter
  sync_official.py       # Standalone official-source sync (official_sources.json registry)
  sync_openrouter.py     # OpenRouter catalog sync (aggregator prices)
  sync_modelsdev.py      # models.dev catalog sync
  validate.py            # Schema + consistency validation
  audit.py               # Repo-wide audit (version, counts, zero-price, docs bilingual)
  build_human.py         # Generate human pages (en + zh-CN)
  stats.py               # Exact data statistics for README
  bump_version.py        # Version bump (year.content.feature) + changelog entries
  merge_research.py      # Merge research-subagent JSON output
CONTRIBUTING.md          # contribution guide (en + zh-CN)
```

## Reading Data (for agents building tools)

1. Fetch `data/feed/index.json` first. Check `schema_version` (major bump = breaking).
2. Each `providers[]` / `resellers[]` entry has `file` (relative path), `model_count`, `updated_at`.
3. Model shape: `{id, name, category, status, modalities, context_window, max_output, pricing, notes}`.
   `status` = **online | offline** only. Offline models keep the reason (retired/deprecated/superseded)
   in `notes` and stay as historical entries with a ❌ mark in the human pages.
4. `pricing` fields (all USD per 1M tokens unless `currency` says otherwise):
   - `per_mtok.{input,output,cache_read,cache_write}`
   - `batch.{input,output}` — 50% off batch APIs
   - `per_image[]` — tiers for image models
   - `per_audio_second`, `per_character`, `per_request`, `credits` (points systems),
     `gpu[]` (per-second/hour SKUs), `neuron_second`, `finetune`, `provisioned`
5. **`null` means "not offered / unknown" — never treat as zero.** `0` means free.
6. Plans: `{id, provider_id, product, plan, category, pricing_model, billing, price_usd, limits, includes, url, verified_at}`.
   `pricing_model` (flat_monthly / flat_yearly / per_seat_monthly / per_seat_yearly / credits / free / custom) is the
   subscription pricing structure — distinct from per-token model pricing. Yearly plans store the **total yearly price**
   in `price_usd`; per-seat plans store the price per seat.
   Models included in a subscription plan have `per_mtok` = null (never 0) with an explanatory note.
7. `channel` semantics: `first_party` | `cloud` | `hosted` | `aggregator` | `reseller` | `subscription`.
   The same model may appear under several channels with different prices — that is correct.

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
2. Fetches models.dev catalog → updates `per_mtok.input/output/cache_read` where they differ
   (never touches hand-maintained fields like `batch` or `cache_write`).
3. Refreshes `index.json` counts; rebuilds human pages; updates `manifest.json`.
4. Flags plans whose `verified_at` is older than 30 days → writes `--stale-report` markdown →
   syncs the "每日价格核实提醒" GitHub issue.
5. Auto-merges changes into `main` with bot identity (bump_version.py first, `[skip ci]`), or exits cleanly if nothing changed.

**Truthfulness guarantees** (and their limits):
- Auto-sync sources (OpenRouter, models.dev) refresh daily; they are republished prices from
  those platforms, which are themselves aggregations — treat as "as-of" data.
- Human-verified entries carry `verified_at` + `source` URLs; stale ones surface in the
  stale-plans issue so a human can re-verify.
- The repository cannot invent or guess prices: unknown values are `null` with `notes`,
  never fabricated numbers.

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
