"""Google Gemini API official pricing check (tier 0). Direct fetch of the SSR devsite
pricing page. Each model section looks like:

  <model-id> Try it in Google AI Studio <desc> Standard Free Tier Paid Tier,
  per 1M tokens in USD Input price (Free of charge|Not available) $X ...
  Output price (including thinking tokens) (Free of charge|Not available) $Y ...
  Context caching price (Not available|Free of charge)( Same as Standard)? $Z ...
  Batch ... Input price (Not available|Free of charge) $Bi ... Output price ... $Bo

Variants handled:
  - two-tier models: '$2.00, prompts $4.00, prompts > 200k tokens' -> record <200k tier
  - audio-modality inputs: '$0.30 (text / image / video) $1.00 (audio)' -> record text price
  - image/video output: '$12.00 (text and thinking) $120.00 (images)' -> record the
    images/video token rate; '$0.039 per image*' -> use the footnote rate
    ('output is priced at $30 per 1,000,000 tokens') and skip per-image units.
  - batch tier is stored when a per-token batch rate is present (per-image-only batch
    rates are skipped).
Model segments are bounded at the next model id so values never bleed across models.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "google"
URL = "https://ai.google.dev/gemini-api/docs/pricing"

PRICE_RE = {
    "input": re.compile(r"Input price(?: \([^)]*\))? (?:Free of charge|Not available) \$([\d.]+)"),
    "cache": re.compile(r"Context caching price (?:Not available|Free of charge)(?: Same as Standard)? \$([\d.]+)"),
}
MULTI_OUT_RE = re.compile(r"\$([\d.]+) \((?:text and thinking|text)\) \$([\d.]+) \((?:images|video)\)")
PER_TOK_FN_RE = re.compile(r"output is priced at \$([\d.]+) per 1,000,000 tokens")
PLAIN_OUT_RE = re.compile(r"Output price(?: \([^)]*\))? (?:Not available|Free of charge) \$([\d.]+)")
BATCH_IN_RE = re.compile(r"Input price (?:Not available|Free of charge) \$([\d.]+)")
BATCH_OUT_RE = re.compile(r"Output price(?: \([^)]*\))? (?:Not available|Free of charge) \$([\d.]+)")
MID_RE = re.compile(r"([a-z][a-z0-9.\-]{2,})\s+Try it in Google AI Studio")
# next card boundary: a model id (lowercase, contains a digit) followed by a description
# ('Try it', 'Warning', capital, '('). Deprecated cards lack 'Try it in Google AI Studio'
# but still start with '<id> <Capital>'. Pure-alpha words ('capable Flash') never match.
NEXT_CARD_RE = re.compile(r"[a-z][a-z0-9.\-]*[0-9][a-z0-9.\-]*\s+(?:Try it in Google AI Studio|[A-Z(])")


def _std_output(std, full):
    """Return the standard-tier per-token output price, or None."""
    mm = MULTI_OUT_RE.search(std)
    if mm:
        return float(mm.group(2))  # images/video token rate
    mm = PER_TOK_FN_RE.search(full)  # footnote may sit after the Batch/Flex/Priority blocks
    if mm:
        return float(mm.group(1))
    if "per image" in std:
        return None  # per-image unit without per-token footnote
    mm = PLAIN_OUT_RE.search(std)
    return float(mm.group(1)) if mm else None


def _batch(std, batch):
    """Return {input, output} batch prices (per-token only), or None."""
    if "per image" in batch:
        return None
    b = {}
    mm = BATCH_IN_RE.search(batch)
    if mm:
        b["input"] = float(mm.group(1))
    mm = MULTI_OUT_RE.search(batch)
    if mm:
        b["output"] = float(mm.group(2))
    else:
        mm = BATCH_OUT_RE.search(batch)
        if mm:
            b["output"] = float(mm.group(1))
    return b if len(b) == 2 else None


def _model_sections(text):
    """Yield (model_id, standard_segment, batch_segment, full_section) bounded per model."""
    for m in MID_RE.finditer(text):
        mid = m.group(1)
        rest = text[m.end():m.end() + 3000]
        if "Standard" not in rest:
            continue
        nxt = NEXT_CARD_RE.search(rest)
        if nxt:
            rest = rest[:nxt.start()]
        std, _, batch = rest.partition("Batch")
        yield mid, std, batch, rest


def parse(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    out = {}
    for mid, std, batch, full in _model_sections(text):
        vals = {}
        for k, rx in PRICE_RE.items():
            mm = rx.search(std)
            if mm:
                vals[k] = float(mm.group(1))
        outp = _std_output(std, full)
        if "input" not in vals or outp is None:
            continue
        out[mid] = {
            "per_mtok": {
                "input": vals["input"],
                "output": outp,
                "cache_read": vals.get("cache"),
                "cache_write": None,
            },
            "batch": _batch(std, batch),
            "notes": ("Official ai.google.dev/gemini-api/docs/pricing (USD/1M tokens, standard tier; "
                      "two-tier models recorded at the <200k tier; audio inputs recorded at text price; "
                      "image/video models recorded at the images/video token rate). "
                      "Parsed by check google."),
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
