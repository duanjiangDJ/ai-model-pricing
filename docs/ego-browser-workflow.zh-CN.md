> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.
# 使用 Ego (Lite) 浏览器进行官方价格重新核实

> 本仓库的 A 级数据采集方式：**官方定价页，由 AI agent 通过
> [ego-lite](https://github.com/citrolabs/ego-lite) 浏览器读取**（MIT 协议，CitroLabs 出品）。
> ego-lite 为 agent 提供共享浏览器，其高质量页面**快照（Snapshot）** 能看到纯 HTTP 抓取
> 无法获取的 JS 渲染定价表（OpenAI、Anthropic、Google……）。

## 为什么存在这一层

`sync_official.py`（CI，每日）直接抓取它所能获取的内容：
- **静态页面**（DeepSeek、百度千帆、Anthropic SSR）：仓库内解析，全自动。
- **JS 渲染页面**（OpenAI、Google）：通过 Wayback Machine 快照尽力而为 —— 这些
  快照滞后数天且可能不可靠（重定向、二进制捕获）。

ego-lite 补上了这个缺口：agent 打开*实时*定价页并读取渲染后的表格。这是可信度最高的
一层（官方页面、当前内容、人工/agent 核对）。

## 前置条件

- 已安装 [ego lite](https://github.com/citrolabs/ego-lite) 的 macOS（Windows/Linux 在路线图上）。
- 为你的 agent 添加 `ego-browser` 技能：
  ```bash
  npx skills add citrolabs/ego-lite
  ```
  或让 agent 自行配置："帮我设置 ego lite：https://github.com/citrolabs/ego-lite"。

## 重新核实工作流（单个提供商）

1. 触发：`reports/stale-plans.md` 或每日检查的 issue，或任何 `verified_at`
   早于 30 天的提供商。
2. 让 agent（Claude Code / Codex / Cursor / DSH agent）执行：
   > 使用 ego-browser 打开 `<provider>` 的 `<官方定价页>`。读取模型：`<list>`
   > 当前的每百万 tokens 价格。与 `data/machine/providers/<id>.json` 对比，
   > 并报告一份包含来源 URL 的差异表。
3. agent 驱动 ego-browser（快照 → 滚动 → 快照），提取渲染后的价格。
4. 将结果按研究契约 JSON 格式（见 `docs/research-contract.md`）写入
   `pricing_research/<id>_pricing.json`，然后：
   ```bash
   python scripts/merge_research.py pricing_research/<id>_pricing.json
   python scripts/validate.py && python scripts/build_human.py
   ```
5. 提交时在提交信息中附上官方页面 URL。

## 建议用 ego-lite 重新核实的提供商（当前缺口）

| 提供商 | 官方页面 | 为何 ego-lite 是合适的工具 |
|---|---|---|
| OpenAI | https://platform.openai.com/docs/pricing | 完全 JS 渲染；wayback 滞后 |
| Google | https://ai.google.dev/gemini-api/docs/pricing | 嵌套促销表；解析器已禁用 |
| xAI | https://docs.x.ai/developers/pricing | JS 渲染 |
| Mistral / Cohere / 其他 | 厂商定价页 | JS 渲染，优先级低 |

## 规则

- 价格必须来自渲染后的官方页面；记录 URL 与 `verified_at`。
- 对 A 级数据，**不要**信任第三方聚合页面的 ego-browser 快照。
- 合并之后，每日检查会保护该提供商免受 models.dev 覆盖
  （它会跳过 `verified_at` 为今天的提供商）。
