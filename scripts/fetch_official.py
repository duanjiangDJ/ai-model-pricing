#!/usr/bin/env python3
"""Fetch OFFICIAL pricing for a model/provider from registered sources.

This is the programmatic "verify against the official source" workflow the agent runs
(policy §15.2). If a price looks suspicious, run:

    python scripts/fetch_official.py <model_id_or_provider> [--json]

and it queries every registered OFFICIAL source and prints that model's official
per_mtok pricing + source URL + a free/rate-derived hint — so the agent gets grounded
official numbers without hand-scraping a page each time.

EVOLVABLE: to add a source, write a `fetch_<name>()` generator and register it in
`SOURCES`. Each fetcher yields dicts:
    {source, model_id, per_mtok, source_url, verified_at, note}

Tech knowledge is FIXED AS CODE here (not re-judged by the LLM each time):
- OpenRouter API returns PER-TOKEN prices; per_mtok is $/1M -> multiply by 1e6.
- models.dev marks free models with a "~" prefix on the model id (pricing=None).
- A uniform cny/usd ratio inside the FX band (6-8) implies exchange-rate-derived USD.
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone

UA = {"User-Agent": "ai-model-pricing-fetch-official"}


def _get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())


def _to_per_m(v):
    """OpenRouter API pricing is PER TOKEN; per_mtok is $ per 1M tokens -> x1e6."""
    if v is None:
        return None
    return round(float(v) * 1e6, 8)


def fetch_openrouter():
    """OpenRouter official API: /api/v1/models returns every model's pricing."""
    data = _get("https://openrouter.ai/api/v1/models")
    for m in data["data"]:
        p = m.get("pricing") or {}
        yield {
            "source": "openrouter",
            "model_id": m.get("id"),
            "per_mtok": {
                "input": _to_per_m(p.get("prompt")),
                "output": _to_per_m(p.get("completion")),
                "cache_read": _to_per_m(p.get("input_cache_read")),
            },
            "source_url": f"https://openrouter.ai/models/{m.get('id')}",
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "note": "OpenRouter API pricing (per-token x1e6 = per-1M)",
        }


def fetch_modelsdev():
    """models.dev official API: api.json grouped by provider id."""
    data = _get("https://models.dev/api.json")
    for prov_id, prov in data.items():
        models = (prov.get("models") or {}) if isinstance(prov, dict) else {}
        items = models.items() if isinstance(models, dict) else []
        for mid, m in items:
            # models.dev marks FREE models with a "~" prefix on the id (pricing None).
            free_hint = "~" in (mid or "") or (m.get("pricing") is None)
            yield {
                "source": f"models.dev/{prov_id}",
                "model_id": mid,
                "per_mtok": m.get("pricing"),  # models.dev lists per-1M pricing
                "source_url": f"https://models.dev/{prov_id}/{mid.replace('/', '-')}",
                "verified_at": datetime.now(timezone.utc).isoformat(),
                "note": ("models.dev marks free; ~ prefix = free, pricing None" if free_hint
                         else "models.dev official pricing"),
            }


SOURCES = {
    "openrouter": fetch_openrouter,
    "models.dev": fetch_modelsdev,
    # Add more official sources here to evolve the workflow, e.g.:
    # "deepseek": fetch_deepseek_official, "zai": fetch_zai_official, ...
}


def main(argv):
    want = argv[1] if len(argv) > 1 else None
    as_json = "--json" in argv
    if not want:
        print("usage: fetch_official.py <model_id|provider> [--json]")
        print("sources:", ", ".join(SOURCES))
        return 2

    want_l = want.lower()
    hits = []
    for src_name, fn in SOURCES.items():
        try:
            for rec in fn():
                mid = (rec.get("model_id") or "").lower()
                if want_l in mid or want_l in rec["source"].lower():
                    hits.append(rec)
        except Exception as e:  # noqa: BLE001
            hits.append({"source": src_name, "error": str(e), "model_id": None})
    if not hits:
        print(f"no official data for '{want}' in sources: {', '.join(SOURCES)}")
        return 1
    if as_json:
        print(json.dumps(hits, ensure_ascii=False, indent=2))
        return 0
    for rec in hits:
        if rec.get("error"):
            print(f"[{rec['source']}] ERROR: {rec['error']}")
            continue
        print(f"[{rec['source']}] {rec['model_id']}")
        print(f"  per_mtok: {json.dumps(rec.get('per_mtok'), ensure_ascii=False)}")
        print(f"  source:   {rec.get('source_url')}")
        print(f"  verified: {rec.get('verified_at')}")
        print(f"  note:     {rec.get('note')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
