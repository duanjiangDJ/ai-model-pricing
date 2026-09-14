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

# Freshness window (hours) for the "verified one-hand not long ago" half of the guard.
FRESH_HOURS = 26


def has_official_collector(pid):
    """True when the repo ships a dedicated collector for this provider (collect_<pid>.py).

    Timestamp-independent: a provider whose price is maintained one-hand from its OWN
    official source must never be written by a third-party republication, no matter how
    old its `verified_at` is.

    2026-09-11 incident: the old guard compared `verified_at[:10] == now[:10]`. deepseek was
    verified 2026-09-10T09:39Z and zhipuai 2026-09-10T21:28Z, but the very next 3h sync ran
    at 2026-09-11T00:39Z — one UTC date later — so the guard opened and models.dev rewrote
    deepseek-flash/v4-flash/v4-pro (to its own off-peak 0.15/0.6/0.003) and zhipuai
    glm-5.3-flash (to the expired promo 0.075/0.25/0.015), also replacing their provenance
    notes. The dedicated collector is the durable signal, not a calendar date.
    """
    return os.path.exists(os.path.join(_THIS, f"collect_{pid}.py"))


CHECKS_DIR = os.path.abspath(os.path.join(_THIS, "..", "..", "checks"))

# Tokens that mark a scripts/checks/ module as a ONE-HAND OFFICIAL SOURCE, as opposed to the
# ~170 auto-generated record/stub checks. A check qualifies when it either FETCHES its own
# official page/API, or persists curated official constants (e.g. tier1_tencent applies the
# hand-verified TokenHub CNY prices because its page is JS-rendered; tier1_xiaomi likewise) --
# both are one-hand maintenance and must outrank a third-party republication.
_ONE_HAND_TOKENS = ("http_get(", "fetch_markdown(", "fetch_json(", "urllib", "requests.",
                    "update_model_prices(")

_ONE_HAND_CHECK_CACHE = None


def _one_hand_check_providers():
    """Provider ids whose scripts/checks/ module fetches its OWN official source.

    Timestamp-independent, exactly like has_official_collector(): the repo's one-hand official
    price for a provider may live in EITHER layer -- the newer collect/collectors/collect_<pid>.py,
    or the classic scripts/checks/tierN_<pid>.py that router.run_router() runs each sync.
    has_official_collector() only sees the first layer, so a check-only provider (opencode,
    opencode-go, moonshotai, tencent) fell through to the aggregator once its verified_at aged
    past FRESH_HOURS.

    Real 2026-09-14: opencode/opencode-go ping-ponged every ~26h -- models.dev wrote its own
    values (opencode kimi-k2.5 cache_read 0.08 vs the official 0.10; gpt-5.6-terra 2.5/15 vs
    2.0/12; and the same for deepseek-v4-pro/minimax-m2.5), then the official check reverted
    them in the SAME run (collectors run before checks). Net price diff zero, but 4 phantom
    "pricing" changelog entries, note churn and a re-rendered view every cycle. If the check
    had failed instead of reverting, the aggregator value would have been left published.
    """
    global _ONE_HAND_CHECK_CACHE
    if _ONE_HAND_CHECK_CACHE is not None:
        return _ONE_HAND_CHECK_CACHE
    found = set()
    try:
        names = sorted(f for f in os.listdir(CHECKS_DIR)
                       if f.endswith(".py") and not f.startswith("_"))
    except OSError:
        names = []
    for fn in names:
        try:
            with open(os.path.join(CHECKS_DIR, fn), encoding="utf-8") as fh:
                body = fh.read()
        except OSError:
            continue
        if not any(tok in body for tok in _ONE_HAND_TOKENS):
            continue  # record/stub check -- not a one-hand source
        for line in body.splitlines():
            s = line.strip()
            if s.startswith("PROVIDER_ID"):
                pid = s.split("=", 1)[-1].strip().strip("\"'")
                if pid:
                    found.add(pid)
                break
    _ONE_HAND_CHECK_CACHE = found
    return found


def has_official_check(pid):
    """True when scripts/checks/ ships a check for `pid` that fetches an official source."""
    return pid in _one_hand_check_providers()


def has_one_hand_source(pid):
    """True when ANY layer maintains this provider from its own official source.

    Either a dedicated collector (collect_<pid>.py) or a price-fetching check module
    (scripts/checks/tierN_<pid>.py). A provider maintained one-hand must never be written by
    a third-party republication, no matter how old its `verified_at` is.
    """
    return has_official_collector(pid) or has_official_check(pid)



def verified_recently(pid, now, hours=FRESH_HOURS):
    """True when this provider's `verified_at` is within `hours` of `now`.

    Covers providers that have no dedicated collector module but still carry a fresh
    one-hand verification (e.g. a research/merge pass). Freshness replaces the old exact
    calendar-date equality, which expired at UTC midnight and left a provider verified the
    previous day open to third-party clobbering. A falsy `now` leaves the guard OPEN (and
    this must stay falsy-safe: the router used to pass {"now": None}, silently disabling the
    guard for every provider — the 2026-09-10 bug).
    """
    if not now:
        return False
    pf = os.path.join(PROVIDERS, f"{pid}.json")
    if not os.path.exists(pf):
        return False
    try:
        with open(pf, encoding="utf-8") as fh:
            stamp = str(json.load(fh).get("verified_at", ""))
        if not stamp:
            return False
        t = _parse_iso(stamp)
        ref = _parse_iso(now)
        if t is None or ref is None:
            return False
        return (ref - t).total_seconds() <= hours * 3600
    except Exception:  # noqa: BLE001
        return False


def _parse_iso(v):
    from datetime import datetime, timezone
    try:
        t = datetime.fromisoformat(str(v).strip().replace("Z", "+00:00"))
    except Exception:  # noqa: BLE001
        return None
    return t.replace(tzinfo=timezone.utc) if t.tzinfo is None else t


def collect(ctx):
    """Fetch models.dev catalog, build per-M prices grouped by provider, return structured."""
    now = ctx.get("now") or ""
    data = fetch_json(URL)
    providers = {}
    for pid, pv in (data or {}).items():
        if any(h in pid for h in SUB_PROVIDER_HINTS):
            continue  # subscription-included: per_mtok stays null, never 0
        # First-party priority: never write a provider the repo already checks one-hand
        # (dedicated collector), nor one verified against an official source very recently.
        if has_one_hand_source(pid) or verified_recently(pid, now):
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
