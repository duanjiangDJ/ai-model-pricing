"""toolbox.py — shared utility library for all scripts.

Central place for HTTP fetching, JSON I/O, changelog helpers, dedup helpers,
language detection, and version helpers. New scripts should import from here;
old scripts import `common` which re-exports this module for compatibility.
"""
import json
import os
import re
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(ROOT, "data", "feed")
PROVIDERS = os.path.join(FEED, "providers")
VIEW = os.path.join(ROOT, "data", "view")
META = os.path.join(ROOT, "data", "meta")

SCHEMA_VERSION = "26.0.1"
UA = "ai-model-pricing-bot/1.0 (+https://github.com/duanjiangDJ/ai-model-pricing)"

_HAN_RE = re.compile(r"[\u4e00-\u9fff]")


# ---------------------------------------------------------------- time & json

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(path, data, indent=2):
    """Atomic write: dump to a temp file then os.replace, so a failing dump (e.g. a
    non-serializable value mid-serialize) cannot leave a truncated/corrupt data file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
        f.write("\n")
    os.replace(tmp, path)


# ---------------------------------------------------------------- network

def http_get(url, timeout=60, headers=None):
    """Fetch a URL and return raw bytes. Raises on HTTP errors."""
    h = {"User-Agent": UA, "Accept": "text/html,*/*"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_json(url, timeout=60):
    return json.loads(http_get(url, timeout=timeout).decode("utf-8", "ignore"))


def to_text(raw):
    """Decode raw bytes with encoding fallbacks (utf-8 -> gb18030)."""
    for enc in ("utf-8", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "ignore")


def default_chrome():
    """Locate the locally-installed Chrome for Testing (headless browser) binary."""
    import glob as _g
    candidates = _g.glob(os.path.expanduser("~/.cache/puppeteer-chrome/chrome/*/chrome-linux64/chrome"))
    return candidates[0] if candidates else None


def js_fetch(url, timeout=60, virtual_time=10000, chrome=None):
    """Fetch a JS-rendered page using headless Chrome (dump-dom + virtual-time budget).

    Returns the rendered HTML as text. Returns '' if Chrome is unavailable or the fetch
    fails. Use this for vendor pricing pages that are client-side rendered (curl/urllib
    only get the empty shell, e.g. open.bigmodel.cn/pricing). Chrome path is taken from
    CHROME_BIN env, the default_chrome() cache location, or the `chrome` argument.
    """
    import subprocess
    chrome_path = chrome or os.environ.get("CHROME_BIN") or default_chrome()
    if not chrome_path or not os.path.exists(chrome_path):
        return ""
    cmd = [chrome_path, "--headless=new", "--no-sandbox", "--disable-gpu",
           "--enable-unsafe-swiftshader", f"--virtual-time-budget={virtual_time}",
           "--dump-dom", url]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout, text=True)
        return r.stdout or ""
    except Exception:  # noqa: BLE001
        return ""


def wayback_snapshot_candidates(url, n=3):
    """Up to n recent Wayback captures (id_ raw mode), newest first."""
    cdx = ("http://web.archive.org/cdx/search/cdx?url={}&output=json&limit=15"
           "&from=20260101".format(url))
    try:
        rows = json.loads(http_get(cdx, timeout=60).decode("utf-8", "ignore"))
    except Exception:  # noqa: BLE001
        return []
    if not isinstance(rows, list) or len(rows) <= 1:
        return []
    candidates = sorted(rows[1:], key=lambda r: r[1], reverse=True)[:n]
    return ["http://web.archive.org/web/{}id_/{}".format(r[1], url) for r in candidates]


# ---------------------------------------------------------------- data helpers

def to_float_or_none(v):
    if v is None or v == "":
        return None
    try:
        f = float(v)
        return f if f >= 0 else None
    except (TypeError, ValueError):
        return None


def has_chinese(text):
    return bool(_HAN_RE.search(text or ""))


# ---------------------------------------------------------------- dual-currency helpers
# Since schema 26.8, per_mtok/batch/per_image prices are objects {usd, cny} (a price may
# be expressed in just one currency). These helpers read/write them uniformly.

def price_of(pm, key, currency="usd"):
    """Get a price field's value for a currency from a dual-price object.
    Falls back to the raw value if the field is still a scalar (pre-migration)."""
    v = (pm or {}).get(key)
    if isinstance(v, dict):
        return v.get(currency)
    return v


def set_price(pm, key, currency, value):
    """Set a price field's value for a currency (creates the dual-price object if needed)."""
    v = pm.get(key)
    if not isinstance(v, dict):
        v = {}
        pm[key] = v
    v[currency] = value


