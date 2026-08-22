> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.

# 供应商全景与状态（providers）

数据库中的每家供应商及其状态与自动化情况。下表由 `python scripts/provider_status.py`
**自动生成**——请勿手改。

- **检查脚本（Check script）**：`scripts/checks/tierN_<供应商>.py` 模块，自动抓取官方定价页
  （由核心路由每 3 小时运行）。
- **状态**：🟢 已自动化（有检查脚本）/ 🟡 人工维护（已入库、无检查脚本）/ ⚪ 待添加（尚未收录）。
- **层级（按模型研发实力划分，非按地区）**：
  - **Tier 0** — 全球最头部模型研发厂商；
  - **Tier 1** — 其他大语言模型研发大厂；
  - **Tier 2** — 其余所有模型研发厂商（任意模型类型）；
  - **Tier 3** — 核心模型中转商/托管商/聚合类网关；
  - **Tier 4** — 其他服务提供商（订阅产品、长尾）。
- 每个 tier 内按字母排序并去重。

<!-- PROVIDERS:BEGIN -->

### Tier 0 — 全球最头部模型研发厂商

| Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|
| `alibaba` | 54 | `https://dashscope-intl.aliyuncs.com/c…` | `—` | 🟡 manual |
| `anthropic` | 16 | `https://api.anthropic.com/v1` | `tier0_anthropic.py` | 🟢 automated |
| `deepseek` | 5 | `https://api.deepseek.com` | `tier0_deepseek.py` | 🟢 automated |
| `google` | 40 | `https://generativelanguage.googleapis…` | `—` | 🟡 manual |
| `meta` | 3 | `https://api.meta.ai/v1` | `—` | 🟡 manual |
| `minimax` | 7 | `https://api.minimax.chat/v1` | `—` | 🟡 manual |
| `mistral` | 33 | `https://api.mistral.ai/v1` | `—` | 🟡 manual |
| `moonshotai` | 14 | `https://api.moonshot.cn/v1` | `—` | 🟡 manual |
| `openai` | 47 | `https://api.openai.com/v1` | `tier0_openai.py` | 🟢 automated |
| `xai` | 17 | `https://api.x.ai/v1` | `—` | 🟡 manual |
| `zai` | 16 | `https://api.z.ai/api/paas/v4` | `—` | 🟡 manual |

### Tier 1 — 其他大语言模型研发大厂

| Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|
| `aws` | 120 | `https://bedrock-runtime.{region}.amaz…` | `—` | 🟡 manual |
| `baidu` | 3 | `https://qianfan.baidubce.com/v2` | `—` | 🟡 manual |
| `cohere` | 14 | `https://api.cohere.com/v1` | `—` | 🟡 manual |
| `nvidia` | 100 | `https://integrate.api.nvidia.com/v1` | `—` | 🟡 manual |
| `perplexity` | 26 | `https://api.perplexity.ai` | `—` | 🟡 manual |
| `stepfun` | 8 | `https://api.stepfun.com/v1` | `—` | 🟡 manual |
| `tencent` | 1 | `https://api.hunyuan.cloud.tencent.com/v1` | `tier1_tencent.py` | 🟢 automated |
| `upstage` | 4 | `https://api.upstage.ai/v1/solar` | `—` | 🟡 manual |
| `volcengine` | 2 | `https://ark.cn-beijing.volces.com/api/v3` | `—` | 🟡 manual |
| `xiaomi` | 10 | `https://api.xiaomimimo.com/v1` | `tier1_xiaomi.py` | 🟢 automated |
| `zhipuai` | 16 | `https://open.bigmodel.cn/api/paas/v4` | `—` | 🟡 manual |
| `ai21` (AI21 Labs) | — | `https://api.ai21.com/studio/v1` | `—` | ⚪ pending |
| `baichuan` (Baichuan AI) | — | `https://api.baichuan-ai.com/v1` | `—` | ⚪ pending |
| `iflytek` (iFlytek Spark) | — | `https://spark-api-open.xf-yun.com/v1` | `—` | ⚪ pending |
| `lingyiwanwu` (01.AI (Lingyiwanwu)) | — | `https://api.lingyiwanwu.com/v1` | `—` | ⚪ pending |

