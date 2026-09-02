"""Independent collector for minimax (official source)."""
import os, sys
_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..")))
from collect.base import fetch_markdown, write_prices  # noqa: E402
from checks.tier0_minimax import parse  # noqa: E402

URL = "https://platform.minimax.io/docs/guides/pricing-paygo.md"
PROVIDER_ID = "minimax"


def collect(ctx):
    now = ctx.get("now")
    text = fetch_markdown(URL)
    updates = parse(text)
    n = len(updates)
    changed = write_prices(PROVIDER_ID, updates, "tier0_minimax:source", now)
    return {"changed": changed, "status": "ok", "detail": f"parsed {n} models, {changed} changed"}


if __name__ == "__main__":
    import json
    print(json.dumps(collect({"now": None}), ensure_ascii=False))
