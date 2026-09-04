"""Independent collector for StepFun (js_fetch, parse_stepfun)."""
import os, sys
_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..")))
from collect.utils import js_fetch, write_prices  # noqa: E402
from checks.tier1_stepfun import parse_stepfun  # noqa: E402

URL = "https://platform.stepfun.com/docs/zh/guides/pricing/details"
PROVIDER_ID = "stepfun"


def collect(ctx):
    now = ctx.get("now")
    html = js_fetch(URL, virtual_time=15000)
    updates = parse_stepfun(html)
    changed = write_prices(PROVIDER_ID, updates, "tier1_stepfun:source", now)
    return {"changed": changed, "status": "ok", "detail": f"parsed {len(updates)} models, {changed} changed"}


if __name__ == "__main__":
    import json
    print(json.dumps(collect({"now": None}), ensure_ascii=False))
