"""Repository-wide audit: consistency checks beyond schema validation.

Checks:
  - VERSION == schema.json#version == index.json#schema_version == meta files
  - index.json counts match actual files (providers/resellers/plans)
  - zero-price models: only allowed where genuinely free (per_mtok 0 + note) — warns otherwise
  - subscription-included providers (coding-plan/token-plan/...) have no 0 prices
  - docs bilingual completeness: every prose doc has en + zh-CN pair
  - version scheme format: year.content.feature (e.g. 26.2.3)
  - broken relative links in markdown docs (generated data/view included)

Usage: python scripts/audit.py  (exit 1 on failures, 0 with warnings ok)
"""
import glob
import json
import os
import re
import sys

from toolbox import any_price_positive, price_all_zero  # noqa: E402

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
dual_suspect = []  # models whose cny/usd ratio is uniform inside the FX band (likely rate-derived)
free_contamination = []  # billing_model declares "free" but per_mtok has a positive price
for f in sorted(glob.glob("data/feed/providers/*.json")):
    p = json.load(open(f, encoding="utf-8"))
    is_sub = any(h in p["provider_id"] for h in SUB_HINTS)
    for m in p.get("models", []):
        st = m.get("status")
        if st is not None and st not in ("online", "offline"):
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
        # dual-currency independence: if cny/usd ratio is IDENTICAL (within 0.5%) across
        # input/output/cache fields AND sits in the plausible FX band (6-8), the cny is almost
        # certainly usd*rate, not an independent official CNY price. Ratios outside the band
        # are independent pricing (only warn on the FX-band subset to avoid noise).
        cny_usd_ratios = []
        for _k in ("input", "output", "cache_read", "cache_write"):
            _pv = pm.get(_k)
            if isinstance(_pv, dict) and _pv.get("usd") and _pv.get("cny"):
                cny_usd_ratios.append(_pv["cny"] / _pv["usd"])
        if (len(cny_usd_ratios) >= 2 and (max(cny_usd_ratios) / min(cny_usd_ratios)) < 1.005
                and 6.0 <= cny_usd_ratios[0] <= 8.0):
            dual_suspect.append(f"{p['provider_id']} :: {m['id']}")
        # off-band anomaly: uniform ratio far outside the plausible FX band (<4 or >9) is almost
        # certainly a promo/list-price mixup or a CNY unit/base shift (e.g. MiniMax-M3 stored the
        # list CNY next to a promo USD -> ratio ~14). Catch the whole class, not just the in-band set.
        elif (len(cny_usd_ratios) >= 2 and (max(cny_usd_ratios) / min(cny_usd_ratios)) < 1.005
                and (cny_usd_ratios[0] < 4.0 or cny_usd_ratios[0] > 9.0)):
            dual_suspect.append(f"{p['provider_id']} :: {m['id']} (off-band uniform ratio {cny_usd_ratios[0]:.2f})")
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
if dual_suspect:
    from collections import Counter as _Cd
    by_pid = _Cd(u.split(" :: ")[0] for u in dual_suspect)
    warn(f"cny/usd ratio uniform in FX band (looks exchange-rate-derived, non-independent; {len(dual_suspect)} models): "
         + ", ".join(f"{pid} x{c}" for pid, c in by_pid.most_common(12)))
if free_contamination:
    from collections import Counter as _Cf
    by_pid = _Cf(u.split(" :: ")[0] for u in free_contamination)
    warn(f"billing_model declares 'free' but per_mtok has a positive price (free-model contamination; {len(free_contamination)} models): "
         + ", ".join(f"{pid} x{c}" for pid, c in by_pid.most_common(12)))
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

if failures:
    print(f"\nAUDIT FAILED: {len(failures)} failures, {len(warnings)} warnings")
    sys.exit(1)
print(f"\nAUDIT PASSED ({len(warnings)} warnings)")
