# Z.AI Coding Plan

- provider_id: `zai-coding-plan`
- Channel: Subscription
- API base URL: `https://api.z.ai/api/coding/paas/v4`
- Homepage: https://z.ai/subscribe
- Pricing page: https://docs.z.ai/devpack/overview
- Currency: USD
- Data updated: 2026-08-27T17:11:11Z
- Verified: 2026-08-27T15:38:33.587025Z

**6** models in total.

| Model | Status | Category | Billing | Context | Input $/MTok | Output $/MTok | Cache read | Cache write | Batch (in/out) | Other billing | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `glm-5.3-flash` | — | reasoning | sub-included | 1M | — | — | — | — | —/— | ⚡ peak/off-peak | Included in GLM Coding Plan (credits-based). Credit multipliers: input 2.3, c… |
| `glm-5.3` | — | reasoning | sub-included | 1M | — | — | — | — | —/— | ⚡ peak/off-peak | Included in GLM Coding Plan (credits-based). Credit multipliers: input 6.9, c… |
| `glm-5.2` | — | reasoning | sub-included | 1M | — | — | — | — | —/— | — | Included in GLM Coding Plan; requests to glm-5.2 are routed to glm-5.3 (flags… |
| `glm-5.2-highspeed` | — | reasoning | sub-included | 1M | — | — | — | — | —/— | — | Included in GLM Coding Plan (high-speed lane). |
| `glm-5-turbo` | — | reasoning | sub-included | 204.8K | — | — | — | — | —/— | — | Included in GLM Coding Plan; requests to glm-5-turbo are routed to glm-5.3-fl… |
| `glm-4.7` | — | reasoning | sub-included | 204.8K | — | — | — | — | —/— | — | Included in GLM Coding Plan; requests to glm-4.7 are routed to glm-5.3-flash. |
