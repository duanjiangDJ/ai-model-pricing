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
| `ernie-5.1` | — | chat | 128K | $4 | $18 | — | — | —/— | — | Official price: input ≤32k ¥4/1M tokens, output ¥18/1M; 32k<input≤128k: ¥6/¥2… |
| `ernie-5.0` | — | reasoning | 128K | $6 | $24 | — | — | —/— | — | Official price: input ¥6/1M, output ¥24/1M; 32k+ input ¥10/output ¥40 per 1M.… |
| `ernie-4.5-turbo` | — | chat | 128K | $0.8 | $3.2 | $0.2 | — | $0.32/$1.28 | — | Official price: input ¥0.8/1M, cache hit ¥0.2/1M, output ¥3.2/1M; batch infer… |
