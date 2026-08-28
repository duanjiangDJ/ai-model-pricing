# DeepSeek

- provider_id: `deepseek`
- Channel: First-party
- API base URL: `https://api.deepseek.com`
- Homepage: https://api-docs.deepseek.com/quick_start/pricing
- Pricing page: https://api-docs.deepseek.com/zh-cn/quick_start/pricing
- Currency: USD
- Data updated: 2026-08-28T09:39:56.778415Z
- Verified: 2026-08-28T09:39:34Z

**5** models in total.

| Model | Status | Category | Billing | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `deepseek-chat` | ❌ offline | chat | per-token | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (V3.2 era), superseded by deepseek-v4-flash; old prices $0.28/$0… |
| `deepseek-reasoner` | ❌ offline | reasoning | per-token | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (R1 era), superseded by deepseek-v4-flash/pro thinking mode; old… |
| `deepseek-v4-flash` | — | chat | per-token | 1M | $0.44 / ¥3 | $1.32 / ¥9 | $0.014 / ¥0.1 | ¥0.05 | —/— | ⚡ peak/off-peak | Domestic api-docs.deepseek.com/zh-cn pricing (CNY/1M tokens, peak tier; indep… |
| `deepseek-v4-flash-vision-exp` | ✅ online | vision | per-token | 1M | $0.44 / ¥3 | $1.32 / ¥9 | $0.014 / ¥0.1 | ¥0.05 | —/— | ⚡ peak/off-peak | Domestic api-docs.deepseek.com/zh-cn pricing (CNY/1M tokens, peak tier; indep… |
| `deepseek-v4-pro` | — | chat | per-token | 1M | $1.32 / ¥9 | $3.96 / ¥27 | $0.044 / ¥0.3 | ¥0.15 | —/— | ⚡ peak/off-peak | Domestic api-docs.deepseek.com/zh-cn pricing (CNY/1M tokens, peak tier; indep… |
