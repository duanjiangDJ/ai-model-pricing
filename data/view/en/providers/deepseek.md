# DeepSeek

- provider_id: `deepseek`
- Channel: First-party
- API base URL: `https://api.deepseek.com`
- Homepage: https://api-docs.deepseek.com/quick_start/pricing
- Pricing page: https://api-docs.deepseek.com/zh-cn/quick_start/pricing
- Currency: USD
- Data updated: 2026-09-02T23:23:35Z
- Verified: 2026-09-02T23:23:35Z

**5** models in total.

| Model | Status | Category | Billing | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `deepseek-chat` | ❌ offline | chat | per-token | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (V3.2 era), superseded by deepseek-v4-flash; old prices $0.28/$0… |
| `deepseek-reasoner` | ❌ offline | reasoning | per-token | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (R1 era), superseded by deepseek-v4-flash/pro thinking mode; old… |
| `deepseek-v4-flash` | — | chat | per-token | 1M | $0.44 / ¥3/$0.22 / ¥1.5 | $1.32 / ¥9/$0.66 / ¥4.5 | $0.014 / ¥0.1/$0.007 / ¥0.05 | ¥0.05/¥0.025 | —/— | ⚡ off-peak x0.5 | Official page peak tier; off-peak via pricing.off_peak. Parsed by check deeps… |
| `deepseek-v4-flash-vision-exp` | ✅ online | vision | per-token | 1M | $0.44 / ¥3/$0.22 / ¥1.5 | $1.32 / ¥9/$0.66 / ¥4.5 | $0.014 / ¥0.1/$0.007 / ¥0.05 | ¥0.05/¥0.025 | —/— | ⚡ off-peak x0.5 | Official page peak tier; off-peak via pricing.off_peak. Parsed by check deeps… |
| `deepseek-v4-pro` | — | chat | per-token | 1M | $1.32 / ¥9/$0.66 / ¥4.5 | $3.96 / ¥27/$1.98 / ¥13.5 | $0.044 / ¥0.3/$0.022 / ¥0.15 | ¥0.15/¥0.075 | —/— | ⚡ off-peak x0.5 | Official page peak tier; off-peak via pricing.off_peak. Parsed by check deeps… |
