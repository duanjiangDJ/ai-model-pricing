"""Repository-wide audit: consistency checks beyond schema validation.

Checks:
  - VERSION == schema.json#version == index.json#schema_version == meta files
  - index.json counts match actual files (providers/resellers/plans)
  - zero-price models: only allowed where genuinely free (per_mtok 0 + note) — warns otherwise
  - subscription-included providers (coding-plan/token-plan/...) have no 0 prices
  - docs bilingual completeness: every prose doc has en + zh-CN pair
  - version scheme format: year.content.feature (e.g. 26.2.3)
  - broken relative links in markdown docs (generated data/view included)
  - sync-health: an auto_sync manifest source that is stale-but-green (never refreshed)

Usage: python scripts/audit.py  (exit 1 on failures, 0 with warnings ok)
"""
import glob
import json
import os
import re
import sys

from datetime import datetime, timezone  # noqa: E402

from toolbox import any_price_positive, price_all_zero, mixed_currency_zero  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

failures = []
warnings = []


def fail(msg):
    failures.append(msg)
    print("FAIL:", msg)


def warn(msg):
    warnings.append(msg)
    print("WARN:", msg)


# 1. version consistency
try:
    version = open("VERSION", encoding="utf-8").read().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(f"VERSION format invalid: {version}")
    schema_v = json.load(open("data/feed/schema.json", encoding="utf-8"))["version"]
    index_v = json.load(open("data/feed/index.json", encoding="utf-8"))["schema_version"]
    plans_v = json.load(open("data/feed/plans.json", encoding="utf-8"))["schema_version"]
    manifest_v = json.load(open("data/meta/manifest.json", encoding="utf-8"))["schema_version"]
    changelog_v = json.load(open("data/meta/changelog.json", encoding="utf-8"))["schema_version"]
    for name, v in (("schema", schema_v), ("index", index_v), ("plans", plans_v),
                    ("manifest", manifest_v), ("changelog", changelog_v)):
        if v != version:
            fail(f"version mismatch: VERSION={version} vs {name}={v}")
    seg = version.split(".")
    if seg[0] == "0":
        fail("year segment is 0")
    print(f"OK version {version} consistent")
except Exception as e:  # noqa: BLE001
    fail(f"version check error: {e}")

# 2. index counts
idx = json.load(open("data/feed/index.json", encoding="utf-8"))
for lst in (idx.get("providers", []), idx.get("resellers", [])):
    for e in lst:
        f = os.path.join("data/feed", e["file"])
        if not os.path.exists(f):
            fail(f"index references missing file {e['file']}")
            continue
        actual = len(json.load(open(f, encoding="utf-8")).get("models", []))
        if actual != e["model_count"]:
            fail(f"index count mismatch {e['id']}: index={e['model_count']} file={actual}")
plans_count = len(json.load(open("data/feed/plans.json", encoding="utf-8")).get("plans", []))
if plans_count != idx.get("plan_count"):
    fail(f"plan_count mismatch: index={idx.get('plan_count')} plans.json={plans_count}")
# reverse check: every provider file must be referenced in index (providers OR resellers)
indexed_ids = {e["id"] for e in idx.get("providers", [])} | {e["id"] for e in idx.get("resellers", [])}
for pf in sorted(glob.glob("data/feed/providers/*.json")):
    pid = json.load(open(pf, encoding="utf-8")).get("provider_id")
    if pid not in indexed_ids:
        fail(f"provider file {pf} not referenced in index.json (providers/resellers)")
print(f"OK index counts: {idx.get('provider_count')} providers, {idx.get('model_count')} models, {plans_count} plans")

