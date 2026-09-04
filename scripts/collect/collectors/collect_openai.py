"""Independent collector for openai (official source). Structured-return contract.

collect(ctx) fetches OpenAI's official pricing markdown, parses per-M prices, and returns a
STRUCTURED result (never writes the DB). Persistence is owned by price_check.py via utils.write_prices.
"""
import os
import sys

_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..","..")))
from ..utils import fetch_markdown  # noqa: E402
from checks.tier0_openai import parse  # noqa: E402

URL = "https://developers.openai.com/api/docs/pricing.md"
PROVIDER_ID = "openai"
SOURCE = "tier0_openai:openai-official"


def collect(ctx):
    """Fetch + parse official OpenAI pricing, return structured result (no DB write)."""
    del ctx  # ctx = {"now", "dry_run"}; we only fetch+parse here
    text = fetch_markdown(URL)
    updates = parse(text)  # {model_id: {per_mtok, notes}}
    parsed = {}
    for mid, info in (updates or {}).items():
        parsed[mid] = {
            "per_mtok": info.get("per_mtok"),
            "notes": info.get("notes"),
        }
    return {
        "provider_id": PROVIDER_ID,
        "source": SOURCE,
        "status": "ok" if parsed else "no_source",
        "parsed": parsed,
        "errors": [],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(collect({"now": None}), ensure_ascii=False, indent=1)[:900])
