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

    Returns the number of change events (NOT unique models: a model counts once per changed
    field, e.g. pricing + batch). Fails soft (0) if the provider is not in the DB.
    """
    provider = load_provider(provider_id)
    if not provider:
        print(f"  WARN {provider_id}: provider not in DB, skipping write")
        return 0
    now = now or now_iso()
    changed = update_model_prices(provider, updates, now, source)
    # update_model_prices returns the LIST of changed model ids, but this function's
    # contract (and every caller: price_check sums it, the gen_collect template prints it
    # as "N changed") is a COUNT. Returning the list made price_check crash with
    # "unsupported operand type(s) for +=: 'int' and 'list'" on the models.dev
    # cross_provider result, aborting the WHOLE unified persist path (real 2026-09-10 run).
    return len(changed) if isinstance(changed, list) else changed


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


_PRICE_KEYS = ("input", "output", "cache_read", "cache_write")


def make_result(provider_id, source, updates, status=None):
    """Build a structured collector result from {model_id: {per_mtok, notes}} (no DB write).

    Returns the contract shape the router collects and price_check persists:
      {"provider_id", "source", "status", "parsed": {model_id: {per_mtok, notes}}, "errors"}

    FAIL-LOUD on a contract violation: an update entry that carries raw per-token price keys
    (input/output/cache_read/cache_write) but no "per_mtok" wrapper is a shape mismatch that
    would otherwise silently become per_mtok=None, so the collector parses fine yet writes
    NOTHING (a dead collector). This caught collect_stepfun / collect_baidu (2026-09-11): both
    passed a check's low-level flat {input, output, cache_read} dict straight to make_result.
    Wrap flat parses with a check's build_updates() (see checks/tier1_stepfun.build_updates)."""
    updates = updates or {}
    parsed = {}
    for mid, info in updates.items():
        if not isinstance(info, dict):
            raise ValueError(
                f"{provider_id}: collector update for {mid!r} must be a dict "
                f"{{'per_mtok': ..., 'notes': ...}}, got {type(info).__name__}")
        if "per_mtok" not in info and any(k in info for k in _PRICE_KEYS):
            raise ValueError(
                f"{provider_id}: collector update for {mid!r} looks like a raw price dict "
                f"{sorted(set(info) & set(_PRICE_KEYS))} without a 'per_mtok' wrapper. "
                f"make_result would emit per_mtok=None and the collector would silently write "
                f"NOTHING (dead collector). Wrap it as "
                f"{{'per_mtok': {{'input': {{'cny'|'usd': ...}}, ...}}, 'notes': ...}} — "
                f"see checks/tier1_stepfun.build_updates().")
        parsed[mid] = {"per_mtok": info.get("per_mtok"), "notes": info.get("notes")}
    return {
        "provider_id": provider_id,
        "source": source,
        "status": status or ("ok" if updates else "no_source"),
        "parsed": parsed,
        "errors": [],
    }
