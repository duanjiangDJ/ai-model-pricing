> **Language: English (en)** — This document is written in en only.
# Contributing

Thanks for helping make the pricing database better! All changes go through **pull requests**
reviewed by the automated checks in `.github/workflows/pr-check.yml`:
1. `python scripts/validate.py` — JSON Schema + cross-consistency checks;
2. `python scripts/build_human.py` + `git diff --exit-code` — generated pages must be regenerated;
3. version consistency — `VERSION` == `schema.json#version` == `index.json#schema_version`.

Direct pushes to `main` are blocked by branch protection.

## Report an error (issue)

Open an issue with:
- provider id + model id (e.g. `openai` / `gpt-5.6-terra`), or plan id;
- the **expected price** and the **official pricing-page URL** you verified it from;
- (optional) a suggested fix.

## Request a feature / new source (issue)

- new provider, new billing mode, new data source or acquisition strategy — describe the
  source URL and how to fetch it (static page? API? JS-rendered? needs a browser?).

## Fix data (PR)

1. Edit `data/machine/providers/<id>.json` or `data/machine/plans.json`.
2. Rules:
   - prices must come from official pages/APIs; record `verified_at` (UTC) and the source URL in `notes`;
   - unknown values are `null` (never 0, never invented); `0` means genuinely free;
   - subscription-included models: `per_mtok` = `null` + note "included in <plan>", never 0;
   - deprecated/retired models get `"status": "deprecated" | "retired" | "superseded"` and stay as historical entries;
   - append a `data/meta/changelog.json` entry (`kind: update|add|remove`, `old`/`new`);
   - if it's a pricing data change, bump the **content** segment of the version (see `CHANGELOG.md`);
     other changes bump the **feature** segment — update `VERSION`, `schema.json#version`,
     `index.json#schema_version` all together.
3. Run `python scripts/validate.py`, then `python scripts/build_human.py` (regenerates `data/human/`).
4. Commit and open a PR; the checks must pass.

## Improve scripts/docs (PR)

- Scripts are stdlib + `jsonschema` only. Keep `null` semantics, keep the daily-check pipeline
  (official → models.dev → OpenRouter) intact.
- All prose documents must have an English default + a `*.zh-CN.md` version, each with the
  `> **Language:**` banner on the first line.

## Style

- Provider files: `provider_id` = stable kebab-case; model `id` = the official API id when known.
- Notes in English by default; Chinese notes carry a `[zh]` marker.
- Keep generated files (`data/human/`, `index.json`, `changelog.json`, `manifest.json`) in sync
  by running the generators — never hand-edit them.