def any_price_positive(pm, keys=("input", "output", "cache_read")):
    """True if any of the given per_mtok keys has a positive price in any currency."""
    for k in keys:
        v = (pm or {}).get(k)
        if isinstance(v, dict):
            if any((x or 0) > 0 for x in v.values()):
                return True
        elif v and v > 0:
            return True
    return False


def price_all_zero(pm, keys=("input", "output", "cache_read")):
    """True if the given per_mtok keys all resolve to 0 (free) across the present currency."""
    vals = []
    for k in keys:
        v = (pm or {}).get(k)
        if v is None:
            continue
        if isinstance(v, dict):
            vals.extend(x for x in v.values() if x is not None)
        else:
            vals.append(v)
    return bool(vals) and all(x == 0 for x in vals)


def has_zero_price(pm, keys=("input", "output", "cache_read")):
    """True if any of the given per_mtok keys is 0 in some currency (free tier present,
    possibly alongside a paid tier, e.g. Gemini free+paid)."""
    for k in keys:
        v = (pm or {}).get(k)
        if isinstance(v, dict):
            if any(x == 0 for x in v.values() if x is not None):
                return True
        elif v == 0:
            return True
    return False


def mixed_currency_zero(pm, keys=("input", "output", "cache_read", "cache_write")):
    """Return the per_mtok fields that mix a zero and a positive value across currencies.

    A field such as {"usd": 0, "cny": 0.15} is self-contradictory: 0 means "free", while a
    positive value in the *other* currency proves the model is paid. This happens when a
    CNY-only vendor (domestic page) keeps a stale/fabricated usd=0 from an earlier
    aggregator write; the CNY-only collector then only supplies cny, so update_model_prices
    (which merges per currency and never clears a value) leaves usd=0 stuck forever. The
    correct form for a single-currency vendor is the schema-blessed single-currency entry
    ({"cny": 0.15}) or usd=null -- never 0 (real case: zhipuai glm-4.7-flash).
    """
    out = []
    for k in keys:
        v = (pm or {}).get(k)
        if isinstance(v, dict):
            vals = [x for x in v.values() if x is not None]
            if any(x == 0 for x in vals) and any(x > 0 for x in vals):
                out.append(k)
    return out


def model_map(provider):
    return {m["id"]: m for m in provider.get("models", [])}


def load_provider(provider_id):
    path = os.path.join(PROVIDERS, f"{provider_id}.json")
    return read_json(path) if os.path.exists(path) else None


def save_provider(provider):
    write_json(os.path.join(PROVIDERS, f"{provider['provider_id']}.json"), provider)


