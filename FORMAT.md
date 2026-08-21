# 机器可读格式规范（Machine-Readable Format Specification）

> 版本：**1.0.0**（由 `data/machine/schema.json` 的 `version` 字段与各文件 `schema_version` 字段声明）
> 本格式专为爬虫/程序/工具链设计：稳定、版本化、可校验、可增量同步。

## 目录结构

```
data/machine/
├── schema.json          # JSON Schema（draft 2020-12），本格式的唯一权威定义
├── index.json           # 入口文件：先读它，再按需抓取
├── providers/           # 每个供应商一个文件
│   ├── openai.json
│   ├── openrouter.json  # 聚合站（转售价，channel=aggregator）
│   └── ...
├── plans.json           # 订阅/编码工具计划（月度/年度订阅、点数制）
└── (resellers.json)     # 中转站（可选，与 plans.json 同构：{schema_version, updated_at, items})

data/meta/
├── manifest.json        # 数据源健康状态、最近同步时间
└── changelog.json       # 全部变更历史（add/update/remove/verify）
```

## 读取协议（给爬虫/程序）

1. 固定入口：`https://raw.githubusercontent.com/duanjiangDJ/ai-model-pricing/main/data/machine/index.json`
2. `index.json` 给出：
   - `schema_version`（不兼容变更会 bump 主版本，消费方必须检查）
   - `generated_at`（本次全量生成时间）
   - `providers[]` / `resellers[]`：每个条目含 `id`、`model_count`、`file`（相对路径）、`updated_at`
   - `model_count`、`plan_count` 总览
3. 按 `file` 字段拼接抓取各供应商 JSON；需要全量平铺数据时，`models[]` 已含全部字段，直接 concat 即可。
4. 每个模型的价格字段：见下方「价格结构」。所有价格默认 **USD/百万 tokens**，非 USD 的 provider 在顶层 `currency` 声明（如 `"CNY"`）。
5. 校验：可用 `scripts/validate.py`（`pip install jsonschema`）对全部数据做 schema + 交叉一致性校验。
6. 增量：`data/meta/changelog.json` 按时间倒序记录每次变更（`kind: add|update|remove|verify`）。

## 价格结构（model.pricing）

| 字段 | 类型 | 单位/说明 |
|---|---|---|
| `per_mtok.input` / `.output` | number\|null | USD / 1M tokens |
| `per_mtok.cache_read` | number\|null | 缓存命中输入价（通常为 input 的 10%~25%） |
| `per_mtok.cache_write` | number\|null | 缓存写入价（Anthropic 为 input × 1.25） |
| `per_mtok.reasoning_effort[]` | array | 按推理强度分档定价（如 OpenAI o 系列） |
| `batch.input` / `.output` | number\|null | 批处理 API 价（通常 50%） |
| `per_image[]` | array | 图像生成按张：`[{name, price}]` 分档 |
| `per_audio_second.input/.output` | object | TTS/STT 按秒/分钟 |
| `per_character.price` | object | 按字符（含 `unit: per_char|per_1k_char`） |
| `per_request` | number\|null | 按请求次数 |
| `credits` | object | 点数制：`topup{amount_usd, credits}`、`model_rate{per_mtok_input, ...}`、`convertible` |
| `gpu[]` | array | GPU 计费：`[{sku, price, unit: per_second|per_hour}]` |
| `neuron_second` | object | Cloudflare 神经元秒 |
| `finetune` | object | 微调：`training_input/output/hosting` |
| `provisioned` | "contact_sales"\|null | 预留容量（企业定制） |

**规则**：`null` = 无此计费方式或未知；缺失**绝不**用 0 表示。免费模型价格为 `0`。

## 订阅计划（plans.json）

每个计划：`id`、`provider_id`、`product`、`plan`、`category`（consumer/coding/team/enterprise/student/api_credits/free）、
`billing`（monthly/yearly/one_time）、`price_usd`（年付记年总价）、`limits`、`includes[]`、`url`、`verified_at`。

## 渠道语义（channel）

`first_party`（官方直供） / `cloud`（云平台托管） / `hosted`（推理托管平台） /
`aggregator`（聚合站转售价，如 OpenRouter） / `reseller`（中转站） / `subscription`（订阅产品）。

同一模型在不同渠道价格不同属正常现象，各渠道分别记录、互不覆盖；`notes` 注明口径。

## 版本策略

- 新增可选字段：patch 版本（1.0.x），向后兼容。
- 新增必填字段 / 重命名字段 / 改变单位：minor 或 major 版本，并在 `CHANGELOG.md`（仓库根）说明迁移。
- 消费方应校验 `schema_version` 前缀是否匹配其支持的版本。

## 每日更新机制

`.github/workflows/daily-check.yml` 每天 01:23 UTC 运行 `scripts/daily_check.py`：

1. 拉取 OpenRouter 目录并 diff 本地数据 → 有变化则更新 + 写入 changelog；
2. 检查 `plans.json` 中超过 30 天未核实的条目 → 生成 `reports/stale-plans.md`，并同步 GitHub issue「每日价格核实提醒」；
3. 重建人类可读页面（`data/human/`）；
4. 有变更则自动 commit & push（bot 身份，`[skip ci]`）。

手动触发：仓库 Actions 页面 → Daily Price Check → Run workflow。