# 3. zero-price policy
SUB_HINTS = ("coding-plan", "token-plan", "copilot", "kimi-for-coding")
zero_free = 0
zero_suspect = 0
bad_status = 0
BILLING_ENUM = ("pay_per_token", "pay_per_image", "subscription_included", "credits", "free", "unknown")
unknown_models = []
no_price_models = []
paid_no_note = []
dual_suspect = []  # models whose cny/usd ratio is uniform inside the FX band (likely rate-derived)
dual_nonuniform = []  # models whose cny/usd ratio varies >4x across fields (one field likely wrong-conversion)
dual_fabricated = []  # models with a per_mtok field where usd literally == cny (a CNY value copied into the USD column on a CNY-only vendor; fabrication)
free_contamination = []  # billing_model declares "free" but per_mtok has a positive price
promo_stale = []  # expired promo whose list_price DIFFERS from per_mtok (discount over but promo price still published)
promo_redundant = []  # expired promo whose list_price already EQUALS per_mtok (stale no-op block)
asym_cny = []  # per_mtok sub-field carrying ONLY a cny value on a USD-declared provider (a secondary/CNY parser injected a field the primary USD source does not publish; mis-parse signature)
for f in sorted(glob.glob("data/feed/providers/*.json")):
    p = json.load(open(f, encoding="utf-8"))
    is_sub = any(h in p["provider_id"] for h in SUB_HINTS)
    for m in p.get("models", []):
        st = m.get("status")
        if st is None:
            # Explicit online/offline is required (PR #169 materialised the implicit default).
            # A missing status must not pass silently: a new catalog entry without one shipped
            # a "—" status into the human pages and the gate stayed green.
            bad_status += 1
            fail(f"missing model status in {p['provider_id']} :: {m['id']} (explicit online/offline required)")
        elif st not in ("online", "offline"):
            bad_status += 1
            fail(f"invalid model status '{st}' in {p['provider_id']} :: {m['id']} (only online/offline allowed)")
        pm = (m.get("pricing") or {}).get("per_mtok") or {}
        # zero-price policy (free): every present currency value is 0
        if price_all_zero(pm):
            if is_sub:
                zero_suspect += 1
                fail(f"zero price in subscription-included provider {p['provider_id']} :: {m['id']}")
            else:
                note = (m.get("notes") or "").lower()
                mid_l = m["id"].lower()
                if mid_l.endswith(":free") or mid_l.endswith("-free") or ":free" in mid_l:
                    zero_free += 1  # id already declares free (OpenRouter-style suffix)
                elif not any(k in note for k in ("free", "免费")):
                    zero_suspect += 1
                    warn(f"zero price without 'free' note: {p['provider_id']} :: {m['id']}")
                else:
                    zero_free += 1
        # context_window sanity: placeholder values (video/image models without token context)
        cw = m.get("context_window")
        if cw and (cw > 10_000_000 or 0 < cw < 100):
            warn(f"suspicious context_window {cw} in {p['provider_id']} :: {m['id']} (check placeholder)")
        # per_mtok magnitude sanity: per_mtok is $ per 1M tokens. A non-zero value
        # below 1e-4 ($0.0001/1M) is impossible for any priced API and is the signature
        # of a per-token value stored as per-1M (the ~1e6x bug that once shipped, e.g.
        # OpenRouter $0.22/M stored as 2.2e-7). That is a data-truth bug -> hard-fail so
        # a bot sync can never merge a per-token-as-per-M value. The [1e-4, 1e-3) band and
        # >1e5 remain suspect-but-not-obviously-misfiled -> warn (borderline cheap/absurd).
        for _pk, _pv in pm.items():
            if not isinstance(_pv, dict):
                continue
            for _cur, _val in _pv.items():
                if _val is None:
                    continue
                _f = float(_val)
                if _f != 0 and abs(_f) < 1e-4:
                    fail(
                        f"per_mtok {_pk}.{_cur}={_val} in {p['provider_id']} :: {m['id']} "
                        f"is $/1M tokens; a non-zero value below 1e-4 is impossible for a "
                        f"priced API (likely per-token stored as per-M, ~1e6 too small)"
                    )
                elif _f != 0 and (abs(_f) < 1e-3 or abs(_f) > 1e5):
                    warn(
                        f"suspicious per_mtok {_pk}.{_cur}={_val} in {p['provider_id']} :: {m['id']} "
                        f"(expected $/1M in [1e-3,1e5]; borderline cheap or absurd)"
                    )
        # promo expiry: `pricing.promo` is a TEMPORARY discount (per_mtok = promo price,
        # promo.list_price = pre-promo price). Once ends_at has passed, per_mtok must have
        # moved to the list price and the promo block is stale metadata. An expired promo
        # that still DIFFERS from list_price publishes a price that no longer exists
        # (data-truth bug) -> fail. An expired promo whose list_price already EQUALS
        # per_mtok is a redundant no-op block (and renders a misleading "🔥 promo" badge)
        # -> warn. Real case 2026-09-10: zai glm-5.3-flash kept promo.list_price == per_mtok
        # after its 2026-09-09 promo ended.
        _promo = (m.get("pricing") or {}).get("promo")
        if isinstance(_promo, dict) and _promo.get("ends_at"):
            try:
                _end = datetime.fromisoformat(str(_promo["ends_at"]).replace("Z", "+00:00"))
                if _end.tzinfo is None:
                    _end = _end.replace(tzinfo=timezone.utc)
                if _end < datetime.now(timezone.utc):
                    _lp = _promo.get("list_price") or {}
                    _ov = [k for k in ("input", "output", "cache_read", "cache_write")
                           if _lp.get(k) is not None and pm.get(k) is not None]
                    if _ov and any(_lp[k] != pm[k] for k in _ov):
                        promo_stale.append(f"{p['provider_id']} :: {m['id']} (expired {str(_promo['ends_at'])[:10]}, per_mtok != list_price)")
                    elif _ov:
                        promo_redundant.append(f"{p['provider_id']} :: {m['id']} (expired {str(_promo['ends_at'])[:10]}, list_price == per_mtok)")
            except ValueError:
                pass
        # cache_read/cache_write zero policy: a zero on a NON-free model is a data-truth bug.
        # Per schema "null = not offered/unknown (never 0)" and docs/price-types.md, 0 is
        # reserved for genuinely-free models (billing_model=free/subscription_included). A
        # non-free model that does not support caching must store null, not 0 (see PR #147
        # gpt-3.5-turbo cache_read 0 -> null; the same class existed across resellers). Hard-fail
        # so a bot sync can never re-introduce a 0-as-not-offered cache field.
        _bm = m.get("billing_model")
        _bm_list = _bm if isinstance(_bm, list) else ([_bm] if _bm else [])
        _is_free_billing = any(_b in ("free", "subscription_included") for _b in _bm_list)
        if not _is_free_billing:
            for _cfield in ("cache_read", "cache_write"):
                _cv = pm.get(_cfield)
                if isinstance(_cv, dict) and _cv.get("usd") == 0:
                    fail(
                        f"{p['provider_id']} :: {m['id']} {_cfield}.usd=0 on a non-free model "
                        f"(0 is reserved for free; use null for not-offered)"
                    )
        # mixed-currency zero: a per_mtok field that is 0 in one currency but >0 in another is
        # self-contradictory (0 = free, yet the other currency proves the model is paid). This is
        # a fabricated zero -- typically a stale usd=0 left on a CNY-only model whose collector
        # only supplies cny (update_model_prices merges per currency and never clears a value, so
        # the bad value survives every 3h sync). Hard-fail so a bot sync can't keep it alive.
        # Real case 2026-09-10: zhipuai glm-4.7-flash {usd:0, cny:0.15}. The correct form is the
        # schema-blessed single-currency entry ({"cny": ...}) or usd=null -- never 0.
        for _mf in mixed_currency_zero(pm):
            fail(
                f"{p['provider_id']} :: {m['id']} per_mtok.{_mf}={pm[_mf]} mixes a 0 and a "
                f"positive value across currencies (a 0 in one currency on a model priced in "
                f"another is a fabricated zero; use null or drop the currency, 0 is for free)"
            )
        # billing_model consistency (required since schema 26.6.x)
        # per_image magnitude sanity: per_image[] prices are USD per SINGLE image
        # (image-gen models), realistically >= ~1e-3 (e.g. $0.004/image). A non-zero
        # value in (0, 1e-4) is almost certainly a per-token image-context price misfiled
        # as per-image — OpenRouter's per-token `image` value (~1e-7) stored as a per-image
        # price. Catch the unit-bug class so it can never silently re-enter (audit only
        # covered per_mtok magnitude for the analogous bug).
        _per_img = (m.get("pricing") or {}).get("per_image")
        if isinstance(_per_img, list):
            for _pt in _per_img:
                _ppr = _pt.get("price") if isinstance(_pt, dict) else None
                if isinstance(_ppr, dict):
                    for _cur2, _val2 in _ppr.items():
                        if _val2 is None:
                            continue
                        _f2 = float(_val2)
                        if _f2 != 0 and abs(_f2) < 1e-4:
                            fail(
                                f"suspicious per_image {_cur2}={_val2} in {p['provider_id']} :: {m['id']} "
                                f"(expected $/image >= 1e-4; likely per-token value stored as per-image)"
                            )
        bm = m.get("billing_model")
        if not bm:
            fail(f"missing billing_model: {p['provider_id']} :: {m['id']}")
            continue
        for b in bm:
            if b not in BILLING_ENUM:
                fail(f"invalid billing_model value '{b}' in {p['provider_id']} :: {m['id']}")
        has_val = any_price_positive(pm)
        if has_val and "pay_per_token" not in bm:
            fail(f"per_mtok has prices but billing_model {bm} lacks pay_per_token: {p['provider_id']} :: {m['id']}")
        if "pay_per_token" in bm and not has_val and not pm.get("per_image"):
            no_price_models.append(f"{p['provider_id']} :: {m['id']}")
        # free-classification contradiction: pay_per_token (published pricing) but
        # all per_mtok prices are zero. Semantically this model is free; if billing_model
        # is pay_per_token the sync writer misclassified a $0 model (see sync_openrouter
        # string-vs-float bug). Catch the class so it can never silently re-enter.
        if "pay_per_token" in bm and price_all_zero(pm):
            warn(f"billing_model=pay_per_token but all per_mtok prices zero (model is free): "
                 + f"{p['provider_id']} :: {m['id']}")
        # free-classification contradiction (reverse): billing_model declares 'free' but
        # per_mtok carries a positive price. A genuine free model has per_mtok=0/null (see
        # zero-price policy); a positive value means the model is actually billed. This
        # catches the "free-model contamination" class (legacy models.dev writer marked
        # any-zero-price models as free, e.g. embedding output=0) so a paid price can
        # never silently sit under a free flag.
        # Only flag a model that claims 'free' WITHOUT also claiming pay_per_token yet
        # carries a paid price (true mislabel). The legitimate multi-method combo
        # ['free','pay_per_token'] (free tier + paid, e.g. Gemini) is NOT contamination.
        if "free" in bm and "pay_per_token" not in bm and has_val:
            free_contamination.append(f"{p['provider_id']} :: {m['id']}")
        if bm == ["unknown"] and (m.get("notes") or ""):
            unknown_models.append(f"{p['provider_id']} :: {m['id']}")
        # provenance: a PAID (positively priced) model must carry a source note (AGENTS.md:
        # check notes/verified_at before trusting a number). update_model_prices only persisted
        # a writer's notes alongside a price CHANGE, so a check that verified an already-correct
        # price could never stamp its source -- 71 opencode/opencode-go models went sourceless
        # (2026-09-11, fixed). Repo-wide this is now 0; the warn keeps the class from regressing.
        if has_val and not (m.get("notes") or "").strip():
            paid_no_note.append(f"{p['provider_id']} :: {m['id']}")
        # dual-currency independence: if cny/usd ratio is IDENTICAL (within 0.5%) across
        # input/output/cache fields AND sits in the plausible FX band (6-8), the cny is almost
        # certainly usd*rate, not an independent official CNY price. Ratios outside the band
        # are independent pricing (only warn on the FX-band subset to avoid noise).
        cny_usd_ratios = []
        for _k in ("input", "output", "cache_read", "cache_write"):
            _pv = pm.get(_k)
            if isinstance(_pv, dict) and _pv.get("usd") and _pv.get("cny"):
                cny_usd_ratios.append(_pv["cny"] / _pv["usd"])
        # fabricatation signature: a single field where usd == cny exactly means the CNY
        # value was copied into the USD column (a CNY-only vendor with no official USD page,
        # e.g. Tencent hunyuan). Detect it per-field so a 1-field dual-price model is caught
        # too, not only via the >=2-field uniform-ratio heuristic. Hard bug class ($13).
        for _fk in ("input", "output", "cache_read", "cache_write"):
            _fpv = pm.get(_fk)
            if isinstance(_fpv, dict) and _fpv.get("usd") is not None and _fpv.get("cny") is not None \
                    and abs(_fpv["usd"] - _fpv["cny"]) < 1e-9:
                dual_fabricated.append(f"{p['provider_id']} :: {m['id']} ({_fk} usd==cny)")
        # asymmetric dual-currency on a USD-declared provider: a per_mtok sub-field that
        # carries ONLY a cny value while sibling fields carry usd means a secondary/CNY
        # parser wrote a field the primary USD source does not publish — a mis-parse
        # signature (real case 2026-09-10: deepseek cache_write.cny held the OFF-PEAK
        # cache-hit price, mapped from a page row that does not exist). Structural signal
        # (not a price heuristic) -> warn for review.
        if p.get("currency") == "USD":
            _sib_usd = any(
                isinstance(pm.get(_sk), dict) and pm.get(_sk).get("usd") is not None
                for _sk in ("input", "output", "cache_read", "cache_write")
            )
            if _sib_usd:
                for _ak in ("input", "output", "cache_read", "cache_write"):
                    _apv = pm.get(_ak)
                    if isinstance(_apv, dict) and _apv.get("cny") is not None and _apv.get("usd") is None:
                        asym_cny.append(f"{p['provider_id']} :: {m['id']} ({_ak} cny-only)")
        if (len(cny_usd_ratios) >= 2 and (max(cny_usd_ratios) / min(cny_usd_ratios)) < 1.005
                and 6.0 <= cny_usd_ratios[0] <= 8.0):
            dual_suspect.append(f"{p['provider_id']} :: {m['id']}")
        # off-band anomaly: uniform ratio far outside the plausible FX band (<4 or >9) is almost
        # certainly a promo/list-price mixup or a CNY unit/base shift (e.g. MiniMax-M3 stored the
        # list CNY next to a promo USD -> ratio ~14). Catch the whole class, not just the in-band set.
        elif (len(cny_usd_ratios) >= 2 and (max(cny_usd_ratios) / min(cny_usd_ratios)) < 1.005
                and (cny_usd_ratios[0] < 4.0 or cny_usd_ratios[0] > 9.0)):
            dual_suspect.append(f"{p['provider_id']} :: {m['id']} (off-band uniform ratio {cny_usd_ratios[0]:.2f})")
        # non-uniform dual-currency: cny/usd rate for the SAME model's fields should be one
        # FX rate (dual-currency is a single rate pair). A large spread (>4x) across fields
        # means one field got a wrong unit/scale conversion (e.g. deepseek-v4-pro cache_read
        # usd stored as 0.003625 when cny 0.30 / 6.8 = 0.044). Hard gate (bug class).
        elif (len(cny_usd_ratios) >= 2 and (max(cny_usd_ratios) / min(cny_usd_ratios)) > 4.0):
            _spread = max(cny_usd_ratios) / min(cny_usd_ratios)
            dual_nonuniform.append(f"{p['provider_id']} :: {m['id']} (non-uniform ratio {_spread:.1f}x)")
        # currency consistency: an item that carries a structured cny price (dual-currency
        # model, schema 26.8) legitimately mentions CNY in notes — never warn on those.
        # Warn only when a USD-declared model mentions CNY but has NO cny price field.
        if p.get("currency") == "USD":
            has_cny_field = any(
                isinstance((pm or {}).get(k), dict) and (pm.get(k) or {}).get("cny") is not None
                for k in ("input", "output", "cache_read")
            )
            note_cn = (m.get("notes") or "")
            if not has_cny_field and ("¥" in note_cn or "Priced in CNY" in note_cn or "CNY/1M" in note_cn) \
                    and "no official USD" not in note_cn:
                warn(f"CNY amount mentioned in USD-declared provider {p['provider_id']} :: {m['id']} (check currency/notes)")
