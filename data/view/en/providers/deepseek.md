# DeepSeek

- provider_id: `deepseek`
- Channel: First-party
- API base URL: `https://api.deepseek.com`
- Homepage: https://api-docs.deepseek.com/quick_start/pricing
- Pricing page: https://api-docs.deepseek.com/zh-cn/quick_start/pricing
- Currency: USD
- Data updated: 2026-08-27T17:11:11Z
- Verified: 2026-08-27T15:37:35.738047Z

**5** models in total.

| Model | Status | Category | Billing | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `deepseek-chat` | ❌ offline | chat | per-token | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (V3.2 era), superseded by deepseek-v4-flash; old prices $0.28/$0… |
| `deepseek-reasoner` | ❌ offline | reasoning | per-token | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (R1 era), superseded by deepseek-v4-flash/pro thinking mode; old… |
| `deepseek-v4-flash` | — | chat | per-token | 1M | $0.44 | $1.32 | $0.014 | — | —/— | ⚡ peak/off-peak | Official page (USD/1M tokens, peak tier; off-peak = 50%, peak = Mon-Fri 01:00… |
| `deepseek-v4-flash-vision-exp` | ✅ online | vision | per-token | 1M | $0.44 | $1.32 | $0.014 | — | —/— | ⚡ peak/off-peak | Official page (USD/1M tokens, peak tier; off-peak = 50%, peak = Mon-Fri 01:00… |
| `deepseek-v4-pro` | — | chat | per-token | 1M | $1.32 | $3.96 | $0.044 | — | —/— | ⚡ peak/off-peak | Official page (USD/1M tokens, peak tier; off-peak = 50%, peak = Mon-Fri 01:00… |
