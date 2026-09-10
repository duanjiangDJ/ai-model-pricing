# DeepSeek

- provider_id: `deepseek`
- Channel: First-party
- API base URL: `https://api.deepseek.com`
- Homepage: https://api-docs.deepseek.com/quick_start/pricing
- Pricing page: https://api-docs.deepseek.com/zh-cn/quick_start/pricing
- Currency: USD
- Data updated: 2026-09-10T00:00:00Z
- Verified: 2026-09-10T00:00:00Z

**6** models in total.

| Model | Status | Category | Billing | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `deepseek-v4.1-flash` | ✅ online | chat | per-token | 1M | $0.3 / ¥2/$0.15 / ¥1 | $1.2 / ¥8/$0.6 / ¥4 | $0.006 / ¥0.04/$0.003 / ¥0.02 | — | —/— | ⚡ off-peak x0.5 | Official page (USD/1M tokens, peak tier; off-peak = 50%, peak = Mon-Fri 01:00… |
| `deepseek-chat` | ❌ offline | chat | per-token | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (V3.2 era), superseded by deepseek-v4-flash; old prices $0.28/$0… |
| `deepseek-reasoner` | ❌ offline | reasoning | per-token | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (R1 era), superseded by deepseek-v4-flash/pro thinking mode; old… |
| `deepseek-v4-flash` | ❌ offline | chat | per-token | 1M | $0.44 / ¥3/$0.22 / ¥1.5 | $1.32 / ¥9/$0.66 / ¥4.5 | $0.014 / ¥0.1/$0.007 / ¥0.05 | — | —/— | ⚡ off-peak x0.5 | RETIRED — superseded by the official deepseek-flash (DeepSeek-V4.1-Flash) mod… |
| `deepseek-v4-flash-vision-exp` | ❌ offline | vision | per-token | 1M | $0.44 / ¥3/$0.22 / ¥1.5 | $1.32 / ¥9/$0.66 / ¥4.5 | $0.014 / ¥0.1/$0.007 / ¥0.05 | — | —/— | ⚡ off-peak x0.5 | RETIRED — superseded by the official deepseek-flash (DeepSeek-V4.1-Flash) mod… |
| `deepseek-v4-pro` | — | chat | per-token | 1M | $1.32 / ¥9/$0.66 / ¥4.5 | $3.96 / ¥27/$1.98 / ¥13.5 | $0.044 / ¥0.3/$0.022 / ¥0.15 | — | —/— | ⚡ off-peak x0.5 | Official page (USD/1M tokens, peak tier; off-peak = 50%, peak = Mon-Fri 01:00… |
