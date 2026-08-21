# AI Model Pricing — 全模型定价数据库

[![Daily Price Check](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/daily-check.yml/badge.svg)](https://github.com/duanjiangDJ/ai-model-pricing/actions/workflows/daily-check.yml)

收集市面上**所有可获取的 AI 模型定价**的开源数据库，覆盖多种收费形式：
API 按 token / 缓存 / 批处理 / 按图 / 按音频秒 / 按请求 / 点数制 / GPU 秒 / 订阅月费 等。

- **人类可读版**：`data/human/`（Markdown 表格，按供应商分页）
- **机器可读版**：`data/machine/`（版本化 JSON + JSON Schema，供爬虫/程序消费）
- **每日自动更新**：GitHub Actions 每天 01:23 UTC 检查上游价格并自动提交变更

## 快速开始（机器读取）

```python
import json, urllib.request

index = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/duanjiangDJ/ai-model-pricing/main/data/machine/index.json"))
print(f"{index['model_count']} models, {index['plan_count']} plans, schema v{index['schema_version']}")

# 抓取第一个供应商
entry = index["providers"][0]
provider = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/duanjiangDJ/ai-model-pricing/main/data/machine/" + entry["file"]))
```

格式规范见 [FORMAT.md](FORMAT.md)，权威 schema 见 `data/machine/schema.json`。

## 覆盖范围

| 渠道 | 说明 | 状态 |
|---|---|---|
| 官方 AI 厂商（国际） | OpenAI、Anthropic、Google、xAI、Mistral、Cohere 等 | 采集中 |
| 官方 AI 厂商（国内） | DeepSeek、Qwen、豆包、GLM、Kimi、MiniMax、阶跃、零一、百度、腾讯、讯飞 | 采集中 |
| 云平台托管 | Azure、AWS Bedrock、Vertex AI 等 | 待采集 |
| 推理托管平台 | OpenRouter（419 模型，自动同步）、Together、Groq、Cerebras、SiliconFlow 等 | OpenRouter 已自动同步，其余采集中 |
| 聚合/中转站 | OpenRouter（自动）、Poe、AIMLAPI、国内中转站（样本） | 部分 |
| 消费级订阅 | ChatGPT、Claude、Gemini、Perplexity、Poe 等 | 采集中 |
| 编码工具计划 | Copilot、Cursor、Windsurf、Claude Code、JetBrains AI 等 | 采集中 |

> 诚实声明：**没有任何单一来源覆盖全部定价**（已核实 OpenRouter / models.dev / LiteLLM 等仅覆盖 API token 定价）。
> 本仓库以「官方定价页 + 公开 API 自动同步 + 人工核实」组合方式尽量逼近全集；
> 长尾国内中转站数量以千计且随时变动，仅收录有公开定价页的代表样本，不做穷举承诺。

## 供应商全景与收费形式

- [供应商全景清单（7 大类）](docs/providers.md)
- [收费形式口径（14 种）](docs/price-types.md)

## 仓库结构

```
data/
├── machine/            # 机器可读（JSON，schema 校验）
│   ├── schema.json     # JSON Schema 1.0.0（权威定义）
│   ├── index.json      # 入口索引
│   ├── providers/      # 每供应商一文件
│   └── plans.json      # 订阅/编码计划
├── human/              # 人类可读（Markdown，由脚本生成，勿手改）
└── meta/               # manifest + changelog
scripts/                # 同步/校验/生成脚本（stdlib + jsonschema）
.github/workflows/      # daily-check.yml（每日自动检查）
docs/                   # 口径与全景文档
reports/                # 每日检查报告（如 stale-plans.md）
```

## 每日更新机制

1. `scripts/sync_openrouter.py` — 从 OpenRouter API 同步聚合转售价（419+ 模型）；
2. `scripts/daily_check.py` — 每日 diff、更新、记录 changelog、检查订阅计划过期（30 天）、重建人类可读页；
3. `scripts/validate.py` — schema + 交叉一致性校验（CI 与每日任务都会跑）；
4. 过期计划自动生成/同步 GitHub issue「每日价格核实提醒」。

手动触发：仓库 Actions → **Daily Price Check** → Run workflow。

## 开发

```bash
pip install jsonschema
python scripts/sync_openrouter.py --write   # 同步 OpenRouter
python scripts/build_human.py               # 重建人类可读页
python scripts/daily_check.py               # 每日检查（含网络）
python scripts/validate.py                  # 全量校验
```

## 贡献

- 修正价格：直接改 `data/machine/providers/<id>.json` 或 `plans.json`，更新 `verified_at` 并附 `source`（定价页 URL）；
- 新增供应商：按 `schema.json` 结构新建 `data/machine/providers/<id>.json`，再跑 `validate.py`；
- 数据错误请提 issue（注明定价页链接）。

## 免责声明

价格会随时变动，本仓库尽力及时同步但不保证实时准确。所有数据以各厂商官方定价页为准；
本仓库数据仅供参考，不构成任何购买/采购建议。价格为含税前的公开标价，实际账单以厂商结算为准。
