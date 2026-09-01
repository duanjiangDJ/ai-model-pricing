> **Language: English (en)** — This document is written in en only.

# Changelog

## Versioning Rules

Version number format: **`year.content.feature`** (e.g. `26.2.3` = the 2nd content update and the 3rd feature update of 2026).

- **Year**: the year of first release (two digits, e.g. 2026 → `26`); when the year changes, the following two segments reset to 0.
- **Content update** (second segment, +1): **pricing data ONLY** — price changes, model add/retire (status change), plan add/price change. E.g. fixing a model's input/output, adding the ChatGPT Go plan, marking a model offline.
- **Feature update** (third segment, +1): **everything else** — data structure (schema/format), scripts (router/checks/toolbox), workflows, docs, translations, directory renames, CI mechanics. E.g. adding a check script, renaming a directory, updating AGENTS.
- Boundary: when a PR mixes pricing and feature changes, bump only ONE segment by the dominant type (pricing -> content; otherwise -> feature).
- Each rule advances only its own segment; they never reset each other.
- The current version is in the `VERSION` file; `data/feed/schema.json`'s `version` and every data file's `schema_version` match it.
- Version increments are decided by maintainers/bots based on the change type and recorded in this file's entries.

---

## 26.23.24 — 2026-09-01T01:53Z (content update)

- fix(openrouter): convert per-token price to per-1M (x1e6), keep api_base_url; audit: per_mtok magnitude check

## 26.22.24 — 2026-08-31T21:22Z (content update)

- price sync (38 changes):
- **cortecs** (+1): `deepseek-v4-pro-0813`
- **openrouter** (+30): `ibm-granite/granite-4.2-8b`, `openai/gpt-3.5-turbo:batch`, `openai/gpt-4-turbo:batch`, `openai/gpt-4.1-mini:batch`, `openai/gpt-4.1-nano:batch`, `openai/gpt-4.1:batch`, `openai/gpt-4o-mini:batch`, `openai/gpt-4o:batch`, `openai/gpt-5-mini:batch`, `openai/gpt-5-nano:batch`, `openai/gpt-5-pro:batch`, `openai/gpt-5.1:batch`, `openai/gpt-5.2-pro:batch`, `openai/gpt-5.2:batch`, `openai/gpt-5.4-mini:batch`, `openai/gpt-5.4-nano:batch`, `openai/gpt-5.4-pro:batch`, `openai/gpt-5.4:batch`, `openai/gpt-5.5-pro:batch`, `openai/gpt-5.5:batch`, `openai/gpt-5.6-luna-pro:batch`, `openai/gpt-5.6-luna:batch`, `openai/gpt-5.6-sol-pro:batch`, `openai/gpt-5.6-sol:batch`, `openai/gpt-5.6-terra-pro:batch`, `openai/gpt-5.6-terra:batch`, `openai/gpt-5:batch`, `openai/o3-mini:batch`, `openai/o3:batch`, `openai/o4-mini:batch`
- **openrouter** (updated 7): `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`, `google/gemini-3.5-flash`, `qwen/qwen3-next-80b-a3b-instruct`, `qwen/qwen3.8-2.4t-a95b`, `qwen/qwen3.8-2.4t-a95b:batch`, `~deepseek/deepseek-v4-flash-latest`

## 26.21.24 — 2026-08-31T18:22Z (content update)

- price sync (6 changes):
- **openrouter** (updated 6): `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`, `google/gemini-3.5-flash`, `qwen/qwen3.8-2.4t-a95b`, `qwen/qwen3.8-2.4t-a95b:batch`, `tencent/hy3`

## 26.20.24 — 2026-08-31T15:21Z (content update)

- price sync (3 changes):
- **openrouter** (-1): `kwaipilot/kat-coder-air-v2.5`
- **openrouter** (updated 2): `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`

## 26.19.24 — 2026-08-31T12:22Z (content update)

- price sync (3 changes):
- **openrouter** (updated 3): `deepseek/deepseek-v4-flash-vision-exp`, `deepseek/deepseek-v4-pro`, `deepseek/deepseek-v4-pro-0813`

## 26.18.24 — 2026-08-31T09:21Z (content update)

- No data changes this run.

## 26.17.24 — 2026-08-31T06:21Z (content update)

- No data changes this run.

## 26.16.24 — 2026-08-31T03:44Z (content update)

- price sync (63 changes):
- **berget** (+2): `zai-org/GLM-5.3`, `zai-org/GLM-5.3-Flash`
- **crossmodel** (+1): `tencent/hy4-preview`
- **edenai** (updated 6): `flexai/Muse-Glimmer-30B`, `mistral/codestral-latest`, `mistral/devstral-2512`, `mistral/mistral-medium-2604`, `mistral/mistral-medium-latest`, `mistral/mistral-small-latest` — out $1.1; cache $0.03; in $0.4 out $2 cache $0.04; cache $0.15; cache $0.015
- **kilo** (updated 6): `deepseek/deepseek-v4-flash-vision-exp`, `mistralai/devstral-2512`, `mistralai/mistral-nemo`, `mistralai/mistral-small-3.2-24b-instruct`, `~deepseek/deepseek-v4-flash-latest`, `~z-ai/glm-latest` — in $0.44 out $1.32 cache $0.014; in $0.4 out $2 cache $0.04; in $0.019 out $0.03; in $0.075 out $0.2; cache $0.013; in $0 out $0
- **nano-gpt** (updated 33): `Gemma-4-26B-A4B-MeroMero`, `Gemma-4-26B-A4B-MeroMero:thinking`, `Gemma-4-31B-MeroMero-v2`, `Gemma-4-31B-MeroMero-v2:thinking`, `deepseek/deepseek-v4-flash-vision-exp`, `gemma-4-26b-a4b-it-chimerax`, `gemma-4-26b-a4b-it-darksoul`, `gemma-4-26b-a4b-it-luminous`, `gemma-4-26b-a4b-it-moonlight`, `gemma-4-26b-a4b-it-musica`, `gemma-4-26b-a4b-it-opusdistill`, `gemma-4-26b-a4b-it-shadowsiren`, `gemma-4-26b-a4b-uncensored`, `gemma-4-26b-a4b-uncensored:thinking`, `gemma-4-31b-it-darkidol`, `gemma-4-31b-it-fabled`, `gemma-4-31b-it-garnet`, `gemma-4-31b-it-gembrain`, `gemma-4-31b-it-gemsicle`, `gemma-4-31b-it-isometry`, `gemma-4-31b-it-novelist`, `google/gemma-4-26b-a4b-it`, `google/gemma-4-31b-it`, `ornith-ai/ornith-1.5-9b`, `ornith-ai/ornith-1.5-9b:thinking`, `qwen/qwen3.6-35b-a3b-uncensored`, `qwen/qwen3.6-35b-a3b-uncensored:thinking`, `qwen/qwen3.8-27b-fable`, `qwen/qwen3.8-27b-obliterated`, `qwen/qwen3.8-27b-obliterated:thinking`, `qwen/qwen3.8-27b-uncensored`, `qwen/qwen3.8-27b-uncensored:thinking`, `z-ai/glm-5.3-flash-uncensored` — in $0.12 out $0.38 cache $0.06; in $0.1 out $0.45 cache $0.05; in $0.44 out $1.32 cache $0.014; in $0.1 out $0.2 cache $0.05; out $0.95; in $0.25 out $1.5 cache $0.125; in $0.35 out $1.4 cache $0.175
- **openrouter** (updated 7): `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-flash-vision-exp`, `deepseek/deepseek-v4-pro`, `deepseek/deepseek-v4-pro-0813`, `meta-llama/llama-4-maverick`, `moonshotai/kimi-k2.5`, `tencent/hy3`
- **trustedrouter** (+7): `trustedrouter/auto`, `trustedrouter/cheap`, `trustedrouter/e2e`, `trustedrouter/fast`, `trustedrouter/synth`, `trustedrouter/synth-code`, `trustedrouter/zdr`
- **vercel** (+1): `minimax/minimax-h3-max`

