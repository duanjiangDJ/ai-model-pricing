"""Fetch OpenRouter model catalog (aggregator prices) into data/feed/providers/openrouter.json.

OpenRouter pricing fields (USD, string decimals):
  prompt, completion, image, request, web_search, input_cache_read, input_cache_write, internal_reasoning
All prices are RESELLER prices (aggregator channel), kept separate from first-party prices.

Usage: python scripts/sync_openrouter.py [--write]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from common import (  # noqa: E402
    PROVIDERS, FEED, SCHEMA_VERSION, append_changelog, fetch_json, load_index,
    load_manifest, load_provider, now_iso, save_index, save_manifest, to_float_or_none, write_json,
)

def _apply_bidir_guard(cur_new, cur_old, label, surge=5.0):
    """Bidirectional surge guard: keep the OLD value if the new one jumps >surge or <1/surge.

    Guards against a stale/wrong source value clobbering a verified price (sync-source
    tug-of-war). Returns the (possibly guarded) cur_new dict. Values that look like a
    parse/unit error (>5x or <1/5x jump) are kept as the old value.
    """
    if not isinstance(cur_new, dict):
        return cur_new
    for currency, nv in list(cur_new.items()):
        if nv is None:
            continue
        ov = (cur_old or {}).get(currency)
        if ov and nv and (nv / ov > surge or nv / ov < (1.0 / surge)):
            print(f"  GUARD-SKIP {label}.{currency}: {ov} -> {nv} (tug-of-war surge); keeping {ov}")
            cur_new[currency] = ov
    return cur_new


OPENROUTER_URL = "https://openrouter.ai/api/v1/models"


def map_modalities(m):
    out = []
    for im in (m or []):
        if im == "text":
            out.append("text")
        elif im in ("image", "audio", "video"):
            out.append(f"{im}_in")
    return out


def _u(v):
    """Wrap a numeric price into a dual-currency object (usd key); None stays None."""
    return {"usd": v} if v is not None else None


def _per_m(v):
    """OpenRouter API pricing is PER TOKEN (USD decimals). per_mtok semantics is
    per-1M tokens, so multiply per-token by 1e6. Missing this conversion made every
    OpenRouter price land 1e6x too small (e.g. $0.22/M stored as 2.2e-7)."""
    if v is None:
        return None
    return round(v * 1e6, 8)


def _raw(v):
    """Parse a raw OpenRouter price WITHOUT the negative->None filter.

    OpenRouter uses -1 as the sentinel for "no fixed published price" (dynamic routing:
    the request is forwarded to another model and billed at THAT model's rate). The sign
    must survive here so build_model() can tell a dynamic router apart from a genuinely
    free model (whose price is the string "0")."""
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def build_model(entry):
    p = entry.get("pricing") or {}
    # Normalize to float first. OpenRouter returns prices as STRING decimals (e.g. "0"),
    # and per_mtok semantics is $/1M. Comparing raw strings vs int 0 ("0" != 0 is True)
    # misclassified $0 models as payable, so a genuinely free model (all-zero price) got
    # billing_model=["pay_per_token"] with a zero price and no free note — self-contradiction.
    prompt = to_float_or_none(p.get("prompt"))
    completion = to_float_or_none(p.get("completion"))
    cache_read = to_float_or_none(p.get("input_cache_read"))
    cache_write = to_float_or_none(p.get("input_cache_write"))
    token_vals = [prompt, completion, cache_read, cache_write]
    # OpenRouter's `image` pricing field is a PER-TOKEN price for image-token context
    # (it equals the per-token `prompt` on every gemini model, e.g. 0.0000003), NOT a
    # per-image price. Image is billed per-token and is already covered by per_mtok.input,
    # so it must NOT be mapped to pricing.per_image (that field means USD per single image).
    # Mapping it as-is misfiled per-token values ~1e-7 as a per-image price (unit bug).
    # If OpenRouter ever exposes a genuine per-image price (image != prompt), add it back
    # with proper per-image semantics (no ×1e6) and billing_model pay_per_image.
    # The -1 sentinel: to_float_or_none() drops negatives to None, so without the raw
    # check below an all-None price set fell through `all(v == 0 ...)` (which is True on an
    # emptied iterable) and the model was labelled "free" with a "per_mtok = 0" note --
    # a false free price published for 5 dynamic routers (openrouter/auto, auto-beta,
    # bodybuilder, fusion, pareto-code; 2026-09-12). A genuine free model carries the
    # explicit string "0", never an absent price set.
    raw_vals = [_raw(p.get("prompt")), _raw(p.get("completion")),
                _raw(p.get("input_cache_read")), _raw(p.get("input_cache_write"))]
    is_dynamic = any(v is not None and v < 0 for v in raw_vals)
    has_token_price = any(v is not None and v > 0 for v in raw_vals)
    all_present_zero = any(v is not None for v in raw_vals) and all(
        v == 0 for v in raw_vals if v is not None)
    if is_dynamic:
        billing = ["unknown"]
    elif has_token_price:
        billing = ["pay_per_token"]
    elif entry["id"].lower().endswith(":free") or all_present_zero:
        billing = ["free"]
    else:
        billing = ["unknown"]
    arch = entry.get("architecture") or {}
    tp = entry.get("top_provider")
    if isinstance(tp, dict):
        tp = tp.get("id") or tp.get("provider_id") or tp.get("name")
    note = f"OpenRouter reseller price; top provider: {tp}" if tp else "OpenRouter reseller price"
    if billing == ["free"]:
        note += " | Free model (per_mtok = 0)."
    elif is_dynamic:
        note += (" | Dynamic routing price: billed at the selected model's rate "
                 "(no fixed per-token price; OpenRouter sentinel -1).")
    pricing = {
        "per_mtok": {
            "input": _u(_per_m(prompt)),
            "output": _u(_per_m(completion)),
            "cache_read": _u(_per_m(cache_read)),
            "cache_write": _u(_per_m(cache_write)),
        },
        "per_image": None,  # OpenRouter exposes no per-image price (image is per-token)
        "promo": None,
    }
    return {
        "id": entry["id"],
        "name": entry.get("name", entry["id"]),
        "category": "reasoning" if entry.get("reasoning") else "chat",
        "modalities": map_modalities(arch.get("input_modalities")),
        "context_window": entry.get("context_length") or None,
        "max_output": None,
        "billing_model": billing,
        "pricing": pricing,
        "notes": note,
    }


def preserve_local_status(local_models, remote_models):
    """Carry a locally-assigned `status` onto a rewritten catalog entry.

    OpenRouter's catalog has no notion of "offline" and build_model() never emits a
    `status`. daily_check() wholesale-replaces openrouter.json's model list, so a model
    locally marked offline (retired/superseded, reason in notes) would be silently
    resurrected — its status dropped — on the next catalog change. Preserve it by id.
    """
    prev = {m["id"]: m["status"] for m in local_models if m.get("status")}
    n = 0
    for m in remote_models:
        st = prev.get(m["id"])
        if st and m.get("status") != st:
            m["status"] = st
            n += 1
    return n


def default_catalog_status(models):
    """Give a newly discovered live catalog entry an explicit `status`.

    build_model() emits no status and preserve_local_status() only carries one over for an
    EXISTING id, so a brand-new OpenRouter catalog entry used to be persisted with no status
    at all — regressing PR #169's explicit-status invariant (and, once audit hard-fails a
    missing status, failing the gate). A model present in the live catalog is online.
    """
    n = 0
    for m in models:
        if not m.get("status"):
            m["status"] = "online"
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="persist files (default: dry-run to stdout)")
    args = ap.parse_args()

    data = fetch_json(OPENROUTER_URL)
    models = [build_model(m) for m in data["data"]]
    models.sort(key=lambda m: m["id"])

    now = now_iso()
    provider = {
        "provider_id": "openrouter",
        "name": "OpenRouter",
        "channel": "aggregator",
        "category": "aggregator",
        "region": "global",
        "homepage": "https://openrouter.ai",
        "pricing_page": "https://openrouter.ai/models",
        "api_base_url": "https://openrouter.ai/api/v1",
        "currency": "USD",
        "updated_at": now,
        "verified_at": now,
        "models": models,
    }

    if not args.write:
        print(f"OpenRouter: {len(models)} models, dry-run only (use --write to persist)")
        return

    # Bidirectional surge guard (see §15.1 regression / sync-source tug-of-war): a stale or
    # wrong source value must not clobber a verified price on main. For each model field,
    # if the new value jumps >5x or <1/5x vs the currently-stored value, keep the old value.
    try:
        _prev = load_provider("openrouter") or {}
        _pmodels = {m["id"]: m for m in (_prev.get("models") or [])}
    except Exception:
        _pmodels = {}

    for m in provider.get("models", []):
        pm = m.get("pricing", {}).get("per_mtok") or {}
        old = (_pmodels.get(m["id"]) or {}).get("pricing", {}).get("per_mtok") or {}
        for _k in ("input", "output", "cache_read", "cache_write"):
            if _k in pm and isinstance(pm[_k], dict):
                _apply_bidir_guard(pm[_k], old.get(_k), f"{m['id']}.{_k}")

    write_json(os.path.join(PROVIDERS, "openrouter.json"), provider)

    # update index.json
    index = load_index() or {
        "schema_version": SCHEMA_VERSION,
        "generated_at": now,
        "currency": "USD",
        "provider_count": 0,
        "model_count": 0,
        "plan_count": 0,
        "providers": [],
        "resellers": [],
    }
    for lst in (index["providers"], index["resellers"]):
        lst[:] = [e for e in lst if e["id"] != "openrouter"]
    index["resellers"].append({
        "id": "openrouter",
        "name": "OpenRouter",
        "channel": "aggregator",
        "model_count": len(models),
        "file": "providers/openrouter.json",
        "updated_at": now,
    })
    index["generated_at"] = now
    index["provider_count"] = len(index["providers"])
    index["model_count"] = sum(e["model_count"] for e in index["providers"]) + sum(
        e["model_count"] for e in index["resellers"]
    )
    save_index(index)

    # update manifest
    manifest = load_manifest() or {"schema_version": SCHEMA_VERSION, "sources": [], "coverage": {}}
    srcs = [s for s in manifest.get("sources", []) if s["name"] != "OpenRouter API"]
    srcs.append({"name": "OpenRouter API", "url": OPENROUTER_URL, "auto_sync": True, "last_ok": now, "last_error": None})
    manifest["sources"] = srcs
    manifest["last_daily_check"] = now
    save_manifest(manifest)

    append_changelog([{
        "date": now,
        "kind": "update",
        "scope": "provider",
        "provider_id": "openrouter",
        "item_id": "openrouter",
        "field": "catalog",
        "new": {"model_count": len(models)},
        "source": OPENROUTER_URL,
    }])
    print(f"OpenRouter: {len(models)} models written.")


if __name__ == "__main__":
    main()
