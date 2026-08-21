<!-- 感谢提交 PR！请填写以下内容（中英文均可）-->

## 变更类型 / Change type
- [ ] 内容更新（定价数据）/ Content update (pricing data)
- [ ] 功能更新（脚本/文档/结构）/ Feature update (scripts/docs/structure)

## 数据来源 / Data source
<!-- 修改价格必须附官方定价页/文档 URL -->
- URL: 

## 涉及文件 / Files changed
- [ ] `data/machine/providers/*.json` / `plans.json`
- [ ] `VERSION` / `schema.json` / `index.json#schema_version`（版本号已同步修改）
- [ ] `data/human/`（已运行 `python scripts/build_human.py` 重新生成）
- [ ] `data/meta/changelog.json`（已追加条目）

## 自检 / Self-check
- [ ] `python scripts/validate.py` 通过
- [ ] 未知价格使用 `null`（未用 0 表示未知）
- [ ] 订阅包含的模型 `per_mtok: null` + notes 说明
- [ ] 过时模型已标注 `status`
