> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.
# 贡献指南（Contributing）

欢迎帮助改进这个定价数据库！本文说明**你能贡献什么**、**如何贡献**。所有变更一律通过 **Pull Request** 提交，并由 `.github/workflows/pr-check.yml` 自动校验（schema 校验、仓库审计、生成页一致性、版本/CHANGELOG 强制检查）。

## 能贡献什么

| # | 贡献类型 | 示例 | 难度 |
|---|---|---|---|
| 1 | **修正价格** | 错误/过时的价格、缺失的缓存/批处理字段 | ★☆☆ |
| 2 | **新增订阅计划** | 新的订阅/编码计划（附官方 URL） | ★☆☆ |
| 3 | **标记模型状态** | 凭官方证据标记模型退役/弃用 | ★☆☆ |
| 4 | **新增供应商** | 按 `docs/research-contract.md` 调研，用 `merge_research.py` 入库 | ★★☆ |
| 5 | **新的获取策略** | 可解析的官方定价页、新的 API 数据源 | ★★☆ |
| 6 | **编写厂商检查脚本** | 新增 `scripts/checks/tierN_<供应商>.py` 模块（见下） | ★★★ |
| 7 | **脚本与工具** | router、toolbox、sync/validate/audit 的改进 | ★★★ |
| 8 | **文档与翻译** | 文档、中英双版同步、README/AGENTS/CONTRIBUTING | ★☆☆ |
| 9 | **issue 排查与调研** | 核实数据错误、重新核实过期供应商 | ★☆☆ |

## 如何贡献

### 1. 修正价格 / 新增计划（最简单）

1. 编辑 `data/machine/providers/<id>.json`（模型价格/状态）或 `data/machine/plans.json`。
2. 规则：
   - 价格必须来自官方定价页/API；来源 URL 写入 `notes` 并刷新 `verified_at`；
   - 未知值填 `null`（绝不用 0、绝不编造）；`0` 仅表示真正免费；
   - 订阅包含的模型：`per_mtok: null` + notes 注明"包含于 <计划>"，绝不用 0；
   - 弃用/退役模型：`"status": "deprecated" | "retired" | "superseded"`，保留为历史条目；
   - notes 使用英文。
3. 提升版本（定价数据 = **内容更新**）：
   ```bash
   python scripts/bump_version.py --content --message "fix openai gpt-5.6-terra price"
   ```
4. 重建页面并校验：
   ```bash
   python scripts/build_human.py && python scripts/validate.py && python scripts/audit.py
   ```
5. 提交并开 PR，pr-check 必须通过。

### 2. 新增供应商

1. 在 `docs/optimization-roadmap.md` 中选定层级。
2. 收集官方定价数据（官方定价页 URL、per-MTok 价格、订阅计划）。
3. 按 `data/machine/schema.json` 创建 `data/machine/providers/<id>.json`（**必须包含 `api_base_url`**）。
4. 若通过子代理调研，按 `docs/research-contract.md` 输出并用以下命令合并：
   ```bash
   python scripts/merge_research.py <research.json>
   ```
5. 若官方页可解析，请同时新增检查脚本（见下），让数据每日自动保鲜。
6. 版本提升（新增供应商基础设施=功能更新，价格=内容更新）、重建、开 PR。

### 3. 编写厂商检查脚本（让价格每日自动更新）

每个检查脚本位于 `scripts/checks/tierN_<供应商>.py`，暴露：

```python
TIER = 0              # 路线图层级
PROVIDER_ID = "openai"
URL = "https://platform.openai.com/docs/pricing"

def run(ctx) -> dict:  # ctx: {"now": iso, "dry_run": bool}
    # 抓取官方页（toolbox.http_get / wayback 工具），解析，然后：
    changed = toolbox.update_model_prices(provider, parsed, ctx["now"], URL)
    return {"changed": len(changed), "detail": "..."}
```

**核心检查路由**（`python scripts/router.py`）会自动发现所有 checks，按层级顺序执行，
逐供应商隔离失败，并把每个检查的状态写入 `data/meta/manifest.json`。每日检查调用路由。
参考现有示例：`scripts/checks/tier0_deepseek.py`（静态页）、`tier0_openai.py`（wayback）、
`tier1_tencent.py`（已核实常量）。

**工具库**：`scripts/toolbox.py` 集中存放共享工具（http_get、to_text、JSON 读写、
changelog、index/manifest、去重辅助）。检查脚本不要重复造轮子。

### 4. 脚本与工具

- 只使用标准库 + `jsonschema`。
- 新的共享工具放 `toolbox.py`；新的厂商逻辑放 `checks/`。
- 保持每日管线顺序：官方（router）→ models.dev → OpenRouter。

### 5. 文档与翻译

- 每份纯文字文档需要英文默认版 + `*.zh-CN.md` 中文版，首行带 `> **Language:**` 标注。
- `CHANGELOG.md` 与 `CHANGELOG.zh-CN.md` 保持同步（相同的版本章节）。

## PR 自检清单（pr-check 会强制大部分）

- [ ] `python scripts/validate.py` 通过
- [ ] `python scripts/audit.py` 通过（api_base_url 完整性、无同端点重复）
- [ ] 已运行 `python scripts/build_human.py` 并提交生成页
- [ ] `VERSION` 已提升，且 `CHANGELOG.md` / `CHANGELOG.zh-CN.md` 有 `## <版本>` 章节
- [ ] 未知价格用 `null`；订阅包含模型 `null` + notes；免费 = 0 + "free" 标注
- [ ] 包含 `api_base_url`（仅订阅产品可为 null）
- [ ] `notes` 含来源 URL

## Issue 模板

- 数据错误：`.github/ISSUE_TEMPLATE/data-error.md` —— 提供供应商/模型 id、期望值、官方来源 URL。
- 功能/数据源建议：`.github/ISSUE_TEMPLATE/feature-request.md`。

## 从哪开始

在 `docs/optimization-roadmap.md` 中任选标记 ⬜ 的供应商（优先 Tier 0/1），按清单执行：
官方页 → 收费模式 → 模型清单/状态 → notes → 人类页面 → 版本提升。
或者认领标记了 `good first issue` 的 issue。


---

## 相关文档

- [README.zh-CN.md](README.zh-CN.md) — 总览与精确统计
- [FORMAT.zh-CN.md](FORMAT.zh-CN.md) — 机器格式规范
- [docs/providers.zh-CN.md](docs/providers.zh-CN.md) — 供应商全景与状态
- [docs/price-types.zh-CN.md](docs/price-types.zh-CN.md) — 收费形式口径
- [docs/verification.zh-CN.md](docs/verification.zh-CN.md) — 核实与真实性机制
- [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md) — 如何贡献
- [AGENTS.md](AGENTS.md) — AI Agent 指南（英文）
