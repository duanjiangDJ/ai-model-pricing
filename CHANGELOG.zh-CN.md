> **Language: 中文（简体）(zh-CN)** — This document is written in zh-CN only.

# Changelog / 变更日志

## 版本规则（Versioning）

版本号格式：**`年份.内容更新.功能更新`**（如 `26.2.3` = 2026 年第 2 次内容更新、第 3 次功能更新）。

- **年份**：首次发布所在年份（两位数，如 2026 → `26`）；年份变化时重置后两段为 0。
- **内容更新**（第二段，+1）：**仅限定价数据**——价格变化、模型新增/退役（status 变更）、订阅计划新增/改价。示例：修正某模型 input/output、新增 ChatGPT Go 计划、标记模型下线。
- **功能更新**（第三段，+1）：**除定价以外的所有变更**——数据结构（schema/格式）、脚本（router/checks/toolbox）、工作流、文档、翻译、目录重组、CI 机制。示例：新增检查脚本、重命名目录、更新 AGENTS。
- 边界判定：一个 PR 同时含定价与功能变更时，按**主要变更类型**只 bump 一段（定价为主→内容更新；其余→功能更新）。
- 两条规则都只 +1 自身段位，**互不重置**。
- 当前版本见 `VERSION` 文件；`data/feed/schema.json` 的 `version` 与各数据文件 `schema_version` 与之一致。
- 版本递增由维护者/机器人按变更类型决定，记录于本文件条目。

---

## 26.16.24 — 2026-08-31T03:24Z（内容更新）

- 价格同步（77 处变更）：
- **alibaba**（更新 14）：`qwen3.7-plus`, `qwen3.6-flash`, `qwen-vl-ocr`, `qwen3.6-35b-a3b`, `qwen3-next-80b-a3b-thinking`, `qwen3-next-80b-a3b-instruct`, `qwen3-32b` — 入 $0.72 出 $0.72; 入 $0.7 出 $2.8; 入 $0.5 出 $2; 入 $0.5 出 $6; 入 $0.248 出 $1.485; 入 $0.1875 出 $1.125; 入 $0.5 出 $3
- **berget**（新增 2）：`zai-org/GLM-5.3`, `zai-org/GLM-5.3-Flash`
- **deepseek**（更新 6）：`deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-v4-flash-vision-exp` — 入 $0.14 出 $0.28 缓存 $0.0028; 入 $0.14 出 $0.28 缓存 $0.0028; 入 $0.435 出 $0.87
- **edenai**（更新 6）：`flexai/Muse-Glimmer-30B`, `mistral/codestral-latest`, `mistral/devstral-2512`, `mistral/mistral-medium-2604`, `mistral/mistral-medium-latest`, `mistral/mistral-small-latest` — 出 $1.1; 缓存 $0.03; 入 $0.4 出 $2 缓存 $0.04; 缓存 $0.15; 缓存 $0.15; 缓存 $0.015
- **kilo**（更新 5）：`deepseek/deepseek-v4-flash-vision-exp`, `mistralai/devstral-2512`, `mistralai/mistral-nemo`, `mistralai/mistral-small-3.2-24b-instruct`, `~deepseek/deepseek-v4-flash-latest` — 入 $0.44 出 $1.32 缓存 $0.014; 入 $0.4 出 $2 缓存 $0.04; 入 $0.019 出 $0.03; 入 $0.075 出 $0.2; 缓存 $0.013
- **minimax**（更新 2）：`MiniMax-M2.5-highspeed` — 缓存 $0.06
- **mistral**（更新 2）：`ministral-3b-latest`, `ministral-8b-latest` — 入 $0.04 出 $0.04; 入 $0.1 出 $0.1
- **nano-gpt**（更新 33）：`Gemma-4-26B-A4B-MeroMero`, `Gemma-4-26B-A4B-MeroMero:thinking`, `Gemma-4-31B-MeroMero-v2`, `Gemma-4-31B-MeroMero-v2:thinking`, `deepseek/deepseek-v4-flash-vision-exp`, `gemma-4-26b-a4b-it-chimerax`, `gemma-4-26b-a4b-it-darksoul`, `gemma-4-26b-a4b-it-luminous`, `gemma-4-26b-a4b-it-moonlight`, `gemma-4-26b-a4b-it-musica`, `gemma-4-26b-a4b-it-opusdistill`, `gemma-4-26b-a4b-it-shadowsiren`, `gemma-4-26b-a4b-uncensored`, `gemma-4-26b-a4b-uncensored:thinking`, `gemma-4-31b-it-darkidol`, `gemma-4-31b-it-fabled`, `gemma-4-31b-it-garnet`, `gemma-4-31b-it-gembrain`, `gemma-4-31b-it-gemsicle`, `gemma-4-31b-it-isometry`, `gemma-4-31b-it-novelist`, `google/gemma-4-26b-a4b-it`, `google/gemma-4-31b-it`, `ornith-ai/ornith-1.5-9b`, `ornith-ai/ornith-1.5-9b:thinking`, `qwen/qwen3.6-35b-a3b-uncensored`, `qwen/qwen3.6-35b-a3b-uncensored:thinking`, `qwen/qwen3.8-27b-fable`, `qwen/qwen3.8-27b-obliterated`, `qwen/qwen3.8-27b-obliterated:thinking`, `qwen/qwen3.8-27b-uncensored`, `qwen/qwen3.8-27b-uncensored:thinking`, `z-ai/glm-5.3-flash-uncensored` — 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.1 出 $0.45 缓存 $0.05; 入 $0.1 出 $0.45 缓存 $0.05; 入 $0.44 出 $1.32 缓存 $0.014; 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.1 出 $0.45 缓存 $0.05; 入 $0.1 出 $0.45 缓存 $0.05; 入 $0.1 出 $0.45 缓存 $0.05; 入 $0.1 出 $0.45 缓存 $0.05; 入 $0.1 出 $0.45 缓存 $0.05; 入 $0.1 出 $0.45 缓存 $0.05; 入 $0.1 出 $0.45 缓存 $0.05; 入 $0.12 出 $0.38 缓存 $0.06; 入 $0.1 出 $0.45 缓存 $0.05; 入 $0.1 出 $0.2 缓存 $0.05; 入 $0.1 出 $0.2 缓存 $0.05; 出 $0.95; 出 $0.95; 入 $0.25 出 $1.5 缓存 $0.125; 入 $0.25 出 $1.5 缓存 $0.125; 入 $0.25 出 $1.5 缓存 $0.125; 入 $0.25 出 $1.5 缓存 $0.125; 入 $0.25 出 $1.5 缓存 $0.125; 入 $0.35 出 $1.4 缓存 $0.175
- **openrouter**（更新 7）：`deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-flash-vision-exp`, `deepseek/deepseek-v4-pro`, `deepseek/deepseek-v4-pro-0813`, `meta-llama/llama-4-maverick`, `moonshotai/kimi-k2.5`, `tencent/hy3`
- **trustedrouter**（新增 7）：`trustedrouter/auto`, `trustedrouter/cheap`, `trustedrouter/e2e`, `trustedrouter/fast`, `trustedrouter/synth`, `trustedrouter/synth-code`, `trustedrouter/zdr`
- **vercel**（新增 1）：`minimax/minimax-h3-max`

