# SAP AI Core

- provider_id: `sap-ai-core`
- Channel: Inference host
- API base URL: `https://api.ai.prod.eu-central-1.aws.sap.corp`
- Homepage: https://help.sap.com/docs/sap-ai-core
- Pricing page: https://help.sap.com/docs/sap-ai-core
- Currency: USD
- Data updated: 2026-09-01T09:18:24Z
- Verified: 2026-09-01T09:18:24Z

**48** models in total.

| Model | Status | Category | Billing | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `amazon--nova-lite` | — | reasoning | per-token | 1M | $0.3 | $2.37 | — | — | —/— | — | models.dev official list price |
| `amazon--nova-micro` | — | chat | per-token | 128K | $0.03 | $0.1 | — | — | —/— | — | models.dev official list price |
| `amazon--nova-pro` | — | chat | per-token | 300K | $0.56 | $2.13 | — | — | —/— | — | models.dev official list price |
| `amazon--titan-embed-text` | — | embedding | per-token | 8.192K | $0.14 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `anthropic--claude-3-haiku` | — | chat | per-token | 200K | $0.25 | $1.25 | $0.03 | — | —/— | — | models.dev official list price |
| `anthropic--claude-3-opus` | — | chat | per-token | 200K | $15 | $75 | $1.5 | — | —/— | — | models.dev official list price |
| `anthropic--claude-3-sonnet` | — | chat | per-token | 200K | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `anthropic--claude-3.5-sonnet` | — | chat | per-token | 200K | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `anthropic--claude-3.7-sonnet` | — | reasoning | per-token | 200K | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `anthropic--claude-4-opus` | — | reasoning | per-token | 200K | $15 | $75 | $1.5 | — | —/— | — | models.dev official list price |
| `anthropic--claude-4-sonnet` | — | reasoning | per-token | 200K | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `anthropic--claude-4.5-haiku` | — | reasoning | per-token | 200K | $1 | $5 | $0.1 | — | —/— | — | models.dev official list price |
| `anthropic--claude-4.5-opus` | — | reasoning | per-token | 200K | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `anthropic--claude-4.5-sonnet` | — | reasoning | per-token | 200K | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `anthropic--claude-4.6-opus` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `anthropic--claude-4.6-sonnet` | — | reasoning | per-token | 1M | $3 | $15 | $0.3 | — | —/— | — | models.dev official list price |
| `anthropic--claude-4.7-opus` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `anthropic--claude-4.8-opus` | — | reasoning | per-token | 1M | $5 | $25 | $0.5 | — | —/— | — | models.dev official list price |
| `cohere--command-a-reasoning` | — | reasoning | per-token | 256K | $0.63 | $5.05 | — | — | —/— | — | models.dev official list price |
| `gemini-2.5-flash` | — | reasoning | per-token | 1.04858M | $0.3 | $2.5 | $0.03 | — | —/— | — | models.dev official list price |
| `gemini-2.5-flash-lite` | — | reasoning | per-token | 1.04858M | $0.1 | $0.4 | $0.01 | — | —/— | — | models.dev official list price |
| `gemini-2.5-pro` | — | reasoning | per-token | 1.04858M | $1.25 | $10 | $0.125 | — | —/— | — | models.dev official list price |
| `gemini-3.1-flash-lite` | — | reasoning | per-token | 1.04858M | $0.25 | $1.5 | $0.025 | — | —/— | — | models.dev official list price |
| `gemini-3.5-flash` | — | reasoning | per-token | 1.04858M | $1.5 | $9 | $0.15 | — | —/— | — | models.dev official list price |
| `gemini-embedding` | — | embedding | per-token | 2.048K | — | — | — | — | —/— | — | models.dev official list price |
| `gemini-embedding-2` | — | embedding | per-token | 8.192K | — | — | — | — | —/— | — | models.dev official list price |
| `gpt-4.1` | — | chat | per-token | 1.04758M | $2 | $8 | $0.32 | — | —/— | — | models.dev official list price |
| `gpt-4.1-mini` | — | chat | per-token | 1.04758M | $0.4 | $1.6 | $0.1 | — | —/— | — | models.dev official list price |
| `gpt-4.1-nano` | — | chat | per-token | 1.04758M | $0.08 | $0.26 | — | — | —/— | — | models.dev official list price |
| `gpt-5` | — | reasoning | per-token | 400K | $1.25 | $10 | $0.125 | — | —/— | — | models.dev official list price |
| `gpt-5-mini` | — | reasoning | per-token | 400K | $0.25 | $2 | $0.025 | — | —/— | — | models.dev official list price |
| `gpt-5-nano` | — | reasoning | per-token | 400K | $0.05 | $0.4 | $0.005 | — | —/— | — | models.dev official list price |
| `gpt-5.2` | — | reasoning | per-token | 400K | $1.25 | $9.44 | $0.12 | — | —/— | — | models.dev official list price |
| `gpt-5.4` | — | reasoning | per-token | 1.05M | $2.5 | $15 | $0.25 | — | —/— | — | models.dev official list price |
| `gpt-5.5` | — | reasoning | per-token | 1.05M | $5 | $30 | $0.5 | — | —/— | — | models.dev official list price |
| `gpt-5.6-luna` | — | reasoning | per-token | 1.05M | $1 | $6 | $0.1 | — | —/— | — | models.dev official list price |
| `gpt-5.6-sol` | — | reasoning | per-token | 1.05M | $5 | $30 | $0.5 | — | —/— | — | models.dev official list price |
| `gpt-5.6-terra` | — | reasoning | per-token | 1.05M | $2.5 | $15 | $0.25 | — | —/— | — | models.dev official list price |
| `mistralai--mistral-medium` | — | reasoning | per-token | 262.144K | — | — | — | — | —/— | — | models.dev official list price |
| `mistralai--mistral-medium-instruct` | — | chat | per-token | 128K | $0.36 | $1.22 | — | — | —/— | — | models.dev official list price |
| `mistralai--mistral-small` | — | reasoning | per-token | 128K | $0.07 | $0.28 | — | — | —/— | — | models.dev official list price |
| `nvidia--llama-3.2-nv-embedqa-1b` | — | embedding | per-token | 8.192K | $0.07 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `sap-abap-1` | — | chat | per-token | 32.768K | $0.48 | $1.7 | — | — | —/— | — | models.dev official list price |
| `sonar` | — | chat | per-token | 128K | $1 | $1 | — | — | —/— | — | models.dev official list price |
| `sonar-deep-research` | — | reasoning | per-token | 128K | $2 | $8 | — | — | —/— | — | models.dev official list price |
| `sonar-pro` | — | chat | per-token | 200K | $3 | $15 | — | — | —/— | — | models.dev official list price |
| `text-embedding-3-large` | — | embedding | per-token | 8.191K | $0.09 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
| `text-embedding-3-small` | — | embedding | per-token | 8.191K | $0.02 | $0 | — | — | —/— | — | models.dev official list price \| Free model (per_mtok = 0). |