## 26.15.24 — 2026-08-30T23:24Z (content update)

- price sync (1 change):
- **openrouter** (updated 1): `deepseek/deepseek-v4-flash`

## 26.14.24 — 2026-08-30T20:54Z (content update)

- price sync (3 changes):
- **neuralwatt** (+1): `glm-5.3`
- **openrouter** (updated 2): `openai/gpt-4.1-nano`, `~deepseek/deepseek-v4-flash-latest`

## 26.13.24 — 2026-08-30T16:27Z (content update)

- price sync (4 changes):
- **openrouter** (updated 4): `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`, `mistralai/devstral-2512`, `tencent/hy3`

## 26.12.24 — 2026-08-30T11:39Z (content update)

- price sync (3 changes):
- **openrouter** (updated 3): `arcee-ai/trinity-large-thinking`, `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`

## 26.11.24 — 2026-08-30T04:43Z (content update)

- price sync (88 changes):
- **aiand** (+2): `qwen/qwen3.8-27b`, `zai-org/glm-5.3`
- **alibaba** (updated 14): `qwen3.7-plus`, `qwen3.6-flash`, `qwen-vl-ocr`, `qwen3.6-35b-a3b`, `qwen3-next-80b-a3b-thinking`, `qwen3-next-80b-a3b-instruct`, `qwen3-32b` — in $0.72 out $0.72; in $0.7 out $2.8; in $0.5 out $2; in $0.5 out $6; in $0.248 out $1.485; in $0.1875 out $1.125; in $0.5 out $3
- **crof** (+1): `glm-5.3`
- **deepseek** (updated 6): `deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-v4-flash-vision-exp` — in $0.14 out $0.28 cache $0.0028; in $0.435 out $0.87
- **digitalocean** (+1): `glm-5.3`
- **fireworks-ai** (+1): `accounts/fireworks/models/glm-5p3-flash`
- **friendli** (+1): `zai-org/GLM-5.3`
- **kilo** (updated 2): `google/gemma-4-31b-it`, `~deepseek/deepseek-v4-flash-latest` — in $0.09 out $0.34 cache $0.05; out $0.16 cache $0.01
- **llmgateway** (updated 1): `glm-5.3` — in $1.3 out $4 cache $0.25
- **minimax** (updated 2): `MiniMax-M2.5-highspeed` — cache $0.06
- **mistral** (updated 4): `ministral-3b-latest`, `ministral-8b-latest` — in $0.04 out $0.04; in $0.1 out $0.1
- **nano-gpt** (+47): `abliteration-ai/abliterated-model`, `abliteration-ai/abliterated-model-large`, `gemma-4-26b-a4b-it-chimerax`, `gemma-4-26b-a4b-it-darksoul`, `gemma-4-26b-a4b-it-luminous`, `gemma-4-26b-a4b-it-moonlight`, `gemma-4-26b-a4b-it-musica`, `gemma-4-26b-a4b-it-opusdistill`, `gemma-4-26b-a4b-it-shadowsiren`, `gemma-4-26b-a4b-uncensored`, `gemma-4-26b-a4b-uncensored:thinking`, `gemma-4-31b-it-darkidol`, `gemma-4-31b-it-fabled`, `gemma-4-31b-it-garnet`, `gemma-4-31b-it-gembrain`, `gemma-4-31b-it-gemsicle`, `gemma-4-31b-it-isometry`, `gemma-4-31b-it-novelist`, `z-ai/GLM-4.5-Air`, `z-ai/GLM-4.5-Air:thinking`, `z-ai/GLM-4.5:thinking`, `z-ai/GLM-4.6-turbo`, `z-ai/GLM-4.6-turbo:thinking`, `z-ai/glm-4.5`, `z-ai/glm-4.6-original`, `z-ai/glm-4.6v`, `z-ai/glm-4.6v-flash-original`, `z-ai/glm-4.6v-original`, `z-ai/glm-4.7`, `z-ai/glm-4.7-flash`, `z-ai/glm-4.7-flash-original`, `z-ai/glm-4.7-flash-original:thinking`, `z-ai/glm-4.7-flash:thinking`, `z-ai/glm-4.7-original`, `z-ai/glm-4.7-original:thinking`, `z-ai/glm-4.7:thinking`, `z-ai/glm-5`, `z-ai/glm-5-original`, `z-ai/glm-5-original:thinking`, `z-ai/glm-5.1`, `z-ai/glm-5.1:thinking`, `z-ai/glm-5.2`, `z-ai/glm-5.2:thinking`, `z-ai/glm-5.3`, `z-ai/glm-5.3:thinking`, `z-ai/glm-5:thinking`, `z-ai/glm-latest`
- **nano-gpt** (updated 4): `moonshotai/kimi-k3`, `moonshotai/kimi-latest`, `qwen3.8-27b`, `qwen3.8-27b:thinking` — in $2 out $10 cache $0.2; in $0.15 out $0.7
- **ollama-cloud** (+1): `glm-5.3`
- **opencode-go** (updated 1): `hy3` — in $0.14 out $0.58 cache $0.035
- **openrouter** (updated 6): `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`, `qwen/qwen3-next-80b-a3b-instruct`, `tencent/hy3`, `z-ai/glm-5.1`, `~deepseek/deepseek-v4-flash-latest`
- **orcarouter** (+1): `z-ai/glm-5.3-flash`
- **synthetic** (+1): `hf:zai-org/GLM-5.3-Flash`
- **togetherai** (+1): `zai-org/GLM-5.3`

