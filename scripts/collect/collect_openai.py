"""Independent collector for OpenAI official pricing (developers.openai.com pricing.md).

Reuses the mature parser from checks/tier0_openai.parse and writes via common.write_prices
(which wraps toolbox.update_model_prices).
"""
import os
import sys

_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..")))  # scripts/

from collect.base import fetch_markdown, write_prices  # noqa: E402
from checks.tier0_openai import parse  # noqa: E402

URL = "https://developers.openai.com/api/docs/pricing.md"
PROVIDER_ID = "openai"


def collect(ctx):
    """Fetch OpenAI pricing.md, parse it, and write per-M prices to the openai provider."""
    now = ctx.get("now")
    text = fetch_markdown(URL)
    updates = parse(text)
    n = len(updates)
    changed = write_prices(PROVIDER_ID, updates, "openai:pricing.md", now)
    return {"changed": changed, "status": "ok", "detail": f"parsed {n} models, {changed} changed"}


if __name__ == "__main__":
    import json

    print(json.dumps(collect({"now": None}), ensure_ascii=False))