# aggregate unknown warnings per provider (one line per provider, not per model)
if unknown_models:
    from collections import Counter as _C
    by_pid = _C(u.split(" :: ")[0] for u in unknown_models)
    warn(f"billing_model=unknown, needs human review ({len(unknown_models)} models): "
         + ", ".join(f"{pid} x{c}" for pid, c in by_pid.most_common(12)))
if no_price_models:
    from collections import Counter as _C
    by_pid = _C(u.split(" :: ")[0] for u in no_price_models)
    warn(f"billing_model=pay_per_token but per_mtok all null (price not published, {len(no_price_models)} models): "
         + ", ".join(f"{pid} x{c}" for pid, c in by_pid.most_common(12)))
if paid_no_note:
    from collections import Counter as _Cpn
    by_pid = _Cpn(u.split(" :: ")[0] for u in paid_no_note)
    warn(f"paid model with no provenance note (source/traceability gap; {len(paid_no_note)} models): "
         + ", ".join(f"{pid} x{c}" for pid, c in by_pid.most_common(12)))
if dual_suspect:
    from collections import Counter as _Cd
    by_pid = _Cd(u.split(" :: ")[0] for u in dual_suspect)
    warn(f"cny/usd ratio uniform in FX band (looks exchange-rate-derived, non-independent; {len(dual_suspect)} models): "
         + ", ".join(f"{pid} x{c}" for pid, c in by_pid.most_common(12)))
