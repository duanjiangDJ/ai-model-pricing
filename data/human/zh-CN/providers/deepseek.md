# DeepSeek

- provider_id: `deepseek`
- 渠道: 官方直供
- API 地址: `https://api.deepseek.com`
- 官网: https://api-docs.deepseek.com/quick_start/pricing
- 定价页: https://api-docs.deepseek.com/zh-cn/quick_start/pricing
- 币种: USD
- 数据更新时间: 2026-08-21T13:59:17Z
- 核实时间: 2026-08-21T13:59:17Z

共 **5** 个模型。

| 模型 | 状态 | 类别 | 上下文 | 输入 $/MTok | 输出 $/MTok | 缓存读 | 缓存写 | 批处理(入/出) | 其他计费 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|
| `deepseek-chat` | 🔁 已被取代 | chat | — | — | — | — | — | —/— | — | 旧型号（V3.2 时代），已被 deepseek-v4-flash 取代；旧价 $0.28/$0.42 不再适用于当前官方在售模型，保留条目仅作历史参考。… |
| `deepseek-reasoner` | 🔁 已被取代 | reasoning | — | — | — | — | — | —/— | — | 旧型号（R1 时代），已被 deepseek-v4-flash/pro 的思考模式取代；旧价 $0.55/$2.19 不再适用于当前官方在售模型，保留条目… |
| `deepseek-v4-flash` | — | chat | 1M | $3 | $9 | $0.1 | — | —/— | ⚡ 峰谷双档 | 官方价（CNY/百万tokens，2026-08-21 官方文档）：输入(缓存未命中) 高峰 ¥3.0 / 闲时 ¥1.5；输出 高峰 ¥9.0 / 闲时… |
| `deepseek-v4-flash-vision-exp` | 🧪 预览 | vision | 1M | $3 | $9 | $0.1 | — | —/— | ⚡ 峰谷双档 | 官方价（CNY/百万tokens）与 flash 相同：输入(未命中) 高峰 ¥3.0/闲时 ¥1.5；输出 ¥9.0/¥4.5；缓存命中 ¥0.10/¥… |
| `deepseek-v4-pro` | — | chat | 1M | $9 | $27 | $0.3 | — | —/— | ⚡ 峰谷双档 | 官方价（CNY/百万tokens）：输入(缓存未命中) 高峰 ¥9.0 / 闲时 ¥4.5；输出 高峰 ¥27.0 / 闲时 ¥13.5；输入(缓存命中)… |
