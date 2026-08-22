> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.

# 供应商全景与状态（providers）

数据库中的每家供应商及其状态与自动化情况。下表由 `python scripts/provider_status.py`
**自动生成**——请勿手改。

- **检查脚本（Check script）**：`scripts/checks/tierN_<供应商>.py` 模块，自动抓取官方定价页
  （由核心路由每 3 小时运行）。
- **状态**：🟢 已自动化（有检查脚本）/ 🟡 人工维护（人工核实或第三方同步）。
- 优化顺序 = 表格顺序：核心模型研发厂商（Tier 0/1）优先，外围在后。
  每家清单：官方页 → 收费模式 → 模型清单/状态 → notes → 人类页面。

<!-- PROVIDERS:BEGIN -->

### Tier 0 — 全球核心模型研发厂商

| # | Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|---|
| 1 | aws | 120 | `https://bedrock-runtime.{region}.amazon…` | `—` | 🟡 manual |
| 2 | nvidia | 100 | `https://integrate.api.nvidia.com/v1` | `—` | 🟡 manual |
| 3 | openai | 47 | `https://api.openai.com/v1` | `tier0_openai.py` | 🟢 automated |
| 4 | google | 40 | `https://generativelanguage.googleapis.c…` | `—` | 🟡 manual |
| 5 | mistral | 33 | `https://api.mistral.ai/v1` | `—` | 🟡 manual |
| 6 | perplexity | 26 | `https://api.perplexity.ai` | `—` | 🟡 manual |
| 7 | xai | 17 | `https://api.x.ai/v1` | `—` | 🟡 manual |
| 8 | anthropic | 16 | `https://api.anthropic.com/v1` | `tier0_anthropic.py` | 🟢 automated |
| 9 | cohere | 14 | `https://api.cohere.com/v1` | `—` | 🟡 manual |
| 10 | deepseek | 5 | `https://api.deepseek.com` | `tier0_deepseek.py` | 🟢 automated |
| 11 | meta | 3 | `https://api.meta.ai/v1` | `—` | 🟡 manual |

### Tier 1 — 中国核心模型研发厂商

| # | Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|---|
| 1 | alibaba-cn | 86 | `https://dashscope.aliyuncs.com/compatib…` | `—` | 🟡 manual |
| 2 | alibaba | 54 | `https://dashscope-intl.aliyuncs.com/com…` | `—` | 🟡 manual |
| 3 | zai | 16 | `https://api.z.ai/api/paas/v4` | `—` | 🟡 manual |
| 4 | zhipuai | 16 | `https://open.bigmodel.cn/api/paas/v4` | `—` | 🟡 manual |
| 5 | moonshotai | 14 | `https://api.moonshot.cn/v1` | `—` | 🟡 manual |
| 6 | xiaomi | 10 | `https://api.xiaomimimo.com/v1` | `tier1_xiaomi.py` | 🟢 automated |
| 7 | stepfun | 8 | `https://api.stepfun.com/v1` | `—` | 🟡 manual |
| 8 | minimax | 7 | `https://api.minimax.chat/v1` | `—` | 🟡 manual |
| 9 | baidu | 3 | `https://qianfan.baidubce.com/v2` | `—` | 🟡 manual |
| 10 | tencent-tokenhub | 2 | `https://tokenhub.tencentmaas.com/v1` | `—` | 🟡 manual |
| 11 | volcengine | 2 | `https://ark.cn-beijing.volces.com/api/v3` | `—` | 🟡 manual |
| 12 | tencent | 1 | `https://api.hunyuan.cloud.tencent.com/v1` | `tier1_tencent.py` | 🟢 automated |

### Tier 2 — 云平台托管

| # | Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|---|
| 1 | azure | 84 | `https://{resource}.openai.azure.com` | `—` | 🟡 manual |
| 2 | google-vertex | 42 | `https://{region}-aiplatform.googleapis.com` | `—` | 🟡 manual |

### Tier 3 — 推理托管平台

| # | Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|---|
| 1 | novita-ai | 107 | `https://api.novita.ai/v3/openai` | `—` | 🟡 manual |
| 2 | digitalocean | 92 | `https://inference.do-ai.run/v1` | `—` | 🟡 manual |
| 3 | huggingface | 69 | `https://router.huggingface.co/v1` | `—` | 🟡 manual |
| 4 | siliconflow | 61 | `https://api.siliconflow.cn/v1` | `—` | 🟡 manual |
| 5 | deepinfra | 60 | `https://api.deepinfra.com/v1/openai` | `—` | 🟡 manual |
| 6 | sap-ai-core | 48 | `https://api.ai.prod.eu-central-1.aws.sa…` | `—` | 🟡 manual |
| 7 | togetherai | 36 | `https://api.together.xyz/v1` | `—` | 🟡 manual |
| 8 | nebius | 34 | `https://api.studio.nebius.ai/v1` | `—` | 🟡 manual |
| 9 | databricks | 30 | `https://${DATABRICKS_HOST}/ai-gateway/m…` | `—` | 🟡 manual |
| 10 | cloudflare-workers-ai | 25 | `https://api.cloudflare.com/client/v4/ac…` | `—` | 🟡 manual |
| 11 | snowflake-cortex | 25 | `https://${SNOWFLAKE_ACCOUNT}.snowflakec…` | `—` | 🟡 manual |
| 12 | fireworks-ai | 23 | `https://api.fireworks.ai/inference/v1/` | `—` | 🟡 manual |
| 13 | baseten | 19 | `https://inference.baseten.co/v1` | `—` | 🟡 manual |
| 14 | groq | 15 | `https://api.groq.com/openai/v1` | `—` | 🟡 manual |
| 15 | ovhcloud | 14 | `https://oai.endpoints.kepler.ai.cloud.o…` | `—` | 🟡 manual |
| 16 | scaleway | 14 | `https://api.scaleway.ai/v1` | `—` | 🟡 manual |
| 17 | vultr | 10 | `https://api.vultrinference.com/v1` | `—` | 🟡 manual |
| 18 | watsonx | 5 | `https://{region}.ml.cloud.ibm.com` | `—` | 🟡 manual |
| 19 | cerebras | 2 | `https://api.cerebras.ai/v1` | `—` | 🟡 manual |
| 20 | modal | 2 | `https://inference.us-west.modal.direct/v1` | `—` | 🟡 manual |

### Tier 4 — 聚合/网关

| # | Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|---|
| 1 | nano-gpt | 597 | `https://api.nano-gpt.com/v1` | `—` | 🟡 manual |
| 2 | llmgateway | 556 | `https://api.llmgateway.io/v1` | `—` | 🟡 manual |
| 3 | openrouter | 420 | `https://openrouter.ai/api/v1` | `—` | 🟡 manual |
| 4 | kilo | 363 | `https://api.kilo.ai/api/gateway` | `—` | 🟡 manual |
| 5 | vercel | 350 | `https://api.vercel.com/v1/ai` | `—` | 🟡 manual |
| 6 | edenai | 232 | `https://api.edenai.run/v3` | `—` | 🟡 manual |
| 7 | merge-gateway | 174 | `https://api-gateway.merge.dev/v1/ai-sdk` | `—` | 🟡 manual |
| 8 | requesty | 139 | `https://router.requesty.ai/v1` | `—` | 🟡 manual |
| 9 | poe | 137 | `https://api.poe.com/v1` | `—` | 🟡 manual |
| 10 | zenmux | 120 | `https://zenmux.ai/api/v1` | `—` | 🟡 manual |
| 11 | 302ai | 97 | `https://api.302.ai/v1` | `—` | 🟡 manual |
| 12 | orcarouter | 81 | `https://api.orcarouter.ai/v1` | `—` | 🟡 manual |
| 13 | aihubmix | 70 | `https://aihubmix.com/v1` | `—` | 🟡 manual |
| 14 | cloudflare-ai-gateway | 67 | `https://gateway.ai.cloudflare.com/v1/{a…` | `—` | 🟡 manual |
| 15 | opencode | 63 | `https://opencode.ai/zen/v1/models` | `—` | 🟡 manual |
| 16 | fastrouter | 47 | `https://go.fastrouter.ai/api/v1` | `—` | 🟡 manual |
| 17 | anyapi | 30 | `https://api.anyapi.ai/v1` | `—` | 🟡 manual |
| 18 | opencode-go | 23 | `https://opencode.ai/zen/go/v1/models` | `—` | 🟡 manual |
| 19 | unorouter | 23 | `https://api.unorouter.com/v1` | `—` | 🟡 manual |

### Tier 5 — 订阅与编码产品

| # | Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|---|
| 1 | github | 33 | `https://api.githubcopilot.com` | `—` | 🟡 manual |
| 2 | v0 | 3 | `—` | `—` | 🟡 manual |
| 3 | cursor | 0 | `—` | `—` | 🟡 manual |
| 4 | devin | 0 | `—` | `—` | 🟡 manual |
| 5 | jetbrains | 0 | `—` | `—` | 🟡 manual |
| 6 | replit | 0 | `—` | `—` | 🟡 manual |
| 7 | tabnine | 0 | `—` | `—` | 🟡 manual |
| 8 | windsurf | 0 | `—` | `—` | 🟡 manual |

### Tier 6 — 长尾

| # | Provider | Models | API base URL | Check script | Status |
|---|---|---|---|---|---|
| 1 | abacus | 108 | `https://routellm.abacus.ai/v1` | `—` | 🟡 manual |
| 2 | cortecs | 108 | `https://api.cortecs.ai/v1` | `—` | 🟡 manual |
| 3 | ofox | 107 | `https://api.ofox.ai/v1` | `—` | 🟡 manual |
| 4 | pioneer | 103 | `https://api.pioneer.ai/v1` | `—` | 🟡 manual |
| 5 | venice | 99 | `https://api.venice.ai/api/v1` | `—` | 🟡 manual |
| 6 | qiniu-ai | 91 | `https://api.qnaigc.com/v1` | `—` | 🟡 manual |
| 7 | helicone | 90 | `https://ai-gateway.helicone.ai/v1` | `—` | 🟡 manual |
| 8 | impossibl | 76 | `https://api.impossibl.com/v1` | `—` | 🟡 manual |
| 9 | jiekou | 61 | `https://api.jiekou.ai/openai` | `—` | 🟡 manual |
| 10 | empiriolabs | 55 | `https://api.empiriolabs.ai/v1` | `—` | 🟡 manual |
| 11 | crossmodel | 52 | `https://api.crossmodel.ai/v1` | `—` | 🟡 manual |
| 12 | neon | 42 | `${NEON_AI_GATEWAY_BASE_URL}/v1` | `—` | 🟡 manual |
| 13 | kenari | 38 | `https://kenari.id/v1` | `—` | 🟡 manual |
| 14 | greenpt | 37 | `https://api.greenpt.ai/v1` | `—` | 🟡 manual |
| 15 | nearai | 37 | `https://cloud-api.near.ai/v1` | `—` | 🟡 manual |
| 16 | llmtr | 32 | `https://llmtr.com/v1` | `—` | 🟡 manual |
| 17 | wandb | 29 | `https://api.inference.wandb.ai/v1` | `—` | 🟡 manual |
| 18 | crof | 26 | `https://crof.ai/v1` | `—` | 🟡 manual |
| 19 | frogbot | 26 | `https://app.frogbot.ai/api/v1` | `—` | 🟡 manual |
| 20 | hyper | 26 | `https://hyper.charm.land/v1` | `—` | 🟡 manual |
| 21 | alibaba-token-plan-cn | 25 | `https://token-plan.cn-beijing.maas.aliy…` | `—` | 🟡 manual |
| 22 | alibaba-token-plan | 25 | `https://token-plan.ap-southeast-1.maas.…` | `—` | 🟡 manual |
| 23 | tensorx | 25 | `https://api.tensorx.ai/v1` | `—` | 🟡 manual |
| 24 | gitlab | 23 | `https://gitlab.com/api/v4/duo` | `—` | 🟡 manual |
| 25 | neuralwatt | 22 | `https://api.neuralwatt.com/v1` | `—` | 🟡 manual |
| 26 | ollama-cloud | 20 | `https://ollama.com/api` | `—` | 🟡 manual |
| 27 | vivgrid | 20 | `https://api.vivgrid.com/v1` | `—` | 🟡 manual |
| 28 | meganova | 19 | `https://api.meganova.ai/v1` | `—` | 🟡 manual |
| 29 | regolo-ai | 18 | `https://api.regolo.ai/v1` | `—` | 🟡 manual |
| 30 | io-net | 17 | `https://api.intelligence.io.solutions/a…` | `—` | 🟡 manual |
| 31 | jalapeno | 17 | `https://api.jalapeno-cloud.ai/v1` | `—` | 🟡 manual |
| 32 | scnet-token-plan | 16 | `https://api.scnet.cn/api/llm/v1` | `—` | 🟡 manual |
| 33 | auriko | 15 | `https://api.auriko.ai/v1` | `—` | 🟡 manual |
| 34 | evroc | 15 | `https://models.think.evroc.com/v1` | `—` | 🟡 manual |
| 35 | model-oracle-ai | 15 | `https://api.modeloracle.com/api/v1` | `—` | 🟡 manual |
| 36 | routing-run | 15 | `https://api.routing.run/v1` | `—` | 🟡 manual |
| 37 | chutes | 14 | `https://llm.chutes.ai/v1` | `—` | 🟡 manual |
| 38 | iflowcn | 14 | `https://api.iflow.cn/v1` | `—` | 🟡 manual |
| 39 | gmicloud | 13 | `https://api.gmi-serving.com/v1` | `—` | 🟡 manual |
| 40 | xpersona | 13 | `https://www.xpersona.co/v1` | `—` | 🟡 manual |
| 41 | alibaba-coding-plan-cn | 12 | `https://coding.dashscope.aliyuncs.com/v1` | `—` | 🟡 manual |
| 42 | alibaba-coding-plan | 12 | `https://coding-intl.dashscope.aliyuncs.…` | `—` | 🟡 manual |
| 43 | clarifai | 12 | `https://api.clarifai.com/v2/ext/openai/v1` | `—` | 🟡 manual |
| 44 | inferx | 12 | `https://model.inferx.net/endpoints/v1` | `—` | 🟡 manual |
| 45 | cline-pass | 11 | `https://api.cline.bot/api/v1` | `—` | 🟡 manual |
| 46 | ambient | 10 | `https://api.ambient.xyz/v1` | `—` | 🟡 manual |
| 47 | freemodel | 10 | `https://cc.freemodel.dev/v1` | `—` | 🟡 manual |
| 48 | infomaniak | 10 | `https://api.infomaniak.com/2/ai/${INFOM…` | `—` | 🟡 manual |
| 49 | aiand | 9 | `https://api.aiand.com/v1` | `—` | 🟡 manual |
| 50 | berget | 9 | `https://api.berget.ai/v1` | `—` | 🟡 manual |
| 51 | daoxe | 9 | `https://daoxe.com/v1` | `—` | 🟡 manual |
| 52 | hpc-ai | 9 | `https://api.hpc-ai.com/inference/v1` | `—` | 🟡 manual |
| 53 | inference | 9 | `https://inference.net/v1` | `—` | 🟡 manual |
| 54 | modelis | 9 | `https://modelishub.com/v1` | `—` | 🟡 manual |
| 55 | qihang-ai | 9 | `https://api.qhaigc.net/v1` | `—` | 🟡 manual |
| 56 | qvac | 9 | `http://localhost:{port}/v1` | `—` | 🟡 manual |
| 57 | submodel | 9 | `https://llm.submodel.ai/v1` | `—` | 🟡 manual |
| 58 | the-grid-ai | 9 | `https://api.thegrid.ai/v1` | `—` | 🟡 manual |
| 59 | crusoe | 8 | `https://api.inference.crusoecloud.com/v1` | `—` | 🟡 manual |
| 60 | stackit | 8 | `https://api.openai-compat.model-serving…` | `—` | 🟡 manual |
| 61 | synthetic | 8 | `https://api.synthetic.new/openai/v1` | `—` | 🟡 manual |
| 62 | tencent-coding-plan | 8 | `https://api.lkeap.cloud.tencent.com/cod…` | `—` | 🟡 manual |
| 63 | tinfoil | 8 | `https://inference.tinfoil.sh/v1` | `—` | 🟡 manual |
| 64 | umans-ai | 8 | `https://api.code.umans.ai/v1` | `—` | 🟡 manual |
| 65 | arcee | 7 | `https://api.arcee.ai/api/v1` | `—` | 🟡 manual |
| 66 | llama | 7 | `https://api.llama.com/compat/v1/` | `—` | 🟡 manual |
| 67 | modelscope | 7 | `https://api-inference.modelscope.cn/v1` | `—` | 🟡 manual |
| 68 | privatemode-ai | 7 | `http://localhost:8080/v1` | `—` | 🟡 manual |
| 69 | trustedrouter | 7 | `https://api.trustedrouter.com/v1` | `—` | 🟡 manual |
| 70 | aki-io | 6 | `https://aki.io/v1` | `—` | 🟡 manual |
| 71 | dinference | 6 | `https://api.dinference.com/v1` | `—` | 🟡 manual |
| 72 | ai-router | 5 | `https://api.ai-router.dev/v1` | `—` | 🟡 manual |
| 73 | atomic-chat | 5 | `http://127.0.0.1:1337/v1` | `—` | 🟡 manual |
| 74 | cloudferro-sherlock | 5 | `https://api-sherlock.cloudferro.com/ope…` | `—` | 🟡 manual |
| 75 | friendli | 5 | `https://api.friendli.ai/serverless/v1` | `—` | 🟡 manual |
| 76 | mixlayer | 5 | `https://models.mixlayer.ai/v1` | `—` | 🟡 manual |
| 77 | runinfra | 5 | `https://api.runinfra.ai/v1` | `—` | 🟡 manual |
| 78 | wafer.ai | 5 | `https://pass.wafer.ai/v1` | `—` | 🟡 manual |
| 79 | ebcloud | 4 | `https://maas-api.ebcloud.com/v1` | `—` | 🟡 manual |
| 80 | inceptron | 4 | `https://api.inceptron.io/v1` | `—` | 🟡 manual |
| 81 | lilac | 4 | `https://api.getlilac.com/v1` | `—` | 🟡 manual |
| 82 | lucidquery | 4 | `https://api.lucidquery.com/v1` | `—` | 🟡 manual |
| 83 | sakana | 4 | `https://api.sakana.ai/v1` | `—` | 🟡 manual |
| 84 | scx-ai | 4 | `https://api.scx.ai/v1` | `—` | 🟡 manual |
| 85 | stepfun-step-plan | 4 | `https://api.stepfun.com/step_plan/v1` | `—` | 🟡 manual |
| 86 | upstage | 4 | `https://api.upstage.ai/v1/solar` | `—` | 🟡 manual |
| 87 | coralbricks | 3 | `https://inference.coralbricks.ai/v1` | `—` | 🟡 manual |
| 88 | drun | 3 | `https://chat.d.run/v1` | `—` | 🟡 manual |
| 89 | lmstudio | 3 | `http://localhost:1234/v1` | `—` | 🟡 manual |
| 90 | morph | 3 | `https://api.morphllm.com/v1` | `—` | 🟡 manual |
| 91 | poolside | 3 | `https://inference.poolside.ai/v1` | `—` | 🟡 manual |
| 92 | stepfun-ai-step-plan | 3 | `https://api.stepfun.ai/step_plan/v1` | `—` | 🟡 manual |
| 93 | abliteration-ai | 2 | `https://api.abliteration.ai/v1` | `—` | 🟡 manual |
| 94 | bailing | 2 | `https://api.tbox.cn/api/llm/v1/chat/com…` | `—` | 🟡 manual |
| 95 | blueclaw | 2 | `https://openai.blueclaw.network/v1` | `—` | 🟡 manual |
| 96 | claudinio | 2 | `https://api.claudin.io/v1` | `—` | 🟡 manual |
| 97 | hetzner | 2 | `https://inference.hetzner.com/api/v1` | `—` | 🟡 manual |
| 98 | inception | 2 | `https://api.inceptionlabs.ai/v1/` | `—` | 🟡 manual |
| 99 | moark | 2 | `https://moark.com/v1` | `—` | 🟡 manual |
| 100 | nova | 2 | `https://api.nova.amazon.com/v1` | `—` | 🟡 manual |
| 101 | sarvam | 2 | `https://api.sarvam.ai/v1` | `—` | 🟡 manual |
| 102 | subconscious | 2 | `https://api.subconscious.dev/v1` | `—` | 🟡 manual |
| 103 | thinkingmachines | 2 | `https://tinker.thinkingmachines.dev/ser…` | `—` | 🟡 manual |
| 104 | amd | 1 | `https://developer.amd.com.cn/radeon/api/v1` | `—` | 🟡 manual |
| 105 | echo | 1 | `https://echo.tracerml.ai/v1` | `—` | 🟡 manual |
| 106 | kosmik | 1 | `https://api.koscompute.com/v1` | `—` | 🟡 manual |
| 107 | kuae-cloud-coding-plan | 1 | `https://coding-plan-endpoint.kuaecloud.…` | `—` | 🟡 manual |
| 108 | longcat | 1 | `https://api.longcat.chat/openai` | `—` | 🟡 manual |
| 109 | lynkr | 1 | `http://127.0.0.1:8081/v1` | `—` | 🟡 manual |
| 110 | salad-cloud | 1 | `https://api.salad.com/v1` | `—` | 🟡 manual |
| 111 | tencent-token-plan | 1 | `https://api.lkeap.cloud.tencent.com/pla…` | `—` | 🟡 manual |
| 112 | zeldoc | 1 | `https://api.zeldoc.ai/v1` | `—` | 🟡 manual |
| 113 | zenifra | 1 | `https://ai.zenifra.com/v1` | `—` | 🟡 manual |


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