## 26.15.24 — 2026-08-30T23:24Z（内容更新）

- 价格同步（1 处变更）：
- **openrouter**（更新 1）：`deepseek/deepseek-v4-flash`

## 26.14.24 — 2026-08-30T20:54Z（内容更新）

- 价格同步（3 处变更）：
- **neuralwatt**（新增 1）：`glm-5.3`
- **openrouter**（更新 2）：`openai/gpt-4.1-nano`, `~deepseek/deepseek-v4-flash-latest`

## 26.13.24 — 2026-08-30T16:27Z（内容更新）

- 价格同步（4 处变更）：
- **openrouter**（更新 4）：`deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`, `mistralai/devstral-2512`, `tencent/hy3`

## 26.12.24 — 2026-08-30T11:39Z（内容更新）

- 价格同步（3 处变更）：
- **openrouter**（更新 3）：`arcee-ai/trinity-large-thinking`, `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`

## 26.11.24 — 2026-08-30T04:43Z（内容更新）

- 价格同步（88 处变更）：
- **aiand**（新增 2）：`qwen/qwen3.8-27b`, `zai-org/glm-5.3`
- **alibaba**（更新 14）：`qwen3.7-plus`, `qwen3.6-flash`, `qwen-vl-ocr`, `qwen3.6-35b-a3b`, `qwen3-next-80b-a3b-thinking`, `qwen3-next-80b-a3b-instruct`, `qwen3-32b` — 入 $0.72 出 $0.72; 入 $0.7 出 $2.8; 入 $0.5 出 $2; 入 $0.5 出 $6; 入 $0.248 出 $1.485; 入 $0.1875 出 $1.125; 入 $0.5 出 $3
- **crof**（新增 1）：`glm-5.3`
- **deepseek**（更新 6）：`deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-v4-flash-vision-exp` — 入 $0.14 出 $0.28 缓存 $0.0028; 入 $0.14 出 $0.28 缓存 $0.0028; 入 $0.435 出 $0.87
- **digitalocean**（新增 1）：`glm-5.3`
- **fireworks-ai**（新增 1）：`accounts/fireworks/models/glm-5p3-flash`
- **friendli**（新增 1）：`zai-org/GLM-5.3`
- **kilo**（更新 2）：`google/gemma-4-31b-it`, `~deepseek/deepseek-v4-flash-latest` — 入 $0.09 出 $0.34 缓存 $0.05; 出 $0.16 缓存 $0.01
- **llmgateway**（更新 1）：`glm-5.3` — 入 $1.3 出 $4 缓存 $0.25
- **minimax**（更新 2）：`MiniMax-M2.5-highspeed` — 缓存 $0.06
- **mistral**（更新 4）：`ministral-3b-latest`, `ministral-8b-latest` — 入 $0.04 出 $0.04; 入 $0.1 出 $0.1
- **nano-gpt**（新增 47）：`abliteration-ai/abliterated-model`, `abliteration-ai/abliterated-model-large`, `gemma-4-26b-a4b-it-chimerax`, `gemma-4-26b-a4b-it-darksoul`, `gemma-4-26b-a4b-it-luminous`, `gemma-4-26b-a4b-it-moonlight`, `gemma-4-26b-a4b-it-musica`, `gemma-4-26b-a4b-it-opusdistill`, `gemma-4-26b-a4b-it-shadowsiren`, `gemma-4-26b-a4b-uncensored`, `gemma-4-26b-a4b-uncensored:thinking`, `gemma-4-31b-it-darkidol`, `gemma-4-31b-it-fabled`, `gemma-4-31b-it-garnet`, `gemma-4-31b-it-gembrain`, `gemma-4-31b-it-gemsicle`, `gemma-4-31b-it-isometry`, `gemma-4-31b-it-novelist`, `z-ai/GLM-4.5-Air`, `z-ai/GLM-4.5-Air:thinking`, `z-ai/GLM-4.5:thinking`, `z-ai/GLM-4.6-turbo`, `z-ai/GLM-4.6-turbo:thinking`, `z-ai/glm-4.5`, `z-ai/glm-4.6-original`, `z-ai/glm-4.6v`, `z-ai/glm-4.6v-flash-original`, `z-ai/glm-4.6v-original`, `z-ai/glm-4.7`, `z-ai/glm-4.7-flash`, `z-ai/glm-4.7-flash-original`, `z-ai/glm-4.7-flash-original:thinking`, `z-ai/glm-4.7-flash:thinking`, `z-ai/glm-4.7-original`, `z-ai/glm-4.7-original:thinking`, `z-ai/glm-4.7:thinking`, `z-ai/glm-5`, `z-ai/glm-5-original`, `z-ai/glm-5-original:thinking`, `z-ai/glm-5.1`, `z-ai/glm-5.1:thinking`, `z-ai/glm-5.2`, `z-ai/glm-5.2:thinking`, `z-ai/glm-5.3`, `z-ai/glm-5.3:thinking`, `z-ai/glm-5:thinking`, `z-ai/glm-latest`
- **nano-gpt**（更新 4）：`moonshotai/kimi-k3`, `moonshotai/kimi-latest`, `qwen3.8-27b`, `qwen3.8-27b:thinking` — 入 $2 出 $10 缓存 $0.2; 入 $2 出 $10 缓存 $0.2; 入 $0.15 出 $0.7; 入 $0.15 出 $0.7
- **ollama-cloud**（新增 1）：`glm-5.3`
- **opencode-go**（更新 1）：`hy3` — 入 $0.14 出 $0.58 缓存 $0.035
- **openrouter**（更新 6）：`deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`, `qwen/qwen3-next-80b-a3b-instruct`, `tencent/hy3`, `z-ai/glm-5.1`, `~deepseek/deepseek-v4-flash-latest`
- **orcarouter**（新增 1）：`z-ai/glm-5.3-flash`
- **synthetic**（新增 1）：`hf:zai-org/GLM-5.3-Flash`
- **togetherai**（新增 1）：`zai-org/GLM-5.3`

## 26.10.24 — 2026-08-29T23:12Z（内容更新）