if dual_nonuniform:
    from collections import Counter as _Cnd
    by_pid = _Cnd(u.split(" :: ")[0] for u in dual_nonuniform)
    fail(f"non-uniform dual-currency (one field cny/usd ratio >4x siblings; likely wrong unit conversion; {len(dual_nonuniform)} models): "
         + ", ".join(f"{pid} x{c}" for pid, c in by_pid.most_common(12)))
if dual_fabricated:
    from collections import Counter as _Cfab
    by_pid = _Cfab(u.split(" :: ")[0] for u in dual_fabricated)
    fail(f"usd==cny (a CNY value copied into the USD column on a CNY-only vendor; fabricated USD; {len(dual_fabricated)} fields): "
         + ", ".join(f"{pid} x{c}" for pid, c in by_pid.most_common(12)))
if asym_cny:
    from collections import Counter as _Cac
    _by_pid = _Cac(u.split(" :: ")[0] for u in asym_cny)
    warn(f"cny-only per_mtok field on USD-declared provider (secondary/CNY parser injected a field the USD source lacks; check for mis-parse; {len(asym_cny)} models): "
         + ", ".join(f"{pid} x{c}" for pid, c in _by_pid.most_common(12)))
if free_contamination:
    from collections import Counter as _Cf
    by_pid = _Cf(u.split(" :: ")[0] for u in free_contamination)
    warn(f"billing_model declares 'free' but per_mtok has a positive price (free-model contamination; {len(free_contamination)} models): "
         + ", ".join(f"{pid} x{c}" for pid, c in by_pid.most_common(12)))
