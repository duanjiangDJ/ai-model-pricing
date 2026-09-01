# NEAR AI Cloud

- provider_id: `nearai`
- Channel: Inference host
- API base URL: `https://cloud-api.near.ai/v1`
- Homepage: https://docs.near.ai/
- Pricing page: https://docs.near.ai/
- Currency: USD
- Data updated: 2026-09-01T09:18:24Z
- Verified: 2026-09-01T09:18:24Z

**37** models in total.

| Model | Status | Category | Billing | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `Qwen/Qwen3-30B-A3B-Instruct-2507` | — | chat | per-token | 262.144K | $0.15 | $0.55 | — | — | —/— | — | models.dev official list price |
| `Qwen/Qwen3-Embedding-0.6B` | — | embedding | per-token + free | 40.96K | $0.01 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `Qwen/Qwen3-Reranker-0.6B` | — | rerank | per-token | 40.96K | $0.01 | $0.01 | — | — | —/— | — | models.dev official list price |
| `Qwen/Qwen3-VL-30B-A3B-Instruct` | — | chat | per-token | 256K | $0.15 | $0.55 | — | — | —/— | — | models.dev official list price |
| `Qwen/Qwen3.5-122B-A10B` | — | reasoning | per-token | 131.072K | $0.4 | $3.2 | — | — | —/— | — | models.dev official list price |
| `Qwen/Qwen3.6-35B-A3B-FP8` | — | reasoning | per-token | 262.144K | $0.17 | $1.1 | $0.056 | — | —/— | — | models.dev official list price |
| `anthropic/claude-haiku-4-5` | — | reasoning | per-token | 200K | $1 | $5 | $0.1 | — | —/— | — | models.dev official list price |
| `anthropic/claude-opus-4-6` | — | reasoning | per-token | 200K | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `anthropic/claude-opus-4-7` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `anthropic/claude-sonnet-4-5` | — | reasoning | per-token | 200K | $3 | $15.5 | $0.3 | — | —/— | — | models.dev official list price |
| `anthropic/claude-sonnet-4-6` | — | reasoning | per-token | 1M | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `black-forest-labs/FLUX.2-klein-4B` | — | chat | per-token | 128K | $1 | $1 | — | — | —/— | — | models.dev official list price |
| `google/gemini-2.5-flash` | — | reasoning | per-token | 1.04858M | $0.3 | $2.5 | $0.03 | — | —/— | — | models.dev official list price |
| `google/gemini-2.5-flash-lite` | — | reasoning | per-token | 1.04858M | $0.1 | $0.4 | $0.01 | — | —/— | — | models.dev official list price |
| `google/gemini-2.5-pro` | — | reasoning | per-token | 1.04858M | $1.25 | $10 | $0.125 | — | —/— | — | models.dev official list price |
| `google/gemini-3-pro` | — | reasoning | per-token + free | 1.04858M | $1.25 | $15 | $0 | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `google/gemini-3.1-flash-lite` | — | reasoning | per-token | 1.04858M | $0.25 | $1.5 | $0.025 | — | —/— | — | models.dev official list price |
| `google/gemini-3.5-flash` | — | reasoning | per-token | 1.04858M | $1.5 | $9 | $0.15 | — | —/— | — | models.dev official list price |
| `google/gemma-4-31B-it` | — | reasoning | per-token | 262.144K | $0.13 | $0.4 | $0.026 | — | —/— | — | models.dev official list price |
| `openai/gpt-4.1` | — | chat | per-token | 1.04758M | $2 | $8 | $0.5 | — | —/— | — | models.dev official list price |
| `openai/gpt-4.1-mini` | — | chat | per-token | 1.04758M | $0.4 | $1.6 | $0.1 | — | —/— | — | models.dev official list price |
| `openai/gpt-4.1-nano` | — | chat | per-token | 1.04758M | $0.1 | $0.4 | $0.025 | — | —/— | — | models.dev official list price |
| `openai/gpt-5` | — | reasoning | per-token | 400K | $1.25 | $10 | $0.125 | — | —/— | — | models.dev official list price |
| `openai/gpt-5-mini` | — | reasoning | per-token | 400K | $0.25 | $2 | $0.025 | — | —/— | — | models.dev official list price |
| `openai/gpt-5-nano` | — | reasoning | per-token | 400K | $0.05 | $0.4 | $0.005 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.1` | — | reasoning | per-token | 400K | $1.25 | $10 | $0.125 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.2` | — | reasoning | per-token | 400K | $1.8 | $15.5 | $0.18 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.4` | — | reasoning | per-token | 1.05M | $2.5 | $15 | $0.25 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.4-mini` | — | reasoning | per-token | 400K | $0.75 | $4.5 | $0.075 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.4-nano` | — | reasoning | per-token | 400K | $0.2 | $1.25 | $0.02 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.5` | — | reasoning | per-token | 1.05M | $5 | $30 | $0.5 | — | —/— | — | models.dev official list price |
| `openai/gpt-oss-120b` | — | reasoning | per-token | 131K | $0.15 | $0.55 | — | — | —/— | — | models.dev official list price |
| `openai/o3` | — | reasoning | per-token | 200K | $2 | $8 | $0.5 | — | —/— | — | models.dev official list price |
| `openai/o3-mini` | — | reasoning | per-token | 200K | $1.1 | $4.4 | $0.55 | — | —/— | — | models.dev official list price |
| `openai/o4-mini` | — | reasoning | per-token | 200K | $1.1 | $4.4 | $0.275 | — | —/— | — | models.dev official list price |
| `openai/whisper-large-v3` | — | chat | per-token + free | 448 | $0.01 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `zai-org/GLM-5.1-FP8` | — | reasoning | per-token | 202.752K | $0.85 | $3.3 | — | — | —/— | — | models.dev official list price |