- 价格同步（5 处变更）：
- **openrouter**（更新 5）：`deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-flash-0731`, `deepseek/deepseek-v4-pro`, `thinkingmachines/inkling`, `~deepseek/deepseek-v4-flash-latest`

## 26.9.24 — 2026-08-29T18:20Z（内容更新）

- 价格同步（3 处变更）：
- **openrouter**（更新 3）：`deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`, `tencent/hy3`

## 26.8.24 — 2026-08-29T13:00Z（内容更新）

- 价格同步（151 处变更）：
- **alibaba**（新增 1）：`qwen3.8-flash`
- **alibaba**（更新 14）：`qwen3.7-plus`, `qwen3.6-flash`, `qwen-vl-ocr`, `qwen3.6-35b-a3b`, `qwen3-next-80b-a3b-thinking`, `qwen3-next-80b-a3b-instruct`, `qwen3-32b` — 入 $0.72 出 $0.72; 入 $0.7 出 $2.8; 入 $0.5 出 $2; 入 $0.5 出 $6; 入 $0.248 出 $1.485; 入 $0.1875 出 $1.125; 入 $0.5 出 $3
- **alibaba-cn**（新增 1）：`qwen3.8-flash`
- **amd**（新增 1）：`Qwen3.8-Flash-Next`
- **baseten**（新增 1）：`zai-org/GLM-5.3`
- **cloudflare-workers-ai**（新增 1）：`@cf/zai-org/glm-5.3`
- **cortecs**（新增 3）：`glm-5.3`, `glm-5.3-flash`, `qwen3.8-flash-next`
- **crof**（新增 2）：`deepseek-v4-pro-0813`, `glm-5.3-flash`
- **crof**（更新 2）：`deepseek-v4-flash-0731`, `qwen3.8-27b` — 入 $0.08 出 $0.1; 入 $0.2 出 $1.5 缓存 $0.03
- **crossmodel**（新增 1）：`qwen/qwen3.8-flash`
- **deepinfra**（新增 1）：`zai-org/GLM-5.3`
- **deepseek**（更新 6）：`deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-v4-flash-vision-exp` — 入 $0.14 出 $0.28 缓存 $0.0028; 入 $0.14 出 $0.28 缓存 $0.0028; 入 $0.435 出 $0.87 缓存 $0.003625
- **digitalocean**（更新 10）：`deepseek-3.2`, `deepseek-4-flash`, `deepseek-v4-flash-0731`, `deepseek-v4-pro`, `glm-5.2`, `kimi-k3`, `llama-4-maverick`, `mimo-v2.5-pro`, `openai-gpt-5.6-sol`, `openai-gpt-oss-120b` — 入 $0.25 出 $0.8 缓存 $0.075; 入 $0.0679 出 $0.168 缓存 $0.0168; 入 $0.08 出 $0.252 缓存 $0.0252; 入 $0.87 出 $1.74 缓存 $0.174; 入 $0.7 出 $2.2 缓存 $0.105; 入 $2.85 出 $14.25 缓存 $0.285; 入 $0.2 出 $0.696; 入 $0.4 出 $1.5 缓存 $0.08; 入 $4 出 $20 缓存 $0.4; 入 $0.055 出 $0.385
- **edenai**（新增 4）：`deepinfra/tencent/Hy3`, `mistral/voxtral-small-latest`, `qwen/qwen3.8-flash`, `tensorx/deepseek/deepseek-v4-pro-0813`
- **edenai**（更新 6）：`flexai/gpt-oss-20b`, `ionos/meta-llama/Llama-3.3-70B-Instruct`, `ionos/openai/gpt-oss-120b`, `scaleway/deepseek-v4-flash-0731`, `scaleway/gpt-oss-120b`, `scaleway/llama-3.3-70b-instruct` — 入 $0.02 出 $0.1; 入 $0.756795 出 $0.756795; 入 $0.174645 出 $0.756795; 入 $0.46572 出 $0.93144; 入 $0.174645 出 $0.69858; 入 $1.04787 出 $1.04787
- **fireworks-ai**（新增 1）：`accounts/fireworks/models/glm-5p3`
- **huggingface**（新增 1）：`zai-org/GLM-5.3`
- **hyper**（更新 4）：`gemma-4-26b-a4b-it`, `glm-5.1`, `llama-4-maverick-17b-128e-instruct-fp8`, `minimax-m2.7` — 入 $0.11 出 $0.408; 入 $1.314 出 $4.268; 入 $0.284 出 $0.934; 入 $0.404 出 $1.496
- **inceptron**（更新 2）：`moonshotai/Kimi-K2.6`, `zai-org/GLM-5.2` — 入 $0.53 缓存 $0.17; 入 $0.71 出 $2.35 缓存 $0.12
- **kilo**（新增 1）：`tencent/hy4-preview`
- **kilo**（更新 5）：`google/gemma-4-31b-it`, `meta-llama/llama-4-maverick`, `z-ai/glm-5.3-flash`, `~google/gemini-flash-latest`, `~z-ai/glm-latest` — 入 $0.07 缓存 $0.1; 出 $0.696; 入 $0.15 出 $0.5 缓存 $0.03; 入 $0.75 出 $3.75 缓存 $0.075; 入 $1.1875 出 $4.18 缓存 $0.247
- **llmgateway**（新增 2）：`qwen3.8-27b`, `qwen3.8-flash`
- **llmgateway**（更新 3）：`glm-5.3-flash`, `kimi-k2.7-code`, `kimi-k3` — 入 $0.13 出 $0.4 缓存 $0.024; 入 $0.89 出 $3.71 缓存 $0.18; 入 $2.83 出 $14.13 缓存 $0.28
- **minimax**（更新 2）：`MiniMax-M2.5-highspeed` — 缓存 $0.06
- **mistral**（更新 4）：`ministral-3b-latest`, `ministral-8b-latest` — 入 $0.04 出 $0.04; 入 $0.1 出 $0.1
- **nano-gpt**（新增 19）：`TEE/glm-5.3-flash`, `abliterated-model`, `abliterated-model-large`, `google/gemma-4-26b-a4b-it-chimerax`, `google/gemma-4-26b-a4b-it-darksoul`, `google/gemma-4-26b-a4b-it-luminous`, `google/gemma-4-26b-a4b-it-moonlight`, `google/gemma-4-26b-a4b-it-musica`, `google/gemma-4-26b-a4b-it-opusdistill`, `google/gemma-4-26b-a4b-it-shadowsiren`, `google/gemma-4-31b-it-darkidol`, `google/gemma-4-31b-it-fabled`, `google/gemma-4-31b-it-garnet`, `google/gemma-4-31b-it-gembrain`, `google/gemma-4-31b-it-gemsicle`, `google/gemma-4-31b-it-isometry`, `google/gemma-4-31b-it-novelist`, `qwen/qwen3.8-27b-fable`, `tencent/hy4-preview`
- **nano-gpt**（更新 12）：`claw-high`, `claw-low`, `claw-medium`, `hermes-high`, `hermes-low`, `hermes-medium`, `openai/gpt-5.6-luna`, `openai/gpt-5.6-luna-pro`, `openai/gpt-5.6-terra`, `openai/gpt-5.6-terra-pro`, `zai-org/glm-5.3`, `zai-org/glm-5.3:thinking` — 入 $1 出 $3.2 缓存 $0.2; 入 $1 出 $3.2 缓存 $0.2; 入 $1 出 $3.2 缓存 $0.2; 入 $1 出 $3.2 缓存 $0.2; 入 $1 出 $3.2 缓存 $0.2; 入 $1 出 $3.2 缓存 $0.2; 入 $0.2 出 $1.2 缓存 $0.02; 入 $0.2 出 $1.2 缓存 $0.02; 入 $2 出 $12 缓存 $0.2; 入 $2 出 $12 缓存 $0.2; 入 $1 出 $3.2 缓存 $0.2; 入 $1 出 $3.2 缓存 $0.2
- **opencode**（新增 1）：`ling-3.0-flash-fin-free`
- **opencode-go**（新增 2）：`hy4-preview`, `qwen3.8-flash`
- **openrouter**（新增 18）：`deepseek/deepseek-v4-flash-0731:batch`, `deepseek/deepseek-v4-pro-0813:batch`, `google/gemma-4-31b-it:batch`, `meta/muse-glimmer-30b:batch`, `mistralai/codestral-2508:batch`, `mistralai/ministral-8b-2512:batch`, `mistralai/mistral-large-2512:batch`, `mistralai/mistral-medium-3-5:batch`, `mistralai/mistral-medium-3.1:batch`, `mistralai/mistral-small-2603:batch`, `moonshotai/kimi-k3:batch`, `openai/gpt-oss-120b:batch`, `openai/gpt-oss-20b:batch`, `qwen/qwen3.5-9b:batch`, `qwen/qwen3.8-2.4t-a95b:batch`, `tencent/hy4-preview`, `thinkingmachines/inkling-small:batch`, `z-ai/glm-5.3-flash:batch`
- **openrouter**（下架 2）：`allenai/olmo-3-32b-think`, `arcee-ai/virtuoso-large`
- **openrouter**（更新 13）：`deepseek/deepseek-v3.2`, `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-flash-0731`, `deepseek/deepseek-v4-pro`, `google/gemini-3.7-flash`, `meta/muse-glimmer-30b`, `nvidia/nemotron-3.5-lightning`, `openai/gpt-4.1-nano`, `qwen/qwen3-vl-30b-a3b-instruct`, `qwen/qwen3.5-122b-a10b`, `qwen/qwen3.6-27b`, `~google/gemini-flash-latest`, `~z-ai/glm-latest`
- **regolo-ai**（新增 1）：`qwen3.8-27b`
- **requesty**（新增 1）：`glm-5.3@eu`
- **tencent**（更新 1）：`hunyuan-hy3`
- **tencent-tokenhub**（新增 1）：`hy4-preview`
- **vercel**（新增 2）：`alibaba/wan-v3.0-video-prime`, `tencent/hy4-preview`
- **vercel**（更新 7）：`alibaba/qwen3.8-2.4t-a95b`, `alibaba/qwen3.8-27b`, `deepseek/deepseek-v4-pro`, `moonshotai/kimi-k2.7-code`, `nvidia/nemotron-3.5-lightning`, `tencent/hy3`, `zai/glm-5.3` — 缓存 $0.25; 入 $0.5 出 $3 缓存 $0.1; 入 $0.66 出 $1.98 缓存 $0.022; 缓存 $0.16; 出 $0.2 缓存 $0.01; 入 $0.14 出 $0.58 缓存 $0.035; 缓存 $0.14
- **wandb**（新增 1）：`deepseek-ai/DeepSeek-V4-Pro-0813`

