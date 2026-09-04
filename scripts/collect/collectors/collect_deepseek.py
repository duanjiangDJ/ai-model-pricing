"""Independent collector for deepseek (official source)."""
import os, sys
_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..","..")))
from ..utils import make_result,fetch_markdown, write_prices  # noqa: E402
from checks.tier0_deepseek import parse  # noqa: E402

URL = "https://api-docs.deepseek.com/quick_start/pricing"
PROVIDER_ID = "deepseek"


def collect(ctx):
    now = ctx.get("now")
    text = fetch_markdown(URL)
    updates = parse(text)
    n = len(updates)
    return make_result(PROVIDER_ID, "tier0_deepseek:source", updates)
    # (return moved to make_result): changed, "status": "ok", "detail": f"parsed {n} models, {changed} changed"}


if __name__ == "__main__":
    import json
    print(json.dumps(collect({"now": None}), ensure_ascii=False))
