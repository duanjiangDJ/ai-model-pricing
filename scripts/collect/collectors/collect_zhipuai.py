"""Independent collector for ZAI (bigmodel, js_fetch, parse_bigmodel)."""
import os, sys
_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..","..")))
from ..utils import js_fetch, write_prices  # noqa: E402
from checks.tier1_zhipuai import parse_bigmodel  # noqa: E402

URL = "https://open.bigmodel.cn/pricing"
PROVIDER_ID = "zhipuai"


def collect(ctx):
    now = ctx.get("now")
    html = js_fetch(URL, virtual_time=10000)
    updates = parse_bigmodel(html)
    changed = write_prices(PROVIDER_ID, updates, "tier1_zhipuai:source", now)
    return {"changed": changed, "status": "ok", "detail": f"parsed {len(updates)} models, {changed} changed"}


if __name__ == "__main__":
    import json
    print(json.dumps(collect({"now": None}), ensure_ascii=False))
