# Azure

- provider_id: `azure`
- Channel: Inference host
- API base URL: `https://{resource}.openai.azure.com`
- Homepage: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
- Pricing page: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
- Currency: USD
- Data updated: 2026-08-28T08:54:00Z
- Verified: 2026-08-28T05:09:26Z

**84** models in total.

| Model | Status | Category | Billing | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `claude-fable-5` | — | reasoning | per-token | 1M | $10 | $50 | $1 | — | —/— | — | models.dev official list price |
| `claude-haiku-4-5` | — | reasoning | per-token | 200K | $1 | $5 | $0.1 | — | —/— | — | models.dev official list price |
| `claude-mythos-5` | — | reasoning | per-token | 1M | $10 | $50 | $1 | — | —/— | — | models.dev official list price |
| `claude-opus-4-1` | — | reasoning | per-token | 200K | $15 | $75 | $1.5 | — | —/— | — | models.dev official list price |
| `claude-opus-4-5` | — | reasoning | per-token | 200K | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `claude-opus-4-6` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `claude-opus-4-7` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `claude-opus-4-8` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `claude-opus-5` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `claude-sonnet-4-5` | — | reasoning | per-token | 200K | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `claude-sonnet-4-6` | — | reasoning | per-token | 1M | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `claude-sonnet-5` | — | reasoning | per-token | 1M | $2 | $10 | $0.2 | — | —/— | — | models.dev official list price |
| `codestral-2501` | — | chat | per-token | 256K | $0.3 | $0.9 | — | — | —/— | — | models.dev official list price |
| `codex-mini` | — | reasoning | per-token | 200K | $1.5 | $6 | $0.375 | — | —/— | — | models.dev official list price |
| `cohere-command-a` | — | reasoning | per-token | 131.072K | $2.5 | $10 | — | — | —/— | — | models.dev official list price |
| `cohere-embed-v-4-0` | — | embedding | per-token + free | 128K | $0.12 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `cohere-embed-v3-english` | — | embedding | per-token + free | 512 | $0.1 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `cohere-embed-v3-multilingual` | — | embedding | per-token + free | 512 | $0.1 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `deepseek-r1` | — | reasoning | per-token | 163.84K | $1.35 | $5.4 | — | — | —/— | — | models.dev official list price |
| `deepseek-v3.2` | — | reasoning | per-token | 128K | $0.58 | $1.68 | — | — | —/— | — | models.dev official list price |
| `deepseek-v3.2-speciale` | — | reasoning | per-token | 128K | $0.58 | $1.68 | — | — | —/— | — | models.dev official list price |
| `deepseek-v4-flash` | — | reasoning | per-token | 1M | $0.19 | $0.51 | — | — | —/— | — | models.dev official list price |
| `deepseek-v4-pro` | — | reasoning | per-token | 1M | $1.74 | $3.48 | — | — | —/— | — | models.dev official list price |
| `gpt-3.5-turbo-0125` | — | chat | per-token | 16.384K | $0.5 | $1.5 | — | — | —/— | — | models.dev official list price |
| `gpt-3.5-turbo-1106` | — | chat | per-token | 16.384K | $1 | $2 | — | — | —/— | — | models.dev official list price |
| `gpt-3.5-turbo-instruct` | — | chat | per-token | 4.096K | $1.5 | $2 | — | — | —/— | — | models.dev official list price |
| `gpt-4-turbo` | — | chat | per-token | 128K | $10 | $30 | — | — | —/— | — | models.dev official list price |
| `gpt-4-turbo-vision` | — | chat | per-token | 128K | $10 | $30 | — | — | —/— | — | models.dev official list price |
| `gpt-4.1` | — | chat | per-token | 1.04758M | $2 | $8 | $0.5 | — | —/— | — | models.dev official list price |
| `gpt-4.1-mini` | — | chat | per-token | 1.04758M | $0.4 | $1.6 | $0.1 | — | —/— | — | models.dev official list price |
| `gpt-4.1-nano` | — | chat | per-token | 1.04758M | $0.1 | $0.4 | $0.025 | — | —/— | — | models.dev official list price |
| `gpt-4o` | — | chat | per-token | 128K | $2.5 | $10 | $1.25 | — | —/— | — | models.dev official list price |
| `gpt-4o-mini` | — | chat | per-token | 128K | $0.15 | $0.6 | $0.075 | — | —/— | — | models.dev official list price |
| `gpt-5` | — | reasoning | per-token | 400K | $1.25 | $10 | $0.13 | — | —/— | — | models.dev official list price |
| `gpt-5-codex` | — | reasoning | per-token | 400K | $1.25 | $10 | $0.13 | — | —/— | — | models.dev official list price |
| `gpt-5-mini` | — | reasoning | per-token | 400K | $0.25 | $2 | $0.03 | — | —/— | — | models.dev official list price |
| `gpt-5-nano` | — | reasoning | per-token | 400K | $0.05 | $0.4 | $0.01 | — | —/— | — | models.dev official list price |
| `gpt-5-pro` | — | reasoning | per-token | 400K | $15 | $120 | — | — | —/— | — | models.dev official list price |
| `gpt-5.1` | — | reasoning | per-token | 400K | $1.25 | $10 | $0.125 | — | —/— | — | models.dev official list price |
| `gpt-5.1-codex` | — | reasoning | per-token | 400K | $1.25 | $10 | $0.125 | — | —/— | — | models.dev official list price |
| `gpt-5.1-codex-max` | — | reasoning | per-token | 400K | $1.25 | $10 | $0.125 | — | —/— | — | models.dev official list price |
| `gpt-5.1-codex-mini` | — | reasoning | per-token | 400K | $0.25 | $2 | $0.025 | — | —/— | — | models.dev official list price |
| `gpt-5.2` | — | reasoning | per-token | 400K | $1.75 | $14 | $0.125 | — | —/— | — | models.dev official list price |
| `gpt-5.2-codex` | — | reasoning | per-token | 400K | $1.75 | $14 | $0.175 | — | —/— | — | models.dev official list price |
| `gpt-5.3-codex` | — | reasoning | per-token | 400K | $1.75 | $14 | $0.175 | — | —/— | — | models.dev official list price |
| `gpt-5.4` | — | reasoning | per-token | 1.05M | $2.5 | $15 | $0.25 | — | —/— | — | models.dev official list price |
| `gpt-5.4-mini` | — | reasoning | per-token | 400K | $0.75 | $4.5 | $0.075 | — | —/— | — | models.dev official list price |
| `gpt-5.4-nano` | — | reasoning | per-token | 400K | $0.2 | $1.25 | $0.02 | — | —/— | — | models.dev official list price |
| `gpt-5.4-pro` | — | reasoning | per-token | 1.05M | $30 | $180 | — | — | —/— | — | models.dev official list price |
| `gpt-5.5` | — | reasoning | per-token | 1.05M | $5 | $30 | $0.5 | — | —/— | — | models.dev official list price |
| `gpt-5.6-luna` | — | reasoning | per-token | 1.05M | $0.2 | $1.2 | $0.02 | — | —/— | — | models.dev official list price |
| `gpt-5.6-sol` | — | reasoning | per-token | 1.05M | $5 | $30 | $0.5 | — | —/— | — | models.dev official list price |
| `gpt-5.6-terra` | — | reasoning | per-token | 1.05M | $2 | $12 | $0.2 | — | —/— | — | models.dev official list price |
| `gpt-chat-latest` | — | reasoning | per-token | 128K | $5 | $30 | $0.5 | — | —/— | — | models.dev official list price |
| `gpt-image-1` | — | chat | per-token | — | $5 | $40 | $1.25 | — | —/— | — | models.dev official list price |
| `gpt-image-1.5` | — | chat | per-token | — | $5 | $32 | $1.25 | — | —/— | — | models.dev official list price |
| `gpt-image-2` | — | chat | per-token | — | $5 | $30 | $1.25 | — | —/— | — | models.dev official list price |
| `grok-4-1-fast-non-reasoning` | — | chat | per-token | 128K | $0.2 | $0.5 | $0.05 | — | —/— | — | models.dev official list price |
| `grok-4-1-fast-reasoning` | — | reasoning | per-token | 128K | $0.2 | $0.5 | $0.05 | — | —/— | — | models.dev official list price |
| `grok-4-20-non-reasoning` | — | chat | per-token | 262K | $2 | $6 | — | — | —/— | — | models.dev official list price |
| `grok-4-20-reasoning` | — | reasoning | per-token | 262K | $2 | $6 | — | — | —/— | — | models.dev official list price |
| `kimi-k2.5` | — | reasoning | per-token | 262.144K | $0.6 | $3 | — | — | —/— | — | models.dev official list price |
| `kimi-k2.6` | — | reasoning | per-token | 262.144K | $0.95 | $4 | — | — | —/— | — | models.dev official list price |
| `kimi-k2.7-code` | — | reasoning | per-token | 262.144K | $0.95 | $4 | $0.19 | — | —/— | — | models.dev official list price |
| `llama-3.3-70b-instruct` | — | chat | per-token | 128K | $0.71 | $0.71 | — | — | —/— | — | models.dev official list price |
| `llama-4-maverick-17b-128e-instruct-fp8` | — | chat | per-token | 1M | $0.25 | $1 | — | — | —/— | — | models.dev official list price |
| `llama-4-scout-17b-16e-instruct` | — | chat | per-token | 128K | $0.2 | $0.78 | — | — | —/— | — | models.dev official list price |
| `ministral-3b` | — | chat | per-token | 128K | $0.04 | $0.04 | — | — | —/— | — | models.dev official list price |
| `mistral-medium-2505` | — | chat | per-token | 128K | $0.4 | $2 | — | — | —/— | — | models.dev official list price |
| `mistral-small-2503` | — | chat | per-token | 128K | $0.1 | $0.3 | — | — | —/— | — | models.dev official list price |
| `model-router` | — | chat | per-token + free | 200K | $0.14 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `o1` | — | reasoning | per-token | 200K | $15 | $60 | $7.5 | — | —/— | — | models.dev official list price |
| `o3` | — | reasoning | per-token | 200K | $2 | $8 | $0.5 | — | —/— | — | models.dev official list price |
| `o3-mini` | — | reasoning | per-token | 200K | $1.1 | $4.4 | $0.55 | — | —/— | — | models.dev official list price |
| `o4-mini` | — | reasoning | per-token | 200K | $1.1 | $4.4 | $0.275 | — | —/— | — | models.dev official list price |
| `phi-4` | — | chat | per-token | 128K | $0.125 | $0.5 | — | — | —/— | — | models.dev official list price |
| `phi-4-mini` | — | chat | per-token | 128K | $0.075 | $0.3 | — | — | —/— | — | models.dev official list price |
| `phi-4-mini-reasoning` | — | reasoning | per-token | 128K | $0.075 | $0.3 | — | — | —/— | — | models.dev official list price |
| `phi-4-multimodal` | — | chat | per-token | 128K | $0.08 | $0.32 | — | — | —/— | — | models.dev official list price |
| `phi-4-reasoning` | — | reasoning | per-token | 32K | $0.125 | $0.5 | — | — | —/— | — | models.dev official list price |
| `phi-4-reasoning-plus` | — | reasoning | per-token | 32K | $0.125 | $0.5 | — | — | —/— | — | models.dev official list price |
| `text-embedding-3-large` | — | embedding | per-token + free | 8.191K | $0.13 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `text-embedding-3-small` | — | embedding | per-token + free | 8.191K | $0.02 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `text-embedding-ada-002` | — | embedding | per-token + free | 8.192K | $0.1 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
