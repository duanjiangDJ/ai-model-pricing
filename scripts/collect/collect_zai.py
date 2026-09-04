"""Independent collector for zai (official source)."""
import os, sys
_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..")))
from collect.utils import fetch_markdown, write_prices  # noqa: E402
from checks.tier0_zai import parse  # noqa: E402

URL = "https://docs.z.ai/guides/overview/pricing.md"
PROVIDER_ID = "zai"


def collect(ctx):
    now = ctx.get("now")
    text = fetch_markdown(URL)
    updates = parse(text)
    n = len(updates)
    changed = write_prices(PROVIDER_ID, updates, "tier0_zai:source", now)
    return {"changed": changed, "status": "ok", "detail": f"parsed {n} models, {changed} changed"}


if __name__ == "__main__":
    import json
    print(json.dumps(collect({"now": None}), ensure_ascii=False))
