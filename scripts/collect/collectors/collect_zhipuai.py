"""Independent collector for Zhipu (bigmodel.cn) — the official CNY "API 定价" rate card.

Source: https://docs.bigmodel.cn/cn/guide/start/pricing.md (static Mintlify Markdown; no
headless Chrome needed). See checks/tier1_zhipuai.py for the parser + the 2026-09-11 revamp
note (the old JS marketing page was reworded, silently breaking the previous parser).
"""
import os
import sys

_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..", "..")))
from ..utils import fetch_markdown, make_result  # noqa: E402
from checks.tier1_zhipuai import PROVIDER_ID, URL, build_updates, parse  # noqa: E402


def collect(ctx):
    text = fetch_markdown(URL)
    updates, _free = build_updates(parse(text), ctx.get("now"))
    return make_result(PROVIDER_ID, "tier1_zhipuai:source", updates)


if __name__ == "__main__":
    import json
    print(json.dumps(collect({"now": None}), ensure_ascii=False))