## 26.7.24 — 2026-08-29T12:50Z（功能更新）

- fix: moonshotai batch 价格为双币对象（schema 26.8 batch 校验）

## 26.7.23 — 2026-08-29T01:32Z（功能更新）

- fix: 规范 batch 价格为双币对象（schema 26.8 batch 校验）

## 26.7.22 — 2026-08-28T10:47Z（功能更新）

- feat: 移除 changelog 同步摘要的模型省略限制（完整列出）

## 26.7.21 — 2026-08-28T12:05Z（功能更新）

- **feat(moonshot kimi 全 CNY)**：从 platform.kimi.com 为完整 Kimi 当前系列补充 CNY 分支（元/百万）：k3 ¥20/¥100（缓存 ¥2）、k2.7-code 与 k2.6 ¥6.5/¥27、k2.7-code-highspeed ¥13/¥54、k2.5 ¥4/¥21（缓存 ¥0.7）。旧 K2 preview/thinking 模型标记为历史。CNY 补全新增正价的模型 billing_model 修正为 pay_per_token。

## 26.7.20 — 2026-08-28T11:40Z（功能更新）

- **feat(minimax CNY)**：核对 MiniMax 开放平台按量计费文档（platform.minimaxi.com，元/百万 标准档）：MiniMax-M3 ¥4.2/¥16.8（≤512k；五折→2.10/8.40）、M2.7 ¥2.1/¥8.4、M2.7-highspeed ¥4.2/¥16.8。M2/M2.1/M2.5 标记为历史模型。新增 tier1_minimax.py 记录抓取状态（页面为浏览器渲染）。

## 26.7.19 — 2026-08-28T11:20Z（功能更新）

- **feat(moonshot kimi-k3 CNY)**：为 Kimi K3 补充 CNY 分支（platform.kimi.com，元/百万：缓存未命中输入 ¥20、缓存命中 ¥2、输出 ¥100）。k3/k3-256k 的 billing_model 修正为 pay_per_token。其余 Kimi 子页模型（K2.7 Code 等）暂缓。

## 26.7.18 — 2026-08-28T11:05Z（功能更新）

- **feat(alibaba CNY)**：从阿里云百炼计费页为通义主要 Qwen 模型补充 CNY 分支（元/百万token）：qwen-max ¥2.4/¥9.6、qwen-flash ¥0.15/¥1.5、qwen-turbo ¥0.3/¥3、qwen-vl-max ¥1.6/¥4、qwen3.8-max ¥12/¥36、qvq-max ¥8/¥32。国内 CNY 与国际 USD 列表相互独立。复杂档位/区域模型（qwen-plus 等）暂缓。

## 26.7.17 — 2026-08-28T10:50Z（功能更新）

