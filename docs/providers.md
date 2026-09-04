> **Language: English (en)** — This document is written in en only.

# Provider Landscape & Status (providers)

Every provider in the database, its status, and its automation. The table below is
**generated** by `python scripts/provider_status.py` — never edit it by hand.

- **Check script**: a `scripts/checks/tierN_<provider>.py` module that fetches the official
  pricing page automatically (run by the core router every 3 hours).
- **Status**: 🟢 automated (check script) / 🟡 manual (in DB, no check) / ⚪ pending (not in DB yet).
- **Tiers (by model R&D leadership, not geography)**:
  - **Tier 0** — the world's leading model R&D vendors (headline labs);
  - **Tier 1** — other major LLM R&D vendors;
  - **Tier 2** — all remaining model R&D vendors (any model type);
  - **Tier 3** — core inference hosts / resellers / aggregator gateways;
  - **Tier 4** — other service providers (subscription products, long-tail).
- Within each tier providers are sorted alphabetically and deduplicated.

<!-- PROVIDERS:BEGIN -->

### Tier 0 — World's leading model R&D vendors

| Provider | Name | Models | API base URL | Check script | Status | Official 1st-party |
|---|---|---|---|---|---|---|
| `alibaba` | Alibaba | 55 | `https://dashscope-intl.aliyuncs.com/c…` | `tier0_alibaba.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `anthropic` | Anthropic | 17 | `https://api.anthropic.com/v1` | `tier0_anthropic.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `deepseek` | DeepSeek | 5 | `https://api.deepseek.com` | `tier0_deepseek.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `google` | Google | 41 | `https://generativelanguage.googleapis…` | `tier0_google.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `meta` | Meta | 5 | `https://api.meta.ai/v1` | `tier0_meta.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `minimax` | MiniMax (minimax.io) | 7 | `https://api.minimax.chat/v1` | `tier0_minimax.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `mistral` | Mistral | 34 | `https://api.mistral.ai/v1` | `tier0_mistral.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `moonshotai` | Moonshot AI | 14 | `https://api.moonshot.cn/v1` | `tier0_moonshotai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `openai` | OpenAI | 55 | `https://api.openai.com/v1` | `tier0_openai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `xai` | xAI | 17 | `https://api.x.ai/v1` | `tier0_xai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `zai` | Z.AI | 23 | `https://api.z.ai/api/paas/v4` | `tier0_zai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |

### Tier 1 — Other major LLM R&D vendors

| Provider | Name | Models | API base URL | Check script | Status | Official 1st-party |
|---|---|---|---|---|---|---|
| `ai21` | AI21 Labs | 2 | `https://api.ai21.com/v1` | `tier1_ai21.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `aws` | Amazon Web Services | 120 | `https://bedrock-runtime.{region}.amaz…` | `tier1_aws.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `baichuan` | 百川智能 (Baichuan) | 1 | `https://api.baichuan-ai.com/v1` | `tier1_baichuan.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `baidu` | 百度智能云千帆 (Baidu Qianfan) | 3 | `https://qianfan.baidubce.com/v2` | `tier1_baidu.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `cohere` | Cohere | 14 | `https://api.cohere.com/v1` | `tier1_cohere.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `iflytek` | 科大讯飞星火 (iFlytek Spark) | 2 | `https://spark-api-open.xf-yun.com/v1` | `tier1_iflytek.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `lingyiwanwu` | 零一万物 (01.AI) | 2 | `https://api.lingyiwanwu.com/v1` | `tier1_lingyiwanwu.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `nvidia` | Nvidia | 103 | `https://integrate.api.nvidia.com/v1` | `tier1_nvidia.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `perplexity` | Perplexity | 26 | `https://api.perplexity.ai` | `tier1_perplexity.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `stepfun` | StepFun (China) | 8 | `https://api.stepfun.com/v1` | `tier1_stepfun.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `tencent` | 腾讯混元 (Tencent Hunyuan) | 1 | `https://api.hunyuan.cloud.tencent.com/v1` | `tier1_tencent.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `upstage` | Upstage | 4 | `https://api.upstage.ai/v1/solar` | `tier1_upstage.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `volcengine` | 字节跳动·火山引擎方舟 (ByteDance Volcengine Ark / 豆包) | 17 | `https://ark.cn-beijing.volces.com/api/v3` | `tier1_volcengine.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `xiaomi` | Xiaomi | 10 | `https://api.xiaomimimo.com/v1` | `tier1_xiaomi.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `zhipuai` | Zhipu AI | 17 | `https://open.bigmodel.cn/api/paas/v4` | `tier1_zhipuai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `ai21` | AI21 Labs | — | `https://api.ai21.com/studio/v1` | `—` | ⚪ pending | — |
| `baichuan` | Baichuan AI | — | `https://api.baichuan-ai.com/v1` | `—` | ⚪ pending | — |
| `iflytek` | iFlytek Spark | — | `https://spark-api-open.xf-yun.com/v1` | `—` | ⚪ pending | — |
| `lingyiwanwu` | 01.AI (Lingyiwanwu) | — | `https://api.lingyiwanwu.com/v1` | `—` | ⚪ pending | — |