if promo_stale:
    from collections import Counter as _Cps
    _bps = _Cps(u.split(" :: ")[0] for u in promo_stale)
    fail(f"expired promo with per_mtok != list_price (discount ended but the promo price is still published; {len(promo_stale)} models): "
         + ", ".join(f"{pid} x{c}" for pid, c in _bps.most_common(12)))
if promo_redundant:
    from collections import Counter as _Cpr
    _bpr = _Cpr(u.split(" :: ")[0] for u in promo_redundant)
    warn(f"expired promo block with list_price == per_mtok (stale no-op; remove the promo; {len(promo_redundant)} models): "
         + ", ".join(f"{pid} x{c}" for pid, c in _bpr.most_common(12)))
print(f"OK zero-price: {zero_free} free-flagged, {zero_suspect} suspect")

# 4. docs bilingual completeness (AGENTS + agent-policy are English-only by design)
EN_ONLY_DOCS = {"AGENTS.md", "agent-policy.md", "agent-governance-design.md"}
prose_docs = ["README.md", "FORMAT.md", "CHANGELOG.md", "CONTRIBUTING.md"] + \
    [os.path.relpath(f, ROOT).replace("\\", "/") for f in glob.glob("docs/*.md") if "ego" not in f]
for d in prose_docs:
    if d.endswith(".zh-CN.md") or d.endswith(".en.md"):
        continue
    if os.path.basename(d) in EN_ONLY_DOCS:
        continue  # kept English-only by design; no zh-CN required
    zh = d[:-3] + ".zh-CN.md"
    if not os.path.exists(zh):
        warn(f"missing zh-CN version for {d}")
