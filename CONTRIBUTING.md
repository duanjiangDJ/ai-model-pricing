> **Language: English (en)** — This document is written in en only.
# Contributing

Thanks for helping make the pricing database better! This document explains **what you can
contribute** and **how to contribute**. All changes go through **pull requests** checked by
`.github/workflows/pr-check.yml` (schema validation, repository audit, generated-page
consistency, version/CHANGELOG enforcement).

## What you can contribute

| # | Contribution type | Examples | Difficulty |
|---|---|---|---|
| 1 | **Fix a price** | wrong/outdated price, missing cache/batch field | ★☆☆ |
| 2 | **Add a plan** | new subscription/coding plan with official URL | ★☆☆ |
| 3 | **Mark model status** | retire/deprecate a model with official evidence | ★☆☆ |
| 4 | **Add a new provider** | follow `docs/research-contract.md`, use `merge_research.py` | ★★☆ |
| 5 | **New acquisition strategy** | a new official page that can be parsed, a new API source | ★★☆ |
| 6 | **Write a provider check** | a `scripts/checks/tierN_<provider>.py` module (see below) | ★★★ |
| 7 | **Scripts & tooling** | router, toolbox, sync/validate/audit improvements | ★★★ |
| 8 | **Docs & translation** | docs, bilingual sync, README/AGENTS/CONTRIBUTING | ★☆☆ |
| 9 | **Issue triage & research** | verify reported errors, re-verify stale providers | ★☆☆ |

## How to contribute

### 1. Fix a price / add a plan (easiest)

1. Edit `data/feed/providers/<id>.json` (model pricing/status) or `data/feed/plans.json`.
2. Rules:
   - prices must come from official pages/APIs; put the source URL in `notes` and refresh `verified_at`;
   - unknown values are `null` (never 0, never invented); `0` means genuinely free;
   - subscription-included models: `per_mtok: null` + note "included in <plan>", never 0;
   - deprecated/retired models: `"status": "deprecated" | "retired" | "superseded"`, keep as historical entries;
   - notes in English.
3. Bump the version (pricing data = **content** update):
   ```bash
   python scripts/bump_version.py --content --message "fix openai gpt-5.6-terra price"
   ```
4. Regenerate pages and validate:
   ```bash
   python scripts/build_human.py && python scripts/validate.py && python scripts/audit.py
   ```
5. Commit + open a PR. pr-check must pass.

### 2. Add a new provider

1. Pick the roadmap tier (see `docs/optimization-roadmap.md`).
2. Collect official pricing data (official page URL, per-MTok prices, plans).
3. Create `data/feed/providers/<id>.json` following `data/feed/schema.json`
   (include `api_base_url`!).
4. If you researched it via a subagent, output per `docs/research-contract.md` and merge:
   ```bash
   python scripts/merge_research.py <research.json>
   ```
5. If the provider's official page can be parsed, add a check module (see below) so it
   stays fresh automatically.
6. Version bump (feature for new provider infra, content for the prices), rebuild, PR.

### 3. Write a provider check (keeps prices fresh daily)

Every provider check lives in `scripts/checks/tierN_<provider>.py` and exposes:

```python
TIER = 0              # roadmap tier
PROVIDER_ID = "openai"
URL = "https://platform.openai.com/docs/pricing"

def run(ctx) -> dict:  # ctx: {"now": iso, "dry_run": bool}
    # fetch official page (toolbox.http_get / wayback helpers), parse, then:
    changed = toolbox.update_model_prices(provider, parsed, ctx["now"], URL)
    return {"changed": len(changed), "detail": "..."}
```

The router (`python scripts/router.py`) discovers all checks, runs them in tier order,
isolates failures per provider, and records per-check status in `data/meta/manifest.json`.
The daily check calls the router every day. See existing examples:
`scripts/checks/tier0_deepseek.py` (static page), `tier0_openai.py` (wayback),
`tier1_tencent.py` (verified constants).

Tooling: `scripts/toolbox.py` holds shared utilities (http_get, to_text, JSON I/O,
changelog, index/manifest, dedup helpers). Don't duplicate them in checks.

### 4. Scripts & tooling

- Keep everything stdlib + `jsonschema` only.
- New shared helpers go into `toolbox.py`; new per-provider logic goes into `checks/`.
- Preserve the daily pipeline order: official (router) → models.dev → OpenRouter.

### 5. Docs & translation

- Every prose document needs an English default + a `*.zh-CN.md` version, each with the
  `> **Language:**` banner as the first line.
- Keep `CHANGELOG.md` and `CHANGELOG.zh-CN.md` in sync (same version sections).

## PR checklist (pr-check enforces most of this)

- [ ] `python scripts/validate.py` passes
- [ ] `python scripts/audit.py` passes (api_base_url completeness, no same-endpoint duplicates)
- [ ] `python scripts/build_human.py` regenerated and committed
- [ ] `VERSION` bumped + `CHANGELOG.md` / `CHANGELOG.zh-CN.md` have the `## <version>` section
- [ ] Unknown prices use `null`; subscription-included models are `null` + note; free = 0 + "free" note
- [ ] `api_base_url` present (null only for subscription products)
- [ ] Source URL included in `notes`

## Issue templates

- Data error: `.github/ISSUE_TEMPLATE/data-error.md` — include provider/model id, expected
  value, official source URL.
- Feature/source suggestion: `.github/ISSUE_TEMPLATE/feature-request.md`.

## Where to start

Pick any provider marked ⬜ in `docs/optimization-roadmap.md` (Tier 0/1 first) and run its
checklist: official page → billing mode → model list/status → notes → human page → version bump.
Or pick an open issue labeled `good first issue`.


---

## Related docs

- [README](README.md) — overview & exact stats
- [AGENTS.md](AGENTS.md) — guide for AI agents
- [FORMAT.md](FORMAT.md) — machine format spec
- [docs/providers.md](docs/providers.md) — provider landscape & status
- [docs/price-types.md](docs/price-types.md) — price types
- [docs/verification.md](docs/verification.md) — verification model
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute
