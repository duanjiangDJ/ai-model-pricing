"""Independent collector for openrouter (aggregator gateway, treated as a peer provider).

Reuses sync_openrouter.build_model (per-token -> per-M, dual-currency, billing_model/notes) and
returns the structured result; it does NOT write the DB (price_check owns persistence).
"""
import os
import sys

_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..", "..")))  # scripts/ so sync_openrouter is importable

from common import fetch_json  # noqa: E402
from sync_openrouter import OPENROUTER_URL, build_model  # noqa: E402
from collect.utils import make_result  # noqa: E402

URL = OPENROUTER_URL
PROVIDER_ID = "openrouter"
SOURCE = "openrouter:api"


def collect(ctx):
    """Fetch OpenRouter catalog, build per-M prices for the openrouter provider, return structured."""
    del ctx
    data = fetch_json(URL)
    models = {}
    for entry in (data.get("data") or []):
        mid = entry.get("id")
        if not mid:
            continue
        m = build_model(entry)
        pm = (m.get("pricing") or {}).get("per_mtok")
        if pm:
            models[mid] = {"per_mtok": pm, "notes": m.get("notes")}
    return make_result(PROVIDER_ID, SOURCE, models)


if __name__ == "__main__":
    import json
    r = collect({"now": None})
    print(r["status"], "parsed:", len(r["parsed"]), "| source:", r["source"])
