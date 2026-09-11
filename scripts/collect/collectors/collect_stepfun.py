"""Independent collector for StepFun (js_fetch, parse_stepfun + build_updates)."""
import os, sys
_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..","..")))
from ..utils import make_result,js_fetch, write_prices  # noqa: E402
from checks.tier1_stepfun import parse_stepfun, build_updates  # noqa: E402

URL = "https://platform.stepfun.com/docs/zh/guides/pricing/details"
PROVIDER_ID = "stepfun"


def collect(ctx):
    now = ctx.get("now")
    html = js_fetch(URL, virtual_time=15000)
    # build_updates wraps the flat ¥/M parse into {per_mtok:{...cny...}, notes} — the shape
    # make_result/price_check require. Passing the raw flat dict here made make_result emit
    # per_mtok=None for every model, i.e. a collector that parsed fine but wrote NOTHING.
    updates = build_updates(parse_stepfun(html), now)
    return make_result(PROVIDER_ID, "tier1_stepfun:source", updates)
    # (return moved to make_result): changed, "status": "ok", "detail": f"parsed {n} models, {changed} changed"}


if __name__ == "__main__":
    import json
    print(json.dumps(collect({"now": None}), ensure_ascii=False))
