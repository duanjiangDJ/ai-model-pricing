# DeepSeek

- provider_id: `deepseek`
- Channel: First-party
- API base URL: `https://api.deepseek.com`
- Homepage: https://api-docs.deepseek.com/quick_start/pricing
- Pricing page: https://api-docs.deepseek.com/zh-cn/quick_start/pricing
- Currency: USD
- Data updated: 2026-08-21T13:59:17Z
- Verified: 2026-08-21T13:59:17Z

**5** models in total.

| Model | Status | Category | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `deepseek-chat` | 🔁 superseded | chat | — | — | — | — | — | —/— | — | 旧型号（V3.2 时代），已被 deepseek-v4-flash 取代；旧价 $0.28/$0.42 不再适用于当前官方在售模型，保留条目仅作历史参考。… |
| `deepseek-reasoner` | 🔁 superseded | reasoning | — | — | — | — | — | —/— | — | 旧型号（R1 时代），已被 deepseek-v4-flash/pro 的思考模式取代；旧价 $0.55/$2.19 不再适用于当前官方在售模型，保留条目… |
| `deepseek-v4-flash` | — | chat | 1M | $3 | $9 | $0.1 | — | —/— | ⚡ peak/off-peak | 官方价（CNY/百万tokens，2026-08-21 官方文档）：输入(缓存未命中) 高峰 ¥3.0 / 闲时 ¥1.5；输出 高峰 ¥9.0 / 闲时… |
| `deepseek-v4-flash-vision-exp` | 🧪 preview | vision | 1M | $3 | $9 | $0.1 | — | —/— | ⚡ peak/off-peak | 官方价（CNY/百万tokens）与 flash 相同：输入(未命中) 高峰 ¥3.0/闲时 ¥1.5；输出 ¥9.0/¥4.5；缓存命中 ¥0.10/¥… |
| `deepseek-v4-pro` | — | chat | 1M | $9 | $27 | $0.3 | — | —/— | ⚡ peak/off-peak | 官方价（CNY/百万tokens）：输入(缓存未命中) 高峰 ¥9.0 / 闲时 ¥4.5；输出 高峰 ¥27.0 / 闲时 ¥13.5；输入(缓存命中)… |
