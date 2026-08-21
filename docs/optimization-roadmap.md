> **Language: English (en)** — This document is written in en only.

# Provider Optimization Roadmap

Optimization order for all providers, from the **core model R&D vendors** outward to the
periphery. Each provider gets: official pricing-page verification, billing-mode audit,
model-list dedup, notes localization, and human-page review.

Legend: ✅ = already human-verified this round · ⬜ = to do · (n) = model count in DB

---

## Tier 0 — Global core model R&D vendors (highest priority, one by one)

| # | Provider | Models | Notes |
|---|---|---|---|
| 1 | OpenAI | 47 | GPT-5.6 family; official snapshot pipeline in place |
| 2 | Anthropic | 16 | Fable/Opus/Sonnet/Haiku; verified 2026-08 |
| 3 | Google DeepMind | 40 | Gemini 3.x/2.5; JS-rendered page, parser disabled — needs ego-browser pass |
| 4 | xAI | 17 | Grok 4.x; verified 2026-08 |
| 5 | DeepSeek | 5 | V4 series peak/off-peak; verified 2026-08 |
| 6 | Meta | 3 | No official API — track Llama via hosting partners |
| 7 | Mistral AI | 33 | La Plateforme prices need re-verification |
| 8 | Cohere | 14 | Command/Embed/Rerank prices need re-verification |
| 9 | Amazon (Nova/Titan) | 120 | via Bedrock; also Tier 2 cloud |
| 10 | NVIDIA | 100 | NIM catalog; mostly free-tier entries, verify |
| 11 | Perplexity | 26 | Sonar API + subscriptions |

## Tier 1 — China core model R&D vendors (one by one)

| # | Provider | Models | Notes |
|---|---|---|---|
| 12 | Alibaba Qwen (alibaba / alibaba-cn) | 54+86 | DashScope official CNY prices |
| 13 | Zhipu GLM (zhipuai / zai) | 16+16 | open.bigmodel.cn + z.ai |
| 14 | Moonshot Kimi (moonshotai) | 14 | incl. Kimi Code plans |
| 15 | ByteDance Doubao (volcengine) | 2 | Ark official CNY prices — expand model list |
| 16 | MiniMax | 7 | incl. Token Plan |
| 17 | Baidu ERNIE (baidu) | 3 | Qianfan official doc — expand model list |
| 18 | Tencent Hunyuan (tencent / tencent-tokenhub) | 1+2 | TokenHub billing — expand |
| 19 | StepFun (stepfun / stepfun-step-plan) | 8+4 | platform.stepfun.com |
| 20 | Xiaomi MiMo (xiaomi) | 10 | mimo.mi.com official docs |
| 21 | 01.AI / Lingyiwanwu | — | NOT in DB yet — add |
| 22 | iFlytek Spark | — | NOT in DB yet — add |
| 23 | Baichuan | — | NOT in DB yet — add |

## Tier 2 — Cloud platforms hosting official models

| # | Provider | Models | Notes |
|---|---|---|---|
| 24 | Microsoft Azure | 84 | azure + azure-cognitive-services merged |
| 25 | Google Vertex | 42 | gemini + claude-on-vertex |
| 26 | AWS Bedrock | 120 | merged from amazon-bedrock |
| 27 | Alibaba Cloud intl | 86 | dashscope-intl |

## Tier 3 — Core inference hosting platforms (one by one)

Together AI (36) · Groq (15) · Cerebras (2) · DeepInfra (60) · SiliconFlow (61) ·
Fireworks AI (23) · Novita AI (107) · Nebius (34) · Baseten (19) · Modal (2) ·
Hugging Face (69) · Cloudflare Workers AI (25) · Scaleway (14) · OVHcloud (14) ·
Vultr (10) · DigitalOcean (92) · Databricks (30) · Snowflake Cortex (25) · watsonx (5) ·
SAP AI Core (48)

## Tier 4 — Aggregators & gateways (one by one)

