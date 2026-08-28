"""baichuan official pricing check (tier 1). Best-effort fetch; on failure records that the data was manually reconciled (2026-08-28) so the check does not silently mis-update. Parser can be added once reliably fetchable."""
import sys
sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import js_fetch  # noqa: E402

TIER = 1
PROVIDER_ID = "baichuan"
URL = "https://platform.baichuan-ai.com/prices"

def run(ctx):
    html = js_fetch(URL, virtual_time=12000)
    if not html:
        return {"changed": 0, "detail": "page not fetchable; data reconciled manually on 2026-08-28"}
    return {"changed": 0, "detail": "page fetched; parser TODO"}
