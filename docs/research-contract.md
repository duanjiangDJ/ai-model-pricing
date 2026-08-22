> **Language: English (en)** — This document is written in en only.
# Research Subagent Contract (research-contract)

> The repository's "human-verified" data is collected in bulk by **research subagents**. This document defines the input requirements and output format for subagents,
> guaranteeing that the output can be merged directly into the repository by `scripts/merge_research.py`.

## Output format (subagents must return)

A single JSON object (**not** wrapped in a Markdown code block — output raw JSON text):

```json
{
  "providers": [
    {
      "provider_id": "openai",
      "name": "OpenAI",
      "channel": "first_party",          // first_party | cloud | hosted | aggregator | reseller
      "category": "ai_vendor",           // ai_vendor | cloud_platform | inference_host | aggregator | reseller
      "region": "us",                    // global | cn | us | eu | other
      "homepage": "https://openai.com",
      "pricing_page": "https://platform.openai.com/docs/pricing",
      "currency": "USD",                 // default USD; domestic vendors use CNY and add currency_usd_note
      "verified_at": "2026-08-21T00:00:00Z",
      "models": [
        {
          "id": "gpt-4o",
          "name": "GPT-4o",
          "category": "chat",            // chat | reasoning | embedding | image_gen | video_gen | audio_tts | audio_stt | realtime | code ...
          "context_window": 128000,
          "max_output": 16384,
          "pricing": {
            "per_mtok": {"input": 2.5, "output": 10.0, "cache_read": 1.25, "cache_write": 2.5},
            "batch": {"input": 1.25, "output": 5.0},
            "per_image": [{"name": "1024x1024", "price": 0.04}],
            "per_audio_second": null,
            "per_request": null,
            "credits": null
          },
          "notes": "any definitions that need explanation, e.g. tiered pricing, promo periods, retirement status"
        }
      ],
      "plans": [
        {
          "id": "openai-chatgpt-plus",
          "product": "ChatGPT",
          "plan": "Plus",
          "category": "consumer",        // consumer | coding | team | enterprise | student | api_credits | free
          "billing": "monthly",          // monthly | yearly | one_time
          "price_usd": 20,
          "limits": "usage-cap description",
          "includes": ["what's included"],
          "url": "https://openai.com/chatgpt/pricing/",
          "verified_at": "2026-08-21T00:00:00Z"
        }
      ]
    }
  ],
  "sources": ["https://official-pricing-page", "https://secondary-source"]
}
```

## Hard rules

1. **Only fill in numbers you can confirm**; when unsure fill `null`, never fabricate; `0` means free only.
2. **At least one secondary source** for cross-verification (official announcements, review sites, third-party comparison sites).
3. `verified_at` uses the **actual research date** (don't use stale dates from the task description).
4. Retired/removed models keep their entries, `pricing` all `null`, with `notes` stating the retirement time and replacement model.
5. Prices with promos/tiers/dual tiers (e.g., Gemini ≤200K / >200K) are fully described in `notes`; the main fields carry the standard tier.
6. Non-USD pricing (domestic vendors) adds `"price_currency": "CNY"` and `"currency_usd_note"` at the provider top level.
7. Append a line `SOURCES: url1, url2, ...` at the end of the output.

## Consumers

`scripts/merge_research.py <research.json>`:
- providers merged by `provider_id` (research data overwrites the price and metadata of models with the same id, keeping models.dev-exclusive models);
- plans upserted into `data/feed/plans.json` by `id`;
- `index.json` counts refreshed automatically and changelog written.
