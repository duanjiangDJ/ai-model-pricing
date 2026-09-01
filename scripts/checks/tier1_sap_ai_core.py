"""SAP AI Core official pricing check (tier 1, auto-generated collection template).

Official pricing page: https://help.sap.com/docs/sap-ai-core
Auto-collection hook: js_fetch the official page; if it returns content, add a parser
here to extract per-M (USD/CNY) prices. If the page is bot-protected/empty, this records
the fetch attempt with a manual-reconciliation note so the data remains auditable and the
page is re-probed on each sync until it becomes fetchable (then a parser can be added).
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import js_fetch, load_provider, now_iso  # noqa: E402

TIER = 1
PROVIDER_ID = "sap-ai-core"
URL = 'https://help.sap.com/docs/sap-ai-core'


def run(ctx):
    html = js_fetch(URL, virtual_time=15000)
    if not html:
        return {"changed": 0,
                "detail": "auto-gen check: official page not fetchable (bot-protected/empty); "
                          "prices available via aggregation/manual — add parser when page becomes fetchable."}
    # Page is fetchable: a parser can be added (see module docstring).
    return {"changed": 0, "detail": f"official page now fetchable ({len(html)} bytes); parser TODO"}
