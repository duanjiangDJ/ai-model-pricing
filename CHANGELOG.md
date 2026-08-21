# Changelog

## 全面定价复核（2026-08-21，官方文档为准）

- **DeepSeek**：确认 V3.2 时代已结束——官方在售 **V4 系列**（deepseek-v4-flash ¥3/¥9、v4-pro ¥9/¥27 每百万 tokens，CNY；2026-08-16/17 起峰谷分时定价，高峰=北京 9:00-12:00/14:00-18:00，闲时半价；上下文 1M/输出 384K）。旧 deepseek-chat/reasoner 标记 superseded。官方中英文定价页均已直接抓取，多源交叉核实。
- **Anthropic**：13 模型逐一核实（官方 pricing 页 + docs + 5 个二级源）。关键更新：**Sonnet 5 的 $2/$10 于 2026-08-11 永久化**（原定 9/1 涨至 $3/$15 已取消）；新增 claude-mythos-5（$10/$50，受限访问）；补齐全部 cache_write（=input×1.25）与 batch（=50%）；Opus 4.1 标记 legacy。
- **OpenAI**：官方定价页快照（2026-08-12）确认 gpt-5.6-sol/terra/luna 全价（含 cache_write $6.25/$2.5/$0.25、batch 50%、long-context 档、数据驻留 +10%）；官方 deprecations 页（2026-08-10）确认 o 系列/gpt-4 全系/dall-e/embedding-3-small 等 **26 个模型已标记退役提示**；官方 catalog（2026-08-09）显示当前在售 5 个模型（gpt-oss、gpt-5.6 四款）。
- **国内厂商**：百度千帆 ERNIE 5.1/5.0/4.5T（官方计费文档 2026-08-18）、腾讯混元 Hy3（官方新闻）、豆包 2.1 Pro/Turbo（官方发布新闻）此前已按官方来源录入；阿里/智谱/MiniMax/阶跃/Kimi 沿用 models.dev 官方列表价（每日自动同步）。
- **托管平台**：Together/Groq/Cerebras/DeepInfra/SiliconFlow/Novita 等沿用 models.dev 列表价（每日自动同步），未逐项人工复核（复核子代理超时，已在 README 诚实声明）。
- **新增文档**：AGENTS.md（agent 指南）、docs/verification.md（每日检查逻辑与真实性保证机制）。
- **双语化**：README + data/human/ 全量中英双版（英文默认，中文在 zh-CN/）。

## 进度（2026-08-21 第四轮）

- **订阅/编码计划扩充至 51 个**：GitHub Copilot Pro $10/Pro+ $39/Max $100（AI Credits 制）、Cursor Hobby/Pro $20/Pro+ $60/Ultra $200/Teams $40、Windsurf Free/Pro $20/Max $200/Teams $40、JetBrains AI Free/Pro $10/Ultimate $30、Perplexity Pro $20/Max $200、Poe Lite $10/Standard $19.99、Devin Free/Pro $20/Max $200/Teams $80、Amazon Q Free/Pro $19、Tabnine $39/$59、Replit Starter/Core $20/Pro $100
- **国内厂商补录**：百度千帆 ERNIE 5.1/5.0/4.5 Turbo（官方计费文档）、腾讯混元 Hy3（输入 ¥1/百万）、火山方舟豆包 2.1 Pro（¥6/¥30 每百万）——均为 CNY 计价并附汇率说明
- **子代理调研策略调整**：5 个后台调研子代理运行超时无产出（仅 Google/xAI 完成），已中断并改为直接抓取权威第三方聚合页 + 官方文档核实，效率更高

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
