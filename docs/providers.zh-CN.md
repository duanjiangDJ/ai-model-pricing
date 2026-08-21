> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.
# Provider Landscape / 供应商全景（providers）

> 本文件是"市面上可获取模型定价"的供应商地图。所有可获取模型的途径被分为 **7 大类**。
> 机器可读版本见 `data/machine/providers/*.json` 与 `data/machine/plans.json`。

## 分类总览

| 类别 | 定义 | 收费形式特点 | 示例 |
|---|---|---|---|
| A. 第一方 AI 厂商 | 模型原厂直供 API | per MTok（含 cache/batch）、per image、per 音频秒、订阅 | OpenAI、Anthropic、Google、DeepSeek、智谱… |
| B. 云平台托管 | 云厂商托管官方模型（同模型不同价） | per MTok、预留容量按小时 | Azure、AWS Bedrock、Vertex、阿里云百炼… |
| C. 推理托管平台 | 第三方托管（开源/商用模型），自带 GPU | per MTok、按 GPU 秒 | Together、Groq、Cerebras、SiliconFlow、Replicate… |
| D. 聚合/中转站 | 转售多家模型，价格随上游浮动 | per MTok 加价、credits、充值倍数 | OpenRouter、Poe API、AIMLAPI、国内中转站群… |
| E. 消费级订阅 | 面向终端用户的订阅套餐 | 月费/年费、用量上限 | ChatGPT Plus/Pro、Claude Pro/Max、Gemini AI… |
| F. 编码工具计划 | 面向开发者的编码助手订阅 | 月费、额度（部分含 API 用量） | Copilot、Cursor、Windsurf、Claude Code… |
| G. GPU 算力平台 | 按 GPU 出租算力自部署模型 | 按 GPU 小时/秒 | RunPod、Vast.ai、Lambda、Modal… |

---

## A. 第一方 AI 厂商（官方 API 直供）

### 国际
| 厂商 | 主要模型线 | 定价页 |
|---|---|---|
| OpenAI | GPT-4.1 / GPT-4o / o 系列推理 / GPT-5 / embeddings / DALL·E·image / Whisper·TTS / Realtime | platform.openai.com/docs/pricing |
| Anthropic | Claude Opus / Sonnet / Haiku（含 caching、batch） | anthropic.com/pricing |
| Google DeepMind | Gemini 2.0/2.5 系列（Flash/Pro）、Imagen、Veo、Chirp 音频 | ai.google.dev/pricing |
| xAI | Grok 系列、Grok Code Fast、grok-embedding | x.ai/api |
| Mistral AI | Mistral Large/Medium/Small、Codestral、Pixtral、Ministral、Embed | mistral.ai/pricing |
| Cohere | Command A / R+、Embed、Rerank、Classify | cohere.com/pricing |
| AI21 | Jamba 系列 | ai21.com/pricing |
| Stability AI | Stable Image / Video 系列 | stability.ai |
| Perplexity | Sonar API（在线模型） | docs.perplexity.ai |
| ElevenLabs | TTS/STT 音频模型 | elevenlabs.io/pricing |
| Deepgram | STT/TTS 音频模型 | deepgram.com/pricing |
| AssemblyAI | STT/音频理解 | assemblyai.com/pricing |
| Cartesia | 低延迟 TTS | cartesia.ai/pricing |
| Luma AI | Dream Machine 视频 | lumalabs.ai |
| Runway | Gen 系列视频 | runwayml.com/pricing |
| Pika | 视频生成 | pika.art |
| NVIDIA（NIM） | 自托管推理容器（按 GPU 许可） | build.nvidia.com |

### 国内
| 厂商 | 主要模型线 | 平台 |
|---|---|---|
| DeepSeek | deepseek-chat / deepseek-reasoner（V3/R1 系） | platform.deepseek.com |
| 阿里云 | Qwen（通义千问）全系、开源模型托管 | 百炼 Model Studio |
| 字节跳动 | 豆包 Doubao 系列、即梦（图像/视频）、语音 | 火山方舟 Volcano Ark |
| 百度 | 文心 ERNIE 系列 | 千帆 ModelBuilder |
| 腾讯 | 混元 Hunyuan 系列 | 腾讯云 TI/混元 |
| 智谱 AI | GLM-4.5/4.6、GLM-Z1、CogView、CogVideoX、语音 | open.bigmodel.cn |
| 月之暗面 Moonshot | Kimi K2、kimi-thinking、moonshot-v1 | platform.moonshot.cn |
| MiniMax | MiniMax-Text / VL / Speech / Music / Video | platform.minimaxi.com |
| 阶跃星辰 StepFun | Step 系列（文本/图像/视频） | platform.stepfun.com |
| 零一万物 01.AI | Yi 系列 | platform.lingyiwanwu.com |
| 科大讯飞 | 星火 Spark 系列 | xfyun.cn |
| 百川智能 | Baichuan 系列 | platform.baichuan-ai.com |
| 昆仑万维 | Skywork 天工系列 | platform.tiangong.cn |

> Meta（Llama）无官方 API，通过 B/C 类平台分发；上海 AI Lab（InternLM）等开源模型同理，归入 C 类托管平台定价。

---

## B. 云平台托管（官方模型托管，价格独立）

| 平台 | 托管的官方模型 | 特点 |
|---|---|---|
| Microsoft Azure AI Foundry | OpenAI GPT、o 系列、Meta、Mistral 等 | 企业合同价，另有 provisioned 按小时 |
| AWS Bedrock | Claude、Llama、Mistral、Cohere、Titan、Nova | 按量付费，region 差异 |
| Google Vertex AI | Gemini、Imagen、Veo、开源模型 | 按量付费 |
| 阿里云百炼（国际） | Qwen 系 | 与国内版价格不同 |
| IBM watsonx | Granite、Llama、Mistral | 企业为主 |
| Oracle OCI / 腾讯云 / 华为云 | 各自托管 | 企业合同为主 |

---

## C. 推理托管平台（第三方托管，自带算力）

| 平台 | 模型覆盖 | 计费方式 |
|---|---|---|
| OpenRouter | 400+ 模型（聚合，转售价） | per MTok（含 cache）、per image、per request |
| Together AI | Llama/Qwen/DeepSeek 等开源全系 | per MTok |
| Fireworks AI | 开源模型 + 自研函数模型 | per MTok |
| Groq | Llama、DeepSeek、Qwen 等（LPU 极速） | per MTok |
| Cerebras | Llama、DeepSeek 等（最快推理） | per MTok |
| SambaNova | Llama 等 | per MTok |
| DeepInfra | 开源全系 | per MTok |
| Novita AI | 开源全系 + 图像/视频 | per MTok、per image |
| SiliconFlow 硅基流动 | 开源全系（国内） | per MTok（充值即送） |
| Replicate | 图像/视频/音频/文本全系 | 按 GPU 秒 + per 请求 |
| Hugging Face Inference | 开源全系 | 按秒/请求 + Pro 订阅积分 |
| Nebius AI Studio | 开源全系 | per MTok |
| Baseten | 开源全系 | 按 GPU 秒 |
| Modal | 开源全系 | 按 GPU 秒 |
| Cloudflare Workers AI | 部分开源模型 | 按神经元秒 |
| GitHub Models | 主流模型（微软账号额度） | 订阅额度内免费 |
| FAL.ai | 图像/视频模型 | 按秒/按张 |
| Pollinations | 免费图像/文本 | 免费 |

---

## D. 聚合/中转站（转售与代理）

| 类型 | 代表 | 计费方式 |
|---|---|---|
| 国际聚合 | OpenRouter、Poe API、AIMLAPI、Martian、Unify | per MTok 加价 / 订阅点数 |
| 国内中转站 | API2D、CloseAI、OhMyGPT、AiHubMix、GPT-API、uni-api、V3 API、熊猫 API 等 | 通常按官方价倍数或 credits，充值有折扣 |
| 自建中转（OneAPI/NewAPI 系） | 大量个人/小团队实例 | 定价随意、不稳定 |

> 中转站数以千计、价格随时浮动、随时跑路。本仓库对中转站的策略：
> 1) 收录**有公开定价页**的主要中转站（存续性以每日检查标记）；
> 2) 对无法逐一爬取的长尾，提供**定价模式文档**（一般 = 官方价 × 倍率 或 credits 系数），由每日检查报告其定价页漂移。
> 长尾中转站不做穷举承诺（技术上不可行），README 中如实声明覆盖边界。

---

## E. 消费级订阅

| 产品 | 计划 | 备注 |
|---|---|---|
| ChatGPT | Plus / Pro / Team / Business / Enterprise | Pro 含高额度 o 系 |
| Claude | Pro / Max 5x / Max 20x / Team / Enterprise | Max 含 Claude Code |
| Gemini | AI Pro / AI Ultra / Google One AI | 免费档存在 |
| Perplexity | Pro / Enterprise | 含 Sonar API 用量 |
| Poe | Premium / Pro | 订阅点数计价 |
| Kimi（月之暗面） | 会员 | 国内消费订阅 |
| 豆包 / 通义 / 文心 | 会员 | 国内消费订阅 |

---

## F. 编码工具计划

| 工具 | 计划 | 备注 |
|---|---|---|
| GitHub Copilot | Pro / Business / Enterprise | Pro 含 ChatGPT 集成 |
| Cursor | Free / Pro / Ultra / Teams | Ultra 含无限高级模型 |
| Windsurf | Free / Pro / Ultra / Teams | |
| Claude Code | Free / Pro / Max（含 5x/20x） | Max 含 API 额度 |
| JetBrains AI | Pro / Ultimate | |
| Amazon Q Developer | Free / Pro | |
| Google Gemini Code Assist | Free / Enterprise | |
| Tabnine | Pro / Enterprise | |
| Replit | Core / Teams | |
| Augment Code | Pro / Enterprise | |
| Devin | Team / Enterprise | $500/月级 |
| Cline / Aider / Continue | BYOK 或开源 | 无订阅或免费 |

---

## G. GPU 算力平台（自部署成本维度，可选）

RunPod、Vast.ai、Lambda、TensorDock、Salad、Modal、Baseten、Replicate（均按 GPU 小时/秒计费）。
> 这属于"部署成本"而非"模型定价"，本仓库作为附加维度收录，字段 `price_type: gpu_hour`。

---

## 收费形式总表（Price Types）

| 收费形式 | 字段枚举值 | 典型场景 |
|---|---|---|
| 每百万 token（输入/输出） | `per_mtok` | 绝大多数文本 LLM API |
| 缓存读取（输入） | `cache_read` | OpenAI/Anthropic/DeepSeek 等自动缓存 |
| 缓存写入 | `cache_write` | 同上 |
| 批处理折扣 | `batch` | OpenAI/Anthropic 等（通常 5 折） |
| 每张图片 | `per_image` | DALL·E、Imagen、FLUX |
| 每音频秒 | `per_audio_second` | TTS/STT、Realtime 音频 |
| 每字符 | `per_character` | 部分 TTS/翻译 |
| 每次请求/调用 | `per_request` | 图像 API、中转站 |
| 点数/credits | `credits` | Poe、HF Pro、充值平台 |
| GPU 秒/小时 | `gpu_second` / `gpu_hour` | Replicate、Modal、RunPod |
| 神经元秒 | `neuron_second` | Cloudflare Workers AI |
| 月订阅 | `subscription_monthly` | 消费/编码订阅 |
| 年订阅 | `subscription_yearly` | 年付折扣 |
| 免费额度 | `free_tier` | 各平台免费档 |
| 微调训练 | `finetune` | 按训练 token 计费 |

> 逐一核实的详细口径见 `docs/price-types.md`，机器可读枚举定义见 `data/machine/schema.json`。
