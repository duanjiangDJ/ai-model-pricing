"""Fetch official pricing pages directly (direct fetch or Wayback snapshot) and diff/update
the corresponding first-party provider files.

This is the "official-price-first" layer of the daily check. Strategy per source is
declared in scripts/official_sources.json. Parsers return ONLY fields they can confirm;
unknown values are left untouched (never overwritten with guesses).

Usage: python scripts/sync_official.py [--dry-run] [--source <provider_id>]
"""
import argparse
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    PROVIDERS, META, append_changelog, fetch_json, load_manifest, now_iso, read_json,
    save_manifest, write_json,
)

UA = "ai-model-pricing-official-sync/1.0 (+https://github.com/duanjiangDJ/ai-model-pricing)"


def http_get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    return raw


def to_text(raw):
    for enc in ("utf-8", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "ignore")


def wayback_snapshot_candidates(url, n=3):
    """Return up to n recent Wayback capture URLs (id_ raw mode), newest first."""
    cdx = (
        "http://web.archive.org/cdx/search/cdx?url={}&output=json&limit=15"
        "&from=20260101".format(url)
    )
    try:
        raw = http_get(cdx, timeout=60)
        rows = json.loads(raw.decode("utf-8", "ignore"))
    except Exception:  # noqa: BLE001
        return []
    if not isinstance(rows, list) or len(rows) <= 1:
        return []
    candidates = sorted(rows[1:], key=lambda r: r[1], reverse=True)[:n]
    return ["http://web.archive.org/web/{}id_/{}".format(r[1], url) for r in candidates]


# ---------------------------------------------------------------- parsers

def parse_deepseek(text):
    """DeepSeek Docusaurus pricing page. Returns {model_id: {per_mtok, notes}} (CNY).

    Table layout: 3 columns (flash / pro / vision) x 6 price rows:
      cache-hit off/peak, cache-miss off/peak, output off/peak.
    We record the PEAK tier as the list price; notes mention off-peak = 50%.
    """
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    cols = {
        "deepseek-v4-flash": 0,
        "deepseek-v4-pro": 1,
        "deepseek-v4-flash-vision-exp": 2,
    }
    out = {}
    idx = text.find("价格")
    if idx < 0:
        idx = 0
    seg = text[idx:idx + 4000]
    nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*元", seg)]
    for mid, col in cols.items():
        if len(nums) <= col + 15:
            continue
        out[mid] = {
            "per_mtok": {
                "input": nums[col + 9],     # cache-miss peak
                "output": nums[col + 15],   # output peak
                "cache_read": nums[col + 3],  # cache-hit peak
                "cache_write": None,
            },
            "notes": "Official page (CNY/1M tokens, peak tier; off-peak = 50%, peak = BJT 9-12/14-18). Parsed by sync_official.py.",
        }
    return out


def parse_baidu(text):
    """Baidu Qianfan doc page. Returns {model_id: {per_mtok, batch, notes}} (CNY per 1M tokens).

    Page is a series of blocks: '<Model> <versions> 推理服务 输入 <online> <batch> 元/千tokens
    命中缓存 ... 输出 ...'. Split by '推理服务' and parse each block's first price rows.
    """
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"\s+", " ", text)
    name_map = [
        (re.compile(r"ERNIE 5\.1(?:\s+ERNIE-[\w.\-]+)*"), "ernie-5.1"),
        (re.compile(r"ERNIE 5\.0(?:\s+ERNIE-[\w.\-]+)*"), "ernie-5.0"),
        (re.compile(r"ERNIE 4\.5 Turbo(?:\s+ERNIE-[\w.\-]+)*"), "ernie-4.5-turbo"),
    ]
    out = {}
    # blocks: '... <Model> <versions> 推理服务 <rows> ... <next model> 推理服务 ...'
    matches = list(re.finditer(r"([A-Z][\w .\-]{1,150}?)\s+推理服务", text))

    def first_price_after(block, label):
        """First (online, batch) price pair after a row label; '-' batch allowed."""
        i = block.find(label)
        if i < 0:
            return None, None
        m = re.search(r"(\d+(?:\.\d+)?)(?:\s+(\d+(?:\.\d+)?))?\s*(?:-)?\s*元/千tokens", block[i:])
        if not m:
            return None, None
        return float(m.group(1)), (float(m.group(2)) if m.group(2) else None)

    for i, m in enumerate(matches):
        label = None
        for pat, mid in name_map:
            if pat.fullmatch(m.group(1)):
                label = mid
                break
        if not label:
            continue
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[m.end():end]
        inp, batch_in = first_price_after(block, "输入")
        cache, _ = first_price_after(block, "命中缓存")
        outp, batch_out = first_price_after(block, "输出")
        if inp is None:
            continue
        per = {"input": inp * 1000, "output": outp * 1000 if outp else None,
               "cache_read": cache * 1000 if cache else None, "cache_write": None}
        batch = None
        if batch_in is not None:
            batch = {"input": batch_in * 1000, "output": batch_out * 1000 if batch_out else None}
        out[label] = {"per_mtok": per, "batch": batch,
                      "notes": "Official Qianfan doc (CNY/1M tokens, converted from /1K; first tier when tiered). Parsed by sync_official.py."}
    return out


