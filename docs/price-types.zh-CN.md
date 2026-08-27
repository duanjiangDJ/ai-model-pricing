> **Language: 中文（简体）(zh-CN)** — 本文档仅以中文编写。

# 收费方式与单位（price-types）

> 本文档定义数据库当前支持的**每一种计费方式的精确定义**，作为数据采集与机器读取的基线。
> 所有价格默认 **USD**（由 `index.json` 的 `currency` 字段声明；非 USD 条目必须带 `currency` 覆盖字段）。
>
> **计费方式不做投机性添加。** `schema.json` 中的字段只有在有真实数据支撑时才存在。
> 新增方式按 AGENTS.md「To add a billing mode back」流程执行。

## 0. billing_model —— 模型级收费方式分类（必填）

每个模型带 `billing_model` 数组，说明**如何计费**。一个模型可有多种（例如 Gemini 模型既有免费额度又有按量付费：`["free", "pay_per_token"]`）。

| 取值 | 含义 |
|---|---|
| `pay_per_token` | 按 token 计费（`per_mtok`，含缓存与批处理折扣） |
| `pay_per_image` | 按生成张数计费（`per_image` 分档） |
| `subscription_included` | 订阅/编码计划包含（per_mtok = null；见 plans.json） |
| `credits` | 积分/点数制（预留；暂无数据） |
| `free` | 完全免费（per_mtok = 0） |
| `unknown` | 计费方式未确定（待人工核实；audit 会标记） |

标注工具：`scripts/annotate_billing.py`（自动分类 + provider 上下文兜底），再由 `scripts/audit.py` 校验一致性（如 per_mtok > 0 必须含 `pay_per_token`）。

## 1. per_mtok —— 每百万 tokens

- **定义**：`input` = 输入 token 单价（USD/1M tokens）；`output` = 输出 token 单价。
- 模型条目 `pricing` 对象中的 `per_mtok` 必须至少包含 `input` 和 `output`。
- 同一模型的不同上下文档位（如 OpenAI 4M context）用独立 `id` 条目区分。
- **使用方**：几乎所有文本 LLM（OpenAI、Anthropic、Google、xAI、Mistral、DeepSeek、Qwen、GLM、Kimi、豆包、托管平台、聚合站）。

## 2. cache_read / cache_write —— 缓存读写（USD/1M tokens）

- `cache_read`：命中缓存输入 token 单价（OpenAI/Anthropic/DeepSeek 等通常为列表价 10%~25%）。
- `cache_write`：写入缓存输入 token 单价（OpenAI：与普通输入相同；Anthropic：输入价 × 1.25）。
- 不支持的厂商填 `null`，绝不填 0。

## 3. batch —— 批处理折扣（USD/1M tokens）

- OpenAI/Anthropic/Google 等提供 Batch API，通常为同步价 50%。
- `batch.input` / `batch.output`；无批处理则填 `null`。

## 4. per_image —— 按张计费

- 图像生成模型（DALL·E、Imagen、FLUX API、Novita 等）按张计费，可按下分辨率/质量分档。
- 分档用 `tiers` 数组：`[{name: "1024x1024", price: 0.04}]`。
- 此类模型 `billing_model: ["pay_per_image"]`。

## 5. promo —— 限时促销

- 厂商限时折扣（如 Z.ai GLM-5.3-Flash 9/9 前 5 折）时：`per_mtok` 保存**当前折扣价**，`promo` 记录原价与截止时间：
  `promo: {list_price: {input, output, cache_read}, ends_at: "2026-09-09T16:00:00Z"}`。
- `ends_at` 为 UTC ISO。促销结束后须更新为原价并移除 `promo`。

## 6. subscription —— 订阅 / 编码工具计划（plans.json）

- 消费类订阅与编码工具订阅记录在 `plans.json`，**不**作为模型价格。
- 字段：`price_usd`、`billing: monthly|yearly`、`limits`（用量上限说明）、`includes`（包含内容），
  以及 `pricing_model`（flat_monthly / flat_yearly / per_seat_monthly / per_seat_yearly / credits / free / custom）。
- 年付记录**全年总价**（`price_usd` + `billing: yearly`），不折算月价以免精度损失。
- 计划包含的模型：`per_mtok` = null + `billing_model: ["subscription_included"]` + 注明计划名称的 notes。

---

## 数据采集规则（必须遵守）

1. **价格必须来自官方定价页 / 官方 API / 官方文档**（有官方**英文/USD**页时优先用英文页——如 DeepSeek `quick_start/pricing` 英文版、百度千帆国际站）。
   每条记录带 `source_url` 与 `verified_at`（ISO8601 UTC）。**绝不允许把人民币数值写进 USD 声明的文件**；
   厂商只公布人民币价的，设 `currency: "CNY"` 并在 `currency_usd_note` 说明。
2. **同一模型在不同渠道价格不同（官方直供 vs 托管 vs 聚合）**：分别记录在各自 provider 文件，互不覆盖；
   聚合站价格（如 OpenRouter）作为"转售价"与官方价并列，用 `channel` 字段区分（`first_party` / `cloud` / `hosted` / `aggregator` / `reseller` / `subscription`）。
3. **缺失数据**用 `null`；**不适用**用 `null` + `notes` 说明；**绝不用 0 表示缺失**。
4. 价格变更：每日检查脚本与旧值对比；相对变化 > 5× 视为解析错误，跳过并告警（突变护栏）。所有变更写入 `changelog.json`。
5. 订阅计划价格遵循官方定价页；每日检查为超过 30 天未核实的计划生成"待人工核实"清单。
6. 每个模型必须有 `billing_model`；批量导入后运行 `scripts/annotate_billing.py`，并由 `scripts/audit.py` 校验。

---

## 相关文档

- [README](../README.md) — 概览与精确统计
- [AGENTS.md](../AGENTS.md) — AI Agent 指南
- [FORMAT.md](../FORMAT.md) — 机器格式规范
- [providers.md](providers.md) — 供应商全景与状态
- [verification.md](verification.md) — 核实模型
- [CONTRIBUTING.md](../CONTRIBUTING.md) — 如何贡献