OpenRouter (420) · OpenCode Zen (63) / Go (23) · Poe (137) · Vercel AI Gateway (350) ·
LLMGateway/DevPass (556) · Kilo (363) · OrcaRouter (81) · Cloudflare AI Gateway (67) ·
Merge Gateway (174) · FastRouter (47) · UnoRouter (23) · 302AI (97) · AIHubMix (70) ·
Requesty (139) · AnyAPI (30) · NanoGPT (597) · Eden AI (232) · ZenMux (120) · others

## Tier 5 — Subscription & coding products (one by one)

ChatGPT (Plus/Go/Pro/Codex) · Claude (Pro/Max/Claude Code) · GitHub Copilot (33) ·
Cursor · Windsurf · JetBrains AI · Devin · Kimi Code (4 tiers) · MiniMax Token Plan ·
Xiaomi Token Plan (4 tiers) · OpenCode Go (23) · Replit · Tabnine · v0 · Poe (points)

## Tier 6 — Long tail (batched, by model count desc)

Batch A (≥50): abacus (108) · cortecs (108) · ofox (107) · pioneer (103) · venice (99) ·
qiniu-ai (91) · helicone (90) · impossibl (76) · jiekou (61) · empiriolabs (55) ·
crossmodel (52) · neon (42)
Batch B (20–49): kenari (38) · greenpt (37) · nearai (37) · llmtr (32) · wandb (29) ·
crof (26) · frogbot (26) · hyper (26) · tensorx (25) · neuralwatt (22) · ollama-cloud (20) ·
vivgrid (20) · meganova (19) · regolo-ai (18) · io-net (17) · jalapeno (17) · zai (16) ·
scnet-token-plan (16)
Batch C (10–19): auriko (15) · evroc (15) · model-oracle-ai (15) · routing-run (15) ·
chutes (14) · iflowcn (14) · ovhcloud (14) · scaleway (14) · gmicloud (13) · xpersona (13) ·
clarifai (12) · inferx (12) · cline-pass (11) · ambient (10) · freemodel (10) ·
infomaniak (10) · vultr (10) · xiaomi (10) · aiand (9) · berget (9) · daoxe (9) ·
hpc-ai (9) · inference (9) · modelis (9) · qihang-ai (9) · qvac (9) · submodel (9) ·
the-grid-ai (9) · crusoe (8) · stackit (8) · synthetic (8) · tinfoil (8) · arcee (7) ·
llama (7) · modelscope (7) · privatemode-ai (7) · aki-io (6) · dinference (6)
Batch D (≤5): atomic-chat (5) · cloudferro-sherlock (5) · friendli (5) · mixlayer (5) ·
runinfra (5) · wafer.ai (5) · watsonx (5) · ebcloud (4) · inceptron (4) · lilac (4) ·
lucidquery (4) · sakana (4) · scx-ai (4) · upstage (4) · coralbricks (3) · drun (3) ·
lmstudio (3) · morph (3) · poolside (3) · abliteration-ai (2) · bailing (2) · blueclaw (2) ·
cerebras (2) · claudinio (2) · hetzner (2) · inception (2) · moark (2) · modal (2) ·
nova (2) · sarvam (2) · subconscious (2) · thinkingmachines (2) · amd (1) · echo (1) ·
kosmik (1) · longcat (1) · lynkr (1) · zeldoc (1) · zenifra (1)

## Per-provider optimization checklist

1. Official pricing page / API: fetch, parse, verify (official-first layer).
2. Billing-mode audit: per-MTok vs per-request vs per-image vs credits vs subscription.
3. Model list: dedup by api_base_url, mark retired/deprecated with `status`.
4. Notes: English, with source URL + verified_at.
5. Plans (if any): pricing_model + limits/includes in English.
6. Human page: rebuild via `build_human.py` (api_base_url + Notes column).
7. Version bump (content) + changelog + PR through pr-check.
