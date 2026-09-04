"""scripts/collect/utils.py — shared collection utilities.

Architecture chosen by the user (2026-09-02):
    router.py  ->  collect_<provider>.py  ->  utils.py

Each collect_<provider>.py independently fetches THAT provider's official source,
parses per-M prices, and writes them via write_prices() (which wraps toolbox
.update_model_prices). Providers without an independent official source fall back
to the aggregation sources (openrouter / models.dev).
"""
import os
import sys

_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..")))  # scripts/ so `toolbox` is importable

from toolbox import (  # noqa: E402,F401
    http_get,
    js_fetch,
    to_text,
    load_provider,
    update_model_prices,
    now_iso,
)


def fetch_markdown(url, timeout=90):
    """Fetch a pricing page as markdown/text (works for Mintlify-style .md pages)."""
    return to_text(http_get(url, timeout=timeout))


def write_prices(provider_id, updates, source, now=None):
    """Apply {model_id: {per_mtok: ..., notes: ...}} updates to a provider via update_model_prices.

    Returns the number of changed models. Fails soft (0) if the provider is not in the DB.
    """
    provider = load_provider(provider_id)
    if not provider:
        print(f"  WARN {provider_id}: provider not in DB, skipping write")
        return 0
    now = now or now_iso()
    return update_model_prices(provider, updates, now, source)


def get_provider(provider_id):
    """Return the provider dict (or None)."""
    return load_provider(provider_id)


def load_collector(provider_id):
    """Import scripts/collect/collect_<provider_id>.py with sanitized module name."""
    import importlib

    name = "collect_" + provider_id.replace("-", "_").replace(".", "_")
    try:
        return importlib.import_module(f"collect.{name}")
    except Exception:  # noqa: BLE001
        return None


def make_result(provider_id, source, updates, status=None):
    """Build a structured collector result from {model_id: {per_mtok, notes}} (no DB write).

    Returns the contract shape the router collects and price_check persists:
      {"provider_id", "source", "status", "parsed": {model_id: {per_mtok, notes}}, "errors"}
    """
    updates = updates or {}
    return {
        "provider_id": provider_id,
        "source": source,
        "status": status or ("ok" if updates else "no_source"),
        "parsed": {mid: {"per_mtok": info.get("per_mtok"), "notes": info.get("notes")}
                   for mid, info in updates.items()},
        "errors": [],
    }
