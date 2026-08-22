> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.
# 验证与真实性模型

每日检查如何运作，以及本仓库数据的准确性得到了哪些保证（以及未得到哪些保证）。

## 1. 每日检查流水线（`.github/workflows/daily-check.yml`，cron 01:23 UTC）

`scripts/daily_check.py` 每天执行以下步骤：

0. **官方价格层** — `scripts/sync_official.py` **直接抓取官方定价页**（来源注册表：`scripts/official_sources.json`）：
   - 直接抓取并解析：DeepSeek、百度千帆、Anthropic（静态/SSR 页面）；
   - Wayback 快照兜底：OpenAI（JS 渲染）、Google（暂禁用，待更好的解析器）；
   - 解析得到的值更新 `per_mtok.{input,output,cache_read,cache_write}`/`batch`，即使价格未变也刷新 `verified_at`（"今日已检查"），并在 manifest 中记录每个来源的 `last_ok`/`last_error`。
1. **OpenRouter 差异比对** — 抓取 `https://openrouter.ai/api/v1/models`（完整目录），将每个模型的定价与 `data/feed/providers/openrouter.json` 对比：
   - 新模型 → `kind: add` changelog 条目
   - 移除的模型 → `kind: remove`
   - 价格变化 → 更新并追加 `kind: update` 条目，含 `old`/`new` 值
2. **models.dev 差异比对** — 抓取 `https://models.dev/api.json`（192+ 个提供商），凡有差异即更新三个每百万 tokens 字段（`input`、`output`、`cache_read`）。
   它刻意**不**覆盖人工维护的字段（`batch`、`cache_write`、notes、plans），以免人工工作被覆盖。**`verified_at` 为今天（刚被官方层核实过）的提供商会整段跳过** —— 第三方转载不得覆盖官方检查结果。
3. **索引刷新** — 按提供商重新计算 `index.json` 的模型数量。
4. **过期计划检查** — 任何 `verified_at` 早于 30 天的计划都会列在 `reports/stale-plans.md` 中，并同步到 "每日价格核实提醒" GitHub issue，从而请求人工重新核实。
5. **人工页面重建** — 由机器数据重新生成 `data/view/`（en + zh-CN）。
6. **Manifest 更新** — 记录 `last_daily_check`、各来源的 `last_ok` / `last_error`。
7. **提交** — 若有任何变更，以机器人身份提交（`[skip ci]`）并推送。若无变更，则干净退出，不产生提交。

工作流每次运行还会执行 `scripts/validate.py`（JSON Schema + 索引计数一致性 + 重复 id 检查）；校验失败会导致工作流运行失败。

## 2. 数据来源层级与真实性保证

| 层级 | 来源 | 更新节奏 | 可信度 |
|---|---|---|---|
| A+. 官方页面（agent 经 ego-browser） | 由 AI agent 通过 ego-lite 浏览器读取的实时 JS 渲染官方页面 | 按需，按重新核实活动执行 | 最高 —— 当前官方页面，已渲染 |
| A. 官方页面（直接解析） | 仓库内直接解析的静态/SSR 官方页面（DeepSeek、百度、Anthropic）+ JS 页面的 Wayback 快照 | 每日自动同步（`sync_official.py`） | 高 —— 直接来自厂商（快照可能滞后） |
| B. models.dev | 第三方维护的官方挂牌价转载 | 每日自动同步（A/A+ 今日已核实时跳过） | 第一方条目可信度高；仍属第三方转载 |
| C. OpenRouter API | 转售商/聚合商价格（OpenRouter 实际收取的价格） | 每日自动同步 | 作为 OpenRouter 的价格是正确的；与官方价格存在设计性差异 |

我们确实提供的保证：

- **可追溯性** — 每条记录都有 `verified_at`（UTC），人工核实的数据还有 `source` URL（定价页或官方文档）。`changelog.json` 保留每次变更的完整历史（old → new），因此数据库中的任何数字都能追溯到其来源时间与来源位置。
- **绝不编造** — 未知价格存为 `null` 并附说明性 `notes`；`0` 仅表示"免费"。任何数字都不会被猜测或外推（显式标注的换算除外，如按指定汇率 CNY→USD）。
- **过期暴露** — 超过 30 天的计划自动提出 GitHub issue；自动同步的价格带有 `updated_at`，供使用者自行判断时效性。
- **机械一致性** — 每个文件都通过 `schema.json` 校验；索引计数根据实际文件重新计算；重复的模型 id 会被拒绝。

我们明确**不**提供的保证：

- 自动同步层级（B/C）是第三方*转载* —— 若其上游数据有误或过期，在下次同步之前我们的数据同样有误或过期。我们不会直接爬取每家厂商的网站（多数定价页是 JS 渲染且形态不断变化）。
- 长尾（数千家国内转售商、企业定制价、预置吞吐）无法穷尽追踪；README 如实声明了这一范围。
- 价格随时可能变化；该数据库是"截至某时点"的数据，不是实时报价服务。

## 3. 重新核实活动

周期性（例如模型发布或价格战之后）会执行一次完整的重新核实：调研子代理按厂商检查官方文档，将结果写入 `pricing_research/*.json`，再经 `scripts/merge_research.py` 合并（按模型 id upsert，并刷新 `verified_at`）。这些活动的契约记录在 `docs/research-contract.md`。

## 4. 如何自行核对某个具体数字

1. 读取条目：`data/feed/providers/<id>.json` → model → `pricing` + `notes`。
2. 记下 `verified_at`（人工）或 `updated_at`（自动同步）以及 `source` URL。
3. 对自动同步的值，`data/meta/changelog.json` 显示其最后变更时间。
4. 打开来源 URL 并对比。如有出入，请修正或提出 issue。


---

## 相关文档

- [README.zh-CN.md](README.zh-CN.md) — 总览与精确统计
- [FORMAT.zh-CN.md](FORMAT.zh-CN.md) — 机器格式规范
- [docs/providers.zh-CN.md](docs/providers.zh-CN.md) — 供应商全景与状态
- [docs/price-types.zh-CN.md](docs/price-types.zh-CN.md) — 收费形式口径
- [docs/verification.zh-CN.md](docs/verification.zh-CN.md) — 核实与真实性机制
- [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md) — 如何贡献
- [AGENTS.md](AGENTS.md) — AI Agent 指南（英文）
