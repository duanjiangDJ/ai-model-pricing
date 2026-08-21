> **Language: English (en)** — This document is written in en only.
# Official-Price Re-verification with Ego (Lite) Browser

> Tier-A data collection for this repo: **official pricing pages, read by an AI agent
> through the [ego-lite](https://github.com/citrolabs/ego-lite) browser** (MIT, by CitroLabs).
> ego-lite gives agents a shared browser whose high-quality page **Snapshot** can see
> JS-rendered pricing tables that plain HTTP fetches cannot (OpenAI, Anthropic, Google…).

## Why this layer exists

`sync_official.py` (CI, daily) directly fetches what it can:
- **Static pages** (DeepSeek, Baidu Qianfan, Anthropic SSR): parsed in-repo, fully automatic.
- **JS-rendered pages** (OpenAI, Google): best-effort via Wayback Machine snapshots — these
  lag by days and can be unreliable (redirects, binary captures).

ego-lite closes the gap: an agent opens the *live* pricing page and reads the rendered
table. This is the highest-trust tier (official page, current content, human/agent check).

## Prerequisites

- macOS with [ego lite installed](https://github.com/citrolabs/ego-lite) (Windows/Linux on roadmap).
- The `ego-browser` skill added to your agent:
  ```bash
  npx skills add citrolabs/ego-lite
  ```
  or let your agent set it up: "Set up ego lite for me: https://github.com/citrolabs/ego-lite".

## Re-verification workflow (one provider)

1. Trigger: `reports/stale-plans.md` or a daily-check issue, or any provider whose
   `verified_at` is older than 30 days.
2. Ask your agent (Claude Code / Codex / Cursor / DSH agent):
   > Use ego-browser to open `<official pricing page>` for `<provider>`. Read the current
   > per-MTok prices for models: `<list>`. Compare with `data/machine/providers/<id>.json`
   > and report a diff table with your source URL.
3. Agent drives ego-browser (snapshot → scroll → snapshot), extracts the rendered prices.
4. Write the result as a research-contract JSON (see `docs/research-contract.md`) into
   `pricing_research/<id>_pricing.json`, then:
   ```bash
   python scripts/merge_research.py pricing_research/<id>_pricing.json
   python scripts/validate.py && python scripts/build_human.py
   ```
5. Commit with the official page URL in the message.

## Providers to re-verify with ego-lite (current gaps)

| Provider | Official page | Why ego-lite is the right tool |
|---|---|---|
| OpenAI | https://platform.openai.com/docs/pricing | fully JS-rendered; wayback lags |
| Google | https://ai.google.dev/gemini-api/docs/pricing | nested promo tables; parser disabled |
| xAI | https://docs.x.ai/developers/pricing | JS-rendered |
| Mistral / Cohere / others | vendor pricing pages | JS-rendered, low priority |

## Rules

- Prices must come from the rendered official page; record the URL and `verified_at`.
- Do **not** trust ego-browser snapshots of third-party aggregator pages for Tier-A data.
- After merging, the daily check will protect the provider from models.dev overwrites
  (it skips providers whose `verified_at` is today).
