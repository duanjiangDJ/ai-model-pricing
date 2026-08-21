> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.

# 供应商优化路线图（Provider Optimization Roadmap）

所有供应商的优化顺序：从**核心模型研发厂商**出发，一步步延伸到外围。
每家供应商的优化项：官方定价页核实、收费模式审计、模型清单去重、notes 本地化、人类可读页面复查。

图例：✅ = 本轮已人工核实 · ⬜ = 待优化 · (n) = 库内模型数

---

## Tier 0 — 全球核心模型研发厂商（最高优先级，逐家）

| # | 供应商 | 模型数 | 说明 |
|---|---|---|---|
| 1 | OpenAI | 47 | GPT-5.6 全系；官方快照管线已就绪 |
| 2 | Anthropic | 16 | Fable/Opus/Sonnet/Haiku；2026-08 已核实 |
| 3 | Google DeepMind | 40 | Gemini 3.x/2.5；JS 渲染页解析器未启用——需 ego-browser 复核 |
| 4 | xAI | 17 | Grok 4.x；2026-08 已核实 |
| 5 | DeepSeek | 5 | V4 系列峰谷双档；2026-08 已核实 |
| 6 | Meta | 3 | 无官方 API——通过托管伙伴追踪 Llama |
| 7 | Mistral AI | 33 | La Plateforme 价格需重新核实 |
| 8 | Cohere | 14 | Command/Embed/Rerank 价格需重新核实 |
| 9 | Amazon（Nova/Titan） | 120 | 经 Bedrock；同时属 Tier 2 云平台 |
| 10 | NVIDIA | 100 | NIM 目录；多为免费条目，需核实 |
| 11 | Perplexity | 26 | Sonar API + 订阅 |

## Tier 1 — 中国核心模型研发厂商（逐家）

| # | 供应商 | 模型数 | 说明 |
|---|---|---|---|
| 12 | 阿里 Qwen（alibaba / alibaba-cn） | 54+86 | 百炼官方 CNY 价格 |
| 13 | 智谱 GLM（zhipuai / zai） | 16+16 | open.bigmodel.cn + z.ai |
| 14 | 月之暗面 Kimi（moonshotai） | 14 | 含 Kimi Code 计划 |
| 15 | 字节豆包（volcengine） | 2 | 火山方舟官方 CNY 价——需扩充模型清单 |
| 16 | MiniMax | 7 | 含 Token Plan |
| 17 | 百度 ERNIE（baidu） | 3 | 千帆官方文档——需扩充模型清单 |
| 18 | 腾讯混元（tencent / tencent-tokenhub） | 1+2 | TokenHub 计费——需扩充 |
| 19 | 阶跃星辰（stepfun / stepfun-step-plan） | 8+4 | platform.stepfun.com |
| 20 | 小米 MiMo（xiaomi） | 10 | mimo.mi.com 官方文档 |
| 21 | 零一万物 | — | **未收录**——需新增 |
| 22 | 科大讯飞星火 | — | **未收录**——需新增 |
| 23 | 百川智能 | — | **未收录**——需新增 |

## Tier 2 — 云平台托管（承载官方模型）

| # | 供应商 | 模型数 | 说明 |
|---|---|---|---|
| 24 | Microsoft Azure | 84 | azure 与 azure-cognitive-services 已合并 |
| 25 | Google Vertex | 42 | gemini + claude-on-vertex |
| 26 | AWS Bedrock | 120 | 已并入 amazon-bedrock |
| 27 | 阿里云国际版 | 86 | dashscope-intl |

## Tier 3 — 核心推理托管平台（逐家）

Together AI (36) · Groq (15) · Cerebras (2) · DeepInfra (60) · SiliconFlow (61) ·
Fireworks AI (23) · Novita AI (107) · Nebius (34) · Baseten (19) · Modal (2) ·
Hugging Face (69) · Cloudflare Workers AI (25) · Scaleway (14) · OVHcloud (14) ·
Vultr (10) · DigitalOcean (92) · Databricks (30) · Snowflake Cortex (25) · watsonx (5) ·
SAP AI Core (48)