## 26.10.24 — 2026-08-29T23:12Z (content update)

- price sync (5 changes):
- **openrouter** (updated 5): `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-flash-0731`, `deepseek/deepseek-v4-pro`, `thinkingmachines/inkling`, `~deepseek/deepseek-v4-flash-latest`

## 26.9.24 — 2026-08-29T18:20Z (content update)

- price sync (3 changes):
- **openrouter** (updated 3): `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`, `tencent/hy3`

## 26.8.24 — 2026-08-29T13:00Z (content update)

- price sync (151 changes):
- **alibaba** (+1): `qwen3.8-flash`
- **alibaba** (updated 14): `qwen3.7-plus`, `qwen3.6-flash`, `qwen-vl-ocr`, `qwen3.6-35b-a3b`, `qwen3-next-80b-a3b-thinking`, `qwen3-next-80b-a3b-instruct`, `qwen3-32b` — in $0.72 out $0.72; in $0.7 out $2.8; in $0.5 out $2; in $0.5 out $6; in $0.248 out $1.485; in $0.1875 out $1.125; in $0.5 out $3
- **alibaba-cn** (+1): `qwen3.8-flash`
- **amd** (+1): `Qwen3.8-Flash-Next`
- **baseten** (+1): `zai-org/GLM-5.3`
- **cloudflare-workers-ai** (+1): `@cf/zai-org/glm-5.3`
- **cortecs** (+3): `glm-5.3`, `glm-5.3-flash`, `qwen3.8-flash-next`
- **crof** (+2): `deepseek-v4-pro-0813`, `glm-5.3-flash`
- **crof** (updated 2): `deepseek-v4-flash-0731`, `qwen3.8-27b` — in $0.08 out $0.1; in $0.2 out $1.5 cache $0.03
- **crossmodel** (+1): `qwen/qwen3.8-flash`
- **deepinfra** (+1): `zai-org/GLM-5.3`
- **deepseek** (updated 6): `deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-v4-flash-vision-exp` — in $0.14 out $0.28 cache $0.0028; in $0.435 out $0.87 cache $0.003625
- **digitalocean** (updated 10): `deepseek-3.2`, `deepseek-4-flash`, `deepseek-v4-flash-0731`, `deepseek-v4-pro`, `glm-5.2`, `kimi-k3`, `llama-4-maverick`, `mimo-v2.5-pro`, `openai-gpt-5.6-sol`, `openai-gpt-oss-120b` — in $0.25 out $0.8 cache $0.075; in $0.0679 out $0.168 cache $0.0168; in $0.08 out $0.252 cache $0.0252; in $0.87 out $1.74 cache $0.174; in $0.7 out $2.2 cache $0.105; in $2.85 out $14.25 cache $0.285; in $0.2 out $0.696; in $0.4 out $1.5 cache $0.08; in $4 out $20 cache $0.4; in $0.055 out $0.385
- **edenai** (+4): `deepinfra/tencent/Hy3`, `mistral/voxtral-small-latest`, `qwen/qwen3.8-flash`, `tensorx/deepseek/deepseek-v4-pro-0813`
- **edenai** (updated 6): `flexai/gpt-oss-20b`, `ionos/meta-llama/Llama-3.3-70B-Instruct`, `ionos/openai/gpt-oss-120b`, `scaleway/deepseek-v4-flash-0731`, `scaleway/gpt-oss-120b`, `scaleway/llama-3.3-70b-instruct` — in $0.02 out $0.1; in $0.756795 out $0.756795; in $0.174645 out $0.756795; in $0.46572 out $0.93144; in $0.174645 out $0.69858; in $1.04787 out $1.04787
- **fireworks-ai** (+1): `accounts/fireworks/models/glm-5p3`
- **huggingface** (+1): `zai-org/GLM-5.3`
- **hyper** (updated 4): `gemma-4-26b-a4b-it`, `glm-5.1`, `llama-4-maverick-17b-128e-instruct-fp8`, `minimax-m2.7` — in $0.11 out $0.408; in $1.314 out $4.268; in $0.284 out $0.934; in $0.404 out $1.496
- **inceptron** (updated 2): `moonshotai/Kimi-K2.6`, `zai-org/GLM-5.2` — in $0.53 cache $0.17; in $0.71 out $2.35 cache $0.12
- **kilo** (+1): `tencent/hy4-preview`
- **kilo** (updated 5): `google/gemma-4-31b-it`, `meta-llama/llama-4-maverick`, `z-ai/glm-5.3-flash`, `~google/gemini-flash-latest`, `~z-ai/glm-latest` — in $0.07 cache $0.1; out $0.696; in $0.15 out $0.5 cache $0.03; in $0.75 out $3.75 cache $0.075; in $1.1875 out $4.18 cache $0.247
- **llmgateway** (+2): `qwen3.8-27b`, `qwen3.8-flash`
- **llmgateway** (updated 3): `glm-5.3-flash`, `kimi-k2.7-code`, `kimi-k3` — in $0.13 out $0.4 cache $0.024; in $0.89 out $3.71 cache $0.18; in $2.83 out $14.13 cache $0.28
- **minimax** (updated 2): `MiniMax-M2.5-highspeed` — cache $0.06
- **mistral** (updated 4): `ministral-3b-latest`, `ministral-8b-latest` — in $0.04 out $0.04; in $0.1 out $0.1
- **nano-gpt** (+19): `TEE/glm-5.3-flash`, `abliterated-model`, `abliterated-model-large`, `google/gemma-4-26b-a4b-it-chimerax`, `google/gemma-4-26b-a4b-it-darksoul`, `google/gemma-4-26b-a4b-it-luminous`, `google/gemma-4-26b-a4b-it-moonlight`, `google/gemma-4-26b-a4b-it-musica`, `google/gemma-4-26b-a4b-it-opusdistill`, `google/gemma-4-26b-a4b-it-shadowsiren`, `google/gemma-4-31b-it-darkidol`, `google/gemma-4-31b-it-fabled`, `google/gemma-4-31b-it-garnet`, `google/gemma-4-31b-it-gembrain`, `google/gemma-4-31b-it-gemsicle`, `google/gemma-4-31b-it-isometry`, `google/gemma-4-31b-it-novelist`, `qwen/qwen3.8-27b-fable`, `tencent/hy4-preview`
- **nano-gpt** (updated 12): `claw-high`, `claw-low`, `claw-medium`, `hermes-high`, `hermes-low`, `hermes-medium`, `openai/gpt-5.6-luna`, `openai/gpt-5.6-luna-pro`, `openai/gpt-5.6-terra`, `openai/gpt-5.6-terra-pro`, `zai-org/glm-5.3`, `zai-org/glm-5.3:thinking` — in $1 out $3.2 cache $0.2; in $0.2 out $1.2 cache $0.02; in $2 out $12 cache $0.2
- **opencode** (+1): `ling-3.0-flash-fin-free`
- **opencode-go** (+2): `hy4-preview`, `qwen3.8-flash`
- **openrouter** (+18): `deepseek/deepseek-v4-flash-0731:batch`, `deepseek/deepseek-v4-pro-0813:batch`, `google/gemma-4-31b-it:batch`, `meta/muse-glimmer-30b:batch`, `mistralai/codestral-2508:batch`, `mistralai/ministral-8b-2512:batch`, `mistralai/mistral-large-2512:batch`, `mistralai/mistral-medium-3-5:batch`, `mistralai/mistral-medium-3.1:batch`, `mistralai/mistral-small-2603:batch`, `moonshotai/kimi-k3:batch`, `openai/gpt-oss-120b:batch`, `openai/gpt-oss-20b:batch`, `qwen/qwen3.5-9b:batch`, `qwen/qwen3.8-2.4t-a95b:batch`, `tencent/hy4-preview`, `thinkingmachines/inkling-small:batch`, `z-ai/glm-5.3-flash:batch`
- **openrouter** (-2): `allenai/olmo-3-32b-think`, `arcee-ai/virtuoso-large`
- **openrouter** (updated 13): `deepseek/deepseek-v3.2`, `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-flash-0731`, `deepseek/deepseek-v4-pro`, `google/gemini-3.7-flash`, `meta/muse-glimmer-30b`, `nvidia/nemotron-3.5-lightning`, `openai/gpt-4.1-nano`, `qwen/qwen3-vl-30b-a3b-instruct`, `qwen/qwen3.5-122b-a10b`, `qwen/qwen3.6-27b`, `~google/gemini-flash-latest`, `~z-ai/glm-latest`
- **regolo-ai** (+1): `qwen3.8-27b`
- **requesty** (+1): `glm-5.3@eu`
- **tencent** (updated 1): `hunyuan-hy3`
- **tencent-tokenhub** (+1): `hy4-preview`
- **vercel** (+2): `alibaba/wan-v3.0-video-prime`, `tencent/hy4-preview`
- **vercel** (updated 7): `alibaba/qwen3.8-2.4t-a95b`, `alibaba/qwen3.8-27b`, `deepseek/deepseek-v4-pro`, `moonshotai/kimi-k2.7-code`, `nvidia/nemotron-3.5-lightning`, `tencent/hy3`, `zai/glm-5.3` — cache $0.25; in $0.5 out $3 cache $0.1; in $0.66 out $1.98 cache $0.022; cache $0.16; out $0.2 cache $0.01; in $0.14 out $0.58 cache $0.035; cache $0.14
- **wandb** (+1): `deepseek-ai/DeepSeek-V4-Pro-0813`