print(f"OK docs: {len(prose_docs)} prose docs checked")

# 5. api_base_url completeness + dedup check
by_url = {}
for f in sorted(glob.glob("data/feed/providers/*.json")):
    p = json.load(open(f, encoding="utf-8"))
    pid = p["provider_id"]
    if "api_base_url" not in p:
        fail(f"provider {pid} missing api_base_url field")
        continue
    url = p.get("api_base_url")
    if url is None:
        if p.get("channel") != "subscription":
            warn(f"provider {pid} has api_base_url=null but channel={p.get('channel')} (expected subscription)")
        continue
    # normalize template placeholders for grouping
    norm = url.replace("{region}", "*").replace("{resource}", "*").replace("${ACCOUNT_ID}", "*")
    by_url.setdefault(norm, []).append(pid)
for url, pids in by_url.items():
    if len(pids) < 2:
        continue
    # check model-id overlap between same-base-url providers (dedup requirement)
    sets = {}
    for pid in pids:
        p = json.load(open(f"data/feed/providers/{pid}.json", encoding="utf-8"))
        sets[pid] = {m["id"].lower() for m in p.get("models", [])}
    for i, a in enumerate(pids):
        for b in pids[i + 1:]:
            common = sets[a] & sets[b]
            if common:
                fail(f"duplicate models between same api_base_url ({url}): {a} ∩ {b} = {len(common)} (e.g. {sorted(common)[:3]}); merge them")
