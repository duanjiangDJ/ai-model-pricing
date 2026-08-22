# xAI

- provider_id: `xai`
- 渠道: 官方直供
- API 地址: `https://api.x.ai/v1`
- 官网: https://docs.x.ai/docs/models
- 定价页: https://docs.x.ai/developers/pricing
- 币种: USD
- 数据更新时间: 2026-08-22T09:32:50Z
- 核实时间: 2026-08-22T09:32:50Z

共 **17** 个模型。

| 模型 | 状态 | 类别 | 上下文 | 输入 $/MTok | 输出 $/MTok | 缓存读 | 缓存写 | 批处理(入/出) | 其他计费 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|
| `grok-3` | ❌ 下线 | chat | — | — | — | — | — | —/— | — | grok-3 retired from xAI API 2026-05-15; redirects to grok-4.3 with 'none' rea… |
| `grok-4` | ❌ 下线 | chat | — | — | — | — | — | —/— | — | 2025-era Grok 4 family (grok-4-0709, grok-4-fast-reasoning, grok-4-fast-non-r… |
| `grok-4-fast` | ❌ 下线 | chat | — | — | — | — | — | —/— | — | grok-4-fast-reasoning and grok-4-fast-non-reasoning retired 2026-05-15; redir… |
| `grok-4.20-0309-non-reasoning` | — | chat | 1M | $1.25 | $2.5 | $0.2 | — | $1/$2 | — | Two-tier pricing at 200k prompt tokens: <200k $1.25/$0.20/$2.50; >=200k $2.50… |
| `grok-4.20-0309-reasoning` | — | chat | 1M | $1.25 | $2.5 | $0.2 | — | $1/$2 | — | Two-tier pricing at 200k prompt tokens: <200k $1.25/$0.20/$2.50; >=200k $2.50… |
| `grok-4.20-multi-agent-0309` | — | chat | 1M | $1.25 | $2.5 | $0.2 | — | $1/$2 | — | Two-tier pricing at 200k prompt tokens: <200k $1.25/$0.20/$2.50; >=200k $2.50… |
| `grok-4.3` | ❌ 下线 | chat | 1M | $1.25 | $2.5 | $0.2 | — | $1/$2 | — | Two-tier long-context pricing. <200k: input $1.25 / cached $0.20 / output $2.… |
| `grok-4.5` | — | chat | 500K | $2 | $6 | $0.3 | — | —/— | — | Two-tier long-context pricing. <200k: input $2.00 / cached $0.30 / output $6.… |
| `grok-4.6` | — | chat | 500K | $2 | $6 | $0.5 | — | —/— | — | Two-tier long-context pricing. <200k prompt tokens: input $2.00 / cached $0.5… |
| `grok-build-0.1` | ❌ 下线 | code | 256K | $1 | $2 | $0.2 | — | —/— | — | Agentic coding model. Two-tier pricing at 200k: <200k input $1.00 / cached $0… |
| `grok-code-fast-1` | ❌ 下线 | code | — | — | — | — | — | —/— | — | Retired from xAI API 2026-05-15; redirects to grok-build-0.1 (recommended rep… |
| `grok-embedding` | — | embedding | — | — | — | — | — | —/— | — | No embedding model listed on official xAI pricing or models pages as of 2026-… |
| `grok-imagine-image` | — | chat | 8K | — | — | — | — | —/— | — | models.dev official list price |
| `grok-imagine-image-2.0` | — | chat | 8K | — | — | — | — | —/— | — | models.dev official list price |
| `grok-imagine-image-quality` | — | chat | 8K | — | — | — | — | —/— | — | models.dev official list price |
| `grok-imagine-video` | — | chat | 1.024K | — | — | — | — | —/— | — | models.dev official list price |
| `grok-imagine-video-1.5` | — | chat | 1.024K | — | — | — | — | —/— | — | models.dev official list price |