## 26.7.24 — 2026-08-29T12:50Z (feature update)

- fix: moonshotai batch prices to dual-currency (schema 26.8 batch validation)

## 26.7.23 — 2026-08-29T01:32Z (feature update)

- fix: normalize batch prices to dual-currency objects (schema 26.8 batch validation)

## 26.7.22 — 2026-08-28T10:47Z (feature update)

- feat: lift changelog sync-summary truncation (full model list)

## 26.7.21 — 2026-08-28T12:05Z (feature update)

- **feat(moonshot kimi full CNY)**: added the CNY branch for the full current Kimi lineup from platform.kimi.com (¥/1M): k3 ¥20/¥100 (cache ¥2), k2.7-code & k2.6 ¥6.5/¥27, k2.7-code-highspeed ¥13/¥54, k2.5 ¥4/¥21 (cache ¥0.7). Legacy K2 preview/thinking models marked historical. billing_model corrected to pay_per_token where the CNY backfill added a positive price.

## 26.7.20 — 2026-08-28T11:40Z (feature update)

- **feat(minimax CNY)**: reconciled the MiniMax open-platform billing doc (platform.minimaxi.com, ¥/1M standard): MiniMax-M3 ¥4.2/¥16.8 (≤512k; 50% promo → 2.10/8.40), M2.7 ¥2.1/¥8.4, M2.7-highspeed ¥4.2/¥16.8. M2/M2.1/M2.5 marked legacy. New tier1_minimax.py records fetch status (browser-rendered page).

## 26.7.19 — 2026-08-28T11:20Z (feature update)

- **feat(moonshot kimi-k3 CNY)**: added the CNY branch for Kimi K3 (platform.kimi.com, ¥/1M: cache-miss input ¥20, cache-hit ¥2, output ¥100). k3/k3-256k billing_model corrected to pay_per_token. Other Kimi sub-page models (K2.7 Code etc.) deferred.

## 26.7.18 — 2026-08-28T11:05Z (feature update)

- **feat(alibaba CNY)**: added the CNY branch for the major Qwen models from the Alibaba Bailian billing page (CNY/1M tokens): qwen-max ¥2.4/¥9.6, qwen-flash ¥0.15/¥1.5, qwen-turbo ¥0.3/¥3, qwen-vl-max ¥1.6/¥4, qwen3.8-max ¥12/¥36, qvq-max ¥8/¥32. Domestic CNY independent of the int'l USD list. Complex tiered/region models (qwen-plus etc.) deferred.

## 26.7.17 — 2026-08-28T10:50Z (feature update)

