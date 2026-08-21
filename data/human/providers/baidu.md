# 百度智能云千帆 (Baidu Qianfan)

- provider_id: `baidu`
- Channel: First-party
- API base URL: `https://qianfan.baidubce.com/v2`
- Homepage: https://qianfan.cloud.baidu.com
- Pricing page: https://cloud.baidu.com/doc/qianfan/s/wmh4sv6ya
- Currency: USD
- Data updated: 2026-08-21T13:59:17Z
- Verified: 2026-08-21T13:59:17Z

**3** models in total.

| Model | Status | Category | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `ernie-5.1` | — | chat | 128K | $4 | $18 | — | — | —/— | — | 官方价：输入≤32k ¥4/百万tokens、输出 ¥18/百万；32k<输入≤128k：¥6/¥22 每百万。CNY 计价。 |
| `ernie-5.0` | — | reasoning | 128K | $6 | $24 | — | — | —/— | — | 官方价：输入 ¥6/百万、输出 ¥24/百万；32k+ 输入 ¥10/输出 ¥40 每百万。CNY 计价。 |
| `ernie-4.5-turbo` | — | chat | 128K | $0.8 | $3.2 | $0.2 | — | $0.32/$1.28 | — | 官方价：输入 ¥0.8/百万、命中缓存 ¥0.2/百万、输出 ¥3.2/百万；批量推理 ¥0.32/¥1.28。CNY 计价。 |