def parse_anthropic(text):
    """Anthropic /pricing page. Returns {model_id: {per_mtok, notes}} (USD)."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    out = {}
    known = {
        "Fable 5": "claude-fable-5",
        "Mythos 5": "claude-mythos-5",
        "Opus 5": "claude-opus-5",
        "Sonnet 5": "claude-sonnet-5",
        "Haiku 4.5": "claude-haiku-4-5",
    }
    for label, mid in known.items():
        idx = text.find(label)
        if idx < 0:
            continue
        seg = text[idx:idx + 700]
        m = re.search(
            r"Input\s+\$\s*([\d.]+)\s*/\s*MTok\s+Output\s+\$\s*([\d.]+)\s*/\s*MTok"
            r"\s+Prompt caching\s+Write\s+\$\s*([\d.]+)\s*/\s*MTok\s+Read\s+\$\s*([\d.]+)\s*/\s*MTok",
            seg,
        )
        if not m:
            continue
        out[mid] = {
            "per_mtok": {
                "input": float(m.group(1)), "output": float(m.group(2)),
                "cache_write": float(m.group(3)), "cache_read": float(m.group(4)),
            },
            "notes": "Official anthropic.com/pricing (USD/MTok, incl. cache write/read). Parsed by sync_official.py.",
        }
    return out


def _extract_first_rows(text):
    """Return the first 'rows' JSON array from the page (the Standard-tier table),
    balancing brackets so nested arrays are kept intact."""
    start = text.find('"rows":[1,[[')
    if start < 0:
        return ""
    i = text.find("[", start + 7)
    depth = 0
    j = i
    while j < len(text):
        if text[j] == "[":
            depth += 1
        elif text[j] == "]":
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
        j += 1
    return ""


def parse_openai(text):
    """OpenAI pricing page (Wayback capture). Returns {model_id: {per_mtok, batch, notes}} (USD).

    Only the FIRST rows block (the Standard-tier inference table) is parsed; later
    blocks hold Batch/Flex/Fast-mode and fine-tuning tables with the same row format.
    """
    text = text.replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    seg = _extract_first_rows(text)

    out = {}
    rows = re.findall(
        r'\[0,"(gpt-5[\w.\-]*|gpt-4[\w.\-]*|o[1-4][\w.\-]*)"\],\[0,([\d.]+|"-")\],\[0,([\d.]+|"-")\],\[0,([\d.]+|"-")\],\[0,([\d.]+|"-")\]',
        seg,
    )

    def f(v):
        return None if v == '"-"' else float(v)

    seen = set()
    for name, inp, cached, cw, outp in rows:
        if name in seen:
            continue
        seen.add(name)
        out[name] = {
            "per_mtok": {"input": f(inp), "output": f(outp),
                         "cache_read": f(cached), "cache_write": f(cw)},
            "batch": None,
            "notes": "Official platform.openai.com/docs/pricing (Wayback snapshot, USD/1M, standard tier). Parsed by sync_official.py.",
        }
    return out


def parse_google(text):
    """Google Gemini pricing (best-effort). Returns {model_id: {per_mtok, notes}}."""
    # The page nests Standard/Batch/Flex tables; extract first 'Input price $X' after each model name.
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    out = {}
    for m in re.finditer(r"(gemini-[\w.\-]+)", text):
        mid = m.group(1)
        if mid in out:
            continue
        seg = text[m.end():m.end() + 4000]
        im = re.search(r"Input price\s+(?:Free of charge\s+)?\$([\d.]+)", seg)
        om = re.search(r"Output price\s+\$([\d.]+)", seg)
        if im:
            out[mid] = {
                "per_mtok": {"input": float(im.group(1)),
                             "output": float(om.group(1)) if om else None,
                             "cache_read": None, "cache_write": None},
                "notes": "Official ai.google.dev pricing (USD/1M, first tier found; promo prices noted on page). Parsed by sync_official.py.",
            }
    return out


PARSERS = {
    "deepseek": parse_deepseek,
    "baidu": parse_baidu,
    "anthropic": parse_anthropic,
    "openai": parse_openai,
    "google": parse_google,
}

# ---------------------------------------------------------------- engine


def apply_to_provider(provider_id, parsed, source_url, now, dry_run, parsed_ok=True):
    """Update provider file with parsed fields (never overwrite non-parsed fields).
    When parsed_ok, verified_at is refreshed even if nothing changed (official page was checked today)."""
    path = os.path.join(PROVIDERS, f"{provider_id}.json")
    if not os.path.exists(path):
        print(f"  SKIP {provider_id}: provider file missing")
        return 0
    provider = read_json(path)
    by_id = {m["id"]: m for m in provider["models"]}
    changed = 0
    for mid, data in parsed.items():
        if mid not in by_id:
            print(f"  new model not in DB (skip): {mid}")
            continue
        m = by_id[mid]
        per = data.get("per_mtok") or {}
        pm = m.setdefault("pricing", {}).setdefault("per_mtok", {})
        diffs = []
        for k in ("input", "output", "cache_read", "cache_write"):
            if per.get(k) is not None and pm.get(k) != per[k]:
                diffs.append(f"{k}: {pm.get(k)} -> {per[k]}")
                if not dry_run:
                    pm[k] = per[k]
        if data.get("batch"):
            old_b = m["pricing"].get("batch")
            if old_b != data["batch"]:
                diffs.append(f"batch: {old_b} -> {data['batch']}")
                if not dry_run:
                    m["pricing"]["batch"] = data["batch"]
        if diffs:
            changed += 1
            print(f"  {mid}: " + "; ".join(diffs))
            if not dry_run:
                m["notes"] = (m.get("notes") + " | " + data.get("notes", "")) if m.get("notes") else data.get("notes", "")
    if (changed or parsed_ok) and not dry_run:
        provider["verified_at"] = now
        provider["updated_at"] = now
        write_json(path, provider)
        if changed:
            append_changelog([{
                "date": now, "kind": "update", "scope": "provider", "provider_id": provider_id,
                "item_id": provider_id, "field": "official_sync",
                "new": {"models_changed": changed, "source": source_url},
                "source": source_url,
            }])
        else:
            append_changelog([{
                "date": now, "kind": "verify", "scope": "provider", "provider_id": provider_id,
                "item_id": provider_id, "field": "official_sync",
                "new": {"verified": True, "source": source_url},
                "source": source_url,
            }])
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--source", default=None, help="only run this provider_id")
    args = ap.parse_args()

    now = now_iso()
    manifest = load_manifest()
    registry = read_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "official_sources.json"))
    srcs = [s for s in manifest.get("sources", []) if not s.get("official")]
    total_changed = 0

    for src in registry["official_sources"]:
        if not src.get("enabled", True):
            continue
        if args.source and src["provider_id"] != args.source:
            continue
        parser = PARSERS.get(src["parser"])
        if not parser:
            print(f"SKIP {src['provider_id']}: no parser {src['parser']}")
            continue
        try:
            if src["strategy"] == "direct":
                raw = http_get(src["url"])
                text = to_text(raw)
            else:
                text = None
                snaps = wayback_snapshot_candidates(src["url"])
                snaps += [f"http://web.archive.org/web/{ts}id_/{src['url']}"
                          for ts in src.get("fallback_snapshots", [])]
                for snap in snaps:
                    try:
                        cand = to_text(http_get(snap, timeout=90))
                    except Exception:  # noqa: BLE001
                        continue
                    if len(cand) > 5000 and len(cand) < 5_000_000:  # skip wrappers/binary blobs
                        text = cand
                        break
                if text is None:
                    print(f"WARN {src['provider_id']}: no usable wayback snapshot")
                    srcs.append({"name": src["name"], "url": src["url"], "auto_sync": True,
                                 "official": True, "last_error": "no usable snapshot", "last_ok": None})
                    continue
            parsed = parser(text)
            print(f"[{src['provider_id']}] parsed {len(parsed)} models")
            if parsed:
                n = apply_to_provider(src["provider_id"], parsed, src["url"], now, args.dry_run)
                total_changed += n
                srcs.append({"name": src["name"], "url": src["url"], "auto_sync": True,
                             "official": True, "last_ok": now, "last_error": None})
            else:
                srcs.append({"name": src["name"], "url": src["url"], "auto_sync": True,
                             "official": True, "last_ok": now, "last_error": "parsed 0 models"})
        except Exception as e:  # noqa: BLE001
            print(f"WARN {src['provider_id']}: {str(e)[:120]}")
            srcs.append({"name": src["name"], "url": src["url"], "auto_sync": True,
                         "official": True, "last_error": str(e)[:200], "last_ok": None})

    manifest["sources"] = srcs
    manifest["last_daily_check"] = now
    save_manifest(manifest)
    print(f"official sync done: {total_changed} models updated" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