- **feat(新增 T1 数据)**：补齐 4 家此前无数据文件的 T1 厂商——`ai21`（美元：jamba-1.6-large $2/$8、jamba-1.5-large $0.6/$2.4）、`baichuan`（人民币：baichuan4 ¥100/¥100）、`iflytek`（人民币：spark-4.0-ultra ¥21/¥21、spark-lite 免费）、`lingyiwanwu`（人民币：yi-lightning ¥0.99/¥0.99）。各家按官方清单为单币种（ai21 仅美元；国内三家为人民币）。已在 index.json 注册（186→190 家）。
- **feat(T1 检测覆盖)**：为剩余所有 T1 厂商新增 best-effort `tier1_*` 检测——baichuan/iflytek/lingyiwanwu（新增）+ cohere/nvidia/perplexity/upstage/aws（仅美元，无 CNY 分支——正确）。记录抓取状态，解析器待补。
- T1 双币进度：zhipuai/deepseek/baidu/stepfun/volcengine 已双币；ai21/tencent/xiaomi/cohere/nvidia/perplexity/upstage/aws 单币（按官方）；baichuan/iflytek/lingyiwanwu 人民币。

## 26.7.16 — 2026-08-28T10:20Z（功能更新）

- **feat(stepfun 双币)**：新增 `tier1_stepfun.py` 用 headless Chrome 抓取 stagefun 定价页（platform.stepfun.com/docs/zh/guides/pricing/details）并补充 CNY 分支（step-3.7-flash ¥1.35/¥8.1、step-3.5-flash ¥0.7/¥2.1）。国内 CNY 与国际 USD 列表相互独立。
- **feat(volcengine 双币)**：核对火山方舟模型价格页（docs.volcengine.com/docs/82379/1544106）——deepseek-v4-flash ¥3/¥9、v4-pro ¥9/¥27、glm-5.2 ¥8/¥28、doubao-seed-2.1-pro ¥3/¥15 等。该页有反爬（dump-dom 0 字节），`tier1_volcengine.py` 记录此情况暂无法自动刷新（CNY 来自人工核对的官方页）。
- stepfun/volcengine 共 26 个模型新增 CNY 分支。

## 26.7.15 — 2026-08-28T09:40Z（功能更新）

- **feat(deepseek 双币)**：`tier0_deepseek.py` 现同时抓取中文定价页（api-docs.deepseek.com/zh-cn，JS 渲染）并补充 `cny` 分支——deepseek-v4-flash ¥3/¥9、pro ¥9/¥27。国内 CNY 与 USD 列表相互独立（非汇率换算）。修正 pro `cache_read.usd` 的历史错误值（0.003625 → 0.044）。
- **feat(baidu 双币)**：新增 `tier1_baidu.py` 抓取千帆 ModelBuilder 页（headless Chrome），将 ¥/千tokens 换算为 ¥/1M（×1000）：ernie-5.0 ¥6/¥24（双币）、ernie-5.1 ¥4/¥18、ernie-4.5-turbo ¥0.8/¥3.2（仅 CNY）。国内价与国际 USD 列表相互独立。
- **feat(billing_model 自动同步)**：`update_model_prices` 在模型任一币种有真实正价时自动修正 `billing_model` 为 `pay_per_token`——不再出现补 CNY 后因陈旧 free/subscription/unknown 标签导致 audit 失败。
- 现 13 个模型携带双币（zhipuai + deepseek + baidu）。

## 26.7.14 — 2026-08-28T09:05Z（功能更新）

- **feat(双币 schema)**：每个模型价格字段可同时含 `usd` 和 `cny`（`per_mtok.input = {"usd": 0.44, "cny": 3.0}`），至少一个币种（minProperties: 1）。覆盖 per_mtok、batch、per_image、reasoning_effort、promo.list_price。
- **feat(迁移)**：`scripts/migrate_dual_currency.py` 将全部 186 个 provider 的 18,038 个标量价格重包装为双币对象（USD→usd，CNY→cny），幂等。
- **feat(js_fetch)**：`toolbox.js_fetch()` 用 headless Chrome（dump-dom + virtual-time-budget）抓取客户端渲染的定价页——针对 curl 无法渲染的厂商（如 open.bigmodel.cn）。
- **feat(tier1_zhipuai)**：新增检测脚本抓取 bigmodel.cn（JS）并解析 CNY 国内价（GLM-5.3 ¥8/¥28 等），补充 `cny` 分支同时保留 z.ai `usd` 参考价。确认国内 CNY 定价与 z.ai USD 定价相互独立（非汇率换算）。
- **fix(audit)**：USD 文件内 CNY 检测豁免含结构化 `cny` 价格的模型（双币为设计）；billing_model 一致性现感知 cny 分支（国内付费模型即使 models.dev 标免费/订阅也按 pay_per_token）。
- **适配脚本**：toolbox（update_model_prices 双币 + 分币种 surge）、sync_openrouter/sync_modelsdev（build_model 生成 {usd}）、sync_official（apply_to_provider）、daily_check（models.dev 按币种 diff，保留 cny）、audit/annotate_billing/stats/build_human（用 price_of/set_price 读取）、测试（双币断言 + 保留第二币种用例）。

## 26.7.13 — 2026-08-28T08:18Z（功能更新）

- **feat(changelog 可读性)**：自动同步的 CHANGELOG 条目此前是原始 Python dict 序列化（`{'input': [0.07, 0.72], ...}->{...}`）——不可读且被截断。`print_sync_summary` 现输出人类可读的按供应商摘要：模型列表 + 价格变化格式化为 `入 $0.44 出 $1.32 缓存 $0.014 → 入 $0.14 出 $0.28 缓存 $0.0028`，并标注新增/下架（+N / -N）。
- **feat(changelog 中文版)**：同步摘要现在**中英双语**——`SYNC_SUMMARY_EN`/`SYNC_SUMMARY_ZH` 两块；`bump_version.py` 新增 `--message-zh` 参数；daily-check.yml 分别提取英文与中文写入 CHANGELOG.md / CHANGELOG.zh-CN.md（此前中文版拿到的是未翻译的英文机器格式）。已用新格式重写 26.7.11 条目（中英）。
- **fix(数据)**：占位符 context_window——qiniu-ai kling-v2-6（99,999,999）与 nvidia flux_1-schnell（77）置 null 并注明（视频/图像模型无 token 上下文）；grok-4.1-fast-reasoning（20M）保留待核实。
- **feat(audit)**：反向 index 检查（每个 provider 文件必须被 index.json 的 providers/resellers 引用）；可疑 context_window 检查（>10M 或 <100）。

## 26.7.12 — 2026-08-28T08:10Z（功能更新）

