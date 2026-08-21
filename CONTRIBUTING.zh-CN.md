> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.
# 贡献指南（Contributing）

欢迎帮助改进这个定价数据库！所有变更一律通过 **Pull Request** 提交，并由
`.github/workflows/pr-check.yml` 自动校验：
1. `python scripts/validate.py` — JSON Schema + 交叉一致性检查；
2. `python scripts/build_human.py` + `git diff --exit-code` — 生成页面必须重新生成；
3. 版本一致性 — `VERSION` == `schema.json#version` == `index.json#schema_version`。

`main` 分支受分支保护，禁止直接推送。

## 报告数据错误（issue）

请提供：
- 供应商 id 与模型 id（如 `openai` / `gpt-5.6-terra`）或计划 id；
- **期望价格**与核实所用的**官方定价页 URL**；
- （可选）修改建议。

## 建议新功能/新数据源（issue）

- 新供应商、新收费模式、新数据源或获取策略——请描述来源 URL 与获取方式（静态页？API？JS 渲染？是否需要浏览器？）。

## 修正数据（PR）

1. 编辑 `data/machine/providers/<id>.json` 或 `data/machine/plans.json`。
2. 规则：
   - 价格必须来自官方定价页/API；在 `notes` 记录 `verified_at`（UTC）与来源 URL；
   - 未知值填 `null`（绝不用 0，绝不编造）；`0` 仅表示真正免费；
   - 订阅包含的模型：`per_mtok` = `null` + notes 注明"包含于 <计划>"，绝不用 0；
   - 弃用/退役模型设置 `"status": "deprecated" | "retired" | "superseded"`，保留为历史条目；
   - 在 `data/meta/changelog.json` 追加条目（`kind: update|add|remove`、`old`/`new`）；
   - 定价数据变更：提升版本的**内容更新**段；其他变更提升**功能更新**段——`VERSION`、
     `schema.json#version`、`index.json#schema_version` 三者必须同步修改（规则见 `CHANGELOG.md`）。
3. 运行 `python scripts/validate.py`，再运行 `python scripts/build_human.py`（重新生成 `data/human/`）。
4. 提交并开 PR，校验必须通过。

## 改进脚本/文档（PR）

- 脚本仅使用标准库 + `jsonschema`。保持 `null` 语义，保持每日检查管线（官方 → models.dev → OpenRouter）不变。
- 所有纯文字文档必须有英文默认版 + `*.zh-CN.md` 中文版，首行带 `> **Language:**` 标注。

## 风格

- 供应商文件：`provider_id` 用稳定的 kebab-case；模型 `id` 优先使用官方 API id。
- notes 默认英文；中文 notes 加 `[zh]` 标记。
- 生成文件（`data/human/`、`index.json`、`changelog.json`、`manifest.json`）通过运行生成器保持同步——**绝不手改**。
