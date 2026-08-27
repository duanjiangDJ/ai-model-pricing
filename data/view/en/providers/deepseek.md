# DeepSeek

- provider_id: `deepseek`
- Channel: First-party
- API base URL: `https://api.deepseek.com`
- Homepage: https://api-docs.deepseek.com/quick_start/pricing
- Pricing page: https://api-docs.deepseek.com/zh-cn/quick_start/pricing
- Currency: USD
- Data updated: 2026-08-27T00:36:48Z
- Verified: 2026-08-27T00:36:48Z

**5** models in total.

| Model | Status | Category | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `deepseek-chat` | ❌ offline | chat | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (V3.2 era), superseded by deepseek-v4-flash; old prices $0.28/$0… |
| `deepseek-reasoner` | ❌ offline | reasoning | — | $0.14 | $0.28 | $0.0028 | — | —/— | — | Legacy model (R1 era), superseded by deepseek-v4-flash/pro thinking mode; old… |
| `deepseek-v4-flash` | — | chat | 1M | $3 | $9 | $0.1 | — | —/— | ⚡ peak/off-peak | Official page (CNY/1M tokens, peak tier; off-peak = 50%, peak = Beijing 9:00-… |
| `deepseek-v4-flash-vision-exp` | ✅ online | vision | 1M | $3 | $9 | $0.1 | — | —/— | ⚡ peak/off-peak | Official page (CNY/1M tokens, peak tier; off-peak = 50%, peak = Beijing 9:00-… |
| `deepseek-v4-pro` | — | chat | 1M | $9 | $27 | $0.3 | — | —/— | ⚡ peak/off-peak | Official page (CNY/1M tokens, peak tier; off-peak = 50%, peak = Beijing 9:00-… |