- **fix(测试污染)**：突变护栏单元测试只 mock 了 `save_provider`，但 `update_model_prices` 还会调用 `append_changelog`——每次跑测试都会往生产 `changelog.json` 写入假的 "test-prov" 条目，其中一条还进入了 CHANGELOG.md（26.6.11）。现已同时 mock 两者；2 条污染条目已清除，26.6.11 条目已重写说明无真实变更。
- **fix(free 注释)**：零价格模型必须有 "free" 注释（audit 策略）。`sync_modelsdev` / `sync_openrouter` 的 `build_model` 在判定免费时自动追加 "Free model (per_mtok = 0)."；并为现存 90 个零价格模型补注（kenari/nvidia/opencode/openrouter/orcarouter/venice/vercel）。audit 警告 34 → 2。
- **fix(audit)**：USD 文件内 CNY 检测豁免明确注明 "no official USD" 的条目（百度 ernie-5.1/4.5-turbo、火山 doubao 的有意 CNY-only 标注）。

## 26.7.11 — 2026-08-28T05:09Z（内容更新）

价格同步（341 处变更）：
- **alibaba**（更新 14）：`qwen3.7-plus`, `qwen3.6-flash`, `qwen-vl-ocr`, `qwen3.6-35b-a3b`, `qwen3-next-80b-a3b-thinking` … +2
- **alibaba-cn**（更新 3）：`glm-5`, `glm-5.1`, `qwen3.5-397b-a17b` — 入 $0.573 出 $2.58; 入 $0.825 出 $3.301; 入 $0.172 出 $1.032
- **baseten**（新增 1）：`zai-org/GLM-5.3-Flash`
- **crossmodel**（新增 1）：`z-ai/glm-5.3-flash`
- **deepseek**（更新 6）：`deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-v4-flash-vision-exp` — 入 $0.14 出 $0.28 缓存 $0.0028; 入 $0.14 出 $0.28 缓存 $0.0028; 入 $0.435 出 $0.87 缓存 $0.003625
- **digitalocean**（新增 1）：`glm-5.3-flash`
- **digitalocean**（更新 9）：`deepseek-3.2`, `deepseek-4-flash`, `deepseek-v4-flash-0731`, `deepseek-v4-pro`, `glm-5.2` … +4
- **edenai**（新增 5）：`databricks/databricks-gpt-oss-120b@eu`, `databricks/databricks-gpt-oss-20b@eu`, `vertex/gemini-3.1-flash-lite`, `vertex/gemini-3.1-flash-lite@eu`, `vertex/gemini-3.1-flash-lite@us`
- **edenai**（更新 5）：`ionos/meta-llama/Llama-3.3-70B-Instruct`, `ionos/openai/gpt-oss-120b`, `scaleway/deepseek-v4-flash-0731`, `scaleway/gpt-oss-120b`, `scaleway/llama-3.3-70b-instruct`
- **hyper**（更新 5）：`glm-5`, `kimi-k2.5`, `llama-3.3-70b-instruct`, `minimax-m2.7`, `qwen3.8-flash`
- **inceptron**（更新 2）：`moonshotai/Kimi-K2.6`, `moonshotai/Kimi-K2.7-Code` — 缓存 $0.15; 入 $0.66 缓存 $0.18
- **kenari**（新增 21）：`claude-opus-5`, `claude-sonnet-4-6`, `gemini-3-1-flash-tts`, `gemini-3-1-pro`, `gemini-3-5-flash` … +16
- **kilo**（新增 1）：`inclusionai/ling-3.0-flash-fin:free`
- **kilo**（更新 9）：`google/gemma-4-31b-it`, `meta-llama/llama-4-maverick`, `minimax/minimax-m2.7:free`, `minimax/minimax-m3:free`, `qwen/qwen3.6-35b-a3b` … +4
- **llmgateway**（新增 1）：`deepseek-v4-flash-vision-exp`
- **merge-gateway**（更新 1）：`zai/glm-5.3-flash` — 入 $0.015 出 $0.05 缓存 $0.003
- **minimax**（更新 2）：`MiniMax-M2.5-highspeed` — 缓存 $0.06
- **mistral**（更新 4）：`ministral-3b-latest`, `ministral-8b-latest` — 入 $0.04 出 $0.04; 入 $0.1 出 $0.1
- **modal**（新增 2）：`Qwen/Qwen3.8-2.4T-A95B`, `zai-org/GLM-5.3-Flash`
- **nano-gpt**（新增 1）：`z-ai/glm-5.3-flash-uncensored`
- **neuralwatt**（新增 4）：`kimi-k2.7-code`, `kimi-k2.7-code-fast`, `kimi-k3-flex`, `qwen3.6-35b`
- **neuralwatt**（更新 10）：`gemma-4-31b`, `glm-5.2`, `glm-5.2-fast`, `glm-5.2-flex`, `glm-5.2-short` … +5
- **nvidia**（新增 1）：`deepseek-ai/deepseek-v4-pro-0813`
- **ofox**（新增 1）：`z-ai/glm-5.3-flash`
- **ollama-cloud**（新增 1）：`glm-5.3-flash`
- **openai**（更新 1）：`gpt-5.6-sol` — 入 $4 出 $20 缓存 $0.4
- **openrouter**（下架 37）：`moonshotai/kimi-k2.7-code:batch`, `openai/gpt-3.5-turbo:batch`, `openai/gpt-4-turbo:batch`, `openai/gpt-4.1-mini:batch`, `openai/gpt-4.1-nano:batch` … +32
- **openrouter**（更新 7）：`deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-flash-0731`, `deepseek/deepseek-v4-pro-0813`, `nvidia/nemotron-3-ultra-550b-a55b`, `nvidia/nemotron-3.5-lightning` … +2
- **orcarouter**（新增 42）：`anthropic/claude-fable-5`, `anthropic/claude-opus-4.8`, `anthropic/claude-opus-5`, `anthropic/claude-sonnet-5`, `deepseek/deepseek-v4-flash-0731` … +37
- **orcarouter**（更新 14）：`deepseek/deepseek-chat`, `deepseek/deepseek-reasoner`, `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`, `google/gemini-2.5-pro` … +9
- **requesty**（新增 2）：`glm-5.3-flash`, `glm-5.3-flash@eu`
- **requesty**（更新 127）：`claude-fable-5`, `claude-fable-5@eu`, `claude-haiku-4-5`, `claude-haiku-4-5@eu`, `claude-opus-4-1` … +122
- **runinfra**（新增 2）：`ornith-ai/Ornith-1.5-35B-A3B`, `zai-org/GLM-5.3-Flash`
- **runinfra**（更新 1）：`nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16` — 缓存 $0.01
- **togetherai**（新增 1）：`zai-org/GLM-5.3-Flash`
- **venice**（更新 1）：`z-ai-glm-5-3-flash` — 入 $0.15 出 $0.5 缓存 $0.03
- **vercel**（新增 2）：`inclusionai/ling-3.0-flash-fin`, `inclusionai/ling-3.0-flash-fin-free`
- **vivgrid**（新增 1）：`glm-5.3-flash`
- **wandb**（新增 1）：`zai-org/GLM-5.3-Flash`

