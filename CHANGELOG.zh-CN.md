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