def update_model_prices(provider, updates, now, source, surge_factor=5.0):
    """Apply {model_id: {per_mtok: {...}, batch: {...}, notes: str}} updates.
    Only non-None values overwrite. Returns list of changed model ids.
    A price change of more than surge_factor relative to the stored value is treated
    as a likely parsing/layout error: the field is skipped with a warning.
    """
    by_id = model_map(provider)
    changed = []
    for mid, data in updates.items():
        m = by_id.get(mid)
        if not m:
            continue
        per = data.get("per_mtok") or {}
        pm = m.setdefault("pricing", {}).setdefault("per_mtok", {})
        # per_mtok values are dual-price objects {usd, cny} (schema 26.8); scalars accepted for back-compat.
        for k in ("input", "output", "cache_read", "cache_write"):
            cur_new = per.get(k)
            if cur_new is None:
                continue
            if not isinstance(cur_new, dict):
                cur_new = {"usd": cur_new}
            cur_old = pm.get(k)
            cur_old = dict(cur_old) if isinstance(cur_old, dict) else ({"usd": cur_old} if cur_old is not None else {})
            for currency, nv in cur_new.items():
                if nv is None:
                    continue
                ov = cur_old.get(currency)
                if ov == nv:
                    continue
                # Never let a bare 0 overwrite a real/unknown value: 0 means "free", while an
                # aggregator's 0 usually means "not published" -> that must stay null.
                if nv == 0 and (ov is None or ov != 0):
                    print(f"  SKIP {mid}.{k}.{currency}: refusing to write 0 over {ov!r} (0 means free; unknown must stay null)")
                    continue
                if ov is not None and nv is not None and ov != 0:
                    _ratio = nv / ov
                    if _ratio > surge_factor or _ratio < (1.0 / surge_factor):
                        print(f"  SKIP {mid}.{k}.{currency}: {ov} -> {nv} looks like a parsing error (bidirectional {surge_factor}x surge); keeping old value")
                        continue
                cur_old[currency] = nv
                changed.append(mid)
            pm[k] = cur_old if cur_old else None
        # billing_model sync: once a model has a real (positive) token price in ANY currency,
        # it is billed per token — correct stale free/subscription/unknown labels.
        if changed and any_price_positive(pm):
            bm = m.get("billing_model") or []
            if "pay_per_token" not in bm:
                m["billing_model"] = ["pay_per_token"]
        if data.get("batch"):
            # schema 26.8+: batch.input/output are dual {usd,cny} objects (lowercase keys).
            # Normalize a scalar batch ({input:20}) from any source so it can't break validate.
            nb = {k: (v if isinstance(v, dict) else ({provider.get("currency", "USD").lower(): v} if v is not None else None))
                  for k, v in data["batch"].items()}
            if m["pricing"].get("batch") != nb:
                m["pricing"]["batch"] = nb
                changed.append(mid)
        if data.get("notes") and mid in changed:
            m["notes"] = data["notes"]
        new_status = data.get("status")
        if new_status:
            if new_status in ("online", "offline"):
                if m.get("status") != new_status:
                    m["status"] = new_status
                    if mid not in changed:
                        changed.append(mid)
            else:
                # Refuse schema-invalid status values (modelStatus enum = online|offline):
                # a check/collector literal like "retired" would corrupt the file and make
                # validate/audit hard-fail on the next save.
                print(f"  SKIP {mid}.status: invalid value {new_status!r} (only online/offline allowed)")
    if changed:
        provider["verified_at"] = now
        provider["updated_at"] = now
        save_provider(provider)
        append_changelog([{
            "date": now, "kind": "update", "scope": "model", "provider_id": provider["provider_id"],
            "item_id": ",".join(changed[:20]), "field": "pricing", "new": {"models": len(changed)},
            "source": source,
        }])
    return changed


# ---------------------------------------------------------------- changelog

def load_changelog():
    p = os.path.join(META, "changelog.json")
    if os.path.exists(p):
        return read_json(p)
    return {"schema_version": SCHEMA_VERSION, "entries": []}


def append_changelog(entries):
    cl = load_changelog()
    # Do NOT truncate: the changelog is an append-only audit trail. The previous
    # [:5000] slice silently dropped the oldest entries on every append once the
    # file passed 5000 records (e.g. the ebcloud entry vanished in PR #154).
    cl["entries"] = entries + cl["entries"]
    write_json(os.path.join(META, "changelog.json"), cl)


# ---------------------------------------------------------------- index/manifest

def load_index():
    p = os.path.join(FEED, "index.json")
    return read_json(p) if os.path.exists(p) else None


def save_index(index):
    write_json(os.path.join(FEED, "index.json"), index)


def load_manifest():
    p = os.path.join(META, "manifest.json")
    return read_json(p) if os.path.exists(p) else None


def save_manifest(manifest):
    write_json(os.path.join(META, "manifest.json"), manifest)


def refresh_index_counts(now=None):
    """Recompute index model counts from actual files."""
    index = load_index()
    changed = False
    for lst in (index["providers"], index["resellers"]):
        for entry in lst:
            path = os.path.join(FEED, entry["file"])
            if os.path.exists(path):
                actual = len(read_json(path).get("models", []))
                if actual != entry["model_count"]:
                    entry["model_count"] = actual
                    if now:
                        entry["updated_at"] = now
                    changed = True
    if changed:
        index["model_count"] = sum(e["model_count"] for e in index["providers"]) + sum(
            e["model_count"] for e in index["resellers"])
        save_index(index)
    return changed