### Tier 2 — Other model R&D vendors

| Provider | Name | Models | API base URL | Check script | Status | Official 1st-party |
|---|---|---|---|---|---|---|
| `arcee` | Arcee | 7 | `https://api.arcee.ai/api/v1` | `tier1_arcee.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `inception` | Inception | 2 | `https://api.inceptionlabs.ai/v1/` | `tier1_inception.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `lilac` | Lilac | 4 | `https://api.getlilac.com/v1` | `tier1_lilac.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `morph` | Morph | 3 | `https://api.morphllm.com/v1` | `tier1_morph.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `nova` | Nova | 2 | `https://api.nova.amazon.com/v1` | `tier1_nova.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `poolside` | Poolside | 3 | `https://inference.poolside.ai/v1` | `tier1_poolside.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `sakana` | Sakana AI | 4 | `https://api.sakana.ai/v1` | `tier1_sakana.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `sarvam` | Sarvam AI | 2 | `https://api.sarvam.ai/v1` | `tier1_sarvam.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `submodel` | submodel | 9 | `https://llm.submodel.ai/v1` | `tier1_submodel.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `thinkingmachines` | Thinking Machines | 2 | `https://tinker.thinkingmachines.dev/s…` | `tier1_thinkingmachines.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `assemblyai` | AssemblyAI | — | `https://api.assemblyai.com/v2` | `—` | ⚪ pending | — |
| `cartesia` | Cartesia | — | `https://api.cartesia.ai/v1` | `—` | ⚪ pending | — |
| `deepgram` | Deepgram | — | `https://api.deepgram.com/v1` | `—` | ⚪ pending | — |
| `elevenlabs` | ElevenLabs | — | `https://api.elevenlabs.io/v1` | `—` | ⚪ pending | — |
| `playai` | PlayAI | — | `https://api.play.ai/v1` | `—` | ⚪ pending | — |
| `stability` | Stability AI | — | `https://api.stability.ai/v1` | `—` | ⚪ pending | — |

### Tier 3 — Core inference hosts / resellers / aggregator gateways

| Provider | Name | Models | API base URL | Check script | Status | Official 1st-party |
|---|---|---|---|---|---|---|
| `302ai` | 302.AI | 97 | `https://api.302.ai/v1` | `tier1_302ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `ai-router` | AI-ROUTER | 5 | `https://api.ai-router.dev/v1` | `tier1_ai_router.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `aihubmix` | AIHubMix | 77 | `https://aihubmix.com/v1` | `tier1_aihubmix.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `anyapi` | AnyAPI | 30 | `https://api.anyapi.ai/v1` | `tier1_anyapi.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `baseten` | Baseten | 21 | `https://inference.baseten.co/v1` | `tier1_baseten.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `cerebras` | Cerebras | 2 | `https://api.cerebras.ai/v1` | `tier1_cerebras.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `cloudflare-ai-gateway` | Cloudflare AI Gateway | 79 | `https://gateway.ai.cloudflare.com/v1/…` | `tier1_cloudflare_ai_gateway.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `cloudflare-workers-ai` | Cloudflare Workers AI | 27 | `https://api.cloudflare.com/client/v4/…` | `tier1_cloudflare_workers_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `crusoe` | Crusoe | 8 | `https://api.inference.crusoecloud.com/v1` | `tier1_crusoe.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `databricks` | Databricks | 30 | `https://${DATABRICKS_HOST}/ai-gateway…` | `tier1_databricks.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `deepinfra` | Deep Infra | 63 | `https://api.deepinfra.com/v1/openai` | `tier1_deepinfra.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `digitalocean` | DigitalOcean | 95 | `https://inference.do-ai.run/v1` | `tier1_digitalocean.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `edenai` | Eden AI | 255 | `https://api.edenai.run/v3` | `tier1_edenai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `fastrouter` | FastRouter | 47 | `https://go.fastrouter.ai/api/v1` | `tier1_fastrouter.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `fireworks-ai` | Fireworks AI | 26 | `https://api.fireworks.ai/inference/v1/` | `tier1_fireworks_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `friendli` | Friendli | 6 | `https://api.friendli.ai/serverless/v1` | `tier1_friendli.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `groq` | Groq | 16 | `https://api.groq.com/openai/v1` | `tier1_groq.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `helicone` | Helicone | 90 | `https://ai-gateway.helicone.ai/v1` | `tier1_helicone.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `hetzner` | Hetzner | 2 | `https://inference.hetzner.com/api/v1` | `tier1_hetzner.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `huggingface` | Hugging Face | 73 | `https://router.huggingface.co/v1` | `tier1_huggingface.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `jiekou` | Jiekou.AI | 61 | `https://api.jiekou.ai/openai` | `—` | 🟡 manual | — (aggregation only) |
| `kilo` | Kilo Gateway | 383 | `https://api.kilo.ai/api/gateway` | `tier1_kilo.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `llmgateway` | DevPass (LLM Gateway) | 565 | `https://api.llmgateway.io/v1` | `tier1_llmgateway.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `merge-gateway` | Merge Gateway | 179 | `https://api-gateway.merge.dev/v1/ai-sdk` | `tier1_merge_gateway.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `modal` | Modal | 4 | `https://inference.us-west.modal.direc…` | `tier1_modal.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `nano-gpt` | NanoGPT | 693 | `https://api.nano-gpt.com/v1` | `tier1_nano_gpt.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `nebius` | Nebius Token Factory | 38 | `https://api.studio.nebius.ai/v1` | `tier1_nebius.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `novita-ai` | NovitaAI | 107 | `https://api.novita.ai/v3/openai` | `tier1_novita_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `ollama-cloud` | Ollama Cloud | 22 | `https://ollama.com/api` | `tier1_ollama_cloud.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `opencode` | OpenCode Zen | 99 | `https://opencode.ai/zen/v1/models` | `tier1_opencode.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `opencode-go` | OpenCode Go | 34 | `https://opencode.ai/zen/go/v1/models` | `tier1_opencode_go.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `openrouter` | OpenRouter | 426 | `https://openrouter.ai/api/v1` | `—` | 🟡 manual | — (aggregation only) |
| `orcarouter` | OrcaRouter | 124 | `https://api.orcarouter.ai/v1` | `tier1_orcarouter.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `ovhcloud` | OVHcloud AI Endpoints | 15 | `https://oai.endpoints.kepler.ai.cloud…` | `tier1_ovhcloud.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `poe` | Poe | 137 | `https://api.poe.com/v1` | `tier1_poe.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `requesty` | Requesty | 153 | `https://router.requesty.ai/v1` | `tier1_requesty.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `runinfra` | RunInfra | 7 | `https://api.runinfra.ai/v1` | `tier1_runinfra.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `salad-cloud` | SaladCloud AI Gateway | 1 | `https://api.salad.com/v1` | `tier1_salad_cloud.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `sap-ai-core` | SAP AI Core | 48 | `https://api.ai.prod.eu-central-1.aws.…` | `tier1_sap_ai_core.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `scaleway` | Scaleway | 15 | `https://api.scaleway.ai/v1` | `tier1_scaleway.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `siliconflow` | SiliconFlow | 61 | `https://api.siliconflow.cn/v1` | `tier1_siliconflow.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `snowflake-cortex` | Snowflake Cortex | 25 | `https://${SNOWFLAKE_ACCOUNT}.snowflak…` | `tier1_snowflake_cortex.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `stackit` | STACKIT | 8 | `https://api.openai-compat.model-servi…` | `tier1_stackit.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `togetherai` | Together AI | 38 | `https://api.together.xyz/v1` | `tier1_togetherai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `trustedrouter` | TrustedRouter | 14 | `https://api.trustedrouter.com/v1` | `tier1_trustedrouter.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `unorouter` | UnoRouter | 23 | `https://api.unorouter.com/v1` | `tier1_unorouter.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `vercel` | Vercel AI Gateway | 375 | `https://api.vercel.com/v1/ai` | `tier1_vercel.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `vultr` | Vultr | 10 | `https://api.vultrinference.com/v1` | `tier1_vultr.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `watsonx` | watsonx.ai | 5 | `https://{region}.ml.cloud.ibm.com` | `tier1_watsonx.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `zenmux` | ZenMux | 120 | `https://zenmux.ai/api/v1` | `tier1_zenmux.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `runpod` | RunPod | — | `https://api.runpod.ai/v2` | `—` | ⚪ pending | — |
| `vast` | Vast.ai | — | `https://console.vast.ai/api/v0` | `—` | ⚪ pending | — |

