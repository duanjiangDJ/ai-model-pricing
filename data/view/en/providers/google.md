# Google

- provider_id: `google`
- Channel: First-party
- API base URL: `https://generativelanguage.googleapis.com/v1beta`
- Homepage: https://ai.google.dev/gemini-api/docs/models
- Pricing page: https://ai.google.dev/gemini-api/docs/pricing
- Currency: USD
- Data updated: 2026-08-22T11:20:52Z
- Verified: 2026-08-22T11:20:52Z

**40** models in total.

| Model | Status | Category | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `deep-research-max-preview-04-2026` | — | reasoning | 131.072K | $2 | $12 | $0.2 | — | —/— | — | models.dev official list price |
| `deep-research-preview-04-2026` | — | reasoning | 131.072K | $2 | $12 | $0.2 | — | —/— | — | models.dev official list price |
| `gemini-2.0-flash` | ❌ offline | chat | 1.04858M | $0.1 | $0.4 | $0.025 | — | $0.05/$0.2 | — | DEPRECATED and shut down 2026-06-01 (migrate to newer models). Input $0.10 te… |
| `gemini-2.5-computer-use-preview-10-2025` | — | reasoning | 131.072K | $1.25 | $10 | — | — | —/— | — | models.dev official list price |
| `gemini-2.5-flash` | — | chat | 1.04858M | $0.3 | $2.5 | $0.03 | — | $0.15/$1.25 | — | Input $0.30 text/image/video, $1.00 audio; cache $0.03 text/image/video, $0.1… |
| `gemini-2.5-flash-image` | — | reasoning | 32.768K | $0.3 | $30 | $0.075 | — | —/— | — | models.dev official list price |
| `gemini-2.5-flash-lite` | — | chat | 1.04858M | $0.1 | $0.4 | $0.01 | — | $0.05/$0.2 | — | Input $0.10 text/image/video, $0.30 audio; cache $0.01 text/image/video, $0.0… |
| `gemini-2.5-flash-preview-tts` | — | chat | 8.192K | $0.5 | $10 | — | — | $0.25/$5 | — | Official ai.google.dev/gemini-api/docs/pricing (USD/1M tokens, standard tier;… |
| `gemini-2.5-pro` | — | chat | 1.04858M | $1.25 | $10 | $0.125 | — | $0.625/$5 | — | Two-tier pricing at 200k prompt tokens. <=200k: input $1.25 / output $10.00 /… |
| `gemini-2.5-pro-preview-tts` | — | chat | 8.192K | $1 | $20 | — | — | $0.5/$10 | — | Official ai.google.dev/gemini-api/docs/pricing (USD/1M tokens, standard tier;… |
| `gemini-3-flash-preview` | ❌ offline | chat | 1.04858M | $0.5 | $3 | $0.05 | — | $0.25/$1.5 | — | Preview model. Input $0.50 text/image/video, $1.00 audio; cache $0.05 text/im… |
| `gemini-3-pro-image` | — | reasoning | 131.072K | $2 | $120 | — | — | —/— | — | models.dev official list price |
| `gemini-3-pro-image-preview` | — | reasoning | 131.072K | $2 | $120 | — | — | —/— | — | models.dev official list price |
| `gemini-3.1-flash-image` | — | reasoning | 65.536K | $0.5 | $60 | — | — | —/— | — | models.dev official list price |
| `gemini-3.1-flash-image-preview` | — | reasoning | 65.536K | $0.5 | $60 | — | — | —/— | — | models.dev official list price |
| `gemini-3.1-flash-lite` | — | reasoning | 1.04858M | $0.25 | $1.5 | $0.025 | — | $0.125/$0.75 | — | Official ai.google.dev/gemini-api/docs/pricing (USD/1M tokens, standard tier;… |
| `gemini-3.1-flash-lite-image` | — | reasoning | 65.536K | $0.25 | $30 | — | — | —/— | — | models.dev official list price |
| `gemini-3.1-flash-lite-preview` | — | reasoning | 1.04858M | $0.25 | $1.5 | $0.025 | — | —/— | — | models.dev official list price |
| `gemini-3.1-flash-live-preview` | — | reasoning | 131.072K | $0.75 | $4.5 | — | — | —/— | — | models.dev official list price |
| `gemini-3.1-flash-tts-preview` | — | reasoning | 8.192K | $1 | $20 | — | — | $0.5/$10 | — | Official ai.google.dev/gemini-api/docs/pricing (USD/1M tokens, standard tier;… |
| `gemini-3.1-pro-preview` | ✅ online | chat | 1.04858M | $2 | $12 | $0.2 | — | $1/$6 | — | Two-tier pricing at 200k prompt tokens. <=200k: input $2.00 / output $12.00 /… |
| `gemini-3.1-pro-preview-customtools` | — | reasoning | 1.04858M | $2 | $12 | $0.2 | — | $1/$6 | — | Official ai.google.dev/gemini-api/docs/pricing (USD/1M tokens, standard tier;… |
| `gemini-3.5-flash` | — | reasoning | 1.04858M | $1.5 | $9 | $0.15 | — | $0.75/$4.5 | — | Official ai.google.dev/gemini-api/docs/pricing (USD/1M tokens, standard tier;… |
| `gemini-3.5-flash-lite` | — | reasoning | 1.04858M | $0.3 | $2.5 | $0.03 | — | $0.15/$1.25 | — | Official ai.google.dev/gemini-api/docs/pricing (USD/1M tokens, standard tier;… |
| `gemini-3.5-live-translate-preview` | — | chat | 16.384K | $3.5 | $21 | — | — | —/— | — | models.dev official list price |
| `gemini-3.6-flash` | — | chat | 1.04858M | $0.75 | $3.75 | $0.075 | — | $0.375/$1.875 | — | Introductory pricing through 2026-12-31: input $0.75 / output $3.75 / cache $… |
| `gemini-3.7-flash` | — | reasoning | 1.04858M | $0.75 | $3.75 | $0.075 | — | $0.375/$1.875 | — | Official ai.google.dev/gemini-api/docs/pricing (USD/1M tokens, standard tier;… |
| `gemini-embedding-001` | — | embedding | — | $0.15 | $0 | — | — | $0.075/— | — | Text-only embedding model (gemini-embedding-001). Input billed at $0.15/1M to… |
| `gemini-embedding-2` | — | embedding | — | $0.2 | $0 | — | — | $0.1/— | — | Multimodal embedding model (gemini-embedding-2, endpoint gemini-embedding-2-p… |
| `gemini-flash-latest` | — | reasoning | 1.04858M | $0.75 | $3.75 | $0.075 | — | —/— | — | models.dev official list price |
| `gemini-flash-lite-latest` | — | reasoning | 1.04858M | $0.3 | $2.5 | $0.03 | — | —/— | — | models.dev official list price |
| `gemini-omni-flash-preview` | — | reasoning | 131.072K | $1.5 | $17.5 | — | — | —/— | — | models.dev official list price |
| `gemini-robotics-er-1.6-preview` | — | reasoning | 131.072K | $1 | $5 | — | — | $0.5/$2.5 | — | Official ai.google.dev/gemini-api/docs/pricing (USD/1M tokens, standard tier;… |
| `gemma-4-26b-a4b-it` | — | reasoning | 262.144K | — | — | — | — | —/— | — | models.dev official list price |
| `gemma-4-31b-it` | — | reasoning | 262.144K | — | — | — | — | —/— | — | models.dev official list price |
| `lyria-3-clip-preview` | — | chat | 1.04858M | $0 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `lyria-3-pro-preview` | — | chat | 1.04858M | $0 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `veo-3.1-fast-generate-preview` | — | chat | 480 | — | — | — | — | —/— | — | models.dev official list price |
| `veo-3.1-generate-preview` | — | chat | 480 | — | — | — | — | —/— | — | models.dev official list price |
| `veo-3.1-lite-generate-preview` | — | chat | 480 | — | — | — | — | —/— | — | models.dev official list price |
