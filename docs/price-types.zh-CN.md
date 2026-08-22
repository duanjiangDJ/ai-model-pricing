> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.
# Price Types & Units / 收费形式口径（price-types）

> 本文件定义每种收费形式的**精确口径**，是数据采集和机器读取的基准。枚举值在
> `data/machine/schema.json` 中定义为 `priceType` / `planBilling` 的 enum，此处为人类可读解释。
> 所有价格默认 **USD**（`index.json` 中 `currency` 字段声明；非 USD 的条目必须带 `currency` 覆盖字段）。

## 1. per_mtok —— 每百万 token
- **口径**：`input` = 输入 token 单价（USD/1M tokens）；`output` = 输出 token 单价。
- 一个模型条目中 `pricing` 对象内的 `per_mtok` 至少含 `input`、`output`。
- 同模型不同 context 档位（如 OpenAI 4M 上下文）用独立 `id` 条目区分。
- **谁在用**：几乎所有文本 LLM（OpenAI、Anthropic、Google、xAI、Mistral、DeepSeek、Qwen、GLM、Kimi、豆包、托管平台、聚合站）。

## 2. cache_read / cache_write —— 缓存读写（USD/1M tokens）
- `cache_read`：命中缓存的输入 token 单价（OpenAI/Anthropic/DeepSeek 等通常为原价 10%~25%）。
- `cache_write`：写入缓存的输入 token 单价（OpenAI 与普通输入同价；Anthropic 为输入价 1.25 倍）。
- 不支持的厂商填 `null`，不要填 0。

## 3. batch —— 批处理折扣（USD/1M tokens）
- OpenAI/Anthropic/Google 等提供 Batch API，通常为同步价 50%。
- `batch.input` / `batch.output`；无批处理填 `null`。

## 4. per_image —— 每张图片
- 图像生成模型（DALL·E、Imagen、FLUX via API、Novita 等）按张计价，可随分辨率/质量分档。
- 分档用 `tiers` 数组：`[{name: "1024x1024", price: 0.04}]`。

## 5. per_audio_second —— 每音频秒
- TTS/STT/音频理解（ElevenLabs、Deepgram、AssemblyAI、Whisper、Realtime API 音频）。
- 字段 `input`（识别/理解）与 `output`（合成）语义按模型用途区分，文档注明。

## 6. per_character —— 每字符
- 部分 TTS 与翻译 API 按字符计价（如旧版 TTS、某些中转站）。通常有"每 1K 字符"惯例，单位字段 `unit` 注明 `per_1k_char` 或 `per_char`。

## 7. per_request —— 每次请求/调用
- 图像 API、部分聚合站、旧式付费 API（如某些 embedding 代理）按次计费。
- 单位 `USD/request`。

## 8. credits —— 点数/积分计价
- Poe、Hugging Face Pro、国内充值平台（如"1 元 = 100 点"，模型按点数/次 或 点数/MTok 扣减）。
- 结构：`credits: { topup: {amount_usd, credits}, model_rate: {per_mtok: <credits>} | {per_request: <credits>} }`。
- 无法折算成 USD/MTok 时必须保留原始点数口径并注明 `convertible: false`。

## 9. gpu_second / gpu_hour —— GPU 秒/小时
- Replicate、Modal、Baseten、RunPod 等按 GPU 规格计时收费（如 `A100-40GB: $0.00115/s`）。
- 结构：`gpu: [{sku: "A100-40GB", price_per_second: 0.00115}]`。

## 10. neuron_second —— 神经元秒
- Cloudflare Workers AI 计价单位（每 1M 神经元秒 = $0.011）。保留原始口径。

## 11. subscription_monthly / subscription_yearly —— 订阅
- 消费级与编码工具订阅。字段：`price_usd`、`billing: monthly|yearly`、`limits`（用量上限说明）、`includes`（包含内容）。
- 年付按**年总价**记录（`price_usd` + `billing: yearly`），不折算月价，避免精度损失。

## 12. free_tier —— 免费额度
- 记录免费档的限额（如 Gemini：15 RPM/1500 RPD；Copilot Free：50 条/月）。
- 结构：`{requests_per_month, rpm, rpd, notes}`，无限制填 `null`。

## 13. finetune —— 微调
- 按训练 token 计费（input/output 训练价）与托管价分开记录：`training.input` / `training.output` / `hosting`。

## 14. provisioned —— 预留容量（企业）
- OpenAI/Azure 预留吞吐按小时计费。多数为合同价，字段可填 `"contact_sales"`。

---

## 价格收录规则（采集时必须遵守）

1. **价格一律来自定价页/官方 API/官方文档**，每条记录带 `source_url` 与 `verified_at`（ISO8601 UTC）。
2. **同模型、不同渠道（官方 vs 托管 vs 聚合）价格不同**：不同 provider 文件分别记录，不互相覆盖；OpenRouter 等聚合站价格是"转售价"，与官方价并列，`channel` 字段区分（`first_party` / `cloud` / `hosted` / `aggregator` / `reseller`）。
3. **数据缺失**用 `null`，**不适用**用 `null` + `notes` 说明，**不要用 0 表示缺失**。
4. 价格变动：每日检查脚本对比上次 `verified_at`；变化超过 1% 或任一价格字段变化，写 `changelog.json` 并生成报告。
5. 订阅计划价格以官方定价页为准；每日检查对超过 30 天未核实的计划生成"待人工核实"清单。


---

## 相关文档

- [README.zh-CN.md](README.zh-CN.md) — 总览与精确统计
- [FORMAT.zh-CN.md](FORMAT.zh-CN.md) — 机器格式规范
- [docs/providers.zh-CN.md](docs/providers.zh-CN.md) — 供应商全景与状态
- [docs/price-types.zh-CN.md](docs/price-types.zh-CN.md) — 收费形式口径
- [docs/verification.zh-CN.md](docs/verification.zh-CN.md) — 核实与真实性机制
- [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md) — 如何贡献
- [AGENTS.md](AGENTS.md) — AI Agent 指南（英文）