### Tier 4 — Other service providers (long-tail)

| Provider | Name | Models | API base URL | Check script | Status | Official 1st-party |
|---|---|---|---|---|---|---|
| `abacus` | Abacus | 108 | `https://routellm.abacus.ai/v1` | `tier1_abacus.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `abliteration-ai` | abliteration.ai | 3 | `https://api.abliteration.ai/v1` | `tier1_abliteration_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `aiand` | ai& | 11 | `https://api.aiand.com/v1` | `tier1_aiand.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `aki-io` | AKI.IO | 8 | `https://aki.io/v1` | `tier1_aki_io.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `alibaba-cn` | Alibaba (China) | 87 | `https://dashscope.aliyuncs.com/compat…` | `tier1_alibaba_cn.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `alibaba-coding-plan` | Alibaba Coding Plan | 12 | `https://coding-intl.dashscope.aliyunc…` | `tier1_alibaba_coding_plan.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `alibaba-coding-plan-cn` | Alibaba Coding Plan (China) | 12 | `https://coding.dashscope.aliyuncs.com/v1` | `tier1_alibaba_coding_plan_cn.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `alibaba-token-plan` | Alibaba Token Plan | 25 | `https://token-plan.ap-southeast-1.maa…` | `tier1_alibaba_token_plan.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `alibaba-token-plan-cn` | Alibaba Token Plan (China) | 25 | `https://token-plan.cn-beijing.maas.al…` | `tier1_alibaba_token_plan_cn.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `ambient` | Ambient | 10 | `https://api.ambient.xyz/v1` | `tier1_ambient.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `amd` | AMD | 4 | `https://developer.amd.com.cn/radeon/a…` | `tier1_amd.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `atomic-chat` | Atomic Chat | 5 | `http://127.0.0.1:1337/v1` | `tier1_atomic_chat.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `auriko` | Auriko | 15 | `https://api.auriko.ai/v1` | `tier1_auriko.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `azure` | Azure | 86 | `https://{resource}.openai.azure.com` | `tier1_azure.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `bailing` | Bailing | 2 | `https://api.tbox.cn/api/llm/v1/chat/c…` | `tier1_bailing.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `berget` | Berget.AI | 12 | `https://api.berget.ai/v1` | `tier1_berget.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `blueclaw` | Blue Claw | 2 | `https://openai.blueclaw.network/v1` | `tier1_blueclaw.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `chutes` | Chutes | 14 | `https://llm.chutes.ai/v1` | `tier1_chutes.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `clarifai` | Clarifai | 12 | `https://api.clarifai.com/v2/ext/opena…` | `tier1_clarifai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `claudinio` | Claudinio | 2 | `https://api.claudin.io/v1` | `tier1_claudinio.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `cline-pass` | ClinePass | 13 | `https://api.cline.bot/api/v1` | `tier1_cline_pass.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `cloudferro-sherlock` | CloudFerro Sherlock | 5 | `https://api-sherlock.cloudferro.com/o…` | `tier1_cloudferro_sherlock.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `coralbricks` | CoralBricks | 4 | `https://inference.coralbricks.ai/v1` | `tier1_coralbricks.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `cortecs` | Cortecs | 112 | `https://api.cortecs.ai/v1` | `tier1_cortecs.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `crof` | CrofAI | 30 | `https://crof.ai/v1` | `tier1_crof.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `crossmodel` | CrossModel | 57 | `https://api.crossmodel.ai/v1` | `tier1_crossmodel.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `cursor` | Cursor (Anysphere) | 0 | `—` | `tier1_cursor.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `daoxe` | DaoXE | 9 | `https://daoxe.com/v1` | `tier1_daoxe.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `devin` | Devin (Cognition) | 0 | `—` | `tier1_devin.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `dinference` | DInference | 6 | `https://api.dinference.com/v1` | `tier1_dinference.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `drun` | D.Run (China) | 3 | `https://chat.d.run/v1` | `tier1_drun.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `ebcloud` | EBCloud | 4 | `https://maas-api.ebcloud.com/v1` | `tier1_ebcloud.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `echo` | Echo | 1 | `https://echo.tracerml.ai/v1` | `tier1_echo.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `empiriolabs` | EmpirioLabs AI | 59 | `https://api.empiriolabs.ai/v1` | `tier1_empiriolabs.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `evroc` | evroc | 17 | `https://models.think.evroc.com/v1` | `tier1_evroc.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `freemodel` | FreeModel | 10 | `https://cc.freemodel.dev/v1` | `tier1_freemodel.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `frogbot` | FrogBot | 26 | `https://app.frogbot.ai/api/v1` | `tier1_frogbot.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `github` | GitHub | 33 | `https://api.githubcopilot.com` | `tier1_github.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `gitlab` | GitLab Duo | 24 | `https://gitlab.com/api/v4/duo` | `tier1_gitlab.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `gmicloud` | GMI Cloud | 15 | `https://api.gmi-serving.com/v1` | `tier1_gmicloud.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `google-vertex` | Vertex | 45 | `https://{region}-aiplatform.googleapi…` | `tier1_google_vertex.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `greenpt` | GreenPT | 37 | `https://api.greenpt.ai/v1` | `tier1_greenpt.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `hpc-ai` | HPC-AI | 9 | `https://api.hpc-ai.com/inference/v1` | `tier1_hpc_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `hyper` | Charm Hyper | 32 | `https://hyper.charm.land/v1` | `tier1_hyper.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `iflowcn` | iFlow | 14 | `https://api.iflow.cn/v1` | `tier1_iflowcn.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `impossibl` | Impossibl | 76 | `https://api.impossibl.com/v1` | `tier1_impossibl.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `inceptron` | Inceptron | 4 | `https://api.inceptron.io/v1` | `tier1_inceptron.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `inference` | Inference | 9 | `https://inference.net/v1` | `tier1_inference.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `inferx` | InferX | 12 | `https://model.inferx.net/endpoints/v1` | `tier1_inferx.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `infomaniak` | Infomaniak | 10 | `https://api.infomaniak.com/2/ai/${INF…` | `tier1_infomaniak.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `io-net` | IO.NET | 17 | `https://api.intelligence.io.solutions…` | `tier1_io_net.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `jalapeno` | Jalapeno Cloud | 17 | `https://api.jalapeno-cloud.ai/v1` | `tier1_jalapeno.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `jetbrains` | JetBrains | 0 | `—` | `tier1_jetbrains.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `kenari` | Kenari | 59 | `https://kenari.id/v1` | `tier1_kenari.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `kosmik` | Kosmik Compute | 1 | `https://api.koscompute.com/v1` | `tier1_kosmik.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `kuae-cloud-coding-plan` | KUAE Cloud Coding Plan | 1 | `https://coding-plan-endpoint.kuaeclou…` | `tier1_kuae_cloud_coding_plan.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `llama` | Llama | 7 | `https://api.llama.com/compat/v1/` | `tier1_llama.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `llmtr` | LLMTR | 32 | `https://llmtr.com/v1` | `tier1_llmtr.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `lmstudio` | LMStudio | 3 | `http://localhost:1234/v1` | `tier1_lmstudio.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `longcat` | LongCat | 1 | `https://api.longcat.chat/openai` | `tier1_longcat.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `lucidquery` | LucidQuery | 4 | `https://api.lucidquery.com/v1` | `tier1_lucidquery.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `lynkr` | Lynkr | 1 | `http://127.0.0.1:8081/v1` | `tier1_lynkr.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `meganova` | Meganova | 19 | `https://api.meganova.ai/v1` | `tier1_meganova.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `mixlayer` | Mixlayer | 5 | `https://models.mixlayer.ai/v1` | `tier1_mixlayer.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `moark` | Moark | 2 | `https://moark.com/v1` | `tier1_moark.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `model-oracle-ai` | Model Oracle AI | 15 | `https://api.modeloracle.com/api/v1` | `tier1_model_oracle_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `modelis` | Modelis | 9 | `https://modelishub.com/v1` | `tier1_modelis.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `modelscope` | ModelScope | 7 | `https://api-inference.modelscope.cn/v1` | `tier1_modelscope.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `nearai` | NEAR AI Cloud | 37 | `https://cloud-api.near.ai/v1` | `tier1_nearai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `neon` | Neon | 42 | `${NEON_AI_GATEWAY_BASE_URL}/v1` | `tier1_neon.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `neuralwatt` | Neuralwatt | 30 | `https://api.neuralwatt.com/v1` | `tier1_neuralwatt.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `ofox` | Ofox | 114 | `https://api.ofox.ai/v1` | `tier1_ofox.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `pioneer` | Pioneer | 103 | `https://api.pioneer.ai/v1` | `tier1_pioneer.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `privatemode-ai` | Privatemode AI | 7 | `http://localhost:8080/v1` | `tier1_privatemode_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `qihang-ai` | QiHang | 9 | `https://api.qhaigc.net/v1` | `tier1_qihang_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `qiniu-ai` | Qiniu | 91 | `https://api.qnaigc.com/v1` | `tier1_qiniu_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `qvac` | QVAC | 9 | `http://localhost:{port}/v1` | `tier1_qvac.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `regolo-ai` | Regolo AI | 19 | `https://api.regolo.ai/v1` | `tier1_regolo_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `replit` | Replit | 0 | `—` | `tier1_replit.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `routing-run` | routing.run | 15 | `https://api.routing.run/v1` | `tier1_routing_run.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `scnet-token-plan` | SCNet Token Plan | 16 | `https://api.scnet.cn/api/llm/v1` | `tier1_scnet_token_plan.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `scx-ai` | SCX.ai | 4 | `https://api.scx.ai/v1` | `tier1_scx_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `stepfun-ai-step-plan` | StepFun Step Plan (Global) | 3 | `https://api.stepfun.ai/step_plan/v1` | `tier1_stepfun_ai_step_plan.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `stepfun-step-plan` | StepFun Step Plan (China) | 4 | `https://api.stepfun.com/step_plan/v1` | `tier1_stepfun_step_plan.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `subconscious` | Subconscious | 2 | `https://api.subconscious.dev/v1` | `tier1_subconscious.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `synthetic` | Synthetic | 9 | `https://api.synthetic.new/openai/v1` | `tier1_synthetic.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `tabnine` | Tabnine | 0 | `—` | `tier1_tabnine.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `tencent-coding-plan` | Tencent Coding Plan (China) | 8 | `https://api.lkeap.cloud.tencent.com/c…` | `tier1_tencent_coding_plan.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `tencent-token-plan` | Tencent Token Plan | 1 | `https://api.lkeap.cloud.tencent.com/p…` | `tier1_tencent_token_plan.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `tencent-tokenhub` | Tencent TokenHub | 3 | `https://tokenhub.tencentmaas.com/v1` | `tier1_tencent_tokenhub.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `tensorx` | TensorX | 25 | `https://api.tensorx.ai/v1` | `tier1_tensorx.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `the-grid-ai` | The Grid AI | 9 | `https://api.thegrid.ai/v1` | `tier1_the_grid_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `tinfoil` | Tinfoil | 9 | `https://inference.tinfoil.sh/v1` | `tier1_tinfoil.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `umans-ai` | Umans AI | 8 | `https://api.code.umans.ai/v1` | `tier1_umans_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `v0` | v0 | 3 | `—` | `tier1_v0.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `venice` | Venice AI | 103 | `https://api.venice.ai/api/v1` | `tier1_venice.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `vivgrid` | Vivgrid | 22 | `https://api.vivgrid.com/v1` | `tier1_vivgrid.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `wafer.ai` | Wafer | 5 | `https://pass.wafer.ai/v1` | `tier1_wafer_ai.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `wandb` | Weights & Biases | 32 | `https://api.inference.wandb.ai/v1` | `tier1_wandb.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `windsurf` | Windsurf (Codeium) | 0 | `—` | `tier1_windsurf.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `xpersona` | Xpersona | 13 | `https://www.xpersona.co/v1` | `tier1_xpersona.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `zai-coding-plan` | Z.AI Coding Plan | 6 | `https://api.z.ai/api/coding/paas/v4` | `tier1_zai_coding_plan.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `zeldoc` | Zeldoc | 1 | `https://api.zeldoc.ai/v1` | `tier1_zeldoc.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |
| `zenifra` | Zenifra | 1 | `https://ai.zenifra.com/v1` | `tier1_zenifra.py` | 🟢 automated | ⚠️ manual (daily-check does NOT auto-run official source) |

Legend: 🟢 automated (check script) · 🟡 manual (in DB, no check) · ⚪ pending (not added yet)

<!-- PROVIDERS:END -->

## Billing modes covered

per-MTok (input/output/cache/batch) · per-image · per-audio-second · per-request ·
credits/points · GPU second/hour · neuron-second · subscription monthly/yearly ·
per-seat · free tier · finetune · provisioned — see `price-types.md`.

## Related docs

- [Data statistics (README)](../README.md) — exact counts
- [Price types & units](price-types.md)
- [Verification & truthfulness](verification.md)
- [Machine format spec](../FORMAT.md)
- [Contribution guide](../CONTRIBUTING.md)
- [Guide for AI agents](../AGENTS.md)
