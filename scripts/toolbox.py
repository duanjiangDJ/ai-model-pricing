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
MACHINE = os.path.join(ROOT, "data", "machine")
PROVIDERS = os.path.join(MACHINE, "providers")
HUMAN = os.path.join(ROOT, "data", "human")
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
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
        f.write("\n")


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


def model_map(provider):
    return {m["id"]: m for m in provider.get("models", [])}


def load_provider(provider_id):
    path = os.path.join(PROVIDERS, f"{provider_id}.json")
    return read_json(path) if os.path.exists(path) else None


def save_provider(provider):
    write_json(os.path.join(PROVIDERS, f"{provider['provider_id']}.json"), provider)


def update_model_prices(provider, updates, now, source):
    """Apply {model_id: {per_mtok: {...}, batch: {...}, notes: str}} updates.
    Only non-None values overwrite. Returns list of changed model ids."""
    by_id = model_map(provider)
    changed = []
    for mid, data in updates.items():
        m = by_id.get(mid)
        if not m:
            continue
        per = data.get("per_mtok") or {}
        pm = m.setdefault("pricing", {}).setdefault("per_mtok", {})
        for k in ("input", "output", "cache_read", "cache_write"):
            if per.get(k) is not None and pm.get(k) != per[k]:
                pm[k] = per[k]
                changed.append(mid)
        if data.get("batch"):
            if m["pricing"].get("batch") != data["batch"]:
                m["pricing"]["batch"] = data["batch"]
                changed.append(mid)
        if data.get("notes") and mid in changed:
            m["notes"] = data["notes"]
        if data.get("status"):
            m["status"] = data["status"]
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
    cl["entries"] = entries + cl["entries"][:5000]
    write_json(os.path.join(META, "changelog.json"), cl)


# ---------------------------------------------------------------- index/manifest

def load_index():
    p = os.path.join(MACHINE, "index.json")
    return read_json(p) if os.path.exists(p) else None


def save_index(index):
    write_json(os.path.join(MACHINE, "index.json"), index)


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
            path = os.path.join(MACHINE, entry["file"])
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
