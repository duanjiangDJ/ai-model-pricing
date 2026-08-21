> **Language: English (en)** — This document is written in en only.
# Verification & Truthfulness Model

How the daily check works, and what guarantees (and does not guarantee) the accuracy
of the data in this repository.

## 1. Daily Check Pipeline (`.github/workflows/daily-check.yml`, cron 01:23 UTC)

`scripts/daily_check.py` runs the following steps every day:

0. **Official-price layer** — `scripts/sync_official.py` fetches **official pricing pages
   directly** (source registry: `scripts/official_sources.json`):
   - direct fetch + parse: DeepSeek, Baidu Qianfan, Anthropic (static/SSR pages);
   - Wayback-snapshot fallback: OpenAI (JS-rendered), Google (disabled pending better parser);
   - parsed values update `per_mtok.{input,output,cache_read,cache_write}`/`batch`, refresh
     `verified_at` even when prices are unchanged ("checked today"), and record per-source
     `last_ok`/`last_error` in the manifest.
1. **OpenRouter diff** — fetch `https://openrouter.ai/api/v1/models` (the full catalog),
   compare every model's pricing against `data/machine/providers/openrouter.json`:
   - new model → `kind: add` changelog entry
   - removed model → `kind: remove`
   - price changed → update + `kind: update` entry with `old`/`new` values
2. **models.dev diff** — fetch `https://models.dev/api.json` (192+ providers) and update
   the three per-MTok fields (`input`, `output`, `cache_read`) wherever they differ.
   It deliberately does **not** overwrite hand-maintained fields (`batch`, `cache_write`,
   notes, plans) so human work is never clobbered. **Providers whose `verified_at` is
   today (just verified by the official layer) are skipped entirely** — third-party
   republication must not overwrite an official check.
3. **Index refresh** — recompute `index.json` model counts per provider.
4. **Stale-plan check** — any plan whose `verified_at` is older than 30 days is listed in
   `reports/stale-plans.md` and synced to the "每日价格核实提醒" GitHub issue, so a human
   is asked to re-verify.
5. **Human pages rebuild** — regenerate `data/human/` (en + zh-CN) from machine data.
6. **Manifest update** — record `last_daily_check`, per-source `last_ok` / `last_error`.
7. **Commit** — if anything changed, commit with bot identity (`[skip ci]`) and push.
   If nothing changed, the run exits cleanly with no commit.

The workflow also runs `scripts/validate.py` (JSON Schema + index-count consistency +
duplicate-id checks) on every run; a validation failure fails the workflow run.

## 2. Data-Source Hierarchy & Truthfulness Guarantees

| Tier | Source | Update cadence | Trust level |
|---|---|---|---|
| A+. Official page (agent via ego-browser) | live JS-rendered official pages read by an AI agent with the ego-lite browser | on demand, per re-verification campaign | Highest — current official page, rendered |
| A. Official pages (direct parse) | static/SSR official pages parsed in-repo (DeepSeek, Baidu, Anthropic) + Wayback snapshots for JS pages | daily auto-sync (`sync_official.py`) | High — direct from vendor (snapshots may lag) |
| B. models.dev | republished official list prices, maintained by a third party | daily auto-sync (skipped when A/A+ verified today) | High for first-party entries; still third-party republication |
| C. OpenRouter API | reseller/aggregator prices (the price OpenRouter charges) | daily auto-sync | Correct *as OpenRouter's price*; differs from official prices by design |

Guarantees we do make:

- **Traceability** — every entry has `verified_at` (UTC) and, for human-verified data, a
  `source` URL (pricing page or official doc). `changelog.json` keeps the full history
  (old → new) for every change, so any number in the DB can be traced to when and from
  where it came.
- **No fabrication** — unknown prices are stored as `null` with an explanatory `notes`;
  `0` means "free" only. No number is guessed or extrapolated (except explicitly-flagged
  conversions like CNY→USD at a stated rate).
- **Staleness surfacing** — plans older than 30 days automatically raise a GitHub issue;
  auto-synced prices carry `updated_at` so consumers can judge freshness themselves.
- **Mechanical consistency** — every file validates against `schema.json`; index counts
  are recomputed from actual files; duplicate model ids are rejected.

Guarantees we explicitly do **not** make:

- Auto-synced tiers (B/C) are *republications* by third parties — if their upstream data is
  wrong or stale, so is ours until the next sync. We do not crawl every vendor's website
  directly (most pricing pages are JS-rendered and change shape constantly).
- The long tail (thousands of CN resellers, enterprise custom pricing, provisioned
  throughput) cannot be exhaustively tracked; the README states this scope honestly.
- Prices change at any moment; the DB is "as of" data, not a real-time quote service.

## 3. Re-verification Campaigns

Periodically (e.g. after model releases or price wars) a full re-verification pass is run:
research subagents check official docs per vendor and write results to
`pricing_research/*.json`, which is merged via `scripts/merge_research.py`
(upserts by model id, refreshes `verified_at`). The contract for these campaigns is
documented in `docs/research-contract.md`.

## 4. How to Check a Specific Number Yourself

1. Read the entry: `data/machine/providers/<id>.json` → model → `pricing` + `notes`.
2. Note `verified_at` (human) or `updated_at` (auto-sync) and the `source` URL.
3. For auto-synced values, `data/meta/changelog.json` shows when it last changed.
4. Open the source URL and compare. If it differs, fix it or open an issue.