- **feat(new T1 providers)**: added the 4 TIER-1 vendors that had no data file — `ai21` (USD: jamba-1.6-large $2/$8, jamba-1.5-large $0.6/$2.4), `baichuan` (CNY: baichuan4 ¥100/¥100), `iflytek` (CNY: spark-4.0-ultra ¥21/¥21, spark-lite free), `lingyiwanwu` (CNY: yi-lightning ¥0.99/¥0.99). Each is single-currency per official vendor list (ai21 USD-only; the domestic ones CNY-only for now). Registered in index.json (186→190 providers).
- **feat(T1 check coverage)**: added best-effort `tier1_*` checks for all the remaining T1 vendors so every one of the 15 TIER-1 providers now has a check module — baichuan/iflytek/lingyiwanwu (new) + cohere/nvidia/perplexity/upstage/aws (USD-only, no CNY branch — correct). They record fetch-status and defer parsers.
- T1 dual-currency rollout: zhipuai/deepseek/baidu/stepfun/volcengine now dual-currency; ai21/tencent/xiaomi/cohere/nvidia/perplexity/upstage/aws single-currency (per official); baichuan/iflytek/lingyiwanwu CNY.

## 26.7.16 — 2026-08-28T10:20Z (feature update)

- **feat(stepfun dual-currency)**: new `tier1_stepfun.py` pulls the StepFun pricing page (platform.stepfun.com/docs/zh/guides/pricing/details) via headless Chrome and adds the CNY branch (step-3.7-flash ¥1.35/¥8.1, step-3.5-flash ¥0.7/¥2.1). Domestic CNY independent of the int'l USD list.
- **feat(volcengine dual-currency)**: reconciled the Volcano Ark model-price page (docs.volcengine.com/docs/82379/1544106) — deepseek-v4-flash ¥3/¥9, v4-pro ¥9/¥27, glm-5.2 ¥8/¥28, doubao-seed-2.1-pro ¥3/¥15 etc. The page is bot-protected (dump-dom 0 bytes) so `tier1_volcengine.py` records this and cannot auto-refresh yet (CNY is from the manually-verified official page).
- 26 models across stepfun/volcengine now carry a CNY branch.

## 26.7.15 — 2026-08-28T09:40Z (feature update)

- **feat(deepseek dual-currency)**: `tier0_deepseek.py` now also pulls the Chinese pricing page (api-docs.deepseek.com/zh-cn, JS-rendered) and adds the `cny` branch alongside the `usd` one — deepseek-v4-flash ¥3/¥9, pro ¥9/¥27. Domestic CNY is independent of the USD list (not a conversion). Fixed the pro `cache_read.usd` historical bad value (0.003625 → 0.044).
- **feat(baidu dual-currency)**: new `tier1_baidu.py` pulls the Qianfan ModelBuilder page (headless Chrome), converts ¥/1k tokens → ¥/1M (x1000): ernie-5.0 ¥6/¥24 (dual), ernie-5.1 ¥4/¥18, ernie-4.5-turbo ¥0.8/¥3.2 (CNY-only). Domestic prices independent of the int'l USD list.
- **feat(billing_model auto-sync)**: `update_model_prices` corrects a model's `billing_model` to `pay_per_token` once it has a real positive token price in any currency — no more stale free/subscription/unknown labels surfacing as audit failures after a CNY backfill.
- 13 models now carry both currencies (zhipuai + deepseek + baidu).

## 26.7.14 — 2026-08-28T09:05Z (feature update)

- **feat(dual-currency schema)**: every model price can now carry BOTH `usd` and `cny` in a single field (`per_mtok.input = {"usd": 0.44, "cny": 3.0}`). A model only needs one currency (minProperties: 1). Covers per_mtok, batch, per_image, reasoning_effort, and promo.list_price.
- **feat(migration)**: `scripts/migrate_dual_currency.py` rewrapped 18,038 scalar prices across all 186 providers into dual-currency objects (USD->usd, CNY->cny), idempotent.
- **feat(js_fetch)**: `toolbox.js_fetch()` fetches client-side-rendered pricing pages via headless Chrome (dump-dom + virtual-time-budget) — for vendors whose pages curl can't render (e.g. open.bigmodel.cn).
- **feat(tier1_zhipuai)**: new check fetches bigmodel.cn (JS) and parses the CNY list prices (GLM-5.3 ¥8/¥28 etc.), adding the `cny` branch while keeping the z.ai `usd` list. Confirms domestic CN pricing is INDEPENDENT of the z.ai USD list (not a currency conversion).
- **fix(audit)**: CNY-in-USD warning now exempts models that carry a structured `cny` price (dual-currency is by-design); billing_model consistency now sees the cny branch (domestic paid models are pay_per_token even if models.dev labeled them free/subscription).
- **adapt scripts**: toolbox (update_model_prices dual-currency + surge per-currency), sync_openrouter/sync_modelsdev (build_model emits {usd}), sync_official (apply_to_provider), daily_check (models.dev diff updates per-currency, preserving cny), audit/annotate_billing/stats/build_human (read via price_of/set_price), tests (dual-currency assertions + second-currency-preserved case).

## 26.7.13 — 2026-08-28T08:18Z (feature update)

- **feat(changelog readability)**: auto-sync CHANGELOG entries were raw Python dict dumps (`{'input': [0.07, 0.72], ...}->{...}`) — unreadable and truncated. `print_sync_summary` now emits human-readable, per-provider summaries with model lists and price changes formatted as `in $0.44 out $1.32 cache $0.014 → in $0.14 out $0.28 cache $0.0028`, plus add/remove markers (+N / -N).
- **feat(changelog zh-CN)**: sync summaries are now BILINGUAL — `SYNC_SUMMARY_EN`/`SYNC_SUMMARY_ZH` blocks; `bump_version.py` gained `--message-zh`; daily-check.yml extracts both and writes a proper Chinese entry into CHANGELOG.zh-CN.md (previously zh-CN got the untranslated English dump). Rewrote the 26.7.11 entry (both languages) to the new readable format.
- **fix(data)**: placeholder context_windows — qiniu-ai kling-v2-6 (99,999,999) and nvidia flux_1-schnell (77) set to null with notes (video/image models have no token context); grok-4.1-fast-reasoning (20M) kept pending review.
- **feat(audit)**: reverse index check (every provider file must be referenced in index.json providers/resellers); suspicious context_window check (>10M or <100).

