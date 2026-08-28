> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.

# Changelog / 变更日志

## 版本规则（Versioning）

版本号格式：**`年份.内容更新.功能更新`**（如 `26.2.3` = 2026 年第 2 次内容更新、第 3 次功能更新）。

- **年份**：首次发布所在年份（两位数，如 2026 → `26`）；年份变化时重置后两段为 0。
- **内容更新**（第二段，+1）：**仅限定价数据**——价格变化、模型新增/退役（status 变更）、订阅计划新增/改价。示例：修正某模型 input/output、新增 ChatGPT Go 计划、标记模型下线。
- **功能更新**（第三段，+1）：**除定价以外的所有变更**——数据结构（schema/格式）、脚本（router/checks/toolbox）、工作流、文档、翻译、目录重组、CI 机制。示例：新增检查脚本、重命名目录、更新 AGENTS。
- 边界判定：一个 PR 同时含定价与功能变更时，按**主要变更类型**只 bump 一段（定价为主→内容更新；其余→功能更新）。
- 两条规则都只 +1 自身段位，**互不重置**。
- 当前版本见 `VERSION` 文件；`data/feed/schema.json` 的 `version` 与各数据文件 `schema_version` 与之一致。
- 版本递增由维护者/机器人按变更类型决定，记录于本文件条目。

---

## 26.7.12 — 2026-08-28T08:10Z（功能更新）

- **fix(测试污染)**：突变护栏单元测试只 mock 了 `save_provider`，但 `update_model_prices` 还会调用 `append_changelog`——每次跑测试都会往生产 `changelog.json` 写入假的 "test-prov" 条目，其中一条还进入了 CHANGELOG.md（26.6.11）。现已同时 mock 两者；2 条污染条目已清除，26.6.11 条目已重写说明无真实变更。
- **fix(free 注释)**：零价格模型必须有 "free" 注释（audit 策略）。`sync_modelsdev` / `sync_openrouter` 的 `build_model` 在判定免费时自动追加 "Free model (per_mtok = 0)."；并为现存 90 个零价格模型补注（kenari/nvidia/opencode/openrouter/orcarouter/venice/vercel）。audit 警告 34 → 2。
- **fix(audit)**：USD 文件内 CNY 检测豁免明确注明 "no official USD" 的条目（百度 ernie-5.1/4.5-turbo、火山 doubao 的有意 CNY-only 标注）。

## 26.7.11 — 2026-08-28T05:09Z（内容更新）

