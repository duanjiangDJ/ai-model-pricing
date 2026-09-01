> **Language: 中文（简体）(zh-CN)** — This document is written in zh only.
# AI Model Pricing — 全模型定价数据库

[![Daily Price Check](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/daily-check.yml/badge.svg)](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/daily-check.yml)
[![PR Check](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/pr-check.yml/badge.svg)](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/pr-check.yml)
[![GitHub Stars](https://img.shields.io/github/stars/duanjiangDJ/ai-model-pricing?style=social&label=Stars)](https://github.com/duanjiangDJ/ai-model-pricing/stargazers)

收集市面上**所有可获取的 AI 模型定价**的开源数据库，覆盖多种收费形式：
API 按 token（输入/输出/缓存/批处理）、按图、按音频秒、按请求、点数制、GPU 秒、消费订阅、编码工具计划等。

- **人类可读版**：`data/view/`（Markdown 表格，按供应商分页）— 默认英文，中文版见 `data/view/zh-CN/`
- **机器可读版**：`data/feed/`（版本化 JSON + JSON Schema，供爬虫/程序消费）
- **自动更新**：GitHub Actions 每 3 小时（cron 0 */3 * * *）检查上游价格并**自动合入 main**

> English version: [README.md](README.md)

## ⚠️ 项目状态声明——请先阅读

**本仓库仍在完善中，数据不保证完整与准确。**

- 价格变动极快，部分条目可能**过时、有误或缺失**；
- 部分收费模式（按请求、点数制、订阅包含用量）难以核实，可能存在标注错误；不确定的条目以 `null`/notes 标注并带 `verified_at`；
- 长尾覆盖（国内中转站、企业定制价）有意保持部分收录；
- **欢迎一切贡献**：发现错误或建议新的数据来源/获取策略请提 **issue**；修正价格或改进采集管线请提 **PR**（见 [CONTRIBUTING.md](CONTRIBUTING.md)）。人工更改一律走 PR + 自动校验（含安全审查）；bot 价格同步直接合入 main。（`pr-check.yml`：schema 校验、生成页面一致性、版本一致性）。

**项目技术栈**：本仓库最初基于 [DeepSeek Harness](https://github.com/deepseek-ai/DeepSeek-Harness) 、使用 **deepseek-v4-flash-0731** 模型维护。数据获取结合官方定价页直采（`scripts/sync_official.py`）、公开目录（models.dev、OpenRouter）与人工/Agent 核实。

<!-- STATS:BEGIN -->

## 数据统计（精确值）

- **供应商数**：190
- **模型数**：7465
- **订阅计划数**：67
- **去重后的 API 端点数**：183
- **免费模型数**：472

### 按渠道

| 渠道 | 供应商 | 模型 |
|---|---|---|
| 推理托管 | 138 | 4462 |
| 官方直供 | 20 | 417 |
| 订阅产品 | 18 | 175 |
| 聚合站 | 13 | 2291 |
| 云平台托管 | 1 | 120 |

### 按地区

| 地区 | 供应商 |
|---|---|
| Global | 175 |
| US | 9 |
| China | 6 |

### 模型状态分布

| 状态 | 模型数 |
|---|---|
| offline | 43 |
| online | 18 |
| （未标注） | 7404 |

### 模型数 Top 15 供应商

| 供应商 | 模型数 |
|---|---|
| NanoGPT（`nano-gpt`） | 684 |
| DevPass (LLM Gateway)（`llmgateway`） | 560 |
| OpenRouter（`openrouter`） | 425 |
| Kilo Gateway（`kilo`） | 375 |
| Vercel AI Gateway（`vercel`） | 366 |
| Eden AI（`edenai`） | 246 |
| Merge Gateway（`merge-gateway`） | 176 |
| Requesty（`requesty`） | 142 |
| Poe（`poe`） | 137 |
| OrcaRouter（`orcarouter`） | 124 |
| ZenMux（`zenmux`） | 120 |
| Amazon Web Services（`aws`） | 120 |
| Ofox（`ofox`） | 112 |
| Cortecs（`cortecs`） | 112 |
| Abacus（`abacus`） | 108 |

### 按计价币种

| 币种 | 供应商 |
|---|---|
| USD | 186 |
| CNY | 4 |

<!-- STATS:END -->

## 文档索引

| 文档 | 内容 |
|---|---|
| [README.md](README.md) | English version |
| [FORMAT.zh-CN.md](FORMAT.zh-CN.md) | 机器可读格式规范 |
| [CHANGELOG.zh-CN.md](CHANGELOG.zh-CN.md) | 版本历史（年份.内容.功能） |
| [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md) | 贡献指南 |
| [docs/providers.zh-CN.md](docs/providers.zh-CN.md) | 供应商全景与状态（自动生成表） |
| [docs/price-types.zh-CN.md](docs/price-types.zh-CN.md) | 收费形式口径 |
| [docs/verification.zh-CN.md](docs/verification.zh-CN.md) | 每日检查与真实性机制 |
| [AGENTS.md](AGENTS.md) | AI Agent 指南（英文） |

## 快速开始（机器读取）

```python
import json, urllib.request

index = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/duanjiangDJ/ai-model-pricing/main/data/feed/index.json"))
print(f"{index['model_count']} models, {index['plan_count']} plans, schema v{index['schema_version']}")

# 抓取第一个供应商
entry = index["providers"][0]
provider = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/duanjiangDJ/ai-model-pricing/main/data/feed/" + entry["file"]))
```

格式规范见 [FORMAT.md](FORMAT.md)，权威 schema 见 `data/feed/schema.json`，
给 AI agent 的读写指南见 [AGENTS.md](AGENTS.md)。

## 覆盖范围

| 渠道 | 说明 | 状态 |
|---|---|---|
| 官方 AI 厂商（国际） | OpenAI（GPT-5.6 全系 47 模型）、Anthropic（Fable/Opus/Sonnet/Haiku 13 模型）、Google Gemini 3.x/2.5、xAI Grok 4.x、Mistral、Cohere 等 | ✅ 已入库 |
| 官方 AI 厂商（国内） | DeepSeek、Qwen/阿里、豆包 2.1、GLM/智谱、Kimi、MiniMax、阶跃、百度 ERNIE 5.x、腾讯混元 Hy3 等 | ✅ 主要已入库 |
| 云平台托管 | AWS Bedrock、Azure、Vertex 等（models.dev 收录部分） | 部分 |
| 推理托管平台 | OpenRouter（419 模型自动同步）、Together、Groq、Cerebras、SiliconFlow、DeepInfra、Novita、Nebius 等 | ✅ 已入库 |
| 聚合/中转站 | OpenRouter（自动）、Poe、orcarouter、aihubmix 等；国内长尾中转站按文档策略收录样本 | 部分 |
| 消费级订阅 | ChatGPT Plus/Pro、Claude Pro/Max、Gemini AI、Perplexity、SuperGrok、Poe 等 | ✅ 已入库 |
| 编码工具计划 | Copilot、Cursor、Windsurf、Claude Code、JetBrains AI、Devin、Amazon Q、Replit、Tabnine 等 | ✅ 已入库 |

**当前规模**：204 个供应商、7,700+ 模型（含 OpenRouter 419 个聚合转售价）、51 个订阅计划，
数据每日自动同步（OpenRouter + models.dev），人工核实条目带 `verified_at` 与来源。

> 诚实声明：**没有任何单一来源覆盖全部定价**（已核实 OpenRouter / models.dev / LiteLLM 等仅覆盖 API token 定价）。
> 本仓库以「官方定价页 + 公开 API 自动同步 + 人工核实」组合方式尽量逼近全集；
> 长尾国内中转站数量以千计且随时变动，仅收录有公开定价页的代表样本，不做穷举承诺。

## 供应商全景与收费形式

- [供应商全景清单（7 大类）](docs/providers.md)
- [收费形式口径（17 种）](docs/price-types.md)

## 仓库结构

```
data/
├── machine/            # 机器可读（JSON，schema 校验）
│   ├── schema.json     # JSON Schema 1.0.0（权威定义）
│   ├── index.json      # 入口索引
│   ├── providers/      # 每供应商一文件
│   └── plans.json      # 订阅/编码计划
├── human/              # 人类可读（Markdown，脚本生成；en + zh-CN/）
└── meta/               # manifest + changelog
scripts/                # 同步/校验/生成脚本（stdlib + jsonschema）
.github/workflows/      # daily-check.yml（每日自动检查）
docs/                   # 全景、口径、调研契约
reports/                # 每日检查报告（如 stale-plans.md）
AGENTS.md               # 给 AI agent 的仓库指南
```

## 每日更新机制

1. `scripts/sync_openrouter.py` — 从 OpenRouter API 同步聚合转售价（419+ 模型）；
2. `scripts/daily_check.py` — 每日 diff（OpenRouter + models.dev）、更新、记录 changelog、
   检查订阅计划过期（30 天）、重建人类可读页；
3. `scripts/validate.py` — schema + 交叉一致性校验（CI 与每日任务都会跑）；
4. 过期计划自动生成/同步 GitHub issue「每日价格核实提醒」。

手动触发：仓库 Actions → **Daily Price Check** → Run workflow。

## 开发

```bash
pip install jsonschema
python scripts/sync_openrouter.py --write   # 同步 OpenRouter
python scripts/sync_modelsdev.py --write    # 同步 models.dev 供应商
python scripts/merge_research.py x.json     # 合并调研子代理结果
python scripts/build_human.py               # 重建人类可读页（en + zh-CN）
python scripts/daily_check.py               # 每日检查（含网络）
python scripts/validate.py                  # 全量校验
```

## 贡献

- 修正价格：直接改 `data/feed/providers/<id>.json` 或 `plans.json`，更新 `verified_at` 并附 `source`（定价页 URL）；
- 新增供应商：按 `schema.json` 结构新建 `data/feed/providers/<id>.json`，再跑 `validate.py`；
- 数据错误请提 issue（注明定价页链接）。

## 免责声明

价格会随时变动，本仓库尽力及时同步但不保证实时准确。所有数据以各厂商官方定价页为准；
本仓库数据仅供参考，不构成任何购买/采购建议。价格为含税前的公开标价，实际账单以厂商结算为准。