## 26.7.12 — 2026-08-28T08:10Z (feature update)

- **fix(test pollution)**: surge-guard unit tests only mocked `save_provider`, but `update_model_prices` also calls `append_changelog` — every test run wrote fake "test-prov" entries into the production `changelog.json`, and one such entry reached CHANGELOG.md (26.6.11). Tests now mock both; the 2 polluted changelog entries were removed and the 26.6.11 entry rewritten to explain it had no real changes.
- **fix(free notes)**: zero-price models need a "free" note (audit policy). `sync_modelsdev` / `sync_openrouter` `build_model` now append "Free model (per_mtok = 0)." to notes when classified free; backfilled the note on 90 existing zero-price models (kenari/nvidia/opencode/openrouter/orcarouter/venice/vercel). Audit warnings 34 → 2.
- **fix(audit)**: CNY-in-USD warnings now exempt notes explicitly stating "no official USD" (honest CNY-only annotations for baidu ernie-5.1/4.5-turbo, volcengine doubao — those are intentional).

## 26.7.11 — 2026-08-28T05:09Z (content update)

price sync (341 changes):
- **alibaba** (updated 14): `qwen3.7-plus`, `qwen3.6-flash`, `qwen-vl-ocr`, `qwen3.6-35b-a3b`, `qwen3-next-80b-a3b-thinking` … +2
- **alibaba-cn** (updated 3): `glm-5`, `glm-5.1`, `qwen3.5-397b-a17b` — in $0.86 out $3.15 → in $0.573 out $2.58; in $0.87 out $3.48 → in $0.825 out $3.301; in $0.43 out $2.58 → in $0.172 out $1.032
- **baseten** (+1): `zai-org/GLM-5.3-Flash`
- **crossmodel** (+1): `z-ai/glm-5.3-flash`
- **deepseek** (updated 6): `deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-v4-flash-vision-exp` — in $0.44 out $1.32 cache $0.014 → in $0.14 out $0.28 cache $0.0028; in $1.32 out $3.96 cache $0.044
- **digitalocean** (+1): `glm-5.3-flash`
- **digitalocean** (updated 9): `deepseek-3.2`, `deepseek-4-flash`, `deepseek-v4-flash-0731`, `deepseek-v4-pro`, `glm-5.2` … +4
- **edenai** (+5): `databricks/databricks-gpt-oss-120b@eu`, `databricks/databricks-gpt-oss-20b@eu`, `vertex/gemini-3.1-flash-lite`, `vertex/gemini-3.1-flash-lite@eu`, `vertex/gemini-3.1-flash-lite@us`
- **edenai** (updated 5): `ionos/meta-llama/Llama-3.3-70B-Instruct`, `ionos/openai/gpt-oss-120b`, `scaleway/deepseek-v4-flash-0731`, `scaleway/gpt-oss-120b`, `scaleway/llama-3.3-70b-instruct`
- **hyper** (updated 5): `glm-5`, `kimi-k2.5`, `llama-3.3-70b-instruct`, `minimax-m2.7`, `qwen3.8-flash`
- **inceptron** (updated 2): `moonshotai/Kimi-K2.6`, `moonshotai/Kimi-K2.7-Code` — cache $0.13 → cache $0.15; in $0.67 cache $0.19 → in $0.66 cache $0.18
- **kenari** (+21): `claude-opus-5`, `claude-sonnet-4-6`, `gemini-3-1-flash-tts`, `gemini-3-1-pro`, `gemini-3-5-flash` … +16
- **kilo** (+1): `inclusionai/ling-3.0-flash-fin:free`
- **kilo** (updated 9): `google/gemma-4-31b-it`, `meta-llama/llama-4-maverick`, `minimax/minimax-m2.7:free`, `minimax/minimax-m3:free`, `qwen/qwen3.6-35b-a3b` … +4
- **llmgateway** (+1): `deepseek-v4-flash-vision-exp`
- **merge-gateway** (updated 1): `zai/glm-5.3-flash` — in $0.075 out $0.25 cache $0.015 → in $0.015 out $0.05 cache $0.003
- **minimax** (updated 2): `MiniMax-M2.5-highspeed` — cache $0.03 → cache $0.06
- **mistral** (updated 4): `ministral-3b-latest`, `ministral-8b-latest` — in $0.1 out $0.1 → in $0.04 out $0.04; in $0.15 out $0.15 → in $0.1 out $0.1
- **modal** (+2): `Qwen/Qwen3.8-2.4T-A95B`, `zai-org/GLM-5.3-Flash`
- **nano-gpt** (+1): `z-ai/glm-5.3-flash-uncensored`
- **neuralwatt** (+4): `kimi-k2.7-code`, `kimi-k2.7-code-fast`, `kimi-k3-flex`, `qwen3.6-35b`
- **neuralwatt** (updated 10): `gemma-4-31b`, `glm-5.2`, `glm-5.2-fast`, `glm-5.2-flex`, `glm-5.2-short` … +5
- **nvidia** (+1): `deepseek-ai/deepseek-v4-pro-0813`
- **ofox** (+1): `z-ai/glm-5.3-flash`
- **ollama-cloud** (+1): `glm-5.3-flash`
- **openai** (updated 1): `gpt-5.6-sol` — in $5 out $30 cache $0.5 → in $4 out $20 cache $0.4
- **openrouter** (-37): `moonshotai/kimi-k2.7-code:batch`, `openai/gpt-3.5-turbo:batch`, `openai/gpt-4-turbo:batch`, `openai/gpt-4.1-mini:batch`, `openai/gpt-4.1-nano:batch` … +32
- **openrouter** (updated 7): `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-flash-0731`, `deepseek/deepseek-v4-pro-0813`, `nvidia/nemotron-3-ultra-550b-a55b`, `nvidia/nemotron-3.5-lightning` … +
- **orcarouter** (+42): `anthropic/claude-fable-5`, `anthropic/claude-opus-4.8`, `anthropic/claude-opus-5`, `anthropic/claude-sonnet-5`, `deepseek/deepseek-v4-flash-0731` … +37
- **orcarouter** (updated 14): `deepseek/deepseek-chat`, `deepseek/deepseek-reasoner`, `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-pro`, `google/gemini-2.5-pro` … +9
- **requesty** (+2): `glm-5.3-flash`, `glm-5.3-flash@eu`
- **requesty** (updated 127): `claude-fable-5`, `claude-fable-5@eu`, `claude-haiku-4-5`, `claude-haiku-4-5@eu`, `claude-opus-4-1` … +122
- **runinfra** (+2): `ornith-ai/Ornith-1.5-35B-A3B`, `zai-org/GLM-5.3-Flash`
- **runinfra** (updated 1): `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16` — cache $0.01
- **togetherai** (+1): `zai-org/GLM-5.3-Flash`
- **venice** (updated 1): `z-ai-glm-5-3-flash` — in $0.09375 out $0.3125 cache $0.01875 → in $0.15 out $0.5 cache $0.03
- **vercel** (+2): `inclusionai/ling-3.0-flash-fin`, `inclusionai/ling-3.0-flash-fin-free`
- **vivgrid** (+1): `glm-5.3-flash`
- **wandb** (+1): `zai-org/GLM-5.3-Flash`

## 26.6.11 — 2026-08-27T19:41Z (content update)

- No real data changes in this run. (A transient unit-test pollution wrote two fake
  "test-prov" changelog entries that were cleaned up in 26.7.12; the version bump was
  triggered by that noise and is kept for version history continuity.)

## 26.5.11 — 2026-08-27T17:38Z (feature update)

- **fix(regression, HIGH)**: `sync_openrouter.py` / `sync_modelsdev.py` did not emit the new required `billing_model` field — the next daily auto-sync would have STRIPPED billing_model from every OpenRouter/models.dev model and tripped the audit "missing billing_model" fail, breaking the auto-merge workflow. Both `build_model` functions now classify billing (pay_per_token / pay_per_image / free / unknown) and no longer write the removed `per_request`/`per_audio_second` fields (schema-dead). Verified by running a real sync: all 417 OpenRouter models annotated correctly (388 pay_per_token, 29 pay_per_image+pay_per_token).
- **fix(stats)**: "By channel" model counts were always 0 (`chan_m` was declared but never populated); README/zh-CN stats now show real counts (e.g. Inference host 4,316 / Subscription 173 / Aggregator 2,222).
- **fix(audit)**: aggregated the 235 per-model "pay_per_token but per_mtok all null" warnings into one summary line per provider (these are reseller models billed per-token whose price is simply not published); audit warnings 248 → 14.
- **feat(ui)**: view pages now mark models with a live `promo` as 🔥 promo (en) / 🔥 促销 (zh-CN); Z.ai GLM-5.3-Flash shows the badge.
- **feat(tests)**: 2 new surge-guard tests (normal change applies, >5x surge skipped) via mocked save; test suite now 7 tests.
- **refactor(schema)**: `providerFile` simplified to a pure `$ref` of `$defs.provider`.

## 26.5.10 — 2026-08-27T17:16Z (feature update)

- **feat(billing_model)**: every model now carries a required `billing_model` array (pay_per_token / pay_per_image / subscription_included / credits / free / unknown) — machine-readable "how is this billed" instead of inferring from null/0/notes. 7,239 models annotated via `scripts/annotate_billing.py` (6467 pay_per_token, 384 free, 114 subscription_included, 55 free+pay_per_token, 219 unknown needing review — those have no price in models.dev, honestly marked). Mixed billing supported (e.g. Gemini free tier + paid).
- **feat(schema)**: removed 8 unused pricing fields (per_audio_second, per_character, per_request, credits, gpu, neuron_second, finetune, provisioned — 0 usage); added `promo.{list_price, ends_at}`; `billingModel` enum added; priceType enum trimmed 17→8. Fixed `providerFile` being an empty schema (provider data was previously NOT actually validated). Re-added a billing mode procedure documented in AGENTS.md (fields exist only when backed by data).
- **feat(channel)**: coding-plan/token-plan providers unified to `channel: subscription` (was mixed hosted/subscription across 9 providers).
- **feat(promo)**: Z.ai GLM-5.3-Flash 50% promo recorded (list $0.15/$0.50/$0.03, ends 2026-09-09).
- **feat(audit)**: new checks — billing_model presence/enum/pricing-consistency, currency-vs-CNY notes detection, `:free` id suffix exemption for zero-price warnings.
- **feat(ui)**: view pages gain a "Billing" column (en + zh-CN); subscription channel labels added.
- **feat(tests)**: `tests/test_parsers.py` with HTML fixtures (deepseek EN page, baidu INT'L page); pr-check.yml now runs them.
- **feat(ci)**: daily-check now emits a detailed `SYNC_SUMMARY` (provider/model/old→new) used as the CHANGELOG message instead of bare "chore: price sync".
- **docs**: AGENTS.md (billing_model, add-a-billing-mode procedure, English-comments rule, channel semantics), FORMAT.md (en+zh-CN, incl. model.status online/offline correction), docs/price-types.md (en+zh-CN rewritten to current billing types), README stats refreshed (186 providers, 7,239 models, 67 plans).

## 26.5.9 — 2026-08-27T15:40Z (content update)

- **fix(currency)**: deepseek.json v4 series corrected from CNY values to official EN-page USD prices (flash $0.44/$1.32, pro $1.32/$3.96, peak tier). baidu.json ernie-5.0 → INT'L page USD ($1.4/$5.6); ernie-5.1/4.5-turbo → null + CNY notes (domestic-only). tencent.json currency → CNY (hunyuan ¥1/¥4, official CNY-only). volcengine.json doubao-2.1-pro/turbo → null + CNY notes (no official USD page).
- **fix(parsers)**: deepseek parser now fetches the official EN pricing page (USD) with a structure assertion (18 $prices required — fails loudly instead of writing partial data). baidu parser rewritten for the Qianfan INT'L page (USD, $/M tokens).
- **feat(guardrails)**: price-surge guard (>5x change treated as parsing error, field skipped with warning) in both toolbox.update_model_prices and sync_official.apply_to_provider. OpenRouter catalog rewrite guarded (remote < 50% of local size → refuse overwrite).
- **fix(ci)**: pr-check.yml core-file protection paths corrected from data/machine/ to data/feed/.
- **feat(data)**: new provider zai-coding-plan (GLM-5.3-Flash + GLM-5.3 + routing rules, credit multipliers, off-peak 50% rule) + 3 plan entries (Lite/Pro/Max, credits-based, $18/$72/$160).

## 26.4.9 — 2026-08-27T08:13Z (content update)

- chore: price sync

## 26.3.9 — 2026-08-27T07:56Z (feature update)

- fix: daily-check falls back to branch + alert issue when PAT push is rejected by branch protection (fine-grained PAT cannot bypass)

## 26.3.8 — 2026-08-27T07:39Z (feature update)

- fix: daily-check workflow YAML fix (issue-body indentation) + auto-merge aligns base with latest main before commit (stash/rebase/stash-pop) to avoid rebase conflicts; GH_PAT auto-merge verified working

## 26.3.7 — 2026-08-27T07:22Z (feature update)

- fix: zai check parses Latest Models section + auto-adds new official models; router refreshes index counts; daily-check PR-failure now alerts via issue and fails loudly

## 26.3.6 — 2026-08-27T00:38Z (content update)

- chore: price sync

## 26.2.6 — 2026-08-22T11:46Z (feature update)

- feature: T0 automation for alibaba/google/meta/minimax/mistral/moonshotai/xai/zai (official-page checks); 14 models price-corrected (alibaba 7, ministral 2, minimax cache-write 8, moonshot batch 3, zai cache 2, google batch 9)

## 26.2.5 — 2026-08-22T11:10Z (feature update)

- feature: ByteDance visible in provider name/status table, fix 38 broken cross-doc links, add broken-link check to audit

## 26.2.4 — 2026-08-22T10:57Z (feature update)

- feature: data dirs renamed (data/feed + data/view/en|zh-CN), branch cleanup + branch policy, changelog boundaries + zh translations, core-file update rules documented, pending vendors merged into tiers, opencode-go same tier

## 26.2.3 — 2026-08-22T10:29Z (content update)

- fix: models.dev sync skips subscription-included providers (per_mtok stays null); re-fix 96 zero prices

## 26.1.3 — 2026-08-22T09:33 (content update)

- chore: price sync

## 26.0.3 — 2026-08-22T15:30 (feature update)

- feature: status simplified to online/offline, 3-hourly auto-check with direct merge to main, version increment logic fixed (content/feature independent) with minute-precision timestamps, AGENTS zh-CN removed, docs dedup (ego removed, providers+roadmap merged into generated status doc), cross-linked documentation

## 26.0.2 — 2026-08-22 (feature update)

- feature: core check router (scripts/router.py) + toolbox (scripts/toolbox.py) + per-provider checks (scripts/checks/), CONTRIBUTING guide expanded, daily-check PR fix

## 26.0.1 — 2026-08-22 (feature update)

- feature: api_base_url + Notes column in human pages, dedup checks, pr-check enforces CHANGELOG/VERSION, bump_version.py, README star badge + exact stats, all machine notes localized to English

## 26.1.0 — 2026-08-21 (feature update)

- **Billing-mode fixes** (content): OpenCode Go recorded as subscription (USD-allowance
  based; plan added: $5 first month / $10 mo, $60 usage); ChatGPT Go plan added ($8/mo,
  ad-supported); 436 genuinely-free models explicitly flagged; ChatGPT plan limits marked
  "not publicly specified".
- **Versioning**: scheme reversed to `year.content.feature` (content = pricing updates).
- **Bilingual docs**: every prose document now has English (default) + `*.zh-CN.md`.
- **Repo hardening**: `main` branch protected (PR-only, no force push); `pr-check.yml`
  (validate + audit + generated-page consistency + version consistency); `daily-check.yml`
  now opens a PR instead of pushing directly; `reports/` removed (stale report via
  `--stale-report`); `CONTRIBUTING` + issue/PR templates; `scripts/audit.py` added.
- Project status disclosure (work-in-progress, data may be inaccurate) and tech-stack note
  (DeepSeek Harness + deepseek-v4-flash-0731) added to README/AGENTS.

## 26.0.0 — 2026-08-21 (Initial Normalized Version)

The first version to adopt the new versioning rules (content covers all work completed on 2026-08-21).

### Content Updates (pricing data)
- **Independent pricing structure for subscription plans**: each plan in `plans.json` gains a `pricing_model` field (flat_monthly / flat_yearly / per_seat_monthly / per_seat_yearly / credits / free / custom), clearly distinguished from model per-MTok pricing; all 51 plans are tagged.
- **Fixed the 0-price ambiguity**: 155 "included in subscription/plan" models (coding-plan / token-plan / Copilot / Duo / Kimi-for-Coding, etc. providers) changed their per-MTok price from `0` to `null` + a notes entry stating "included in the subscription plan, no standalone per-token pricing", eliminating the "0 = free" misreading.
- **Structured model status**: new `model.status` field (active / preview / deprecated / retired / superseded); 41 models tagged (OpenAI retired series, xAI retired series, DeepSeek V3 old series, Anthropic Mythos preview, etc.); human-readable pages gain a status column (prominent ❌/⚠️/🔁/🧪 marks).
- Pricing-review results (DeepSeek V4, Anthropic Sonnet 5 permanent pricing, OpenAI 5.6 series, domestic vendors' official prices) are archived together with 26.0.0.

### Feature Updates (repository)
- **Official-price direct-sync layer**: `scripts/sync_official.py` + `scripts/official_sources.json` (direct scraping of DeepSeek / Baidu / Anthropic official pages, OpenAI Wayback snapshot as fallback); the daily check runs in "official → models.dev → OpenRouter" order, and providers already verified officially that day are exempt from third-party overwrites.
- **Strict en/zh separation**: README / human-readable pages (`data/view/` + `zh-CN/`) are bilingual; all docs gain a `Language:` header annotation; doc H1s align with file names.
- **Version management**: `VERSION` file + `year.feature.content` versioning rules; schema version upgraded to `26.0.0`.
- AGENTS.md (agent guide), docs/verification.md (truthfulness mechanism), docs/ego-browser-workflow.md (ego-lite re-verification workflow).

### Historical Background (work before 26.0.0, archived here)
- Repository establishment: schema v1, OpenRouter (419 models) + models.dev (192 providers) auto-sync, dual-version output, daily-check workflow, 51 subscription plans, comprehensive pricing review (DeepSeek / Anthropic / OpenAI / domestic vendors).


---

## Related docs

- [README](README.md) — overview & exact stats
- [AGENTS.md](AGENTS.md) — guide for AI agents
- [FORMAT.md](FORMAT.md) — machine format spec
- [docs/providers.md](docs/providers.md) — provider landscape & status
- [docs/price-types.md](docs/price-types.md) — price types
- [docs/verification.md](docs/verification.md) — verification model
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute
