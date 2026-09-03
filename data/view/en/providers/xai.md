# xAI

- provider_id: `xai`
- Channel: First-party
- API base URL: `https://api.x.ai/v1`
- Homepage: https://docs.x.ai/docs/models
- Pricing page: https://docs.x.ai/developers/pricing
- Currency: USD
- Data updated: 2026-09-03T00:20:55Z
- Verified: 2026-09-03T00:20:55Z

**17** models in total.

| Model | Status | Category | Billing | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `grok-3` | ❌ offline | chat | ? | — | — | — | — | — | —/— | — | grok-3 retired from xAI API 2026-05-15; redirects to grok-4.3 with 'none' rea… |
| `grok-4` | ❌ offline | chat | ? | — | — | — | — | — | —/— | — | 2025-era Grok 4 family (grok-4-0709, grok-4-fast-reasoning, grok-4-fast-non-r… |
| `grok-4-fast` | ❌ offline | chat | ? | — | — | — | — | — | —/— | — | grok-4-fast-reasoning and grok-4-fast-non-reasoning retired 2026-05-15; redir… |
| `grok-4.20-0309-non-reasoning` | — | chat | per-token | 1M | $1.25 | $2.5 | $0.2 | — | $1/$2 | — | Two-tier pricing at 200k prompt tokens: <200k $1.25/$0.20/$2.50; >=200k $2.50… |
| `grok-4.20-0309-reasoning` | — | chat | per-token | 1M | $1.25 | $2.5 | $0.2 | — | $1/$2 | — | Two-tier pricing at 200k prompt tokens: <200k $1.25/$0.20/$2.50; >=200k $2.50… |
| `grok-4.20-multi-agent-0309` | — | chat | per-token | 1M | $1.25 | $2.5 | $0.2 | — | $1/$2 | — | Two-tier pricing at 200k prompt tokens: <200k $1.25/$0.20/$2.50; >=200k $2.50… |
| `grok-4.3` | ❌ offline | chat | per-token | 1M | $1.25 | $2.5 | $0.2 | — | $1/$2 | — | Two-tier long-context pricing. <200k: input $1.25 / cached $0.20 / output $2.… |
| `grok-4.5` | — | chat | per-token | 500K | $2 | $6 | $0.3 | — | —/— | — | Two-tier long-context pricing. <200k: input $2.00 / cached $0.30 / output $6.… |
| `grok-4.6` | — | chat | per-token | 500K | $2 | $6 | $0.5 | — | —/— | — | Two-tier long-context pricing. <200k prompt tokens: input $2.00 / cached $0.5… |
| `grok-build-0.1` | ❌ offline | code | per-token | 256K | $1 | $2 | $0.2 | — | —/— | — | Agentic coding model. Two-tier pricing at 200k: <200k input $1.00 / cached $0… |
| `grok-code-fast-1` | ❌ offline | code | ? | — | — | — | — | — | —/— | — | Retired from xAI API 2026-05-15; redirects to grok-build-0.1 (recommended rep… |
| `grok-embedding` | — | embedding | ? | — | — | — | — | — | —/— | — | No embedding model listed on official xAI pricing or models pages as of 2026-… |
| `grok-imagine-image` | — | chat | ? | 8K | — | — | — | — | —/— | — | models.dev official list price |
| `grok-imagine-image-2.0` | — | chat | ? | 8K | — | — | — | — | —/— | — | models.dev official list price |
| `grok-imagine-image-quality` | — | chat | ? | 8K | — | — | — | — | —/— | — | models.dev official list price |
| `grok-imagine-video` | — | chat | ? | 1.024K | — | — | — | — | —/— | — | models.dev official list price |
| `grok-imagine-video-1.5` | — | chat | ? | 1.024K | — | — | — | — | —/— | — | models.dev official list price |
