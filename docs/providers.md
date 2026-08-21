> **Language: English (en)** — This document is written in en only.
# Provider Landscape (providers)

> This file is the provider map of "prices for all obtainable AI models". All channels through which models can be obtained are grouped into **7 major categories**.
> Machine-readable versions: `data/machine/providers/*.json` and `data/machine/plans.json`.

## Category Overview

| Category | Definition | Billing Characteristics | Examples |
|---|---|---|---|
| A. First-party AI vendors | Direct API from model originators | per MTok (incl. cache/batch), per image, per audio second, subscription | OpenAI, Anthropic, Google, DeepSeek, Zhipu (智谱)… |
| B. Cloud platform hosting | Official models hosted by cloud vendors (same model, different prices) | per MTok, provisioned capacity per hour | Azure, AWS Bedrock, Vertex, Alibaba Cloud Bailian… |
| C. Inference hosting platforms | Third-party hosting (open-source/commercial models) with own GPUs | per MTok, per GPU second | Together, Groq, Cerebras, SiliconFlow, Replicate… |
| D. Aggregators / relay stations | Resell multiple models, prices float with upstream | per MTok markup, credits, top-up multipliers | OpenRouter, Poe API, AIMLAPI, domestic relay stations… |
| E. Consumer subscriptions | Subscription plans for end users | Monthly/yearly fees, usage caps | ChatGPT Plus/Pro, Claude Pro/Max, Gemini AI… |
| F. Coding tool plans | Coding-assistant subscriptions for developers | Monthly fee, quotas (some include API usage) | Copilot, Cursor, Windsurf, Claude Code… |
| G. GPU compute platforms | Rent GPU compute to self-host models | Per GPU hour/second | RunPod, Vast.ai, Lambda, Modal… |

---

## A. First-party AI vendors (official API direct)

### International
| Vendor | Main model lines | Pricing page |
|---|---|---|
| OpenAI | GPT-4.1 / GPT-4o / o-series reasoning / GPT-5 / embeddings / DALL·E image / Whisper·TTS / Realtime | platform.openai.com/docs/pricing |
| Anthropic | Claude Opus / Sonnet / Haiku (incl. caching, batch) | anthropic.com/pricing |
| Google DeepMind | Gemini 2.0/2.5 series (Flash/Pro), Imagen, Veo, Chirp audio | ai.google.dev/pricing |
| xAI | Grok series, Grok Code Fast, grok-embedding | x.ai/api |
| Mistral AI | Mistral Large/Medium/Small, Codestral, Pixtral, Ministral, Embed | mistral.ai/pricing |
| Cohere | Command A / R+, Embed, Rerank, Classify | cohere.com/pricing |
| AI21 | Jamba series | ai21.com/pricing |
| Stability AI | Stable Image / Video series | stability.ai |
| Perplexity | Sonar API (online models) | docs.perplexity.ai |
| ElevenLabs | TTS/STT audio models | elevenlabs.io/pricing |
| Deepgram | STT/TTS audio models | deepgram.com/pricing |
| AssemblyAI | STT/audio understanding | assemblyai.com/pricing |
| Cartesia | Low-latency TTS | cartesia.ai/pricing |
| Luma AI | Dream Machine video | lumalabs.ai |
| Runway | Gen series video | runwayml.com/pricing |
| Pika | Video generation | pika.art |
| NVIDIA (NIM) | Self-hosted inference containers (GPU-licensed) | build.nvidia.com |

### Domestic (China)
| Vendor | Main model lines | Platform |
|---|---|---|
| DeepSeek | deepseek-chat / deepseek-reasoner (V3/R1 series) | platform.deepseek.com |
| Alibaba Cloud | Qwen (Tongyi Qianwen) full lineup, open-source model hosting | Bailian Model Studio |
| ByteDance | Doubao series, Jimeng (image/video), speech | Volcano Ark |
| Baidu | ERNIE (Wenxin) series | Qianfan ModelBuilder |
| Tencent | Hunyuan series | Tencent Cloud TI / Hunyuan |
| Zhipu AI | GLM-4.5/4.6, GLM-Z1, CogView, CogVideoX, speech | open.bigmodel.cn |
| Moonshot AI | Kimi K2, kimi-thinking, moonshot-v1 | platform.moonshot.cn |
| MiniMax | MiniMax-Text / VL / Speech / Music / Video | platform.minimaxi.com |
| StepFun | Step series (text/image/video) | platform.stepfun.com |
| 01.AI | Yi series | platform.lingyiwanwu.com |
| iFlytek | Spark (Xinghuo) series | xfyun.cn |
| Baichuan | Baichuan series | platform.baichuan-ai.com |
| Kunlun Wanwei | Skywork (Tiangong) series | platform.tiangong.cn |

> Meta (Llama) has no official API and is distributed through B/C-class platforms; open-source models such as Shanghai AI Lab (InternLM) follow the same rule and fall under C-class hosted platform pricing.

---

## B. Cloud platform hosting (official model hosting, independent prices)

| Platform | Hosted official models | Notes |
|---|---|---|
| Microsoft Azure AI Foundry | OpenAI GPT, o-series, Meta, Mistral, etc. | Enterprise contract pricing, plus provisioned per hour |
| AWS Bedrock | Claude, Llama, Mistral, Cohere, Titan, Nova | Pay-as-you-go, region differences |
| Google Vertex AI | Gemini, Imagen, Veo, open-source models | Pay-as-you-go |
| Alibaba Cloud Bailian (international) | Qwen series | Prices differ from the domestic version |
| IBM watsonx | Granite, Llama, Mistral | Enterprise-focused |
| Oracle OCI / Tencent Cloud / Huawei Cloud | Their own hosted models | Mostly enterprise contracts |

