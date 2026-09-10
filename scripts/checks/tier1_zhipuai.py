"""Zhipu (bigmodel.cn, domestic) official pricing check (tier 1).

Source: the canonical "API 定价" rate card, published as Mintlify Markdown at
https://docs.bigmodel.cn/cn/guide/start/pricing.md — STATIC (curl-able) and structured
(Markdown tables), so no headless Chrome is needed.

2026-09-11 revamp: the old source (open.bigmodel.cn/pricing, a JS-rendered marketing page)
was reworded to "... 输入单价 8元 / M 输出单价 28元 / M"; the old js_fetch + regex parser
matched 0 rows and raised on EVERY run (manifest check:zhipuai was red for weeks — the
failing check was in fact the signal that the parser needed retargeting). Retargeted here to
the structured rate card above.

Only the CNY branch is written here — USD list prices come from the z.ai international list
and are left untouched (a model carries both currencies). A model the page marks 免费
(e.g. GLM-4.7-Flash) must be stored as billing_model=["free"]; run() RAISES on a mismatch
(fail loud: update_model_prices cannot zero a price, so a paid listing on an officially-free
model would otherwise survive every sync).
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("checks", 1)[0])
from toolbox import http_get, load_provider, now_iso, to_text, update_model_prices  # noqa: E402

TIER = 1
PROVIDER_ID = "zhipuai"
URL = "https://docs.bigmodel.cn/cn/guide/start/pricing.md"

# Repo ids this check governs (a page name lowercased == the repo id). Deliberately limited to
# the models the check already managed: models like glm-5v-turbo carry a models.dev USD value
# that numerically equals the official CNY list (5/22), so writing cny there would trip the
# usd==cny fabrication audit — that needs a separate data-truth call, not a silent write.
TRACKED = {
    "glm-5.3", "glm-5.3-flash", "glm-5.2", "glm-5.1", "glm-5-turbo", "glm-5",
    "glm-4.7", "glm-4.5-air", "glm-4.7-flashx", "glm-4.7-flash",
}

_SEP = re.compile(r":?-{2,}:?")


def _header_indices(cells):
    def find(kw):
        for i, c in enumerate(cells):
            if kw in c:
                return i
        return None
    return {"name": find("模型名称"), "input": find("输入单价"),
            "output": find("输出单价"), "cache": find("缓存命中")}


def _cell_num(cells, i):
    if i is None or i >= len(cells):
        return None
    m = re.match(r"(\d+(?:\.\d+)?)", cells[i].replace(",", ""))
    return float(m.group(1)) if m else None


def _cell_free(cells, i):
    return i is not None and i < len(cells) and "免费" in cells[i]


def parse(text):
    """Parse the bigmodel.cn rate card into {model_id: {input, output, cache, free}}.

    model_id is the lowercased page name (already the repo id for tracked models). Only the
    model-inference tables carrying "输入单价"/"输出单价" columns are read; tiered models list
    their base ([0,32K)) row first, so the first row per id wins. Raises when nothing matched —
    a layout change must never silently no-op the check.
    """
    lines = (text or "").splitlines()
    out, hdr = {}, None
    for i, raw in enumerate(lines):
        line = raw.strip()
        if not line.startswith("|"):
            hdr = None  # left the table
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        nxt_cells = [c.strip() for c in nxt.strip("|").split("|")] if nxt.startswith("|") else []
        if nxt_cells and all(c == "" or _SEP.fullmatch(c) for c in nxt_cells):
            # this is a table header row: keep it only when it is a per-token price table
            hdr = _header_indices(cells) if ("输入单价" in line and "输出单价" in line) else None
            continue
        if hdr is None or hdr["name"] is None:
            continue
        if all(c == "" or _SEP.fullmatch(c) for c in cells):
            continue
        if hdr["name"] >= len(cells):
            continue
        name = cells[hdr["name"]]
        if not name or name == "模型名称":
            continue
        mid = name.lower()
        if mid in out:
            continue
        out[mid] = {
            "input": _cell_num(cells, hdr["input"]),
            "output": _cell_num(cells, hdr["output"]),
            "cache": _cell_num(cells, hdr["cache"]),
            "free": _cell_free(cells, hdr["input"]) or _cell_free(cells, hdr["output"]),
        }
    if not out:
        raise ValueError("bigmodel.cn rate card: no price rows matched (layout changed?)")
    return out


def build_updates(parsed, now=None):
    """Map parsed rows onto tracked repo ids -> ({mid: {per_mtok, notes}}, [free mid, ...])."""
    now = now or now_iso()
    updates, free_mids = {}, []
    for mid, pr in parsed.items():
        if mid not in TRACKED:
            continue
        if pr.get("free"):
            free_mids.append(mid)
            continue
        inp, outp = pr.get("input"), pr.get("output")
        if inp is None or outp is None:
            continue
        updates[mid] = {
            "per_mtok": {"input": {"cny": inp}, "output": {"cny": outp}},
            "notes": (f"Domestic bigmodel.cn pricing (CNY/1M tokens): input ¥{inp:g}, "
                      f"output ¥{outp:g}. Official API 定价 rate card (docs.bigmodel.cn), "
                      f"verified {now} (CNY). Independent of the z.ai USD list — not a "
                      f"currency conversion."),
        }
    return updates, free_mids


def run(ctx):
    text = to_text(http_get(URL, timeout=60))
    if not text or "输入单价" not in text:
        raise ValueError("bigmodel.cn rate card: empty body / no price table")
    parsed = parse(text)
    updates, free_mids = build_updates(parsed, ctx.get("now"))

    provider = load_provider(PROVIDER_ID)
    if not provider:
        return {"changed": 0, "detail": "provider file missing"}

    by_id = {m.get("id"): m for m in provider.get("models", [])}
    for mid in free_mids:
        m = by_id.get(mid)
        if m and "free" not in (m.get("billing_model") or []):
            raise ValueError(
                f"bigmodel.cn lists {mid} as 免费 but the repo bills it "
                f"{m.get('billing_model')} — free/paid conflict needs a data fix"
            )

    changed = update_model_prices(provider, updates, ctx["now"], URL)
    return {"changed": len(changed),
            "detail": f"bigmodel.cn rate card parsed ({len(updates)} models, {len(free_mids)} free)"}
