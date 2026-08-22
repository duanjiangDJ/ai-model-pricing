> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.
# Research Subagent Contract / 调研子代理契约（research-contract）

> 本仓库的"人工核实"数据通过**调研子代理**批量采集。本文档定义子代理的输入要求与输出格式，
> 保证输出可直接被 `scripts/merge_research.py` 合并入库。

## 输出格式（子代理必须返回）

单个 JSON 对象（**不要** Markdown 代码块包裹，直接输出 JSON 文本）：

```json
{
  "providers": [
    {
      "provider_id": "openai",
      "name": "OpenAI",
      "channel": "first_party",          // first_party | cloud | hosted | aggregator | reseller
      "category": "ai_vendor",           // ai_vendor | cloud_platform | inference_host | aggregator | reseller
      "region": "us",                    // global | cn | us | eu | other
      "homepage": "https://openai.com",
      "pricing_page": "https://platform.openai.com/docs/pricing",
      "currency": "USD",                 // 默认 USD；国内厂商填 CNY 并加 currency_usd_note
      "verified_at": "2026-08-21T00:00:00Z",
      "models": [
        {
          "id": "gpt-4o",
          "name": "GPT-4o",
          "category": "chat",            // chat | reasoning | embedding | image_gen | video_gen | audio_tts | audio_stt | realtime | code ...
          "context_window": 128000,
          "max_output": 16384,
          "pricing": {
            "per_mtok": {"input": 2.5, "output": 10.0, "cache_read": 1.25, "cache_write": 2.5},
            "batch": {"input": 1.25, "output": 5.0},
            "per_image": [{"name": "1024x1024", "price": 0.04}],
            "per_audio_second": null,
            "per_request": null,
            "credits": null
          },
          "notes": "任意需要说明的口径，如分档价格、促销期、退役状态"
        }
      ],
      "plans": [
        {
          "id": "openai-chatgpt-plus",
          "product": "ChatGPT",
          "plan": "Plus",
          "category": "consumer",        // consumer | coding | team | enterprise | student | api_credits | free
          "billing": "monthly",          // monthly | yearly | one_time
          "price_usd": 20,
          "limits": "用量上限说明",
          "includes": ["包含内容"],
          "url": "https://openai.com/chatgpt/pricing/",
          "verified_at": "2026-08-21T00:00:00Z"
        }
      ]
    }
  ],
  "sources": ["https://官方定价页", "https://二级来源"]
}
```

## 硬性规则

1. **只填能确认的数字**，拿不准填 `null`，绝不编造；`0` 仅表示免费。
2. **至少一个二级来源**交叉核实（官方公告、评测站、第三方对比站）。
3. `verified_at` 用**实际调研当天日期**（不要用任务描述里的过期日期）。
4. 已退役/下线模型保留条目，`pricing` 全 null，`notes` 注明退役时间与替代模型。
5. 价格有促销/分档/双档（如 Gemini ≤200K / >200K）在 `notes` 完整说明，主字段填标准档。
6. 非 USD 计价（国内厂商）在 provider 顶层加 `"price_currency": "CNY"` 与 `"currency_usd_note"`。
7. 输出末尾附一行 `SOURCES: url1, url2, ...`。

## 消费端

`scripts/merge_research.py <research.json>`：
- provider 按 `provider_id` 合并（调研数据覆盖同 id 模型的价格与元信息，保留 models.dev 独有模型）；
- plans 按 `id` upsert 进 `data/feed/plans.json`；
- 自动刷新 `index.json` 计数并写 changelog。