- price sync (341 changes):
- alibaba update x8: qwen3.7-plus,qwen3.7-plus,qwen3.6-flash,qwen3.6-flash,qwen-vl-ocr,qwen-vl-ocr,qwen3.6-35b-; qwen-vl-ocr: {'input': [0.07, 0.72], 'output': [0.16, 0.72]}->{'input': 0.72, 'output': 0.; qwen3-32b: {'input': [0.16, 0.7], 'output': [0.64, 2.8]}->{'input': 0.7, 'output': 2.8}; qwen3-next-80b-a3b-instruct: {'input': [0.15, 0.5], 'output': [1.2, 2]}->{'input': 0.5, 'o; qwen3-next-80b-a3b-thinking: {'input': [0.15, 0.5], 'output': [1.2, 6]}->{'input': 0.5, 'o
- alibaba-cn update x3: glm-5: {'input': [0.86, 0.573], 'output': [3.15, 2.58]}->{'input': 0.573, 'output': 2.58}; glm-5.1: {'input': [0.87, 0.825], 'output': [3.48, 3.301]}->{'input': 0.825, 'output': 3.3; qwen3.5-397b-a17b: {'input': [0.43, 0.172], 'output': [2.58, 1.032]}->{'input': 0.172, 'ou
- baseten add x1: zai-org/GLM-5.3-Flash: ?->zai-org/GLM-5.3-Flash
- crossmodel add x1: z-ai/glm-5.3-flash: ?->z-ai/glm-5.3-flash
- deepseek update x4: deepseek-v4-flash,deepseek-v4-flash,deepseek-v4-flash,deepseek-v4-pro,deepseek-v4-pro,deep; deepseek-v4-flash: {'input': [0.44, 0.14], 'output': [1.32, 0.28], 'cache_read': [0.014, 0; deepseek-v4-flash-vision-exp: {'input': [0.44, 0.14], 'output': [1.32, 0.28], 'cache_read'; deepseek-v4-pro: {'input': [1.32, 0.435], 'output': [3.96, 0.87], 'cache_read': [0.044, 0.
- digitalocean add x1: glm-5.3-flash: ?->glm-5.3-flash
- digitalocean update x9: deepseek-3.2: {'input': [0.25, 0.5], 'output': [0.8, 1.6], 'cache_read': [0.075, 0.15]}->{; deepseek-4-flash: {'input': [0.0679, 0.14], 'output': [0.168, 0.28], 'cache_read': [0.0168; deepseek-v4-flash-0731: {'input': [0.08, 0.14], 'output': [0.252, 0.28], 'cache_read': [0.; deepseek-v4-pro: {'input': [0.87, 1.74], 'output': [1.74, 3.48], 'cache_read': [0.174, 0.3; glm-5.2: {'input': [0.7, 1.4], 'output': [2.2, 4.4], 'cache_read': [0.105, 0.21]}->{'input
- edenai add x5: databricks/databricks-gpt-oss-120b@eu: ?->databricks/databricks-gpt-oss-120b@eu; databricks/databricks-gpt-oss-20b@eu: ?->databricks/databricks-gpt-oss-20b@eu; vertex/gemini-3.1-flash-lite: ?->vertex/gemini-3.1-flash-lite; vertex/gemini-3.1-flash-lite@eu: ?->vertex/gemini-3.1-flash-lite@eu; vertex/gemini-3.1-flash-lite@us: ?->vertex/gemini-3.1-flash-lite@us
- edenai update x5: ionos/meta-llama/Llama-3.3-70B-Instruct: {'input': [0.758485, 0.756925], 'output': [0.7584; ionos/openai/gpt-oss-120b: {'input': [0.175035, 0.174675], 'output': [0.758485, 0.756925]}; scaleway/deepseek-v4-flash-0731: {'input': [0.46676, 0.4658], 'output': [0.933521, 0.9316]; scaleway/gpt-oss-120b: {'input': [0.175035, 0.174675], 'output': [0.70014, 0.6987]}->{'inp; scaleway/llama-3.3-70b-instruct: {'input': [1.050211, 1.04805], 'output': [1.050211, 1.048
- hyper update x5: glm-5: {'input': [0.92, 0.9], 'output': [2.976, 2.804]}->{'input': 0.9, 'output': 2.804}; kimi-k2.5: {'input': [0.544, 0.5444], 'output': [2.76, 2.855]}->{'input': 0.5444, 'output'; llama-3.3-70b-instruct: {'input': [0.638, 0.6066], 'output': [0.768, 1.0386]}->{'input': 0; minimax-m2.7: {'input': [0.424, 0.408], 'output': [1.612, 1.512]}->{'input': 0.408, 'outpu; qwen3.8-flash: {'input': [0.16, 0.15]}->{'input': 0.15}
- inceptron update x2: moonshotai/Kimi-K2.6: {'cache_read': [0.13, 0.15]}->{'cache_read': 0.15}; moonshotai/Kimi-K2.7-Code: {'input': [0.67, 0.66], 'cache_read': [0.19, 0.18]}->{'input': 
- kenari add x21: claude-opus-5: ?->claude-opus-5; claude-sonnet-4-6: ?->claude-sonnet-4-6; gemini-3-1-flash-tts: ?->gemini-3-1-flash-tts; gemini-3-1-pro: ?->gemini-3-1-pro; gemini-3-5-flash: ?->gemini-3-5-flash
- kilo add x1: inclusionai/ling-3.0-flash-fin:free: ?->inclusionai/ling-3.0-flash-fin:free
- kilo update x9: google/gemma-4-31b-it: {'input': [0.09, 0.08], 'output': [0.34, 0.35], 'cache_read': [0.05; meta-llama/llama-4-maverick: {'output': [0.696, 0.8]}->{'output': 0.8}; minimax/minimax-m2.7:free: {'cache_read': [None, 0]}->{'cache_read': 0}; minimax/minimax-m3:free: {'cache_read': [None, 0]}->{'cache_read': 0}; qwen/qwen3.6-35b-a3b: {'input': [0.14, 0.1], 'output': [1, 0.9]}->{'input': 0.1, 'output':
- llmgateway add x1: deepseek-v4-flash-vision-exp: ?->deepseek-v4-flash-vision-exp
- merge-gateway update x1: zai/glm-5.3-flash: {'input': [0.075, 0.015], 'output': [0.25, 0.05], 'cache_read': [0.015,
- minimax update x2: MiniMax-M2.5-highspeed: ?->{'models': 1}; MiniMax-M2.5-highspeed: {'cache_read': [0.03, 0.06]}->{'cache_read': 0.06}
- mistral update x3: ministral-3b-latest,ministral-3b-latest,ministral-8b-latest,ministral-8b-latest: ?->{'mode; ministral-3b-latest: {'input': [0.1, 0.04], 'output': [0.1, 0.04]}->{'input': 0.04, 'outpu; ministral-8b-latest: {'input': [0.15, 0.1], 'output': [0.15, 0.1]}->{'input': 0.1, 'output
- modal add x2: Qwen/Qwen3.8-2.4T-A95B: ?->Qwen/Qwen3.8-2.4T-A95B; zai-org/GLM-5.3-Flash: ?->zai-org/GLM-5.3-Flash
- nano-gpt add x1: z-ai/glm-5.3-flash-uncensored: ?->z-ai/glm-5.3-flash-uncensored
- neuralwatt add x4: kimi-k2.7-code: ?->kimi-k2.7-code; kimi-k2.7-code-fast: ?->kimi-k2.7-code-fast; kimi-k3-flex: ?->kimi-k3-flex; qwen3.6-35b: ?->qwen3.6-35b
- neuralwatt update x10: gemma-4-31b: {'cache_read': [0.036, 0.0144]}->{'cache_read': 0.0144}; glm-5.2: {'cache_read': [0.3625, 0.145]}->{'cache_read': 0.145}; glm-5.2-fast: {'cache_read': [0.3625, 0.145]}->{'cache_read': 0.145}; glm-5.2-flex: {'input': [0.725, 0.9425], 'output': [2.25, 2.925], 'cache_read': [0.18125, ; glm-5.2-short: {'cache_read': [0.3625, 0.145]}->{'cache_read': 0.145}
- nvidia add x1: deepseek-ai/deepseek-v4-pro-0813: ?->deepseek-ai/deepseek-v4-pro-0813
- ofox add x1: z-ai/glm-5.3-flash: ?->z-ai/glm-5.3-flash

## 26.6.11 — 2026-08-27T19:41Z（内容更新）

- 本次运行无真实数据变更。（一次单元测试污染临时写入了 2 条假的 "test-prov" changelog 条目，已于 26.7.12 清理；版本号因噪音触发提升，保留以维持版本历史连续。）

## 26.5.11 — 2026-08-27T17:38Z（功能更新）

- **fix(回归, HIGH)**：`sync_openrouter.py` / `sync_modelsdev.py` 未生成新增必填字段 `billing_model`——下次每日自动同步会**清空所有 OpenRouter/models.dev 模型的 billing_model** 并触发 audit「missing billing_model」失败，导致自动合并 workflow 挂掉。两个 `build_model` 现已正确分类计费方式（pay_per_token / pay_per_image / free / unknown），且不再写入已删除的 `per_request`/`per_audio_second` 字段。已实测真实同步：417 个 OpenRouter 模型全部正确标注（388 按量、29 按图+按量）。
- **fix(stats)**："By channel" 模型数恒为 0（`chan_m` 声明后从未填充）；README/中文统计现已显示真实数量（如 Inference host 4,316 / Subscription 173 / Aggregator 2,222）。
- **fix(audit)**：235 条逐模型的「pay_per_token 但 per_mtok 全 null」警告聚合为每 provider 一行（这些是按量转售模型、价格未公开）；audit 警告 248 → 14。
- **feat(ui)**：view 页面对有 `promo` 的模型标记 🔥 promo（en）/ 🔥 促销（zh-CN）；Z.ai GLM-5.3-Flash 已显示徽标。
- **feat(tests)**：新增 2 个突变护栏测试（正常变更生效、>5x 突变跳过，mock 保存）；测试套件现共 7 个。
- **refactor(schema)**：`providerFile` 简化为 `$defs.provider` 的纯 `$ref`。

## 26.5.10 — 2026-08-27T17:16Z（功能更新）

- **feat(billing_model)**：每个模型新增必填 `billing_model` 数组（pay_per_token / pay_per_image / subscription_included / credits / free / unknown）——用机器可读字段直接回答"这模型怎么收费"，不再靠 null/0/notes 推断。全库 7,239 个模型经 `scripts/annotate_billing.py` 标注（6467 按量、384 免费、114 订阅包含、55 免费+按量混合、219 未知待人工——这些在 models.dev 无价，如实标记）。支持多收费方式（如 Gemini 免费额度+付费）。
- **feat(schema)**：删除 8 个未使用计费字段（per_audio_second、per_character、per_request、credits、gpu、neuron_second、finetune、provisioned——0 使用）；新增 `promo.{list_price, ends_at}`；新增 `billingModel` 枚举；priceType 枚举 17→8。修复 `providerFile` 空 schema 问题（此前 provider 数据实际未被校验）。新增计费方式回添流程（AGENTS.md，字段只在有数据支撑时存在）。
- **feat(channel)**：coding-plan/token-plan provider 统一为 `channel: subscription`（此前 9 个 provider hosted/subscription 混标）。
- **feat(promo)**：Z.ai GLM-5.3-Flash 五折促销入档（原价 $0.15/$0.50/$0.03，9/9 截止）。
- **feat(audit)**：新校验——billing_model 存在性/枚举/与 pricing 一致性、USD 文件内 CNY 标注检测、`:free` 后缀豁免零价格警告。
- **feat(ui)**：view 页面新增"收费方式"列（中英）；订阅渠道标签补齐。
- **feat(tests)**：`tests/test_parsers.py` + HTML fixture（deepseek 英文页、百度国际站）；pr-check.yml 纳入测试步骤。
- **feat(ci)**：daily-check 输出详细 `SYNC_SUMMARY`（provider/模型/old→new），作为 CHANGELOG 消息，替代笼统的 "chore: price sync"。
- **docs**：AGENTS.md（billing_model、计费字段添加流程、注释全英文规则、channel 语义）、FORMAT.md（中英，含 model.status online/offline 修正）、docs/price-types.md（中英重写为现行计费类型）、README 统计刷新（186 供应商、7,239 模型、67 计划）。

## 26.5.9 — 2026-08-27T15:40Z（内容更新）

- **fix(货币)**: deepseek.json v4 系列由 CNY 数值修正为官方英文页 USD 价格（flash $0.44/$1.32、pro $1.32/$3.96，峰值档）。baidu.json ernie-5.0 → 国际站 USD（$1.4/$5.6）；ernie-5.1/4.5-turbo → null + CNY 说明（仅国内提供）。tencent.json currency → CNY（混元 ¥1/¥4，官方仅 CNY 定价）。volcengine.json doubao-2.1-pro/turbo → null + CNY 说明（无官方 USD 页）。
- **fix(解析器)**: deepseek 解析器改抓官方英文定价页（USD），加结构断言（必须 18 个 $价格，否则报错拒绝写入部分数据）。baidu 解析器重写适配千帆国际站（USD, $/M tokens）。
- **feat(护栏)**: 价格突变护栏（变化 >5x 视为解析错误，跳过该字段并告警）接入 toolbox.update_model_prices 与 sync_official.apply_to_provider。OpenRouter 目录重写加保护（远端 < 本地 50% 拒绝覆盖）。
- **fix(CI)**: pr-check.yml 核心文件保护路径由 data/machine/ 修正为 data/feed/。
- **feat(数据)**: 新增 provider zai-coding-plan（GLM-5.3-Flash + GLM-5.3 + 路由规则、积分倍率、非高峰 50% 规则）+ 3 个订阅计划条目（Lite/Pro/Max，积分制，$18/$72/$160）。

## 26.4.9 — 2026-08-27T08:13Z（内容更新）

- chore: price sync

## 26.3.9 — 2026-08-27T07:56Z（功能更新）

- 修复：PAT 推送 main 被分支保护拒绝（GH006，fine-grained PAT 无法绕过）时，改为推送到分支并发 issue 告警，数据不再丢失

## 26.3.8 — 2026-08-27T07:39Z（功能更新）

- 修复：daily-check 工作流 YAML 语法错误（issue 正文缩进）；自动合并前先对齐最新 main（stash → rebase → stash pop），避免基于旧基线的 rebase 冲突；GH_PAT 自动合并路径已验证可用

## 26.3.7 — 2026-08-27T07:22Z（功能更新）

- 修复：zai 官方检查现可解析 "Latest Models" 章节并自动添加官方新模型（如 GLM-5.3-Flash 促销价直取）；router 自动刷新 index 计数；daily-check 在无法创建 PR 时改为发 issue 告警并使步骤失败（不再静默丢弃，main 不再静默停更）

## 26.3.6 — 2026-08-27T00:38Z（内容更新）

- chore: price sync

## 26.2.6 — 2026-08-22T11:46Z（功能更新）

- 功能：Tier-0 自动化覆盖全部 11 家（新增 alibaba/google/meta/minimax/mistral/moonshotai/xai/zai 官方页检查，deepseek/anthropic/openai 已有）；按官方定价页修正 14 个模型价格（alibaba 7 个、Ministral 3B/8B、minimax 缓存写入 8 个、moonshot 批处理 3 个、zai 缓存 2 个、google 批处理 9 个）；Meta 官方页为客户端渲染，价格经多源交叉验证

## 26.2.5 — 2026-08-22T11:10Z（功能更新）

- 功能：字节跳动（volcengine）在厂商状态表中显示中文名，便于识别；修复 38 处文档间失效链接；audit 新增失效链接检查

## 26.2.4 — 2026-08-22T10:57Z（功能更新）

- feature: data dirs renamed (data/feed + data/view/en|zh-CN), branch cleanup + branch policy, changelog boundaries + zh translations, core-file update rules documented, pending vendors merged into tiers, opencode-go same tier

## 26.2.3 — 2026-08-22T10:29Z（内容更新）

- 修复：models.dev 同步跳过订阅类供应商（per_mtok 保持 null）；重新修正 96 个 0 价条目

## 26.1.3 — 2026-08-22T09:33（内容更新）

- 例行：价格自动同步

## 26.0.3 — 2026-08-22T15:30（功能更新）

- 功能：status 简化为 online/offline；改为每 3 小时自动检查并直接合入 main；版本递增逻辑修复（内容/功能段独立）且时间精确到分钟；删除 AGENTS 中文版；文档去重（移除 ego 文档，供应商清单与路线图合并为生成式状态文档）；文档全互链

## 26.0.2 — 2026-08-22（功能更新）

- 功能：核心检查路由（router.py）+ 工具库（toolbox.py）+ 各供应商检查脚本（checks/）；扩充贡献指南；修复每日检查 PR 创建

## 26.0.1 — 2026-08-22（功能更新）

- 功能：人类页面新增 API 地址与 Notes 列；去重检查；pr-check 强制 CHANGELOG/VERSION 更新；bump_version.py；README 星标徽章与精确统计；机器数据全英文

## 26.1.0 — 2026-08-21（功能更新）

- **收费模式修正**（内容更新）：OpenCode Go 改为订阅制记录（美元额度制；新增计划：首月 $5 / 之后 $10/月，含 $60 额度）；新增 ChatGPT Go 计划（$8/月，含广告）；436 个真正免费模型显式标注；ChatGPT 各计划额度注明"官方未公布"。
- **版本规则**：改为 `年份.内容更新.功能更新`（内容更新=定价更新）。
- **文档全双语**：所有纯文字文档提供英文默认版 + `*.zh-CN.md`。
- **仓库加固**：`main` 分支保护（仅 PR、禁 force push）；新增 `pr-check.yml`（validate + audit + 生成页一致性 + 版本一致性）；`daily-check.yml` 改为开 PR 而非直接推送；删除 `reports/`（stale 报告改走 `--stale-report`）；新增 `CONTRIBUTING` 与 issue/PR 模板、`scripts/audit.py`。
- README/AGENTS 增加项目状态声明（仍在完善、数据可能不准确）与技术栈说明（DeepSeek Harness + deepseek-v4-flash-0731）。

## 26.0.0 — 2026-08-21（初始规范化版本）

首个采用新版本规则的版本（内容为 2026-08-21 当天完成的所有工作）。

### 内容更新（定价数据）
- **订阅计划独立定价结构**：`plans.json` 每个计划新增 `pricing_model` 字段（flat_monthly / flat_yearly / per_seat_monthly / per_seat_yearly / credits / free / custom），与模型 per-MTok 定价明确区分；51 个计划全部标注。
- **修复 0 价歧义**：155 个"订阅/套餐包含"模型（coding-plan / token-plan / Copilot / Duo / Kimi-for-Coding 等 provider）的 per-MTok 价格由 `0` 改为 `null` + notes 说明"包含于订阅计划，无独立按 token 定价"，消除"0 = 免费"误读。
- **模型状态结构化**：新增 `model.status` 字段（active / preview / deprecated / retired / superseded），41 个模型已标注（OpenAI 退役系列、xAI 退役系列、DeepSeek V3 旧系、Anthropic Mythos preview 等）；人类可读页面新增状态列（❌/⚠️/🔁/🧪 显著标记）。
- 定价复核成果（DeepSeek V4、Anthropic Sonnet 5 永久价、OpenAI 5.6 系列、国内厂商官方价）随 26.0.0 一并归档。

### 功能更新（仓库）
- **官方价直采层**：`scripts/sync_official.py` + `scripts/official_sources.json`（DeepSeek / 百度 / Anthropic 官方页直抓，OpenAI Wayback 快照兜底）；每日检查按"官方 → models.dev → OpenRouter"顺序执行，官方当日已核实的 provider 免于第三方覆盖。
- **中英严格分离**：README / 人类可读页面（`data/view/` + `zh-CN/`）双语；全部文档头部增加 `Language:` 标注；文档 H1 与文件名对齐。
- **版本管理**：`VERSION` 文件 + `年份.功能.内容` 版本规则；schema 版本升级为 `26.0.0`。
- AGENTS.md（agent 指南）、docs/verification.md（真实性机制）、docs/ego-browser-workflow.md（ego-lite 复核工作流）。

### 历史背景（26.0.0 之前的工作，归档于此）
- 仓库建立：schema v1、OpenRouter（419 模型）+ models.dev（192 供应商）自动同步、双版本输出、每日检查 workflow、51 个订阅计划、全面定价复核（DeepSeek/Anthropic/OpenAI/国内厂商）。


---

## 相关文档

- [README.zh-CN.md](README.zh-CN.md) — 总览与精确统计
- [FORMAT.zh-CN.md](FORMAT.zh-CN.md) — 机器格式规范
- [docs/providers.zh-CN.md](docs/providers.zh-CN.md) — 供应商全景与状态
- [docs/price-types.zh-CN.md](docs/price-types.zh-CN.md) — 收费形式口径
- [docs/verification.zh-CN.md](docs/verification.zh-CN.md) — 核实与真实性机制
- [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md) — 如何贡献
- [AGENTS.md](AGENTS.md) — AI Agent 指南（英文）
