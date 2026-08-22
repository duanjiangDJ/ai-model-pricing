> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.
# AGENTS.md — 本仓库 AI Agent 工作指南

本文件告知 AI 代理（以及人类）正确读取、校验和更新本仓库所需的全部信息。改动前请通读全文。

## ⚠️ 项目状态

**本仓库仍在完善中。** 数据可能过时、不完整或有误；部分收费模式难以核实。请把所有条目视为"截至某时点"的数据：
- 信任某个数字前先查 `verified_at` / `updated_at` 与 `notes`（来源）；
- `null` 表示未知/不提供——绝不编造数值，绝不用 0 表示"未知"；
- 订阅包含的模型 `per_mtok` 为 `null` + notes 说明（绝不用 0）；
- 弃用/退役模型带 `"status"` 字段并保留为历史条目。

欢迎通过 issue 与 PR 贡献（见 `CONTRIBUTING.md`）；`main` 受分支保护——所有变更一律走 PR，由 `.github/workflows/pr-check.yml` 校验。

**项目技术栈**：本仓库基于 [DeepSeek Harness](https://github.com/deepseek-ai/DeepSeek-Harness) 框架、使用 **deepseek-v4-flash-0731** 模型维护。

## 本仓库是什么

`ai-model-pricing` 是一个涵盖所有可获得渠道的 **AI 模型定价** 开放数据库：官方厂商 API（per-MTok、缓存、批处理）、图像/音频定价、点数系统、GPU 按小时计费、消费级订阅以及编码工具计划。

- 机器可读数据：`data/machine/`（版本化 JSON + JSON Schema）
- 人类可读页面：`data/human/`（Markdown，**自动生成** —— 切勿手工编辑）
- 由 GitHub Actions 每日自动更新：`.github/workflows/daily-check.yml`

## 仓库结构

```
data/machine/
  schema.json            # THE authoritative JSON Schema (26.0.0)
  index.json             # Entry point: providers/resellers lists, counts, timestamps
  providers/*.json       # One file per provider (provider_id.json)
  plans.json             # Subscription & coding-tool plans
data/meta/
  manifest.json          # Sync health: sources, last_ok/last_error
  changelog.json         # Every change (add/update/remove/verify), newest first
data/human/              # GENERATED. en: *.md, zh-CN: zh-CN/*.md
docs/                    # providers.md (landscape), price-types.md, research-contract.md,
                         # optimization-roadmap.md, verification.md
scripts/
  router.py              # 核心检查路由：发现 checks/，按层级顺序执行
  toolbox.py             # 共享工具库（http、JSON、changelog、manifest、去重）
  checks/                # 各厂商官方价检查脚本（tierN_<供应商>.py）
  daily_check.py         # 每日入口：router（官方）-> models.dev -> OpenRouter
  sync_official.py       # 独立官方源同步（official_sources.json 注册表）
  sync_openrouter.py     # OpenRouter 目录同步（聚合转售价）
  sync_modelsdev.py      # models.dev 目录同步
  validate.py            # schema + 一致性校验
  audit.py               # 仓库审计（版本、计数、0 价策略、文档双语）
  build_human.py         # 生成人类页面（en + zh-CN）
  stats.py               # README 精确统计
  bump_version.py        # 版本提升（年份.内容.功能）+ changelog
  merge_research.py      # 合并调研子代理 JSON 输出
CONTRIBUTING.md        # contribution guide (en + zh-CN)
```

## 读取数据（面向构建工具的 agent）

1. 先抓取 `data/machine/index.json`。检查 `schema_version`（主版本号提升 = 不兼容变更）。
2. 每个 `providers[]` / `resellers[]` 条目包含 `file`（相对路径）、`model_count`、`updated_at`。
3. 模型结构：`{id, name, category, status, modalities, context_window, max_output, pricing, notes}`。
   `status` = active | preview | deprecated | retired | superseded —— deprecated/retired/superseded 模型为历史条目，在人类可读页面带有醒目的状态标记。
4. `pricing` 字段（除非 `currency` 另有说明，否则均为 USD / 1M tokens）：
   - `per_mtok.{input,output,cache_read,cache_write}`
   - `batch.{input,output}` — 批处理 API 五折
   - `per_image[]` — 图像模型分档
   - `per_audio_second`、`per_character`、`per_request`、`credits`（点数制）、
     `gpu[]`（按秒/小时的 SKU）、`neuron_second`、`finetune`、`provisioned`
5. **`null` 表示"未提供 / 未知"——切勿当作 0 处理。** `0` 表示免费。
6. 计划：`{id, provider_id, product, plan, category, pricing_model, billing, price_usd, limits, includes, url, verified_at}`。
   `pricing_model`（flat_monthly / flat_yearly / per_seat_monthly / per_seat_yearly / credits / free / custom）是订阅的**定价模型** —— 与按 token 的模型定价严格区分。年付计划在 `price_usd` 中记录**年总价**；按席位计划记录每席位价格。
   订阅计划包含的模型 `per_mtok` = null（绝非 0），并附说明性 notes。
7. `channel` 语义：`first_party` | `cloud` | `hosted` | `aggregator` | `reseller` | `subscription`。
   同一模型可能以不同价格出现在多个渠道 —— 这是正确的。

## 更新数据（你必须遵守的规则）

1. **价格必须来自官方定价页 / 官方 API / 官方文档**，尽可能通过至少一个次要来源核实。记录 `source` URL 和 `verified_at`（核实时间）。
2. 直接编辑 `data/machine/providers/<id>.json` 或 `plans.json`；**切勿编辑 `data/human/`**（改为运行 `python scripts/build_human.py` —— 它会重新生成 en 与 zh-CN 两种页面）。
3. 任何数据变更后，运行 `python scripts/validate.py`（需要 `pip install jsonschema`）。它会检查 schema 符合性、index 数量一致性以及重复模型 id。
4. 价格变化时：更新数值以及 `verified_at`/`updated_at`，然后追加一条 `changelog.json` 记录（`kind: update|add|remove`，`scope: model|plan|provider`，`old`/`new`）。
5. deprecated/retired 模型保留在文件中，`pricing` 全部为 `null`，并以 `notes` 说明退役原因 + 替代模型。切勿静默删除。
6. 非 USD 的 provider（CNY 等）：在 provider 上设置 `currency`/`price_currency`，并在 `currency_usd_note` 中说明换算方式。
7. 研究子代理的输出可自动合并：`python scripts/merge_research.py <research.json>`（格式契约：`docs/research-contract.md`）。

## 自动化（每日检查）

`.github/workflows/daily-check.yml`（cron 01:23 UTC）运行 `scripts/daily_check.py`：
1. 抓取 OpenRouter 目录 → diff `providers/openrouter.json` → 更新变化的价格并写入 changelog。
2. 抓取 models.dev 目录 → 在存在差异处更新 `per_mtok.input/output/cache_read`（绝不触碰手工维护的字段，如 `batch` 或 `cache_write`）。
3. 刷新 `index.json` 计数；重建人类可读页面；更新 `manifest.json`。
4. 标记 `verified_at` 超过 30 天的计划 → `--stale-report` markdown → 同步「每日价格核实提醒」GitHub issue。
5. 以 bot 身份提交变更（`[skip ci]`）；若无任何变化则干净退出。

**真实性保证**（及其局限）：
- 自动同步源（OpenRouter、models.dev）每日刷新；这些是这两个平台转发的价格，而它们本身也是聚合 —— 请视作"as-of"（截至某时点）数据。
- 人工核实的条目带有 `verified_at` + `source` URL；过期条目会出现在 stale-plans issue 中，供人工重新核实。
- 本仓库不会虚构或猜测价格：未知值一律为 `null` 并附 `notes`，绝不编造数字。

## 贡献流程

1. Fork → 编辑机器数据 → `validate.py` → `build_human.py` → 提交信息中写明改动了哪个 provider/哪些价格及来源。
2. PR 必须包含所用的定价页 URL。
3. 大型新增（新厂商）请遵循 `docs/research-contract.md`，并通过 `scripts/merge_research.py` 合并。

## 常用命令

```bash
pip install jsonschema
python scripts/sync_openrouter.py --write   # pull OpenRouter catalog (aggregator prices)
python scripts/sync_modelsdev.py --write    # pull models.dev (official-ish list prices)
python scripts/merge_research.py x.json     # merge subagent research output
python scripts/daily_check.py               # full daily check (network)
python scripts/build_human.py               # regenerate human pages (en + zh-CN)
python scripts/validate.py                  # schema + consistency validation
```