## 26.6.11 — 2026-08-27T19:41Z（内容更新）

- 本次运行无真实数据变更。（一次单元测试污染临时写入了 2 条假的 "test-prov" changelog 条目，已于 26.7.12 清理；版本号因噪音触发提升，保留以维持版本历史连续。）

## 26.5.11 — 2026-08-27T17:38Z（功能更新）

- **fix(回归, HIGH)**：`sync_openrouter.py` / `sync_modelsdev.py` 未生成新增必填字段 `billing_model`——下次每日自动同步会**清空所有 OpenRouter/models.dev 模型的 billing_model** 并触发 audit「missing billing_model」失败，导致自动合并 workflow 挂掉。两个 `build_model` 现已正确分类计费方式（pay_per_token / pay_per_image / free / unknown），且不再写入已删除的 `per_request`/`per_audio_second` 字段。已实测真实同步：417 个 OpenRouter 模型全部正确标注（388 按量、29 按图+按量）。
- **fix(stats)**："By channel" 模型数恒为 0（`chan_m` 声明后从未填充）；README/中文统计现已显示真实数量（如 Inference host 4,316 / Subscription 173 / Aggregator 2,222）。
- **fix(audit)**：235 条逐模型的「pay_per_token 但 per_mtok 全 null」警告聚合为每 provider 一行（这些是按量转售模型、价格未公开）；audit 警告 248 → 14。
- **feat(ui)**：view 页面对有 `promo` 的模型标记 🔥 promo（en）/ 🔥 促销（zh-CN）；Z.ai GLM-5.3-Flash 已显示徽标。
- **feat(tests)**：新增 2 个突变护栏测试（正常变更生效、>5x 突变跳过，mock 保存）；测试套件现共 7 个。
- **refactor(schema)**：`providerFile` 简化为 `$defs.provider` 的纯 `$ref`。

## 26.5.10 — 2026-08-27T17:16Z（功能更新）

- **feat(billing_model)**：每个模型新增必填 `billing_model` 数组（pay_per_token / pay_per_image / subscription_included / credits / free / unknown）——用机器可读字段直接回答"这模型怎么收费"，不再靠 null/0/notes 推断。全库 7,239 个模型经 `scripts/annotate_billing.py` 标注（6467 按量、384 免费、114 订阅包含、55 免费+按量混合、219 未知待人工——这些在 models.dev 无价，如实标记）。支持多收费方式（如 Gemini 免费额度+付费）。
- **feat(schema)**：删除 8 个未使用计费字段（per_audio_second、per_character、per_request、credits、gpu、neuron_second、finetune、provisioned——0 使用）；新增 `promo.{list_price, ends_at}`；新增 `billingModel` 枚举；priceType 枚举 17→8。修复 `providerFile` 空 schema 问题（此前 provider 数据实际未被校验）。新增计费方式回添流程（AGENTS.md，字段只在有数据支撑时存在）。
- **feat(channel)**：coding-plan/token-plan provider 统一为 `channel: subscription`（此前 9 个 provider hosted/subscription 混标）。
- **feat(promo)**：Z.ai GLM-5.3-Flash 五折促销入档（原价 $0.15/$0.50/$0.03，9/9 截止）。
- **feat(audit)**：新校验——billing_model 存在性/枚举/与 pricing 一致性、USD 文件内 CNY 标注检测、`:free` 后缀豁免零价格警告。
- **feat(ui)**：view 页面新增"收费方式"列（中英）；订阅渠道标签补齐。
- **feat(tests)**：`tests/test_parsers.py` + HTML fixture（deepseek 英文页、百度国际站）；pr-check.yml 纳入测试步骤。
- **feat(ci)**：daily-check 输出详细 `SYNC_SUMMARY`（provider/模型/old→new），作为 CHANGELOG 消息，替代笼统的 "chore: price sync"。
- **docs**：AGENTS.md（billing_model、计费字段添加流程、注释全英文规则、channel 语义）、FORMAT.md（中英，含 model.status online/offline 修正）、docs/price-types.md（中英重写为现行计费类型）、README 统计刷新（186 供应商、7,239 模型、67 计划）。

## 26.5.9 — 2026-08-27T15:40Z（内容更新）

- **fix(货币)**: deepseek.json v4 系列由 CNY 数值修正为官方英文页 USD 价格（flash $0.44/$1.32、pro $1.32/$3.96，峰值档）。baidu.json ernie-5.0 → 国际站 USD（$1.4/$5.6）；ernie-5.1/4.5-turbo → null + CNY 说明（仅国内提供）。tencent.json currency → CNY（混元 ¥1/¥4，官方仅 CNY 定价）。volcengine.json doubao-2.1-pro/turbo → null + CNY 说明（无官方 USD 页）。
- **fix(解析器)**: deepseek 解析器改抓官方英文定价页（USD），加结构断言（必须 18 个 $价格，否则报错拒绝写入部分数据）。baidu 解析器重写适配千帆国际站（USD, $/M tokens）。
- **feat(护栏)**: 价格突变护栏（变化 >5x 视为解析错误，跳过该字段并告警）接入 toolbox.update_model_prices 与 sync_official.apply_to_provider。OpenRouter 目录重写加保护（远端 < 本地 50% 拒绝覆盖）。
- **fix(CI)**: pr-check.yml 核心文件保护路径由 data/machine/ 修正为 data/feed/。
- **feat(数据)**: 新增 provider zai-coding-plan（GLM-5.3-Flash + GLM-5.3 + 路由规则、积分倍率、非高峰 50% 规则）+ 3 个订阅计划条目（Lite/Pro/Max，积分制，$18/$72/$160）。

## 26.4.9 — 2026-08-27T08:13Z（内容更新）

- chore: price sync

## 26.3.9 — 2026-08-27T07:56Z（功能更新）

- 修复：PAT 推送 main 被分支保护拒绝（GH006，fine-grained PAT 无法绕过）时，改为推送到分支并发 issue 告警，数据不再丢失

## 26.3.8 — 2026-08-27T07:39Z（功能更新）

- 修复：daily-check 工作流 YAML 语法错误（issue 正文缩进）；自动合并前先对齐最新 main（stash → rebase → stash pop），避免基于旧基线的 rebase 冲突；GH_PAT 自动合并路径已验证可用

## 26.3.7 — 2026-08-27T07:22Z（功能更新）

- 修复：zai 官方检查现可解析 "Latest Models" 章节并自动添加官方新模型（如 GLM-5.3-Flash 促销价直取）；router 自动刷新 index 计数；daily-check 在无法创建 PR 时改为发 issue 告警并使步骤失败（不再静默丢弃，main 不再静默停更）

## 26.3.6 — 2026-08-27T00:38Z（内容更新）

- chore: price sync

## 26.2.6 — 2026-08-22T11:46Z（功能更新）

- 功能：Tier-0 自动化覆盖全部 11 家（新增 alibaba/google/meta/minimax/mistral/moonshotai/xai/zai 官方页检查，deepseek/anthropic/openai 已有）；按官方定价页修正 14 个模型价格（alibaba 7 个、Ministral 3B/8B、minimax 缓存写入 8 个、moonshot 批处理 3 个、zai 缓存 2 个、google 批处理 9 个）；Meta 官方页为客户端渲染，价格经多源交叉验证

## 26.2.5 — 2026-08-22T11:10Z（功能更新）

- 功能：字节跳动（volcengine）在厂商状态表中显示中文名，便于识别；修复 38 处文档间失效链接；audit 新增失效链接检查

## 26.2.4 — 2026-08-22T10:57Z（功能更新）

- feature: data dirs renamed (data/feed + data/view/en|zh-CN), branch cleanup + branch policy, changelog boundaries + zh translations, core-file update rules documented, pending vendors merged into tiers, opencode-go same tier

## 26.2.3 — 2026-08-22T10:29Z（内容更新）

- 修复：models.dev 同步跳过订阅类供应商（per_mtok 保持 null）；重新修正 96 个 0 价条目

## 26.1.3 — 2026-08-22T09:33（内容更新）

- 例行：价格自动同步

## 26.0.3 — 2026-08-22T15:30（功能更新）

- 功能：status 简化为 online/offline；改为每 3 小时自动检查并直接合入 main；版本递增逻辑修复（内容/功能段独立）且时间精确到分钟；删除 AGENTS 中文版；文档去重（移除 ego 文档，供应商清单与路线图合并为生成式状态文档）；文档全互链

## 26.0.2 — 2026-08-22（功能更新）

- 功能：核心检查路由（router.py）+ 工具库（toolbox.py）+ 各供应商检查脚本（checks/）；扩充贡献指南；修复每日检查 PR 创建

## 26.0.1 — 2026-08-22（功能更新）

- 功能：人类页面新增 API 地址与 Notes 列；去重检查；pr-check 强制 CHANGELOG/VERSION 更新；bump_version.py；README 星标徽章与精确统计；机器数据全英文

## 26.1.0 — 2026-08-21（功能更新）

- **收费模式修正**（内容更新）：OpenCode Go 改为订阅制记录（美元额度制；新增计划：首月 $5 / 之后 $10/月，含 $60 额度）；新增 ChatGPT Go 计划（$8/月，含广告）；436 个真正免费模型显式标注；ChatGPT 各计划额度注明"官方未公布"。
- **版本规则**：改为 `年份.内容更新.功能更新`（内容更新=定价更新）。
- **文档全双语**：所有纯文字文档提供英文默认版 + `*.zh-CN.md`。
- **仓库加固**：`main` 分支保护（仅 PR、禁 force push）；新增 `pr-check.yml`（validate + audit + 生成页一致性 + 版本一致性）；`daily-check.yml` 改为开 PR 而非直接推送；删除 `reports/`（stale 报告改走 `--stale-report`）；新增 `CONTRIBUTING` 与 issue/PR 模板、`scripts/audit.py`。
- README/AGENTS 增加项目状态声明（仍在完善、数据可能不准确）与技术栈说明（DeepSeek Harness + deepseek-v4-flash-0731）。

## 26.0.0 — 2026-08-21（初始规范化版本）

首个采用新版本规则的版本（内容为 2026-08-21 当天完成的所有工作）。

### 内容更新（定价数据）
- **订阅计划独立定价结构**：`plans.json` 每个计划新增 `pricing_model` 字段（flat_monthly / flat_yearly / per_seat_monthly / per_seat_yearly / credits / free / custom），与模型 per-MTok 定价明确区分；51 个计划全部标注。
- **修复 0 价歧义**：155 个"订阅/套餐包含"模型（coding-plan / token-plan / Copilot / Duo / Kimi-for-Coding 等 provider）的 per-MTok 价格由 `0` 改为 `null` + notes 说明"包含于订阅计划，无独立按 token 定价"，消除"0 = 免费"误读。
- **模型状态结构化**：新增 `model.status` 字段（active / preview / deprecated / retired / superseded），41 个模型已标注（OpenAI 退役系列、xAI 退役系列、DeepSeek V3 旧系、Anthropic Mythos preview 等）；人类可读页面新增状态列（❌/⚠️/🔁/🧪 显著标记）。
- 定价复核成果（DeepSeek V4、Anthropic Sonnet 5 永久价、OpenAI 5.6 系列、国内厂商官方价）随 26.0.0 一并归档。

### 功能更新（仓库）
- **官方价直采层**：`scripts/sync_official.py` + `scripts/official_sources.json`（DeepSeek / 百度 / Anthropic 官方页直抓，OpenAI Wayback 快照兜底）；每日检查按"官方 → models.dev → OpenRouter"顺序执行，官方当日已核实的 provider 免于第三方覆盖。
- **中英严格分离**：README / 人类可读页面（`data/view/` + `zh-CN/`）双语；全部文档头部增加 `Language:` 标注；文档 H1 与文件名对齐。
- **版本管理**：`VERSION` 文件 + `年份.功能.内容` 版本规则；schema 版本升级为 `26.0.0`。
- AGENTS.md（agent 指南）、docs/verification.md（真实性机制）、docs/ego-browser-workflow.md（ego-lite 复核工作流）。

### 历史背景（26.0.0 之前的工作，归档于此）
- 仓库建立：schema v1、OpenRouter（419 模型）+ models.dev（192 供应商）自动同步、双版本输出、每日检查 workflow、51 个订阅计划、全面定价复核（DeepSeek/Anthropic/OpenAI/国内厂商）。


---

## 相关文档

- [README.zh-CN.md](README.zh-CN.md) — 总览与精确统计
- [FORMAT.zh-CN.md](FORMAT.zh-CN.md) — 机器格式规范
- [docs/providers.zh-CN.md](docs/providers.zh-CN.md) — 供应商全景与状态
- [docs/price-types.zh-CN.md](docs/price-types.zh-CN.md) — 收费形式口径
- [docs/verification.zh-CN.md](docs/verification.zh-CN.md) — 核实与真实性机制
- [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md) — 如何贡献
- [AGENTS.md](AGENTS.md) — AI Agent 指南（英文）
