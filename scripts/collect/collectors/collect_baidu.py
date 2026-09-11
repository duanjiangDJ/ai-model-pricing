"""Independent collector for Baidu Qianfan (js_fetch, parse_qianfan + build_updates)."""
import os, sys
_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..","..")))
from ..utils import make_result,js_fetch, write_prices  # noqa: E402
from checks.tier1_baidu import parse_qianfan, build_updates  # noqa: E402

URL = "https://cloud.baidu.com/doc/qianfan/s/wmh4sv6ya"
PROVIDER_ID = "baidu"


def collect(ctx):
    now = ctx.get("now")
    html = js_fetch(URL, virtual_time=10000)
    # build_updates wraps the flat ¥/M parse into {per_mtok:{...cny...}, notes}. Passing the
    # raw flat dict to make_result emitted per_mtok=None for every model -> dead collector.
    updates = build_updates(parse_qianfan(html), now)
    return make_result(PROVIDER_ID, "tier1_baidu:source", updates)
    # (return moved to make_result): changed, "status": "ok", "detail": f"parsed {len(updates)} models, {changed} changed"}


if __name__ == "__main__":
    import json
    print(json.dumps(collect({"now": None}), ensure_ascii=False))
