"""aws official pricing check (tier 1). Vendor publishes USD-only list prices; a model present here is already single-currency USD (correct — no official CNY price page), so no CNY branch is added. Best-effort fetch; parser can be added once reliably fetchable."""
import sys
sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import js_fetch  # noqa: E402

TIER = 1
PROVIDER_ID = "aws"
URL = "https://aws.amazon.com/q/developer/"

def run(ctx):
    html = js_fetch(URL, virtual_time=12000)
    if not html:
        return {"changed": 0, "detail": "page not fetchable; USD list from models.dev, vendor USD-only"}
    return {"changed": 0, "detail": "page fetched; parser TODO"}