print(f"OK api_base_url: {len(by_url)} distinct endpoints, dup-groups checked")

# 6. broken relative links in markdown docs
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
md_files = [os.path.relpath(f, ROOT).replace("\\", "/")
            for f in glob.glob("*.md") + glob.glob("docs/*.md") +
            glob.glob("data/view/**/*.md", recursive=True)]
broken_links = 0
for f in sorted(md_files):
    txt = open(f, encoding="utf-8", errors="ignore").read()
    for m in LINK_RE.finditer(txt):
        target = m.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#")[0].strip()
        if not target:
            continue
        p = os.path.normpath(os.path.join(os.path.dirname(f), target))
        if not os.path.exists(p):
            broken_links += 1
            fail(f"broken relative link in {f}: [{m.group(1)}] (resolves to {p})")
print(f"OK links: {len(md_files)} markdown files checked, {broken_links} broken")

# 7. sync-health: an auto_sync manifest source that is stale-but-green (silently frozen)
# The manifest's `sources[]` is SYNC HEALTH. A source with auto_sync:true and NO last_error
# looks healthy, but if its last_ok is null/old it is silently dead -- the exact
# "stale-but-green" class this repo guards against (models.dev sat frozen for 3 weeks; the
# legacy sync_official `official` entries froze at 2026-08-21 when that layer was dropped
# from the daily pipeline and superseded by scripts/checks/). A source that is genuinely
# failing shows it via last_error, so we only flag the no-error case.
STALE_SOURCE_DAYS = 7
stale_sources = []
try:
    _mf = json.load(open("data/meta/manifest.json", encoding="utf-8"))
    _now_src = datetime.now(timezone.utc)
    for s in _mf.get("sources", []):
        if not s.get("auto_sync") or s.get("last_error"):
            continue
        _lo = s.get("last_ok")
        if not _lo:
            stale_sources.append(f"{s.get('name')} (never ran)")
            continue
        try:
            _dt = datetime.fromisoformat(str(_lo).replace("Z", "+00:00"))
        except Exception:  # noqa: BLE001
            stale_sources.append(f"{s.get('name')} (unparseable last_ok={_lo!r})")
            continue
        _age = (_now_src - _dt).days
        if _age > STALE_SOURCE_DAYS:
            stale_sources.append(f"{s.get('name')} ({_age}d)")
