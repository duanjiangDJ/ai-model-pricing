> **Language: English (en)** — This document is written in en only.

# Price Types & Units (price-types)

> This document defines the **precise definition** of every billing type currently supported by the
> database and serves as the baseline for data collection and machine reading.
> All prices default to **USD** (declared by the `currency` field in `index.json`; non-USD entries
> must carry a `currency` override field).
>
> **Billing modes are not added speculatively.** Fields exist in `schema.json` only when backed by
> real data. To add a new mode, follow the procedure in AGENTS.md ("To add a billing mode back").

## 0. billing_model — the per-model billing classifier (required)

Every model carries a `billing_model` array describing **how it is billed**. One model can have
several (e.g. Gemini models have a free tier AND pay-per-token pricing: `["free", "pay_per_token"]`).

| Value | Meaning |
|---|---|
| `pay_per_token` | Per-token API pricing (`per_mtok`, incl. cache & batch discounts) |
| `pay_per_image` | Billed per generated image (`per_image` tiers) |
| `subscription_included` | Included in a subscription / coding plan (per_mtok = null; see plans.json) |
| `credits` | Points/credit-based billing (reserved; no data yet) |
| `free` | Truly free (per_mtok = 0) |
| `unknown` | Pricing not yet determined (needs human review; flagged by audit) |

Annotation: `scripts/annotate_billing.py` (auto-classify + provider-context fallback), then
`scripts/audit.py` verifies consistency (e.g. per_mtok > 0 must imply `pay_per_token`).

## 1. per_mtok — per million tokens

- **Definition**: `input` = input token unit price (USD/1M tokens); `output` = output token unit price.
- A `per_mtok` inside the `pricing` object of a model entry must contain at least `input` and `output`.
- Different context tiers of the same model (e.g., OpenAI 4M context) are distinguished with separate `id` entries.
- **Who uses it**: nearly all text LLMs (OpenAI, Anthropic, Google, xAI, Mistral, DeepSeek, Qwen, GLM, Kimi, Doubao, hosting platforms, aggregators).

## 2. cache_read / cache_write — cache read/write (USD/1M tokens)

- `cache_read`: unit price of input tokens that hit the cache (OpenAI/Anthropic/DeepSeek etc. usually 10%–25% of the list price).
- `cache_write`: unit price of input tokens written to cache (OpenAI: same as normal input; Anthropic: 1.25× the input price).
- Vendors that don't support it fill `null`, never 0.

## 3. batch — batch discount (USD/1M tokens)

- OpenAI/Anthropic/Google etc. offer Batch APIs, usually 50% of the synchronous price.
- `batch.input` / `batch.output`; fill `null` if there is no batch offering.

## 4. per_image — per image

- Image generation models (DALL·E, Imagen, FLUX via API, Novita etc.) are priced per image, possibly tiered by resolution/quality.
- Tiers use the `tiers` array: `[{name: "1024x1024", price: 0.04}]`.
- Models billed this way carry `billing_model: ["pay_per_image"]`.

## 5. promo — temporary discounts

- When a vendor runs a limited-time discount (e.g. Z.ai GLM-5.3-Flash 50% off until 2026-09-09):
  `per_mtok` holds the **current discounted price**, and `promo` records the pre-promo price + expiry:
  `promo: {list_price: {input, output, cache_read}, ends_at: "2026-09-09T16:00:00Z"}`.
- `ends_at` is UTC ISO. When the promo expires the data must be updated to the list price and `promo` removed.

## 6. subscription — subscription / coding-tool plans (plans.json)

- Consumer and coding-tool subscriptions live in `plans.json`, NOT as model prices.
- Fields: `price_usd`, `billing: monthly|yearly`, `limits` (usage-cap description), `includes` (what's included),
  and `pricing_model` (flat_monthly / flat_yearly / per_seat_monthly / per_seat_yearly / credits / free / custom).
- Annual billing is recorded as the **total yearly price** (`price_usd` + `billing: yearly`), not converted to a monthly price, to avoid precision loss.
- Models included in a plan have `per_mtok` = null + `billing_model: ["subscription_included"]` + a note naming the plan.

---

## Price collection rules (must be followed when collecting)

## 7. off_peak — time-of-day (peak / off-peak) pricing

When a vendor prices by hour of day (e.g. DeepSeek), the `pricing` object records the mechanism
structurally in an `off_peak` field instead of as prose in `notes`:

```json
"pricing": {
  "per_mtok": { "input": {...}, "output": {...} },      // = PEAK (standard) tier
  "off_peak": {
    "multiplier": 0.5,                                   // off-peak price = per_mtok x multiplier
    "window": {
      "peak": { "days": ["mon","tue","wed","thu","fri"], "utc": ["01:00-04:00","06:00-10:00"] },
      "tz": "UTC",
      "note": "All other hours are off-peak."
    }
  }
}
```

- `per_mtok` always holds the **peak (standard)** tier.
- `off_peak.multiplier` : off-peak price = `per_mtok` x `multiplier` (0.5 = 50% of peak). No redundant
  price copy is stored — off-peak is fully machine-derivable.
- `off_peak.window.peak` : the peak window (`days` + UTC hour ranges). All hours outside it are
  off-peak. Vendors with no time-of-day pricing simply omit `off_peak`.

---

1. **Prices always come from pricing pages / official APIs / official docs** (use the official **English/USD** page when one exists —
   e.g. DeepSeek `quick_start/pricing` EN, Baidu Qianfan INT'L), and every record carries `source_url` and `verified_at` (ISO8601 UTC).
   Never copy CNY amounts into a USD-declared file; if a vendor only publishes CNY prices, set `currency: "CNY"` and explain in `currency_usd_note`.
2. **The same model has different prices across channels (first-party vs hosted vs aggregator)**: record them in separate provider files without overwriting each other; aggregator prices such as OpenRouter are "resale prices" listed alongside official prices, distinguished by the `channel` field (`first_party` / `cloud` / `hosted` / `aggregator` / `reseller` / `subscription`).
3. **Missing data** uses `null`; **not applicable** uses `null` + `notes` explanation; **never use 0 for missing**.
4. Price changes: the daily check script diffs against the previous values; a change > 5× relative is treated as a parsing error and skipped with a warning (surge guard). All changes are written to `changelog.json`.
5. Subscription plan prices follow the official pricing pages; the daily check generates a "needs manual verification" list for plans not verified for more than 30 days.
6. Every model must have a `billing_model`; run `scripts/annotate_billing.py` after bulk imports and let `scripts/audit.py` verify.

---

## Related docs

- [README](../README.md) — overview & exact stats
- [AGENTS.md](../AGENTS.md) — guide for AI agents
- [FORMAT.md](../FORMAT.md) — machine format spec
- [providers.md](providers.md) — provider landscape & status
- [verification.md](verification.md) — verification model
- [CONTRIBUTING.md](../CONTRIBUTING.md) — how to contribute