### Tier 2 — 其他模型研发厂商

| Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|
| `arcee` | 7 | `https://api.arcee.ai/api/v1` | `—` | 🟡 manual |
| `inception` | 2 | `https://api.inceptionlabs.ai/v1/` | `—` | 🟡 manual |
| `lilac` | 4 | `https://api.getlilac.com/v1` | `—` | 🟡 manual |
| `morph` | 3 | `https://api.morphllm.com/v1` | `—` | 🟡 manual |
| `nova` | 2 | `https://api.nova.amazon.com/v1` | `—` | 🟡 manual |
| `poolside` | 3 | `https://inference.poolside.ai/v1` | `—` | 🟡 manual |
| `sakana` | 4 | `https://api.sakana.ai/v1` | `—` | 🟡 manual |
| `sarvam` | 2 | `https://api.sarvam.ai/v1` | `—` | 🟡 manual |
| `submodel` | 9 | `https://llm.submodel.ai/v1` | `—` | 🟡 manual |
| `thinkingmachines` | 2 | `https://tinker.thinkingmachines.dev/s…` | `—` | 🟡 manual |
| `assemblyai` (AssemblyAI) | — | `https://api.assemblyai.com/v2` | `—` | ⚪ pending |
| `cartesia` (Cartesia) | — | `https://api.cartesia.ai/v1` | `—` | ⚪ pending |
| `deepgram` (Deepgram) | — | `https://api.deepgram.com/v1` | `—` | ⚪ pending |
| `elevenlabs` (ElevenLabs) | — | `https://api.elevenlabs.io/v1` | `—` | ⚪ pending |
| `playai` (PlayAI) | — | `https://api.play.ai/v1` | `—` | ⚪ pending |
| `stability` (Stability AI) | — | `https://api.stability.ai/v1` | `—` | ⚪ pending |

### Tier 3 — 核心模型中转/托管/聚合网关

| Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|
| `302ai` | 97 | `https://api.302.ai/v1` | `—` | 🟡 manual |
| `ai-router` | 5 | `https://api.ai-router.dev/v1` | `—` | 🟡 manual |
| `aihubmix` | 70 | `https://aihubmix.com/v1` | `—` | 🟡 manual |
| `anyapi` | 30 | `https://api.anyapi.ai/v1` | `—` | 🟡 manual |
| `baseten` | 19 | `https://inference.baseten.co/v1` | `—` | 🟡 manual |
| `cerebras` | 2 | `https://api.cerebras.ai/v1` | `—` | 🟡 manual |
| `cloudflare-ai-gateway` | 67 | `https://gateway.ai.cloudflare.com/v1/…` | `—` | 🟡 manual |
| `cloudflare-workers-ai` | 25 | `https://api.cloudflare.com/client/v4/…` | `—` | 🟡 manual |
| `crusoe` | 8 | `https://api.inference.crusoecloud.com/v1` | `—` | 🟡 manual |
| `databricks` | 30 | `https://${DATABRICKS_HOST}/ai-gateway…` | `—` | 🟡 manual |
| `deepinfra` | 60 | `https://api.deepinfra.com/v1/openai` | `—` | 🟡 manual |
| `digitalocean` | 92 | `https://inference.do-ai.run/v1` | `—` | 🟡 manual |
| `edenai` | 234 | `https://api.edenai.run/v3` | `—` | 🟡 manual |
| `fastrouter` | 47 | `https://go.fastrouter.ai/api/v1` | `—` | 🟡 manual |
| `fireworks-ai` | 23 | `https://api.fireworks.ai/inference/v1/` | `—` | 🟡 manual |
| `friendli` | 5 | `https://api.friendli.ai/serverless/v1` | `—` | 🟡 manual |
| `groq` | 15 | `https://api.groq.com/openai/v1` | `—` | 🟡 manual |
| `helicone` | 90 | `https://ai-gateway.helicone.ai/v1` | `—` | 🟡 manual |
| `hetzner` | 2 | `https://inference.hetzner.com/api/v1` | `—` | 🟡 manual |
| `huggingface` | 69 | `https://router.huggingface.co/v1` | `—` | 🟡 manual |
| `jiekou` | 61 | `https://api.jiekou.ai/openai` | `—` | 🟡 manual |
| `kilo` | 367 | `https://api.kilo.ai/api/gateway` | `—` | 🟡 manual |
| `llmgateway` | 556 | `https://api.llmgateway.io/v1` | `—` | 🟡 manual |
| `merge-gateway` | 175 | `https://api-gateway.merge.dev/v1/ai-sdk` | `—` | 🟡 manual |
| `modal` | 2 | `https://inference.us-west.modal.direc…` | `—` | 🟡 manual |
| `nano-gpt` | 599 | `https://api.nano-gpt.com/v1` | `—` | 🟡 manual |
| `nebius` | 34 | `https://api.studio.nebius.ai/v1` | `—` | 🟡 manual |
| `novita-ai` | 107 | `https://api.novita.ai/v3/openai` | `—` | 🟡 manual |
| `ollama-cloud` | 20 | `https://ollama.com/api` | `—` | 🟡 manual |
| `opencode` | 95 | `https://opencode.ai/zen/v1/models` | `—` | 🟡 manual |
| `opencode-go` | 28 | `https://opencode.ai/zen/go/v1/models` | `—` | 🟡 manual |
| `openrouter` | 421 | `https://openrouter.ai/api/v1` | `—` | 🟡 manual |
| `orcarouter` | 81 | `https://api.orcarouter.ai/v1` | `—` | 🟡 manual |
| `ovhcloud` | 14 | `https://oai.endpoints.kepler.ai.cloud…` | `—` | 🟡 manual |
| `poe` | 137 | `https://api.poe.com/v1` | `—` | 🟡 manual |
| `requesty` | 139 | `https://router.requesty.ai/v1` | `—` | 🟡 manual |
| `runinfra` | 5 | `https://api.runinfra.ai/v1` | `—` | 🟡 manual |
| `salad-cloud` | 1 | `https://api.salad.com/v1` | `—` | 🟡 manual |
| `sap-ai-core` | 48 | `https://api.ai.prod.eu-central-1.aws.…` | `—` | 🟡 manual |
| `scaleway` | 15 | `https://api.scaleway.ai/v1` | `—` | 🟡 manual |
| `siliconflow` | 61 | `https://api.siliconflow.cn/v1` | `—` | 🟡 manual |
| `snowflake-cortex` | 25 | `https://${SNOWFLAKE_ACCOUNT}.snowflak…` | `—` | 🟡 manual |
| `stackit` | 8 | `https://api.openai-compat.model-servi…` | `—` | 🟡 manual |
| `togetherai` | 36 | `https://api.together.xyz/v1` | `—` | 🟡 manual |
| `trustedrouter` | 7 | `https://api.trustedrouter.com/v1` | `—` | 🟡 manual |
| `unorouter` | 23 | `https://api.unorouter.com/v1` | `—` | 🟡 manual |
| `vercel` | 351 | `https://api.vercel.com/v1/ai` | `—` | 🟡 manual |
| `vultr` | 10 | `https://api.vultrinference.com/v1` | `—` | 🟡 manual |
| `watsonx` | 5 | `https://{region}.ml.cloud.ibm.com` | `—` | 🟡 manual |
| `zenmux` | 120 | `https://zenmux.ai/api/v1` | `—` | 🟡 manual |
| `runpod` (RunPod) | — | `https://api.runpod.ai/v2` | `—` | ⚪ pending |
| `vast` (Vast.ai) | — | `https://console.vast.ai/api/v0` | `—` | ⚪ pending |

### Tier 4 — 其他服务提供商（长尾）

| Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|
| `abacus` | 108 | `https://routellm.abacus.ai/v1` | `—` | 🟡 manual |
| `abliteration-ai` | 2 | `https://api.abliteration.ai/v1` | `—` | 🟡 manual |
| `aiand` | 9 | `https://api.aiand.com/v1` | `—` | 🟡 manual |
| `aki-io` | 6 | `https://aki.io/v1` | `—` | 🟡 manual |
| `alibaba-cn` | 86 | `https://dashscope.aliyuncs.com/compat…` | `—` | 🟡 manual |
| `alibaba-coding-plan` | 12 | `https://coding-intl.dashscope.aliyunc…` | `—` | 🟡 manual |
| `alibaba-coding-plan-cn` | 12 | `https://coding.dashscope.aliyuncs.com/v1` | `—` | 🟡 manual |
| `alibaba-token-plan` | 25 | `https://token-plan.ap-southeast-1.maa…` | `—` | 🟡 manual |
| `alibaba-token-plan-cn` | 25 | `https://token-plan.cn-beijing.maas.al…` | `—` | 🟡 manual |
| `ambient` | 10 | `https://api.ambient.xyz/v1` | `—` | 🟡 manual |
| `amd` | 1 | `https://developer.amd.com.cn/radeon/a…` | `—` | 🟡 manual |
| `atomic-chat` | 5 | `http://127.0.0.1:1337/v1` | `—` | 🟡 manual |
| `auriko` | 15 | `https://api.auriko.ai/v1` | `—` | 🟡 manual |
| `azure` | 84 | `https://{resource}.openai.azure.com` | `—` | 🟡 manual |
| `bailing` | 2 | `https://api.tbox.cn/api/llm/v1/chat/c…` | `—` | 🟡 manual |
| `berget` | 9 | `https://api.berget.ai/v1` | `—` | 🟡 manual |
| `blueclaw` | 2 | `https://openai.blueclaw.network/v1` | `—` | 🟡 manual |
| `chutes` | 14 | `https://llm.chutes.ai/v1` | `—` | 🟡 manual |
| `clarifai` | 12 | `https://api.clarifai.com/v2/ext/opena…` | `—` | 🟡 manual |
| `claudinio` | 2 | `https://api.claudin.io/v1` | `—` | 🟡 manual |
| `cline-pass` | 11 | `https://api.cline.bot/api/v1` | `—` | 🟡 manual |
| `cloudferro-sherlock` | 5 | `https://api-sherlock.cloudferro.com/o…` | `—` | 🟡 manual |
| `coralbricks` | 3 | `https://inference.coralbricks.ai/v1` | `—` | 🟡 manual |
| `cortecs` | 108 | `https://api.cortecs.ai/v1` | `—` | 🟡 manual |
| `crof` | 26 | `https://crof.ai/v1` | `—` | 🟡 manual |
| `crossmodel` | 53 | `https://api.crossmodel.ai/v1` | `—` | 🟡 manual |
| `cursor` | 0 | `—` | `—` | 🟡 manual |
| `daoxe` | 9 | `https://daoxe.com/v1` | `—` | 🟡 manual |
| `devin` | 0 | `—` | `—` | 🟡 manual |
| `dinference` | 6 | `https://api.dinference.com/v1` | `—` | 🟡 manual |
| `drun` | 3 | `https://chat.d.run/v1` | `—` | 🟡 manual |
| `ebcloud` | 4 | `https://maas-api.ebcloud.com/v1` | `—` | 🟡 manual |
| `echo` | 1 | `https://echo.tracerml.ai/v1` | `—` | 🟡 manual |
| `empiriolabs` | 55 | `https://api.empiriolabs.ai/v1` | `—` | 🟡 manual |
| `evroc` | 15 | `https://models.think.evroc.com/v1` | `—` | 🟡 manual |
| `freemodel` | 10 | `https://cc.freemodel.dev/v1` | `—` | 🟡 manual |
| `frogbot` | 26 | `https://app.frogbot.ai/api/v1` | `—` | 🟡 manual |
| `github` | 33 | `https://api.githubcopilot.com` | `—` | 🟡 manual |
| `gitlab` | 23 | `https://gitlab.com/api/v4/duo` | `—` | 🟡 manual |
| `gmicloud` | 13 | `https://api.gmi-serving.com/v1` | `—` | 🟡 manual |
| `google-vertex` | 43 | `https://{region}-aiplatform.googleapi…` | `—` | 🟡 manual |
| `greenpt` | 37 | `https://api.greenpt.ai/v1` | `—` | 🟡 manual |
| `hpc-ai` | 9 | `https://api.hpc-ai.com/inference/v1` | `—` | 🟡 manual |
| `hyper` | 26 | `https://hyper.charm.land/v1` | `—` | 🟡 manual |
| `iflowcn` | 14 | `https://api.iflow.cn/v1` | `—` | 🟡 manual |
| `impossibl` | 76 | `https://api.impossibl.com/v1` | `—` | 🟡 manual |
| `inceptron` | 4 | `https://api.inceptron.io/v1` | `—` | 🟡 manual |
| `inference` | 9 | `https://inference.net/v1` | `—` | 🟡 manual |
| `inferx` | 12 | `https://model.inferx.net/endpoints/v1` | `—` | 🟡 manual |
| `infomaniak` | 10 | `https://api.infomaniak.com/2/ai/${INF…` | `—` | 🟡 manual |
| `io-net` | 17 | `https://api.intelligence.io.solutions…` | `—` | 🟡 manual |
| `jalapeno` | 17 | `https://api.jalapeno-cloud.ai/v1` | `—` | 🟡 manual |
| `jetbrains` | 0 | `—` | `—` | 🟡 manual |
| `kenari` | 38 | `https://kenari.id/v1` | `—` | 🟡 manual |
| `kosmik` | 1 | `https://api.koscompute.com/v1` | `—` | 🟡 manual |
| `kuae-cloud-coding-plan` | 1 | `https://coding-plan-endpoint.kuaeclou…` | `—` | 🟡 manual |
| `llama` | 7 | `https://api.llama.com/compat/v1/` | `—` | 🟡 manual |
| `llmtr` | 32 | `https://llmtr.com/v1` | `—` | 🟡 manual |
| `lmstudio` | 3 | `http://localhost:1234/v1` | `—` | 🟡 manual |
| `longcat` | 1 | `https://api.longcat.chat/openai` | `—` | 🟡 manual |
| `lucidquery` | 4 | `https://api.lucidquery.com/v1` | `—` | 🟡 manual |
| `lynkr` | 1 | `http://127.0.0.1:8081/v1` | `—` | 🟡 manual |
| `meganova` | 19 | `https://api.meganova.ai/v1` | `—` | 🟡 manual |
| `mixlayer` | 5 | `https://models.mixlayer.ai/v1` | `—` | 🟡 manual |
| `moark` | 2 | `https://moark.com/v1` | `—` | 🟡 manual |
| `model-oracle-ai` | 15 | `https://api.modeloracle.com/api/v1` | `—` | 🟡 manual |
| `modelis` | 9 | `https://modelishub.com/v1` | `—` | 🟡 manual |
| `modelscope` | 7 | `https://api-inference.modelscope.cn/v1` | `—` | 🟡 manual |
| `nearai` | 37 | `https://cloud-api.near.ai/v1` | `—` | 🟡 manual |
| `neon` | 42 | `${NEON_AI_GATEWAY_BASE_URL}/v1` | `—` | 🟡 manual |
| `neuralwatt` | 22 | `https://api.neuralwatt.com/v1` | `—` | 🟡 manual |
| `ofox` | 110 | `https://api.ofox.ai/v1` | `—` | 🟡 manual |
| `pioneer` | 103 | `https://api.pioneer.ai/v1` | `—` | 🟡 manual |
| `privatemode-ai` | 7 | `http://localhost:8080/v1` | `—` | 🟡 manual |
| `qihang-ai` | 9 | `https://api.qhaigc.net/v1` | `—` | 🟡 manual |
| `qiniu-ai` | 91 | `https://api.qnaigc.com/v1` | `—` | 🟡 manual |
| `qvac` | 9 | `http://localhost:{port}/v1` | `—` | 🟡 manual |
| `regolo-ai` | 18 | `https://api.regolo.ai/v1` | `—` | 🟡 manual |
| `replit` | 0 | `—` | `—` | 🟡 manual |
| `routing-run` | 15 | `https://api.routing.run/v1` | `—` | 🟡 manual |
| `scnet-token-plan` | 16 | `https://api.scnet.cn/api/llm/v1` | `—` | 🟡 manual |
| `scx-ai` | 4 | `https://api.scx.ai/v1` | `—` | 🟡 manual |
| `stepfun-ai-step-plan` | 3 | `https://api.stepfun.ai/step_plan/v1` | `—` | 🟡 manual |
| `stepfun-step-plan` | 4 | `https://api.stepfun.com/step_plan/v1` | `—` | 🟡 manual |
| `subconscious` | 2 | `https://api.subconscious.dev/v1` | `—` | 🟡 manual |
| `synthetic` | 8 | `https://api.synthetic.new/openai/v1` | `—` | 🟡 manual |
| `tabnine` | 0 | `—` | `—` | 🟡 manual |
| `tencent-coding-plan` | 8 | `https://api.lkeap.cloud.tencent.com/c…` | `—` | 🟡 manual |
| `tencent-token-plan` | 1 | `https://api.lkeap.cloud.tencent.com/p…` | `—` | 🟡 manual |
| `tencent-tokenhub` | 2 | `https://tokenhub.tencentmaas.com/v1` | `—` | 🟡 manual |
| `tensorx` | 25 | `https://api.tensorx.ai/v1` | `—` | 🟡 manual |
| `the-grid-ai` | 9 | `https://api.thegrid.ai/v1` | `—` | 🟡 manual |
| `tinfoil` | 8 | `https://inference.tinfoil.sh/v1` | `—` | 🟡 manual |
| `umans-ai` | 8 | `https://api.code.umans.ai/v1` | `—` | 🟡 manual |
| `v0` | 3 | `—` | `—` | 🟡 manual |
| `venice` | 100 | `https://api.venice.ai/api/v1` | `—` | 🟡 manual |
| `vivgrid` | 20 | `https://api.vivgrid.com/v1` | `—` | 🟡 manual |
| `wafer.ai` | 5 | `https://pass.wafer.ai/v1` | `—` | 🟡 manual |
| `wandb` | 29 | `https://api.inference.wandb.ai/v1` | `—` | 🟡 manual |
| `windsurf` | 0 | `—` | `—` | 🟡 manual |
| `xpersona` | 13 | `https://www.xpersona.co/v1` | `—` | 🟡 manual |
| `zeldoc` | 1 | `https://api.zeldoc.ai/v1` | `—` | 🟡 manual |
| `zenifra` | 1 | `https://ai.zenifra.com/v1` | `—` | 🟡 manual |

Legend: 🟢 automated (check script) · 🟡 manual (in DB, no check) · ⚪ pending (not added yet)

<!-- PROVIDERS:END -->

## 覆盖的收费形式

per-MTok（输入/输出/缓存/批处理）· 按图 · 按音频秒 · 按请求 · 点数制 ·
GPU 秒/小时 · 神经元秒 · 订阅月付/年付 · 按席位 · 免费额度 · 微调 · 预留容量
—— 详见 `docs/price-types.md`。

## 相关文档

- [数据统计（README）](../README.zh-CN.md) —— 精确计数
- [收费形式口径](price-types.zh-CN.md)
- [核实与真实性机制](verification.zh-CN.md)
- [机器格式规范](../FORMAT.zh-CN.md)
- [贡献指南](../CONTRIBUTING.zh-CN.md)
- [AI Agent 指南](../AGENTS.md)（英文）
