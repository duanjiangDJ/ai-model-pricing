# Cloudflare AI Gateway

- provider_id: `cloudflare-ai-gateway`
- Channel: Aggregator
- API base URL: `https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway}`
- Homepage: https://developers.cloudflare.com/ai-gateway/
- Pricing page: https://developers.cloudflare.com/ai-gateway/
- Currency: USD
- Data updated: 2026-09-01T00:17:36Z
- Verified: 2026-09-01T00:17:36Z

**79** models in total.

| Model | Status | Category | Billing | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `alibaba/qwen3-max` | — | chat | per-token | 262.144K | $1.2 | $6 | — | — | —/— | — | models.dev official list price |
| `alibaba/qwen3.5-397b-a17b` | — | reasoning | per-token | 262.144K | $0.6 | $3.6 | — | — | —/— | — | models.dev official list price |
| `alibaba/qwen3.7-max` | — | reasoning | per-token | 1M | $1.25 | $3.75 | $0.25 | — | —/— | — | models.dev official list price |
| `alibaba/qwen3.7-plus` | — | reasoning | per-token | 1M | $0.32 | $1.28 | $0.064 | — | —/— | — | models.dev official list price |
| `alibaba/qwen3.8-max` | — | reasoning | per-token | 1M | $2 | $6 | $0.25 | — | —/— | — | models.dev official list price |
| `anthropic/claude-fable-5` | — | reasoning | per-token | 1M | $10 | $50 | $1 | — | —/— | — | models.dev official list price |
| `anthropic/claude-haiku-4.5` | — | reasoning | per-token | 200K | $1 | $5 | $0.1 | — | —/— | — | models.dev official list price |
| `anthropic/claude-opus-4.5` | — | reasoning | per-token | 200K | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `anthropic/claude-opus-4.6` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `anthropic/claude-opus-4.7` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `anthropic/claude-opus-4.8` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `anthropic/claude-opus-5` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `anthropic/claude-sonnet-4.5` | — | reasoning | per-token | 1M | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `anthropic/claude-sonnet-4.6` | — | reasoning | per-token | 1M | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `anthropic/claude-sonnet-5` | — | reasoning | per-token | 1M | $2 | $10 | $0.2 | — | —/— | — | models.dev official list price |
| `deepseek/deepseek-v4-pro` | — | reasoning | per-token | 131.072K | $1.74 | $3.48 | $0.145 | — | —/— | — | models.dev official list price |
| `moonshotai/kimi-k3` | — | reasoning | per-token | 1.04858M | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `openai/gpt-3.5-turbo` | — | chat | per-token + free | 16.385K | $0.5 | $1.5 | $0 | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `openai/gpt-4` | — | chat | per-token | 8.192K | $30 | $60 | — | — | —/— | — | models.dev official list price |
| `openai/gpt-4-turbo` | — | chat | per-token | 128K | $10 | $30 | — | — | —/— | — | models.dev official list price |
| `openai/gpt-4.1` | — | chat | per-token | 1.04758M | $2 | $8 | $0.5 | — | —/— | — | models.dev official list price |
| `openai/gpt-4.1-mini` | — | chat | per-token | 1.04758M | $0.4 | $1.6 | $0.1 | — | —/— | — | models.dev official list price |
| `openai/gpt-4.1-nano` | — | chat | per-token | 1.04758M | $0.1 | $0.4 | $0.025 | — | —/— | — | models.dev official list price |
| `openai/gpt-4o` | — | chat | per-token | 128K | $1.25 | $5 | $0.625 | — | —/— | — | models.dev official list price |
| `openai/gpt-4o-mini` | — | chat | per-token | 128K | $0.075 | $0.3 | $0.0375 | — | —/— | — | models.dev official list price |
| `openai/gpt-5` | — | reasoning | per-token | 400K | $1.25 | $10 | $0.125 | — | —/— | — | models.dev official list price |
| `openai/gpt-5-mini` | — | reasoning | per-token | 400K | $0.25 | $2 | $0.025 | — | —/— | — | models.dev official list price |
| `openai/gpt-5-nano` | — | reasoning | per-token | 400K | $0.05 | $0.4 | $0.005 | — | —/— | — | models.dev official list price |
| `openai/gpt-5-pro` | — | reasoning | per-token | 400K | $15 | $120 | — | — | —/— | — | models.dev official list price |
| `openai/gpt-5.1` | — | reasoning | per-token | 400K | $1.25 | $10 | $0.125 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.2` | — | reasoning | per-token | 400K | $1.75 | $14 | $0.175 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.2-chat-latest` | — | reasoning | per-token | 128K | $1.75 | $14 | $0.175 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.2-pro` | — | reasoning | per-token | 400K | $21 | $168 | — | — | —/— | — | models.dev official list price |
| `openai/gpt-5.3-chat-latest` | — | chat | per-token | 128K | $1.75 | $14 | $0.175 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.3-codex` | — | reasoning | per-token | 400K | $1.75 | $14 | $0.175 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.3-codex-spark` | — | reasoning | per-token | 128K | $1.75 | $14 | $0.175 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.4` | — | reasoning | per-token | 1.05M | $2.5 | $15 | $0.25 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.4-mini` | — | reasoning | per-token | 400K | $0.75 | $4.5 | $0.075 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.4-nano` | — | reasoning | per-token | 400K | $0.2 | $1.25 | $0.02 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.4-pro` | — | reasoning | per-token | 1.05M | $30 | $180 | — | — | —/— | — | models.dev official list price |
| `openai/gpt-5.5` | — | reasoning | per-token | 1.05M | $5 | $30 | $0.5 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.5-pro` | — | reasoning | per-token | 1.05M | $30 | $180 | — | — | —/— | — | models.dev official list price |
| `openai/gpt-5.6` | — | reasoning | per-token | 1.05M | $5 | $30 | $0.5 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.6-luna` | — | reasoning | per-token | 1.05M | $0.2 | $1.2 | $0.02 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.6-sol` | — | reasoning | per-token | 1.05M | $2 | $10 | $0.25 | — | —/— | — | models.dev official list price |
| `openai/gpt-5.6-terra` | — | reasoning | per-token | 1.05M | $2 | $12 | $0.2 | — | —/— | — | models.dev official list price |
| `openai/o1` | — | reasoning | per-token | 200K | $15 | $60 | $7.5 | — | —/— | — | models.dev official list price |
| `openai/o1-pro` | — | reasoning | per-token | 200K | $150 | $600 | — | — | —/— | — | models.dev official list price |
| `openai/o3` | — | reasoning | per-token | 200K | $2 | $8 | $0.5 | — | —/— | — | models.dev official list price |
| `openai/o3-mini` | — | reasoning | per-token | 200K | $1.1 | $4.4 | $0.55 | — | —/— | — | models.dev official list price |
| `openai/o3-pro` | — | reasoning | per-token | 200K | $20 | $80 | — | — | —/— | — | models.dev official list price |
| `openai/o4-mini` | — | reasoning | per-token | 200K | $1.1 | $4.4 | $0.275 | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/aisingapore/gemma-sea-lion-v4-27b-it` | — | chat | per-token | 128K | $0.351 | $0.555 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b` | — | reasoning | per-token | 80K | $0.497 | $4.881 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/google/gemma-4-26b-a4b-it` | — | reasoning | per-token | 256K | $0.1 | $0.3 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/ibm-granite/granite-4.0-h-micro` | — | chat | per-token | 131K | $0.017 | $0.112 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/meta/llama-3.1-8b-instruct-fp8` | — | chat | per-token | 32K | $0.152 | $0.287 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/meta/llama-3.2-11b-vision-instruct` | — | chat | per-token | 128K | $0.0485 | $0.676 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/meta/llama-3.2-1b-instruct` | — | chat | per-token | 60K | $0.027 | $0.201 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/meta/llama-3.2-3b-instruct` | — | chat | per-token | 80K | $0.0509 | $0.335 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/meta/llama-3.3-70b-instruct-fp8-fast` | — | chat | per-token | 24K | $0.293 | $2.253 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/meta/llama-4-scout-17b-16e-instruct` | — | chat | per-token | 131K | $0.27 | $0.85 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/meta/llama-guard-3-8b` | — | chat | per-token | 131.072K | $0.484 | $0.03 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/mistralai/mistral-small-3.1-24b-instruct` | — | chat | per-token | 128K | $0.351 | $0.555 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/moonshotai/kimi-k2.6` | — | reasoning | per-token | 262.144K | $0.95 | $4 | $0.16 | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/moonshotai/kimi-k2.7-code` | — | reasoning | per-token | 262.144K | $0.95 | $4 | $0.19 | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/nvidia/nemotron-3-120b-a12b` | — | reasoning | per-token | 256K | $0.5 | $1.5 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/openai/gpt-oss-120b` | — | reasoning | per-token | 128K | $0.35 | $0.75 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/openai/gpt-oss-20b` | — | reasoning | per-token | 128K | $0.2 | $0.3 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/qwen/qwen2.5-coder-32b-instruct` | — | chat | per-token | 32.768K | $0.66 | $1 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/qwen/qwen3-30b-a3b-fp8` | — | reasoning | per-token | 32.768K | $0.0509 | $0.335 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/qwen/qwq-32b` | — | reasoning | per-token | 24K | $0.66 | $1 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/zai-org/glm-4.7-flash` | — | reasoning | per-token | 131.072K | $0.0605 | $0.4 | — | — | —/— | — | models.dev official list price |
| `workers-ai/@cf/zai-org/glm-5.2` | — | reasoning | per-token | 262.144K | $1.4 | $4.4 | $0.26 | — | —/— | — | models.dev official list price |
| `xai/grok-4.20-0309-non-reasoning` | — | chat | per-token | 2M | $2 | $6 | $0.2 | — | —/— | — | models.dev official list price |
| `xai/grok-4.20-0309-reasoning` | — | reasoning | per-token | 2M | $2 | $6 | $0.2 | — | —/— | — | models.dev official list price |
| `xai/grok-4.3` | — | reasoning | per-token | 1M | $1.25 | $2.5 | $0.2 | — | —/— | — | models.dev official list price |
| `xai/grok-4.5` | — | reasoning | per-token | 500K | $2 | $6 | $0.3 | — | —/— | — | models.dev official list price |
| `xai/grok-4.6` | — | reasoning | per-token | 500K | $2 | $6 | $0.5 | — | —/— | — | models.dev official list price |
