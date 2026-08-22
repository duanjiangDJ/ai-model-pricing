> **Language: English (en)** — This document is written in en only.
# Price Types & Units (price-types)

> This document defines the **precise definition** of every billing type and serves as the baseline for data collection and machine reading. The enum values are defined as
> the `priceType` / `planBilling` enums in `data/machine/schema.json`; this document is the human-readable explanation.
> All prices default to **USD** (declared by the `currency` field in `index.json`; non-USD entries must carry a `currency` override field).

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

## 5. per_audio_second — per audio second
- TTS/STT/audio understanding (ElevenLabs, Deepgram, AssemblyAI, Whisper, Realtime API audio).
- The semantics of `input` (recognition/understanding) and `output` (synthesis) differ by model purpose; note it in the document.

## 6. per_character — per character
- Some TTS and translation APIs bill per character (e.g., legacy TTS, some relay stations). A "per 1K characters" convention is common; the unit field `unit` records `per_1k_char` or `per_char`.

## 7. per_request — per request/call
- Image APIs, some aggregators, and legacy paid APIs (e.g., some embedding proxies) bill per call.
- Unit: `USD/request`.

## 8. credits — points/credit billing
- Poe, Hugging Face Pro, domestic top-up platforms (e.g., "1 CNY = 100 points", models deducted per point/request or points/MTok).
- Structure: `credits: { topup: {amount_usd, credits}, model_rate: {per_mtok: <credits>} | {per_request: <credits>} }`.
- When it cannot be converted to USD/MTok, the original points definition must be kept with `convertible: false`.

## 9. gpu_second / gpu_hour — GPU second/hour
- Replicate, Modal, Baseten, RunPod etc. bill by GPU spec and time (e.g., `A100-40GB: $0.00115/s`).
- Structure: `gpu: [{sku: "A100-40GB", price_per_second: 0.00115}]`.

## 10. neuron_second — neuron second
- Cloudflare Workers AI billing unit (per 1M neuron seconds = $0.011). Keep the original definition.

## 11. subscription_monthly / subscription_yearly — subscriptions
- Consumer and coding-tool subscriptions. Fields: `price_usd`, `billing: monthly|yearly`, `limits` (usage-cap description), `includes` (what's included).
- Annual billing is recorded as the **total yearly price** (`price_usd` + `billing: yearly`), not converted to a monthly price, to avoid precision loss.

## 12. free_tier — free tier
- Record the free tier's limits (e.g., Gemini: 15 RPM/1500 RPD; Copilot Free: 50 requests/month).
- Structure: `{requests_per_month, rpm, rpd, notes}`; fill `null` if unlimited.

## 13. finetune — finetuning
- Billed per training token (input/output training prices), recorded separately from hosting: `training.input` / `training.output` / `hosting`.

## 14. provisioned — provisioned capacity (enterprise)
- OpenAI/Azure provisioned throughput billed per hour. Mostly contract prices; the field may be filled with `"contact_sales"`.

---

## Price collection rules (must be followed when collecting)

1. **Prices always come from pricing pages / official APIs / official docs**, and every record carries `source_url` and `verified_at` (ISO8601 UTC).
2. **The same model has different prices across channels (first-party vs hosted vs aggregator)**: record them in separate provider files without overwriting each other; aggregator prices such as OpenRouter are "resale prices" listed alongside official prices, distinguished by the `channel` field (`first_party` / `cloud` / `hosted` / `aggregator` / `reseller`).
3. **Missing data** uses `null`; **not applicable** uses `null` + `notes` explanation; **never use 0 for missing**.
4. Price changes: the daily check script compares against the previous `verified_at`; if a change exceeds 1% or any price field changes, write `changelog.json` and generate a report.
5. Subscription plan prices follow the official pricing pages; the daily check generates a "needs manual verification" list for plans not verified for more than 30 days.


---

## Related docs

- [README](README.md) — overview & exact stats
- [AGENTS.md](AGENTS.md) — guide for AI agents
- [FORMAT.md](FORMAT.md) — machine format spec
- [docs/providers.md](docs/providers.md) — provider landscape & status
- [docs/price-types.md](docs/price-types.md) — price types
- [docs/verification.md](docs/verification.md) — verification model
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute
