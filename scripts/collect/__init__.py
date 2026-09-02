"""scripts/collect — per-provider independent collection scripts.

Architecture (chosen by the user, 2026-09-02):
  route (dispatcher)  ->  collect_<provider>.py  ->  common.py (shared utils)

Each collect_<provider>.py independently fetches THAT provider's official source,
parses per-M prices, and writes them back via update_model_prices(). Providers
without an independent official source fall back to the aggregation sources
(openrouter / models.dev). Common logic is extracted here and in toolbox/common.
"""