---

## C. Inference hosting platforms (third-party hosting, own compute)

| Platform | Model coverage | Billing |
|---|---|---|
| OpenRouter | 400+ models (aggregator, resale prices) | per MTok (incl. cache), per image, per request |
| Together AI | Full open-source lineup: Llama/Qwen/DeepSeek etc. | per MTok |
| Fireworks AI | Open-source models + proprietary function models | per MTok |
| Groq | Llama, DeepSeek, Qwen etc. (LPU ultra-fast) | per MTok |
| Cerebras | Llama, DeepSeek etc. (fastest inference) | per MTok |
| SambaNova | Llama etc. | per MTok |
| DeepInfra | Full open-source lineup | per MTok |
| Novita AI | Full open-source lineup + image/video | per MTok, per image |
| SiliconFlow | Full open-source lineup (domestic) | per MTok (top-up bonus) |
| Replicate | Full image/video/audio/text lineup | Per GPU second + per request |
| Hugging Face Inference | Full open-source lineup | Per second/request + Pro subscription credits |
| Nebius AI Studio | Full open-source lineup | per MTok |
| Baseten | Full open-source lineup | Per GPU second |
| Modal | Full open-source lineup | Per GPU second |
| Cloudflare Workers AI | Some open-source models | Per neuron second |
| GitHub Models | Mainstream models (Microsoft account quota) | Free within subscription quota |
| FAL.ai | Image/video models | Per second/per image |
| Pollinations | Free image/text | Free |

---

## D. Aggregators / relay stations (resellers and proxies)

| Type | Representatives | Billing |
|---|---|---|
| International aggregators | OpenRouter, Poe API, AIMLAPI, Martian, Unify | per MTok markup / subscription points |
| Domestic relay stations | API2D, CloseAI, OhMyGPT, AiHubMix, GPT-API, uni-api, V3 API, Panda API, etc. | Usually official price × multiplier or credits, top-up discounts |
| Self-hosted relays (OneAPI/NewAPI family) | Many personal/small-team instances | Arbitrary, unstable pricing |

> There are thousands of relay stations; prices fluctuate at any time and operators may vanish anytime. This repository's policy on relay stations:
> 1) Include major relay stations that **have public pricing pages** (viability marked by daily checks);
> 2) For the long tail that cannot be crawled one by one, provide **pricing-pattern documentation** (generally = official price × multiplier or credit coefficient), with the daily check reporting pricing-page drift.
> The long tail of relay stations is not exhaustively covered (technically infeasible); the README honestly states this coverage boundary.

---

## E. Consumer subscriptions

| Product | Plans | Notes |
|---|---|---|
| ChatGPT | Plus / Pro / Team / Business / Enterprise | Pro includes high-quota o-series |
| Claude | Pro / Max 5x / Max 20x / Team / Enterprise | Max includes Claude Code |
| Gemini | AI Pro / AI Ultra / Google One AI | Free tier exists |
| Perplexity | Pro / Enterprise | Includes Sonar API usage |
| Poe | Premium / Pro | Subscription points billing |
| Kimi (Moonshot) | Membership | Domestic consumer subscription |
| Doubao / Tongyi / Wenxin | Membership | Domestic consumer subscription |

---

## F. Coding tool plans

| Tool | Plans | Notes |
|---|---|---|
| GitHub Copilot | Pro / Business / Enterprise | Pro includes ChatGPT integration |
| Cursor | Free / Pro / Ultra / Teams | Ultra includes unlimited premium models |
| Windsurf | Free / Pro / Ultra / Teams | |
| Claude Code | Free / Pro / Max (incl. 5x/20x) | Max includes API credit |
| JetBrains AI | Pro / Ultimate | |
| Amazon Q Developer | Free / Pro | |
| Google Gemini Code Assist | Free / Enterprise | |
| Tabnine | Pro / Enterprise | |
| Replit | Core / Teams | |
| Augment Code | Pro / Enterprise | |
| Devin | Team / Enterprise | ~$500/month level |
| Cline / Aider / Continue | BYOK or open source | No subscription or free |

---

## G. GPU compute platforms (self-deployment cost dimension, optional)

RunPod, Vast.ai, Lambda, TensorDock, Salad, Modal, Baseten, Replicate (all billed per GPU hour/second).
> This belongs to "deployment cost" rather than "model pricing"; the repository records it as an additional dimension with the field `price_type: gpu_hour`.

---

## Price Types Overview

| Billing type | Field enum value | Typical scenarios |
|---|---|---|
| Per million tokens (input/output) | `per_mtok` | Most text LLM APIs |
| Cache read (input) | `cache_read` | Automatic caching at OpenAI/Anthropic/DeepSeek etc. |
| Cache write | `cache_write` | Same as above |
| Batch discount | `batch` | OpenAI/Anthropic etc. (usually 50% off) |
| Per image | `per_image` | DALL·E, Imagen, FLUX |
| Per audio second | `per_audio_second` | TTS/STT, Realtime audio |
| Per character | `per_character` | Some TTS/translation |
| Per request/call | `per_request` | Image APIs, relay stations |
| Points/credits | `credits` | Poe, HF Pro, top-up platforms |
| GPU second/hour | `gpu_second` / `gpu_hour` | Replicate, Modal, RunPod |
| Neuron second | `neuron_second` | Cloudflare Workers AI |
| Monthly subscription | `subscription_monthly` | Consumer/coding subscriptions |
| Yearly subscription | `subscription_yearly` | Annual-payment discounts |
| Free tier | `free_tier` | Free tiers across platforms |
| Finetuning | `finetune` | Billed per training token |

> Detailed, item-by-item verified definitions in `docs/price-types.md`; machine-readable enum definitions in `data/machine/schema.json`.
