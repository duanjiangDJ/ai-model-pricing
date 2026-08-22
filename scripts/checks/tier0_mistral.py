"""Mistral official API pricing check (tier 0). Direct fetch of the SSR pricing page
https://mistral.ai/pricing/api (the site is an Astro/Payload SPA; the API tab is its
own route whose model cards ARE server-rendered).

Card structure (raw HTML):
  <div class="model-item ..." data-name="...">
    <p class="text-h5 font-mistral text-current">Mistral Medium 3.5</p>
    <p class="text-body-base text-current relative">Input (/M tokens) </p>
    <mistral-atom-text-price data-prices="{&quot;priceEur&quot;:1.25,&quot;priceUsd&quot;:1.5,...}">$1.5</...>
    ...
    <label class="text-button-large ... cursor-text">mistral-medium-latest</label>
  </div>

Only per-token rows (Input / Cached input / Output, per 1M tokens) are mapped to
per_mtok; per-page / per-minute / OCR rows are ignored. Third-party cards (zai-*, ...)
carry ids that do not exist in this provider file and are skipped by update_model_prices.
"""
import html as html_mod
import json
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "mistral"
URL = "https://mistral.ai/pricing/api"

CARD_RE = re.compile(r'<div class="model-item[^>]*>')
ID_RE = re.compile(
    r'<label class="text-button-large font-mistral text-current truncate w-full cursor-text">'
    r"([a-z0-9\-_.]+)</label>"
)
ROW_RE = re.compile(
    r'<p class="text-body-base text-current relative">(Input|Cached input|Output) \(/M tokens\) </p>'
    r'<mistral-atom-text-price[^>]*data-prices="([^"]*)"'
)
FIELD = {"Input": "input", "Cached input": "cache_read", "Output": "output"}


def _usd(data_attr):
    try:
        d = json.loads(html_mod.unescape(data_attr))
        v = d.get("priceUsd")
        return float(v) if isinstance(v, (int, float)) else None
    except (ValueError, TypeError):
        return None


def parse(text):
    out = {}
    for card in CARD_RE.split(text)[1:]:
        mid = ID_RE.search(card)
        if not mid:
            continue
        mid = mid.group(1)
        vals = {}
        for label, data in ROW_RE.findall(card):
            v = _usd(data)
            if v is not None:
                vals[FIELD[label]] = v
        if "input" not in vals or "output" not in vals:
            continue
        out[mid] = {
            "per_mtok": {
                "input": vals["input"],
                "output": vals["output"],
                "cache_read": vals.get("cache_read"),
                "cache_write": None,
            },
            "notes": ("Official mistral.ai/pricing/api (USD per 1M tokens; page lists -latest aliases; "
                      "per-page/per-minute rows ignored). Parsed by check mistral."),
        }
    return out


def run(ctx):
    text = to_text(http_get(URL))
    parsed = parse(text)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = update_model_prices(provider, parsed, ctx["now"], URL)
    return {"changed": len(changed), "detail": f"parsed {len(parsed)} models"}
