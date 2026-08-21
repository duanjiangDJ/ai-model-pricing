# Changelog

## 进度（2026-08-21 第三轮）

- **订阅计划扩充至 18 个**（第三方源核实，2026-08-21）：
  - ChatGPT：Plus $20 / **Pro $100（2026-04 新增档）** / Pro $200
  - Claude：Pro $20（年付 $17/月）/ Max 5x $100 / Max 20x $200 / Claude Code Pro $20
- 关键事实：OpenAI 官方模型价（GPT-5.6 全系 47 模型）与 Anthropic（Fable 5/Opus 4.5-5/Sonnet 4.5-5/Haiku 4.5 共 13 模型）已由 models.dev 自动同步（first_party 渠道）

## 进度（2026-08-21 第二轮）

- **已入库官方定价**（调研子代理核实，verified 2026-08-21）：
  - Google Gemini：Gemini 3.6/3.5 Flash（intro 价 $0.75/$3.75）、3.1 Pro Preview（$2/$12）、3 Flash Preview、2.5 Pro/Flash/Flash-Lite、Embedding 1/2；2.0 系列已退役标记
  - xAI：Grok 4.6/4.5/4.3、4.20 系列、Grok Build 0.1；2025 时代模型退役标记（redirect 至 4.3）
  - 订阅计划 11 个：Google AI Pro $19.99 / Ultra $99.99~$200 / Plus $7.99、Gemini Code Assist Free/Standard $19/Enterprise $45、SuperGrok $30/Heavy $300/Lite $10
- **调研流水线**：`docs/research-contract.md`（子代理输出契约）+ `scripts/merge_research.py`（自动合并入库）
- 其余调研（OpenAI、Anthropic、国内厂商、托管平台、编码计划）进行中

## v1.0.0 (2026-08-21)

- **数据结构定稿**：`data/machine/schema.json` v1.0.0（JSON Schema draft 2020-12），覆盖 17 种收费形式枚举（per MTok / cache / batch / per image / per audio second / per character / per request / credits / GPU / neuron second / 订阅月费年费 / 免费额度 / 微调 / provisioned）。
- **机器可读格式**：`data/machine/index.json` 为固定入口，`providers/*.json` 每供应商一文件，`plans.json` 订阅计划，`data/meta/manifest.json` + `changelog.json` 元数据。规范见 `FORMAT.md`。
- **人类可读版本**：`data/human/` 由脚本从机器数据自动生成（勿手改）。
- **自动同步**：
  - OpenRouter API：419 个模型（聚合转售价）；
  - models.dev：192 个供应商、约 7,300 个模型（官方/托管列表价）；
  - 每日 diff：价格变动自动更新 + changelog 记录。
- **每日检查机制**：`.github/workflows/daily-check.yml`（每天 01:23 UTC）：
  - 自动同步 OpenRouter / models.dev 价格变动并提交；
  - 超过 30 天未核实的订阅计划自动生成「每日价格核实提醒」issue；
  - 数据校验（schema + 交叉一致性）失败则任务失败。
- **文档**：`docs/providers.md`（供应商 7 大类全景）、`docs/price-types.md`（收费形式口径）。
- 供应商全景与收费形式调研结论：**现有公开资源（OpenRouter / models.dev / LiteLLM）均只覆盖 API token 定价，没有统一来源覆盖订阅/编码计划/点数制等全部价格类型**，故自建本仓库。

## 待办（Roadmap）

- [ ] 填充 OpenAI / Anthropic / Google / xAI 官方定价与订阅计划（调研中）
- [ ] 填充国内厂商（DeepSeek / Qwen / 豆包 / GLM / Kimi / MiniMax 等）官方定价
- [ ] 填充编码工具订阅（Copilot / Cursor / Windsurf / Claude Code / JetBrains AI 等）
- [ ] 中转站样本收录与定价模式文档