except Exception as e:  # noqa: BLE001
    fail(f"sync-health check error: {e}")
if stale_sources:
    warn(f"auto_sync source stale-but-green (auto_sync:true, no last_error, last_ok old/null -- a frozen sync-health entry; {len(stale_sources)}): "
         + ", ".join(stale_sources))
else:
    print(f"OK sync-health: all auto_sync sources fresh (<{STALE_SOURCE_DAYS}d)")

# 8. price oscillation across syncs (the OpenRouter `overrides` class)
# A model whose stored per_mtok.input.usd alternates A -> B -> A -> B across consecutive syncs
# is NOT a price move -- it is a time-of-day / override price that a writer stored as ONE
# scalar. OpenRouter exposes time windows in `pricing.overrides`, which sync_openrouter ignores,
# so its aggregator rows flip between tiers depending on the run's UTC hour. Real cases
# (2026-09-12): tencent/hy3 0.0825<->0.132, nvidia/nemotron-3-ultra-550b-a55b 0.6<->0.625,
# minimax/minimax-m1 0.4<->0.55, minimax/minimax-m2.5 0.27<->0.3. WARN (not FAIL): both values
# are real, but the scalar representation loses the peak/off-peak (or promo/list) distinction
# and the price churns forever. The root fix is in the writer (needs sign-off), not the value.
_osc = []
try:
    _cl = json.load(open("data/meta/changelog.json", encoding="utf-8"))
    _seq = {}
    for _e in reversed(_cl.get("entries", [])):  # oldest -> newest
        _iid = _e.get("item_id")
        _new = _e.get("new")
        if not isinstance(_iid, str) or not isinstance(_new, dict):
            continue
        _pm = _new.get("per_mtok")
        _in = _pm.get("input") if isinstance(_pm, dict) else None
        _v = _in.get("usd") if isinstance(_in, dict) else None
        if isinstance(_v, (int, float)) and not isinstance(_v, bool):
            _seq.setdefault((_e.get("provider_id"), _iid), []).append(round(float(_v), 12))
    for (_pid, _iid), _vals in _seq.items():
        _t = _vals[-10:]
        _c = [_t[0]]
        for _x in _t[1:]:
            if _x != _c[-1]:
                _c.append(_x)
        if len(_c) >= 4 and len(set(_c)) == 2 and all(_c[_i] != _c[_i + 1] for _i in range(len(_c) - 1)):
            _osc.append(f"{_pid}:{_iid} ({_c[0]}/{_c[1]}, {len(_c) - 1} flips)")
except Exception as e:  # noqa: BLE001
    fail(f"price-oscillation check error: {e}")
if _osc:
    warn(f"per_mtok alternates between two values across syncs (a time-of-day/override price stored as one scalar; {len(_osc)} models): "
         + ", ".join(sorted(_osc)[:12]))
else:
    print("OK oscillation: no model alternates between two prices across syncs")

if failures:
    print(f"\nAUDIT FAILED: {len(failures)} failures, {len(warnings)} warnings")
    sys.exit(1)
print(f"\nAUDIT PASSED ({len(warnings)} warnings)")
