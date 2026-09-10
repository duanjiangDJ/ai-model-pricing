"""Independent collector for models.dev (aggregation catalog, cross-provider). Peer provider.

Returns a CROSS-PROVIDER structured result: parsed is a dict of
    {provider_id: {model_id: {per_mtok, notes}}}
so price_check can fan out to each affected provider. Reuses sync_modelsdev.build_model.
"""
import os
import sys

_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..", "..")))  # scripts/
import json  # noqa: E402

from common import fetch_json  # noqa: E402
from sync.sync_modelsdev import MODELSDEV_URL, PROVIDERS, build_model  # noqa: E402

URL = MODELSDEV_URL
PROVIDER_ID = "modelsdev"
SOURCE = "models.dev:api"

# Subscription-included providers: models.dev lists their models at 0, but those are
# "included in a plan" - per_mtok must stay null (never 0). Same guard the legacy
# daily_check.sync_modelsdev_diff path used.
SUB_PROVIDER_HINTS = ("coding-plan", "token-plan", "copilot", "kimi-for-coding")


def first_party_today(pid, now):
    """True when this provider was verified against its own official source TODAY.

    Third-party republication (models.dev) must not overwrite one-hand official data. `now`
    MUST be a real ISO timestamp — a falsy `now` returns False, i.e. the guard is open. The
    router used to pass {"now": None}, silently disabling this guard for every provider and
    letting models.dev clobber the first-party deepseek prices (2026-09-10).
    """
    if not now:
        return False
    pf = os.path.join(PROVIDERS, f"{pid}.json")
    if not os.path.exists(pf):
        return False
    try:
        with open(pf, encoding="utf-8") as fh:
            return str(json.load(fh).get("verified_at", ""))[:10] == str(now)[:10]
    except Exception:  # noqa: BLE001
        return False


def collect(ctx):
    """Fetch models.dev catalog, build per-M prices grouped by provider, return structured."""
    now = ctx.get("now") or ""
    data = fetch_json(URL)
    providers = {}
    for pid, pv in (data or {}).items():
        if any(h in pid for h in SUB_PROVIDER_HINTS):
            continue  # subscription-included: per_mtok stays null, never 0
        # First-party priority: if this provider was verified against its official source
        # today, third-party republication (models.dev) must not overwrite it.
        if first_party_today(pid, now):
            continue
        models = {}
        for mid, m in ((pv.get("models") or {}).items()):
            md = build_model(mid, m)
            pm = (md.get("pricing") or {}).get("per_mtok")
            if not pm:
                continue
            models[mid] = {"per_mtok": pm, "notes": md.get("notes")}
        if models:
            providers[pid] = models
    return {
        "provider_id": PROVIDER_ID,
        "source": SOURCE,
        "status": "ok" if providers else "no_source",
        "parsed": providers,   # cross-provider: {pid: {model_id: per_mtok}}
        "errors": [],
        "cross_provider": True,
    }


if __name__ == "__main__":
    import json
    r = collect({"now": None})
    print(r["status"], "| providers:", len(r["parsed"]), "| source:", r["source"])
