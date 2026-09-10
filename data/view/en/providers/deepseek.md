# DeepSeek

- provider_id: `deepseek`
- Channel: First-party
- API base URL: `https://api.deepseek.com`
- Homepage: https://api-docs.deepseek.com/quick_start/pricing
- Pricing page: https://api-docs.deepseek.com/zh-cn/quick_start/pricing
- Currency: USD
- Data updated: 2026-09-10T06:39:07Z
- Verified: 2026-09-10T06:39:07Z

**5** models in total.

| Model | Status | Category | Billing | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `deepseek-chat` | ❌ offline | chat | per-token | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (V3.2 era), superseded by deepseek-v4-flash; old prices $0.28/$0… |
| `deepseek-reasoner` | ❌ offline | reasoning | per-token | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (R1 era), superseded by deepseek-v4-flash/pro thinking mode; old… |
| `deepseek-v4-flash` | — | chat | per-token | 1M | $0.14 / ¥3/$0.07 / ¥1.5 | $0.28 / ¥9/$0.14 / ¥4.5 | $0.014 / ¥0.1/$0.007 / ¥0.05 | — | —/— | ⚡ off-peak x0.5 | models.dev official list price |
| `deepseek-v4-flash-vision-exp` | ✅ online | vision | per-token | 1M | $0.14 / ¥3/$0.07 / ¥1.5 | $0.28 / ¥9/$0.14 / ¥4.5 | $0.014 / ¥0.1/$0.007 / ¥0.05 | — | —/— | ⚡ off-peak x0.5 | models.dev official list price |
| `deepseek-v4-pro` | — | chat | per-token | 1M | $0.435 / ¥9/$0.2175 / ¥4.5 | $0.87 / ¥27/$0.435 / ¥13.5 | $0.044 / ¥0.3/$0.022 / ¥0.15 | — | —/— | ⚡ off-peak x0.5 | models.dev official list price |
