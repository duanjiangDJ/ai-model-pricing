"""OpenCode Go (subscription plan) official pricing check (tier 1).

Source: https://opencode.ai/docs/go/ — a SERVER-RENDERED HTML price table (plain
http_get works; no headless Chrome needed). One row per model:
    Model | Input | Output | Cached Read | Cached Write   (USD per 1M tokens)

2026-09-11 retarget: the previous auto-generated stub only probed the page with
js_fetch and never parsed it, so `opencode-go` prices were maintained purely from the
models.dev aggregation and drifted from the official list (real: deepseek-v4-pro
output 3.84 vs 3.48, kimi-k2.5 cache_read 0.08 vs 0.10). This check now parses the
official table so the vendor's own price list is authoritative.

RAISES when 0 price rows match — a layout change must FAIL LOUD (a dead check that
reports green is worse than a failing one; cf. tier0_alibaba / tier1_zhipuai).

Only the BASE tier of a tiered model is stored: a parenthesised suffix marking the
lower range ("(≤ 272K tokens)") or off-peak ("(Off-Peak)") is kept, a higher range
("(> ...)") or "(Peak)" is skipped — deterministic and independent of page order.
Free rows (all values "Free") carry nothing to write and are skipped.
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, now_iso, to_text, update_model_prices  # noqa: E402

TIER = 1
PROVIDER_ID = "opencode-go"
URL = "https://opencode.ai/docs/go/"

TR_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
TD_RE = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S)
_CELL = lambda c: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip()  # noqa: E731


def _base_row(name):
    """True when a display name denotes the base price tier (no suffix, a lower range,
    or off-peak). Higher-range ('> ...') and '(Peak)' rows are NOT the stored tier."""
    m = re.search(r"\(([^)]*)\)", name)
    if not m:
        return True
    suf = m.group(1)
    if ">" in suf or suf.strip().lower() == "peak":
        return False
    return True


def _norm(s):
    """Normalise a display name / repo id into a comparable key: dots and hyphens both
    collapse to '-', so 'GPT 5.6 Sol' == 'gpt-5.6-sol' == 'gpt-5-6-sol'."""
    s = re.sub(r"\(.*?\)", "", s).lower().replace("&amp;", "&")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def _num(cell):
    cell = cell.replace("$", "").strip()
    if cell in ("-", "", "\u2014"):
        return None
    if cell.lower() == "free":
        return 0.0
    try:
        return float(cell)
    except ValueError:
        return None


def parse(text):
    """-> {key: {input,output,cache_read,cache_write,name}} for priced BASE rows."""
    out = {}
    for tr in TR_RE.findall(text or ""):
        cells = [_CELL(c) for c in TD_RE.findall(tr)]
        if len(cells) < 5 or cells[0].lower() == "model":
            continue
        name = cells[0]
        if not _base_row(name):
            continue
        key = _norm(name)
        if not key or key in out:
            continue
        vals = [_num(x) for x in cells[1:5]]
        if not any(v for v in vals):      # "Free" / no published price -> nothing to write
            continue
        out[key] = {"name": name, "input": vals[0], "output": vals[1],
                    "cache_read": vals[2], "cache_write": vals[3]}
    if not out:
        raise ValueError(f"{PROVIDER_ID}: no price rows matched on the official table "
                         "(layout changed?)")
    return out


def build_updates(parsed, provider, now=None):
    """Map page rows onto repo model ids by normalised name OR id; never guess on an
    unknown or ambiguous key."""
    now = now or now_iso()
    idx = {}
    for m in provider.get("models", []):
        for key in {_norm(m.get("name") or ""), _norm(m["id"])}:
            if key:
                idx.setdefault(key, []).append(m["id"])
    updates, unmapped = {}, []
    for key, pr in parsed.items():
        ids = idx.get(key)
        if not ids or len(ids) > 1:
            unmapped.append(pr["name"])
            continue
        pm = {f: {"usd": pr[f]} for f in ("input", "output", "cache_read", "cache_write")
              if pr[f] is not None}
        updates[ids[0]] = {
            "per_mtok": pm,
            "notes": ("OpenCode Zen official price list (opencode.ai/docs/go/, USD per 1M "
                      f"tokens). Verified {now}."),
        }
    return updates, unmapped


def run(ctx):
    text = to_text(http_get(URL, timeout=60))
    parsed = parse(text)
    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}
    updates, unmapped = build_updates(parsed, provider, ctx.get("now"))
    changed = update_model_prices(provider, updates, ctx["now"], URL)
    return {"changed": len(changed),
            "detail": f"opencode.ai/docs/go/ table parsed ({len(parsed)} priced rows, "
                      f"{len(updates)} mapped, {len(unmapped)} unmapped)"}
