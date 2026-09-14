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
  schema.json            # THE authoritative JSON Schema (version == VERSION)
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
  migrate/
    annotate_billing.py  # (Re-)annotate billing_model across all providers
    merge_research.py    # Merge research-subagent JSON output
    migrate_dual_currency.py  # Dual-currency migration helper
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
   Use `python scripts/migrate/annotate_billing.py` to (re-)annotate; audit flags unknown/pay-per-token inconsistencies.
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
   **Silent-skip surfacing (2026-09-11)**: the guard no longer rejects *silently*. Every rejected
   correction is recorded as a changelog entry (`kind:"verify"`, `field:"surge_skip:<field>.<currency>"`,
   `old={"stored":…}`, `new={"official":…}`), deduped so a 3h sync cannot append a duplicate, and
   `audit.py` check #9 WARNs for as long as the stored value still equals the skipped one (a resolved
   skip drops out automatically). Real case: cortecs `qwen3.8-27b` output stayed $2.451 while
   models.dev — its declared source — reported $0.4 (6.13x), so every sync skipped and the row
   contradicted its own source indefinitely; corrected manually on the bot branch. This applies to
   aggregator writers too (`collect_modelsdev` is cortecs's only source — it has no fetchable official
   page, its `tier1_cortecs.py` being a stub), so an aggregation-only provider has no check to raise
   from and the guard record is its only signal.
   **The writer never ADDS a model — an unseeded official model is skipped silently (2026-09-13)**:
   `update_model_prices()` only updates ids that already exist in the provider file (`if not m:
   continue`), so a first-party check can parse a vendor's live, token-priced models and stay
   GREEN forever while none of them enter the DB. Real case: stepfun's whole `stepaudio-*` family
   (6 models on the official pricing page, 0 in the provider file) — the check's id regex was
   `step-`, which dropped the family entirely, and 4 further ids were parsed but never seeded.
   `price_check.py` now records every unresolved id set as `kind:"verify"`,
   `field:"unseeded_official:<pid>"` (deduped), and `audit.py` check #11 WARNs while any recorded
   id is STILL missing — seeding the models clears the warning automatically. WARN, never FAIL: a
   vendor adding a model must not block a bot-sync PR, and the fix is a seed, not an invention.
   A unit test that calls `price_check.run(dry_run=False)` reaches the REAL persist path: mock
   every writer it can touch (`write_prices`, `load_provider`, `record_unseeded_official`) — a
   fixture id leaked a bogus `unseeded_official:deepseek` entry into the committed changelog.
   When a collector reports missing ids, seed the models from the official page (prices + category
   + status + a source note), then `refresh_index_counts`, `stats.py`, `build_human.py` and bump.
   Same-3h-sync sibling class: an aggregator row can also be *stale* (see the re-verify note below).
   **A stub `tier1_*.py` can hide a real official API (2026-09-12)**: before concluding a provider
   has "no fetchable official source", probe its `/api/models`-style JSON endpoints — several
   auto-generated `tier1_*.py` stubs only `js_fetch` an HTML docs page and report "not fetchable",
   while the vendor in fact publishes exact machine-readable prices. Verification AND manual repair
   must use the first-party API (aggregators are peers, not authorities):
   - deepinfra: `https://api.deepinfra.com/models/list` — `cents_per_input_token` /
     `cents_per_output_token` are **cents per token** (`$/M = value x 1e6 / 100`), and
     `rate_per_input_token_cached` is a **ratio of the input price**, NOT a price
     (`cache_read $/M = ratio x input $/M`; cross-checked on `XiaomiMiMo/MiMo-V2.5-Pro`:
     0.2 x $1.0 = $0.2, a row `audit.py` does not flag, so the interpretation is confirmed).
   - nano-gpt: `https://nano-gpt.com/api/models` — `input_price_per_million` /
     `output_price_per_million` are already **$/M**, and `cacheReadInputPer1kTokens` x 1000 = $/M.
     A `TEE/<model>` id is a **separate SKU** from the plain `<vendor>/<model>` row and is priced
     lower — never copy the plain row's price onto it.
   The 2026-09-12 repair cleared all 6 unresolved surge-skips with these anchors (deepinfra
   `XiaomiMiMo/MiMo-V2.5` output 2 -> 0.28 and cache_read 0.08 -> 0.0028,
   `deepseek-ai/DeepSeek-V4-Flash-Vision-Exp` cache_read 0.14 -> 0.014; nano-gpt
   `TEE/gpt-oss-20b` 0.2/0.8/0.1 -> 0.04/0.15/0.02), each recorded in
   `data/meta/changelog.json` with its official source URL (#226).
   **Mixed-currency zero (fabricated)**: `0` means *free*, so a per_mtok field that is `0` in one
   currency but `>0` in another is self-contradictory — e.g. `{"usd": 0, "cny": 0.15}` claims the
   model is free in USD while it is demonstrably paid in CNY. This happens when a CNY-only vendor's
   collector (which supplies only `cny`) inherits a stale `usd: 0` from an earlier aggregator write:
   `update_model_prices()` merges per currency and **never clears a value**, so the bad `usd: 0`
   survives every 3h sync (and even inflates the README "Free models" count). `audit.py` now
   hard-fails this class via `toolbox.mixed_currency_zero()`. The correct form for a single-currency
   vendor is the schema-blessed single-currency entry (`{"cny": 0.15}`) or `usd: null` — never `0`.
   Real 2026-09-10: zhipuai `glm-4.7-flash` (`usd: 0` vs `cny: 0.15` / `1.5`).
   **Cache-relationship sanity (2026-09-12)**: `cache_read` is a DISCOUNT on fresh `input`, so a
   cache HIT can never cost more than an uncached input token — `cache_read > input` is impossible
   and is the signature of a parser COLUMN SWAP (a page rendering the cache cells "Write before
   Read" drops the write premium into `cache_read`; `tier0_anthropic` once rendered Read-before-Write)
   or of a stale value whose declared source no longer publishes the field (`update_model_prices`
   only writes non-None values and **never clears a removed one**, so a dropped `cache_read` survives
   every sync — real: kilo `openai/gpt-oss-20b` `cache_read 0.03 > input 0.02`, aligned to its source
   models.dev). `audit.py` WARNs on the whole class via `toolbox.cache_read_exceeds_input()`. It is a
   WARN, not a FAIL: an aggregation source can itself publish an odd pair (models.dev reports
   novita-ai `xiaomimimo/mimo-v2-flash` `cache_read 0.3 > input 0.1`), and a check must never block a
   sync for a value we cannot correctly re-derive (guarded by `tests/test_cache_relationship.py`).
   **Token-field zero policy (2026-09-14)**: `input`/`output` `usd: 0` on a NON-free model is the
   same 0-as-unknown class the cache fields already hard-fail on: it claims "these tokens are free"
   while another field is positive, when the real meaning is "the source publishes no such price"
   (models.dev's `cost.output = 0` sentinel) — the correct value is `null`. `audit.py` hard-FAILs via
   `toolbox.zero_token_price_fields()`, which exempts `output` only for the structurally-zero-output
   categories (embedding / rerank / audio_stt / audio_tts / image_gen / video_gen — they generate no
   billed output tokens) and never exempts `input`. These values are UNCLEARABLE by a sync: they were
   written before `sync_modelsdev._u()` mapped `0 -> None`, and `update_model_prices` skips None, so
   only a hand repair clears them. Real 2026-09-14: greenpt `green-s`/`green-s-pro`, azure
   `model-router`, privatemode-ai `voxtral-mini-3b` (`output: {"usd": 0}` + a positive input, all
   sourced from models.dev) — 4 chat rows that passed every gate silently; guarded by
   `tests/test_zero_token_price_fields.py`.
   **Batch-relationship sanity (2026-09-13)**: a batch API is a DISCOUNT on the standard rate
   (OpenAI / Google / Anthropic / xAI batch is ~50-80% of standard), so `batch.<field> >
   per_mtok.<field>` is IMPOSSIBLE — the signature of a stale/shared `batch` block copied from a
   SIBLING model in the same family, or of a unit/scale error. `audit.py` WARNs via
   `toolbox.batch_exceeds_standard()` (same rationale as the cache rule: an aggregation source can
   publish an odd pair, so never hard-fail) and hard-FAILS a `batch` value below `1e-4` (the
   per-token-as-per-M signature — `batch` was previously unchecked, so a mis-scaled batch price
   passed the gate silently). Real case: openai `gpt-5.6` / `-luna` / `-sol` / `-terra` ALL carried
   `batch {input 2.5, output 15}` — that is gpt-5.5's batch, copied onto every gpt-5.6 row — while
   `gpt-5.6-luna`'s own standard input is 0.2 (12.5x) and `-terra`'s is 2.0. **Root cause is
   writer-side**: NO writer sets `batch` for openai (`sync_official.parse_openai` emits
   `batch=None`; `tier0_openai` omits it), so a hand-written block survives every 3h sync and is
   never re-verified against the official Batch table. Corrected to the official
   `developers.openai.com/api/docs/pricing.md` Batch table (sol 2/10, terra 1/6, luna 0.1/0.6;
   gpt-5.6 = sol's standard -> 2/10). Regression: `tests/test_batch_relationship.py`. When adding a
   first-party check that parses a vendor page, parse its Batch table too — otherwise the batch
   price is a frozen hand-written value with no source.
   **per_mtok / batch magnitude is bounded at BOTH ends (2026-09-14)**: `per_mtok` and `batch`
   values are $ per 1M tokens, and EACH end of the scale carries a unit-error signature, so
   `audit.py` hard-FAILs both via `toolbox.per_mtok_magnitude()`: a non-zero value below `1e-4` is
   a per-token value stored as per-M (~1e6x too small, e.g. OpenRouter's `2.2e-7`), and a value
   above `2e3` is a per-1k table stored as per-M (~1e3x too large — several vendors publish a
   CNY-per-1k table beside their per-M one). The ceiling sits 3.3x beyond the priciest published
   per-token price ($600 per 1M, openai o1-pro output), so a value past it is an error rather than
   a new record; the `1e3`-`2e3` band only WARNs. Before this the upper bound was a bare WARN
   above `1e5`, so a per-1k value like `5000` produced ZERO output (probe 2026-09-14: `per_mtok
   output=5000` -> `AUDIT PASSED`, i.e. a whole unit-error class could ship). A threshold cannot
   catch a `1e3x` mis-scale of a sub-$2/M model (that lands inside the legitimate range), but
   every mis-scale of anything pricier is now blocked. Regression:
   `tests/test_per_mtok_magnitude.py`.
   **Provenance notes must persist on a verify, not only on a price change**: a check that
   re-verifies an already-correct price must still be able to (re)stamp its official source, or a
   model whose price an aggregator happened to already match stays sourceless forever.
   `update_model_prices()` writes a writer's `notes` when the price changed **or** when the model
   has no note yet, and never rewrites an existing note on a no-op verify (so an aggregator
   pass-through cannot clobber a first-party note — no tug-of-war). `audit.py` warns on any paid
   model with no provenance note. Real 2026-09-11: the retargeted opencode / opencode-go checks
   left **71 paid models sourceless** because `mid in changed` was empty for every one of them
   (their prices already matched the official page). Regression: `tests/test_notes_backfill.py`.
   **OpenRouter's `-1` sentinel means "dynamic price", NOT free**: `openrouter/auto` and the other
   router models have no fixed published price (the request is forwarded to another model and billed
   at THAT model's rate), which OpenRouter signals with `prompt`/`completion` = `-1`. `to_float_or_none()`
   maps a negative to `None`, and `all(v == 0 ...)` is `True` on the emptied price set, so `build_model()`
   mislabelled 5 routers as `billing_model: ["free"]` with a "per_mtok = 0" note — a **false free price**
   for a model that actually charges. `build_model()` now reads the raw price with the sign intact,
   classifies the sentinel as `billing_model: ["unknown"]` + an explicit "Dynamic routing price" note, and
   only labels `free` when an explicit `0` is present. `audit.py` hard-fails a `free` label whose
   `per_mtok` is all-null (a free model must assert a concrete 0; an all-null free label is a
   dynamic-price sentinel mislabel). Regression: `tests/test_openrouter_dynamic_sentinel.py`.
   **Limit-pair sanity (2026-09-12)**: every token a model does not merely READ but GENERATES also
   occupies a slot in its own `context_window` (input + output share one bounded budget), so
   `max_output > context_window` is self-contradictory — at least one spec is wrong. It is the
   signature of an INVERTED limit block from an aggregation source, or of a stale spec kept after a
   window shrink (`update_model_prices` never clears a value its source stopped publishing).
   `audit.py` WARNs on the whole class via `toolbox.max_output_exceeds_context()` (online rows only —
   an offline row keeps its last published spec on purpose); 99 models across 28 providers were
   publishing such a pair silently. It is a WARN, not a FAIL, because the repo mirrors its declared
   source and models.dev really does publish inverted pairs — real case: models.dev
   `limit: {context: 524288, output: 1048576}` for deepinfra `thinkingmachines/Inkling`, while
   DeepInfra's own first-party API (`https://api.deepinfra.com/v1/openai/models`) reports
   `context_length` 524288 / `max_tokens` 524288 for the same model, i.e. the VENDOR endpoint is the
   anchor that corrects the pair (191/191 deepinfra rows keep `max_tokens <= context_length`, 0
   inverted). **Placeholder sentinels need a DIRECT range check**: models.dev stores
   `99999999` as its "this model has no token output" sentinel. `qiniu-ai/kling-v2-6`
   carried it in BOTH limit fields; a repair cleared `context_window` but left
   `max_output`, and `max_output_exceeds_context()` was blind to it (the pair rule needs
   BOTH fields to be ints, and context was null) -- so 1e8 published silently for weeks.
   `toolbox.suspicious_max_output()` (+ the audit WARN that calls it) asserts the
   plausible range directly, mirroring the inline `context_window` sanity check, so a
   half-cleared placeholder pair of either field is caught. When you clear one side of a
   placeholder pair, clear BOTH. Regression: `tests/test_max_output_context.py`.
   **`max_output` is meaningless for a non-generative category (2026-09-14)**: an embedding or
   rerank model emits a vector / a score, never generated tokens, so `max_output` must be `null`.
   models.dev stores the embedding DIMENSION in `limit.output` (`text-embedding-3-large` 3072,
   `ada-002` / `3-small` 1536, `bge-m3` 1024, `all-mini-lm-l6-v2` 384, rerankers 1) and
   `sync_modelsdev.build_model` copied it verbatim into `max_output`, so 68 embedding/rerank rows
   published a vector size as a token limit. The pair rule above saw only the 7 whose dimension
   happened to EXCEED the context window; the other 61 (e.g. azure/openai
   `text-embedding-3-large`, context 8191 with "max_output" 3072) passed silently — a check that
   fires on only part of a bug class is itself the bug, so this one is a HARD FAIL:
   `toolbox.max_output_on_non_token_category()` + the audit rule that calls it. `build_model` now
   leaves `NON_TOKEN_OUTPUT_CATEGORIES` (embedding, rerank) null. Regression:
   `tests/test_non_token_output_category.py`. To re-verify the rule, inject a violation
   (`max_output` 3072 on an embedding row) → `audit.py` must FAIL → restore.

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
   `docs/providers.md` / `docs/providers.zh-CN.md` are generated too (by
   `provider_status.table_block()`), and `build_human.py` now calls
   `provider_status.refresh_docs()` so BOTH the 3h sync and the PR check re-render them. They used
   to be refreshed only when someone remembered to run `python scripts/provider_status.py`, so the
   per-provider `Models` counts drifted silently with nothing to catch them (real 2026-09-12:
   committed openrouter 426 / deepseek 5 / mistral 34 / edenai 255 vs data 445 / 6 / 35 / 254).
   `audit.py` check #10 hard-fails a stale page — never hand-edit it, run the generator.
3. After any data change, run `python scripts/validate.py` (needs `pip install jsonschema`).
   It checks schema conformance, index count consistency, and duplicate model ids.
4. When prices change: update the value(s) AND `verified_at`/`updated_at`, then append a
   `changelog.json` entry (`kind: update|add|remove`, `scope: model|plan|provider`, `old`/`new`).
5. Deprecated/retired models stay in the file with `pricing` all `null` and a `notes`
   explaining retirement + replacement model. Never silently delete them.
6. Non-USD providers (CNY etc.): set `currency`/`price_currency` on the provider and explain
   the conversion in `currency_usd_note`.
7. Research-subagent output can be merged automatically:
   `python scripts/migrate/merge_research.py <research.json>` (format contract: `docs/research-contract.md`).

8. **`category` must match the model's KIND, never a default.** `category` is a schema enum
   (`chat | reasoning | embedding | image_gen | video_gen | audio_tts | audio_stt | rerank |
   moderation | ...`). The two aggregator writers used to emit `"reasoning"` or `"chat"` and
   nothing else, so speech / image / embedding rows were published as chat models (real
   2026-09-13: 116 rows across 31 providers — `whisper-large-v3` as chat, `openai/tts-1` as
   chat, `bfl/flux-2-pro` as chat, `baai/bge-m3` as chat, `gpt-oss-safeguard-20b` as chat).
   Classification now runs through the SHARED table `toolbox.CATEGORY_SIGNATURES` +
   `toolbox.category_signature_hint()`, used by BOTH writers and by `audit.py`, so the writer's
   inference and the gate can never drift apart. Precedence: the FIRST matching id marker wins
   (`flux-3-video` -> `video_gen` not `image_gen`; `synthetic-video-detector` -> `moderation`
   not `video_gen`; `wan2.7-image` -> `image_gen` not `video_gen`), then the source's OUTPUT
   modality (`image`/`audio`/`video`) — a model that merely ACCEPTS images is still `chat`.
   `audit.py` warns when a row contradicts its own id; fix the row, never the check.
   **Marker coverage must be complete, not just the families already seen** (round 2,
   2026-09-13): the first pass only caught ids containing a literal `video`/`flux`/`tts`, so the
   writers kept re-defaulting 151 more generator rows (54 video, 97 image) to `chat`/`reasoning`
   on every sync — Google Veo, OpenAI Sora, Kuaishou Kling, ByteDance Seedance, Runway, Luma Ray,
   Alibaba wan/wanx, `t2v|i2v|r2v`, and every `*-image`/`gpt-image`/`imagen` id. The table now
   carries those families too, and `tier0_zai.py` (which appends brand-new official models) uses
   `category_signature_hint()` instead of a hardcoded `"chat"`. When a new generator family
   appears, add its marker AND recategorise the rows in the same change.
   **Round 3 (2026-09-14, found by the §15.1 proactive sweep):** three failure modes a
   "families already seen" pass still leaves behind — (a) a *task* marker nobody encoded (`asr`;
   `stepaudio-2.5-asr` and `qwen3-asr-flash` were chat), (b) a marker that only matches ONE
   spelling of the same name (`stable-diffusion` vs poe's hyphen-less `stablediffusionxl`), and
   (c) a spelled-out synonym (`text-to-speech` known, `text-to-audio` not). Make a marker
   hyphen/separator-OPTIONAL and encode the synonym, then recategorise (13 rows across 6
   providers). Also: a vendor-family marker (`fish-audio`) must be inserted AFTER the more
   specific rule it would otherwise outrank — `fish-audio/transcribe-1` is `audio_stt`, so the
   family's `audio_tts` marker belongs below the `whisper|transcribe|asr` rule; the test
   `test_asr_does_not_steal_the_tts_rows` pins that ordering. Do NOT encode an id whose correct
   bucket is not derivable (`gpt-audio`, `grok-voice-*`, `nemotron-voicechat`, `studiovoice`,
   `elevenlabs-music`: audio_tts vs audio_understanding vs realtime is a judgment call) — that
   just moves the error, so it stays a WARN and is listed in the test as deliberately unclassified.
   **Round 4 (2026-09-14, §15.1 "dead category" sweep):** a category the schema declares but the
   signature table can never PRODUCE is a silent hole -- `music_gen` held ZERO rows repo-wide
   while Google's Lyria family (`lyria-3-clip-preview` / `-pro-preview`) and ElevenLabs Music
   were published as `chat` (Lyria again as `audio_tts` on openrouter). A dead enum value is a
   signal: sweep `Counter(category)` against `schema.modelCategory` and treat a 0 as a missing
   marker. Fixed: `lyria|(^|[/_.-])music([/_.-]|$)` -> `music_gen`, boundary-anchored so
   `gemma-...-musica` / `studiovoice` cannot match, plus `gemini-omni` -> `video_gen` (Gemini
   Omni is a video generation/editing family per the official pricing page); 11 rows
   recategorised across 6 providers. `test_no_row_contradicts_its_id` now enforces it -- it had
   passed before only because the marker was absent (`want` was None).

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
6. The sync changelog and its CHANGELOG headline count **distinct models**, not entries and
   not changed fields. A model can legitimately appear in several entries of one run (a
   per-model pass AND an aggregate pass), so `update_model_prices` appends its id at most
   once and `print_sync_summary` counts the merged/deduped model set — never the per-entry
   sum. Real 2026-09-12 (PR #219): `item_id` repeated each id 3x with `new={"models":6}` for
   2 models, and the headline read "updated 4" while listing 3. Guarded by
   `tests/test_changelog_count_dedupe.py`.
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
  model’s OpenRouter-channel value can jump by a clean 2x between runs. When a review flags such
  a jump, a clean 2x matching a first-party peak/off-peak tier is a timing snapshot, not corruption.
  This **oscillates, it does not settle**. OpenRouter publishes the time windows in
  `pricing.overrides` and returns a different scalar for different run hours, while
  `sync_openrouter.build_model()` reads only `pricing.prompt/completion/input_cache_read`
  and ignores `overrides` — so an affected row flips A -> B -> A -> B on every sync, forever
  (2026-09-12: `tencent/hy3` 0.0825<->0.132, `nvidia/nemotron-3-ultra-550b-a55b` 0.6<->0.625,
  `minimax/minimax-m1` 0.4<->0.55, `minimax/minimax-m2.5` 0.27<->0.3,
  `deepseek/deepseek-v4-flash-vision-exp` 0.22<->0.44). `audit.py` check #8 flags the class as a
  WARN — it now scans ALL of `per_mtok` (input/output/cache_read/cache_write x usd/cny) across the
  recent changelog and fires when a value RETURNS to one it already held (A -> B -> A) within a
  small value set, so it also catches the promo/list churn (e.g. `z-ai/glm-5.3-flash` 0.075
  <-> 0.15) that the old strict A/B test missed; a one-way drift (A -> B -> C) is the separate
  note below. The root fix is writer-side: model `overrides` (store the peak
  tier + an `off_peak` block, or promo/list) instead of persisting whichever tier the run landed
  in. That changes sync value semantics, so it needs human sign-off, unlike a check edit.

- **`off_peak` is a machine-checked DERIVED-price contract, not prose.** The field means
  `off-peak price = per_mtok x multiplier`, with `per_mtok` holding the PEAK (standard) tier and
  `window.peak` defining the hours that are off-peak (everything outside them).
  `toolbox.off_peak_violation()`, called by `audit.py`, hard-FAILs a block that contradicts the
  price it derives -- `multiplier` that is not a genuine discount (`0 < m < 1`; `2.0` is the
  signature of a writer that stored peak/off-peak INVERTED), a window whose `days` are not
  weekday names or whose `utc` entries are not `HH:MM-HH:MM` ranges, or an `off_peak` block with
  no non-zero `per_mtok` to discount -- and WARNs when `multiplier`/`window`/`peak`/`tz` is
  missing. `schema.json` only types the block, so until 2026-09-14 all of those passed validate +
  audit with zero output (verified by injecting them into a scratch copy); guarded by
  `tests/test_off_peak_contract.py`. The general rule: when a new pricing MECHANISM is added,
  encode its invariant as a check -- a schema that only checks shape is not a check.
- **An aggregator snapshot is stale the moment it is taken — re-verify it at review time.** A
  `bot/price-sync-*` PR records the aggregator API's values at run time; by the time it is reviewed
  (up to ~3h later) some values have moved. Re-fetch `https://openrouter.ai/api/v1/models` (and
  models.dev) at review time and compare every changed id: if a value drifted, re-pin the data AND
  the sync's own `changelog.json` entry to the live value before merging. 2026-09-11:
  `moonshotai/kimi-k3` + `~moonshotai/kimi-latest` were ~10% low vs live and `~z-ai/glm-latest`
  ~11% high — all three re-pinned. Drift is not fabrication: resolve it by re-pinning,
  never by blocking the PR.
- **An aggregation source must never write a provider the repo already checks one-hand.**
  `collect_modelsdev` skips a provider when `has_official_collector(pid)` (a dedicated
  `collect/collectors/collect_<pid>.py` exists) OR `verified_recently(pid, now)` (its
  `verified_at` is inside a 26h freshness window). 2026-09-11 incident: the guard used to be an
  **exact UTC-date equality** (`verified_at[:10] == now[:10]`), so it expired at midnight —
  deepseek (verified 09-10T09:39Z) and zhipuai (09-10T21:28Z) were rewritten by the 09-11T00:39Z
  sync to models.dev's own off-peak / expired-promo numbers AND lost their provenance notes.
  Never make this guard depend on a calendar date, and never rely on `verified_at` alone: the
  persist path only refreshes it when a price CHANGES, so it is stale for a stable price.
  Guarded by `tests/test_writer_safety_guard.py::TestFirstPartyGuard`.

- **Official-source verification reads each source's real keys.** `scripts/tools/fetch_official.py`
  must read the key each source actually uses: models.dev `api.json` stores prices under
  `cost` (already USD per 1M tokens) — NOT `pricing`; the OpenRouter API stores per-token
  prices under `pricing` and must be scaled ×1e6. A fetcher that reads `pricing` for a
  models.dev entry silently returns no price forever (the “check that never fires” gap).
  When extending the `SOURCES` registry, verify with `python scripts/tools/fetch_official.py <model> --json`.

- **An aggregator-only provider's CATALOG drifts from the vendor's own `/models` — even when its
  prices are exact.** models.dev / OpenRouter republish prices faithfully, but they keep retired
  models and lag new ones, and `sync_modelsdev` stamps every catalog entry `status: "online"` — so
  a provider fed ONLY by an aggregator (a fetch-less tier1 stub is not a real check) accumulates
  phantom `online` rows and misses live models. Verify membership against the vendor's own live
  catalog, not the aggregator. Real 2026-09-12 (`novita-ai`, models.dev-sourced): of 107 repo rows,
  29 are retired at Novita (all 404 on `https://api.novita.ai/openai/v1/models/<id>`) yet still
  `online`, 4 more carry the wrong id CASE (`sao10K/...` vs the official `sao10k/...`), and 39
  live models are absent from the repo (`zai-org/glm-5.3`, `qwen/qwen3.8-max`, `minimax/minimax-m3`,
  `tencent/hy3`, …). Prices for the 74 overlapping models match Novita's own API exactly — the
  drift is membership/status/casing, NOT price. `python scripts/tools/fetch_official.py novita`
  now queries that first-party catalog (registered 2026-09-12); the write-path reconciliation (a
  first-party collector so a retired model is marked `offline` instead of re-stamped online each
  sync) changes value semantics and needs sign-off.
  **Repaired for novita 2026-09-13 (the data half):** the 29 retired rows are now `status:
  offline` with a provenance note (live-catalog absence + the per-model 404 URL), and the 4
  wrong-case ids were renamed to the vendor's casing. The marking PERSISTS because no writer ever
  emits a per-model `status` for an aggregator-only provider: `collect_modelsdev` supplies
  prices/notes only, and `update_model_prices` writes `status` only when an update carries one —
  so the "needs sign-off" concern covers the still-open half alone (a new model has no row for
  `update_model_prices` to patch, so the 39 live-but-absent models must be SEEDED, and the
  first-party collector is what keeps membership fresh). `fetch_official`'s novita record now
  carries `context_window` / `max_output` / `status` (not just the price) so membership and the
  limit pair are verifiable from the vendor catalog.

- **A model id's CASE is part of its key — a casing change creates a DUPLICATE row, not an update.**
  `update_model_prices()` and the providers' `by_id` maps resolve ids EXACTLY, so when an aggregator
  (or a source that published both at once) emits an id in a new casing, the repo ends up with two
  `status: "online"` rows for ONE logical model — and they drift apart, so a consumer reading either
  id gets a divergent price. `validate.py`'s duplicate-id check was case-SENSITIVE and never fired.
  Real 2026-09-12: edenai `flexai/DeepSeek-V4-Flash-0731` ($0.065/$0.18) vs
  `flexai/deepseek-v4-flash-0731` ($0.03/$0.1), and llmgateway `Qwen3.8-27B` ($0.2/$2, ctx 32K) vs
  `qwen3.8-27b` ($0.42/$3, ctx 1M) — in both, the lowercase id is ABSENT from the declared source
  (`https://models.dev/api.json`) and is a stale ghost; the source-published casing is canonical.
  Fix: keep the source's casing, drop the ghost, and `validate.py` now hard-fails the whole class via
  `toolbox.case_variant_duplicate_ids()`. Regression: `tests/test_duplicate_ids.py`.

- **A doc that tells you to run a `scripts/` path that no longer exists is a BROKEN INSTRUCTION —
  and nothing caught it.** The scripts-layer refactor moved `sync_*` / `migrate_*` into
  `scripts/sync/` and `scripts/migrate/`, but AGENTS.md, README(.zh-CN), CONTRIBUTING(.zh-CN),
  FORMAT(.zh-CN) and docs/{price-types,verification,research-contract}(.zh-CN) kept citing the old
  FLAT `scripts/<file>.py` form — every `python <old path>` line in the docs failed with
  "No such file", including the (re-)annotate command AGENTS.md itself recommends. The broken-LINK
  check only resolves markdown link targets, and these references sit in backticks/prose, so a
  `scripts/` path was never validated. Fix 2026-09-13: the paths are corrected AND `audit.py`
  check #6b hard-fails any prose doc referencing a nonexistent script path (`CHANGELOG*.md` is a
  historical provenance log and is EXCLUDED — never rewrite a path that was true then). Rule:
  when a refactor moves an entry point, grep every doc for the old path in the SAME commit.

- **A check's model-id key must resolve in the provider DB, or the check silently no-ops.**
  `update_model_prices()` skips ids it cannot resolve, so a check that keys its update on a
  renamed/never-seeded id parses the page correctly (parse succeeds, `changed=0`) yet writes
  NOTHING and still looks green — a dead check. Real 2026-09-11: PR #166 renamed the DeepSeek DB
  id `deepseek-v4.1-flash` -> `deepseek-flash` (the official `/models` id) but left the old key in
  `tier0_deepseek.py`'s `COLS`, so the live flash column was never verified and never got its
  note. Guarded deterministically by `tests/test_check_model_id_alignment.py` (a check's `COLS`
  keys AND its fixture-parsed ids must resolve in the provider file), and `price_check.py` now
  emits a report-only `WARN` + `summary.missing_ids` for any collector id absent from the DB —
  which is also how an official model that merely needs seeding gets surfaced (e.g.
  `MiniMax-M2.1-highspeed`, `ministral-14b-latest`, seeded 2026-09-11).

- **A collector must hand `make_result` the `{per_mtok, notes}` contract shape — not a raw
  price dict.** `collect/utils.make_result` reads `info.get("per_mtok")`, so a collector that
  reuses a check's LOW-LEVEL flat parse (`tier1_stepfun.parse_stepfun` /
  `tier1_baidu.parse_qianfan` return `{input, output, cache_read}`) silently emits
  `per_mtok=None` for every model: the collector parses the page fine and writes NOTHING —
  a DEAD collector, the sibling of the dead check above. Real 2026-09-11: `collect_stepfun`
  and `collect_baidu` were both dead this way (the CNY branch was never updated). Fix: wrap
  the flat parse with a check-level `build_updates(parsed, now)` that returns
  `{mid: {"per_mtok": {"input": {"cny": ..}, ...}, "notes": ..}}` (CNY-only vendors MUST carry
  the `cny` key — a scalar is coerced to `{"usd": ...}` by `update_model_prices`, storing ¥ as $).
  `make_result` now RAISES on the shape mismatch, and `tests/test_collector_contract.py` locks it.

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

- **A frozen `last_ok` on an `auto_sync` source is a silent failure.** The non-check aggregation
  sources (`models.dev`, `OpenRouter API`) are NOT check modules, so `scripts/router.py` preserves
  their `sources[]` manifest entries verbatim — nothing refreshed them, and `models.dev` kept
  `last_ok: 2026-08-21` for three weeks with `last_error: null` (stale-but-green). `daily_check.py`
  now refreshes both via `_refresh_manifest_sources`: OpenRouter from `summary["network_ok"]`,
  models.dev from the unified router's `modelsdev` result — a failed OR empty parse (`providers == 0`)
  marks it errored. If you add a non-check source, wire an explicit refresh here or it will freeze.
  `scripts/audit.py` now also flags the whole class generically: any `sources[]` entry with
  `auto_sync: true` and NO `last_error` whose `last_ok` is null/older than 7 days is reported as
  "stale-but-green" (a warning). That guard immediately caught the real leftover: the three
  legacy `official` entries (`DeepSeek/Baidu/Anthropic official pricing`) written by the
  now-orphaned `sync_official.py` froze at `2026-08-21` when the 2026-09-04 collection refactor
  dropped that layer from the daily pipeline (superseded by `scripts/checks/`). They were removed
  from the manifest and their registry entries in `scripts/official_sources.json` set
  `enabled: false` (with a supersession note) so a standalone run can't resurrect them. Rule: a
  source that is no longer refreshed by the pipeline must not stay in the manifest claiming
  `auto_sync: true`; either wire a refresh (above) or prune the entry.
  *Note — `check:*` entries also carry `official: true`; when pruning legacy official sources
  filter on `official and not check`, never `official` alone (filtering on `official` alone
  wiped all 190 check entries in one pass).*

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
   `scripts/migrate/merge_research.py`.

## Quick Commands

```bash
pip install jsonschema
python scripts/sync/sync_openrouter.py --write   # pull OpenRouter catalog (aggregator prices)
python scripts/sync/sync_modelsdev.py --write    # pull models.dev (official-ish list prices)
python scripts/migrate/merge_research.py x.json     # merge subagent research output
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
