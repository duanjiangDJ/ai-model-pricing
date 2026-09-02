"""Independent collector for Baidu Qianfan (js_fetch, parse_qianfan)."""
import os, sys
_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..")))
from collect.base import js_fetch, write_prices  # noqa: E402
from checks.tier1_baidu import parse_qianfan  # noqa: E402

URL = "https://cloud.baidu.com/doc/qianfan/s/wmh4sv6ya"
PROVIDER_ID = "baidu"


def collect(ctx):
    now = ctx.get("now")
    html = js_fetch(URL, virtual_time=10000)
    updates = parse_qianfan(html)
    changed = write_prices(PROVIDER_ID, updates, "tier1_baidu:source", now)
    return {"changed": changed, "status": "ok", "detail": f"parsed {len(updates)} models, {changed} changed"}


if __name__ == "__main__":
    import json
    print(json.dumps(collect({"now": None}), ensure_ascii=False))
