"""Shared helpers for ai-model-pricing scripts. Stdlib only."""
import json
import os
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MACHINE = os.path.join(ROOT, "data", "machine")
PROVIDERS = os.path.join(MACHINE, "providers")
HUMAN = os.path.join(ROOT, "data", "human")
META = os.path.join(ROOT, "data", "meta")

SCHEMA_VERSION = "1.0.0"
UA = "ai-model-pricing-sync/1.0 (+https://github.com/duanjiangDJ/ai-model-pricing)"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data, indent=2):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
        f.write("\n")


def fetch_json(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def to_float_or_none(v):
    """OpenRouter sends prices as strings like '0' or '2.5'. Free = 0.0, -1 = unknown."""
    if v is None or v == "":
        return None
    try:
        f = float(v)
        return f if f >= 0 else None
    except (TypeError, ValueError):
        return None


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


def load_changelog():
    p = os.path.join(META, "changelog.json")
    if os.path.exists(p):
        return read_json(p)
    return {"schema_version": SCHEMA_VERSION, "entries": []}


def append_changelog(entries):
    """entries: list of dicts following changelogEntry schema."""
    cl = load_changelog()
    cl["entries"] = entries + cl["entries"]
    # keep last 5000 entries
    cl["entries"] = cl["entries"][:5000]
    write_json(os.path.join(META, "changelog.json"), cl)
