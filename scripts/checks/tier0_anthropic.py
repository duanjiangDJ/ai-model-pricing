"""Anthropic official pricing check (tier 0). SSR page body lists, for every model, a block

    <label> <description> Input $X / MTok Output $Y / MTok
    Prompt caching Read $R / MTok Write $W / MTok

2026-09-10 retarget: the page used to render the cache cells as "Write ... Read ..." and the
parser anchored on 5 fixed labels ("Fable 5", "Mythos 5", "Opus 5", "Sonnet 5", "Haiku 4.5").
Anthropic then (a) swapped the cache order to **Read before Write** and (b) relabelled the
flagship "Fable 5" -> "Fable 5.1". The old regex matched 0 blocks, so `run()` returned
"parsed 0 models" and the manifest kept `check:anthropic` GREEN while Anthropic prices were no
longer verified at all (a dead check is worse than a failing one). The parser now:
  - matches the current Read-before-Write block shape,
  - maps the label that *immediately precedes* each block (nearest match, longest wins) to the
    repo model id — so a new version suffix ("Fable 5.1") is picked up instead of silently
    reusing the older model's row,
  - RAISES when it matches nothing, so a future layout change shows up as a failed check in
    the manifest instead of a silent green.
The page lists both the current "latest models" set and a "detailed pricing" set; ids not in
the repo are ignored by update_model_prices (the check never invents models).
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, to_text, update_model_prices  # noqa: E402

TIER = 0
PROVIDER_ID = "anthropic"
URL = "https://www.anthropic.com/pricing"

# page label -> repo model id. Longest label wins on a positional tie ("Fable 5.1" is matched
# before its "Fable 5" prefix).
LABELS = {
    "Fable 5.1": "claude-fable-5-1",
    "Fable 5": "claude-fable-5",
    "Opus 5": "claude-opus-5",
    "Opus 4.8": "claude-opus-4-8",
    "Opus 4.7": "claude-opus-4-7",
    "Opus 4.6": "claude-opus-4-6",
    "Opus 4.5": "claude-opus-4-5",
    "Opus 4.1": "claude-opus-4-1",
    "Sonnet 5": "claude-sonnet-5",
    "Sonnet 4.6": "claude-sonnet-4-6",
    "Sonnet 4.5": "claude-sonnet-4-5",
    "Haiku 4.5": "claude-haiku-4-5",
    "Mythos 5": "claude-mythos-5",
}

# Current (2026-09-10) block shape: input, output, then cache READ before WRITE.
BLOCK_RE = re.compile(
    r"Input \$([\d.]+) / MTok Output \$([\d.]+) / MTok "
    r"Prompt caching Read \$([\d.]+) / MTok Write \$([\d.]+) / MTok"
)

NOTE = "Official anthropic.com/pricing (USD/MTok, incl. cache read/write). Parsed by check anthropic."


def _nearest_label(segment):
    """The label that immediately precedes a block. Nearest match wins; longest on a tie."""
    best, best_key = None, None
    for lab in LABELS:
        pos = segment.rfind(lab)
        if pos < 0:
            continue
        key = (pos, len(lab))
        if best_key is None or key > best_key:
            best, best_key = lab, key
    return best


def parse(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    out = {}
    matches = list(BLOCK_RE.finditer(text))
    for i, m in enumerate(matches):
        seg_start = matches[i - 1].end() if i else max(0, m.start() - 200)
        label = _nearest_label(text[seg_start:m.start()])
        if not label:
            continue
        mid = LABELS[label]
        if mid in out:
            continue  # first (top-of-page "latest models") row for a model wins
        out[mid] = {
            "per_mtok": {
                "input": float(m.group(1)), "output": float(m.group(2)),
                "cache_read": float(m.group(3)), "cache_write": float(m.group(4)),
            },
            "notes": NOTE,
        }
    if not out:
        # Fail loudly: an empty parse means the layout changed (or we got a stub). Returning
        # {} here lets the check report OK with 0 models, which is how the dead check went
        # unnoticed. Raising marks check:anthropic as errored in the manifest.
        raise ValueError("anthropic pricing page: no model price blocks matched (layout changed?)")
    return out


def run(ctx):
    text = to_text(http_get(URL))
    parsed = parse(text)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    changed = update_model_prices(provider, parsed, ctx["now"], URL)
    return {"changed": len(changed), "detail": f"parsed {len(parsed)} models"}