## Tier 4 — 聚合/网关（逐家）

OpenRouter (420) · OpenCode Zen (63) / Go (23) · Poe (137) · Vercel AI Gateway (350) ·
LLMGateway/DevPass (556) · Kilo (363) · OrcaRouter (81) · Cloudflare AI Gateway (67) ·
Merge Gateway (174) · FastRouter (47) · UnoRouter (23) · 302AI (97) · AIHubMix (70) ·
Requesty (139) · AnyAPI (30) · NanoGPT (597) · Eden AI (232) · ZenMux (120) · 其他

## Tier 5 — 订阅与编码产品（逐家）

ChatGPT（Plus/Go/Pro/Codex）· Claude（Pro/Max/Claude Code）· GitHub Copilot (33) ·
Cursor · Windsurf · JetBrains AI · Devin · Kimi Code（4 档）· MiniMax Token Plan ·
小米 Token Plan（4 档）· OpenCode Go (23) · Replit · Tabnine · v0 · Poe（点数制）

## Tier 6 — 长尾（按模型数从多到少分批）

**批次 A（≥50）**：abacus (108) · cortecs (108) · ofox (107) · pioneer (103) · venice (99) ·
qiniu-ai (91) · helicone (90) · impossibl (76) · jiekou (61) · empiriolabs (55) ·
crossmodel (52) · neon (42)
**批次 B（20–49）**：kenari (38) · greenpt (37) · nearai (37) · llmtr (32) · wandb (29) ·
crof (26) · frogbot (26) · hyper (26) · tensorx (25) · neuralwatt (22) · ollama-cloud (20) ·
vivgrid (20) · meganova (19) · regolo-ai (18) · io-net (17) · jalapeno (17) · zai (16) ·
scnet-token-plan (16)
**批次 C（10–19）**：auriko (15) · evroc (15) · model-oracle-ai (15) · routing-run (15) ·
chutes (14) · iflowcn (14) · ovhcloud (14) · scaleway (14) · gmicloud (13) · xpersona (13) ·
clarifai (12) · inferx (12) · cline-pass (11) · ambient (10) · freemodel (10) ·
infomaniak (10) · vultr (10) · xiaomi (10) · aiand (9) · berget (9) · daoxe (9) ·
hpc-ai (9) · inference (9) · modelis (9) · qihang-ai (9) · qvac (9) · submodel (9) ·
the-grid-ai (9) · crusoe (8) · stackit (8) · synthetic (8) · tinfoil (8) · arcee (7) ·
llama (7) · modelscope (7) · privatemode-ai (7) · aki-io (6) · dinference (6)
**批次 D（≤5）**：atomic-chat (5) · cloudferro-sherlock (5) · friendli (5) · mixlayer (5) ·
runinfra (5) · wafer.ai (5) · watsonx (5) · ebcloud (4) · inceptron (4) · lilac (4) ·
lucidquery (4) · sakana (4) · scx-ai (4) · upstage (4) · coralbricks (3) · drun (3) ·
lmstudio (3) · morph (3) · poolside (3) · abliteration-ai (2) · bailing (2) · blueclaw (2) ·
cerebras (2) · claudinio (2) · hetzner (2) · inception (2) · moark (2) · modal (2) ·
nova (2) · sarvam (2) · subconscious (2) · thinkingmachines (2) · amd (1) · echo (1) ·
kosmik (1) · longcat (1) · lynkr (1) · zeldoc (1) · zenifra (1)

## 每家供应商的优化清单

1. 官方定价页/API：抓取、解析、核实（官方优先层）。
2. 收费模式审计：per-MTok / per-request / per-image / credits / 订阅。
3. 模型清单：按 api_base_url 去重，退役/弃用模型标 `status`。
4. notes：英文，带来源 URL 与 verified_at。
5. 订阅计划（如有）：pricing_model + limits/includes 英文。
6. 人类页面：`build_human.py` 重建（含 api_base_url 与 Notes 列）。
7. 版本提升（内容更新）+ changelog + 走 PR（pr-check 校验）。
