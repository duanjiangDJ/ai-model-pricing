"""toolbox.py — shared utility library for all scripts.

Central place for HTTP fetching, JSON I/O, changelog helpers, dedup helpers,
language detection, and version helpers. New scripts should import from here;
old scripts import `common` which re-exports this module for compatibility.
"""
import json
import os
import re
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(ROOT, "data", "feed")
PROVIDERS = os.path.join(FEED, "providers")
VIEW = os.path.join(ROOT, "data", "view")
META = os.path.join(ROOT, "data", "meta")

SCHEMA_VERSION = "26.0.1"
UA = "ai-model-pricing-bot/1.0 (+https://github.com/duanjiangDJ/ai-model-pricing)"

_HAN_RE = re.compile(r"[\u4e00-\u9fff]")


# ---------------------------------------------------------------- model category
# Unambiguous id markers -> the model `category` they MUST carry. Deliberately narrow: only
# markers that cannot describe a chat model. Shared by the aggregator writers (to infer a new
# model's category) AND audit.py (to catch a regression), so the writer's inference and the
# check can never drift apart. First matching marker wins (an id can carry several, e.g.
# "synthetic-video-detector" matches both "video" and "detector").
CATEGORY_SIGNATURES = (
    (re.compile(r"detector|classifier|moderation|content-safety|guard"), "moderation"),
    # Image generators. The `image` marker covers the Google/OpenAI/Alibaba/xAI/Meta image
    # families (gemini-*-image, gpt-image, chatgpt-image, qwen-image, wan*-image,
    # grok-imagine-image, muse-image); `imagen` covers Google Imagen. It sits BEFORE the video
    # rule so `wan2.7-image` stays image_gen while `wan-v2.6-t2v` becomes video_gen.
    (re.compile(r"imagen|gpt-image|qwen-image|[-_.]image([-_.]|$)"), "image_gen"),
    # Video generators: the generic "video" marker PLUS the generator families whose ids carry
    # no literal "video" (Google Veo, OpenAI Sora, Kuaishou Kling, ByteDance Seedance, Runway,
    # Luma Ray, MiniMax Hailuo, Alibaba wan/wanx) and the t2v/i2v/r2v task suffixes. Without
    # these the writers re-defaulted every one of these rows to "chat"/"reasoning". `kling` and
    # `wan` carry an id boundary because `thinkingmachines/Inkling` is an ordinary chat model.
    (re.compile(r"video|veo|sora|seedance|runway|hailuo|lumalabs|ray-?2($|[/_.-])|t2v|i2v|r2v|gemini-omni|"
                r"(^|[/_.-])kling|(^|[/_.-])wan"), "video_gen"),
    # Speech-to-text: `whisper`/`transcribe` plus the `asr` family marker (Alibaba
    # `qwen3-asr-flash`, StepFun `stepaudio-2.5-asr`) -- both were classified "chat" because
    # the table only knew the two literal words. Boundary-anchored so a random substring
    # cannot match.
    (re.compile(r"whisper|transcribe|(^|[/_.-])asr([/_.-]|$)"), "audio_stt"),
    # Text-to-speech: the `tts` marker, the spelled-out phrase, and the `text-to-audio` variant
    # (`fal-ai/stable-audio-25/text-to-audio`). `fish-audio/*` is the Fish Audio TTS/voice-
    # cloning family (`s1`, `s2-pro`, `s2.1-pro`); it sits AFTER the stt rule on purpose so
    # `fish-audio/transcribe-1` keeps matching `transcribe` -> audio_stt.
    (re.compile(r"(^|[/_.-])tts([/_.-]|$)|-tts$|tts-|text-to-speech|text-to-audio|fish-audio"),
     "audio_tts"),
    # Music generation: Google's Lyria family and ElevenLabs Music emit AUDIO TRACKS, not
    # speech -- they were published as `chat`/`audio_tts` because the table carried no music
    # marker at all, leaving the schema's `music_gen` category with ZERO rows (real 2026-09-14,
    # found by the §15.1 "dead category" sweep). `music` is boundary-anchored so an unrelated
    # suffix (`gemma-4-...-musica`) or `studiovoice` cannot match.
    (re.compile(r"lyria|(^|[/_.-])music([/_.-]|$)"), "music_gen"),
    (re.compile(r"rerank|re-rank"), "rerank"),
    (re.compile(r"embed|bge|e5-|e5_|gte-|gte_|mpnet|minilm|mini-lm|mini_lm"), "embedding"),
    # `stable-?diffusion` is hyphen-OPTIONAL: poe spells SDXL `stablediffusionxl`, which the
    # literal `stable-diffusion` marker missed. `nano-?banana` is the published alias of
    # Google's Gemini image family (poe lists `google/nano-banana[-pro]`).
    (re.compile(r"stable-?diffusion|sdxl|flux|imagen|nano-?banana"), "image_gen"),
)


def category_signature_hint(mid):
    """Return the `category` an unambiguous model-id marker implies, else None.

    Used by the aggregator writers to classify a NEW model and by audit.py to flag a row
    whose category contradicts its own id (the class the writers used to default to
    "chat" for every non-reasoning model: whisper/TTS/flux/embedding rows published as
    chat; real 2026-09-13: 105 rows across 31 providers).
    """
    low = (mid or "").lower()
    for pat, want in CATEGORY_SIGNATURES:
        if pat.search(low):
            return want
    return None


# ---------------------------------------------------------------- time & json

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(path, data, indent=2):
    """Atomic write: dump to a temp file then os.replace, so a failing dump (e.g. a
    non-serializable value mid-serialize) cannot leave a truncated/corrupt data file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
        f.write("\n")
    os.replace(tmp, path)


# ---------------------------------------------------------------- network

def http_get(url, timeout=60, headers=None):
    """Fetch a URL and return raw bytes. Raises on HTTP errors."""
    h = {"User-Agent": UA, "Accept": "text/html,*/*"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_json(url, timeout=60):
    return json.loads(http_get(url, timeout=timeout).decode("utf-8", "ignore"))


def to_text(raw):
    """Decode raw bytes with encoding fallbacks (utf-8 -> gb18030)."""
    for enc in ("utf-8", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "ignore")


def default_chrome():
    """Locate the locally-installed Chrome for Testing (headless browser) binary."""
    import glob as _g
    candidates = _g.glob(os.path.expanduser("~/.cache/puppeteer-chrome/chrome/*/chrome-linux64/chrome"))
    return candidates[0] if candidates else None


def js_fetch(url, timeout=60, virtual_time=10000, chrome=None):
    """Fetch a JS-rendered page using headless Chrome (dump-dom + virtual-time budget).

    Returns the rendered HTML as text. Returns '' if Chrome is unavailable or the fetch
    fails. Use this for vendor pricing pages that are client-side rendered (curl/urllib
    only get the empty shell, e.g. open.bigmodel.cn/pricing). Chrome path is taken from
    CHROME_BIN env, the default_chrome() cache location, or the `chrome` argument.
    """
    import subprocess
    chrome_path = chrome or os.environ.get("CHROME_BIN") or default_chrome()
    if not chrome_path or not os.path.exists(chrome_path):
        return ""
    cmd = [chrome_path, "--headless=new", "--no-sandbox", "--disable-gpu",
           "--enable-unsafe-swiftshader", f"--virtual-time-budget={virtual_time}",
           "--dump-dom", url]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout, text=True)
        return r.stdout or ""
    except Exception:  # noqa: BLE001
        return ""


def wayback_snapshot_candidates(url, n=3):
    """Up to n recent Wayback captures (id_ raw mode), newest first."""
    cdx = ("http://web.archive.org/cdx/search/cdx?url={}&output=json&limit=15"
           "&from=20260101".format(url))
    try:
        rows = json.loads(http_get(cdx, timeout=60).decode("utf-8", "ignore"))
    except Exception:  # noqa: BLE001
        return []
    if not isinstance(rows, list) or len(rows) <= 1:
        return []
    candidates = sorted(rows[1:], key=lambda r: r[1], reverse=True)[:n]
    return ["http://web.archive.org/web/{}id_/{}".format(r[1], url) for r in candidates]


# ---------------------------------------------------------------- data helpers

def to_float_or_none(v):
    if v is None or v == "":
        return None
    try:
        f = float(v)
        return f if f >= 0 else None
    except (TypeError, ValueError):
        return None


def has_chinese(text):
    return bool(_HAN_RE.search(text or ""))


# ---------------------------------------------------------------- dual-currency helpers
# Since schema 26.8, per_mtok/batch/per_image prices are objects {usd, cny} (a price may
# be expressed in just one currency). These helpers read/write them uniformly.

def price_of(pm, key, currency="usd"):
    """Get a price field's value for a currency from a dual-price object.
    Falls back to the raw value if the field is still a scalar (pre-migration)."""
    v = (pm or {}).get(key)
    if isinstance(v, dict):
        return v.get(currency)
    return v


def set_price(pm, key, currency, value):
    """Set a price field's value for a currency (creates the dual-price object if needed)."""
    v = pm.get(key)
    if not isinstance(v, dict):
        v = {}
        pm[key] = v
    v[currency] = value


def any_price_positive(pm, keys=("input", "output", "cache_read")):
    """True if any of the given per_mtok keys has a positive price in any currency."""
    for k in keys:
        v = (pm or {}).get(k)
        if isinstance(v, dict):
            if any((x or 0) > 0 for x in v.values()):
                return True
        elif v and v > 0:
            return True
    return False


def price_all_zero(pm, keys=("input", "output", "cache_read")):
    """True if the given per_mtok keys all resolve to 0 (free) across the present currency."""
    vals = []
    for k in keys:
        v = (pm or {}).get(k)
        if v is None:
            continue
        if isinstance(v, dict):
            vals.extend(x for x in v.values() if x is not None)
        else:
            vals.append(v)
    return bool(vals) and all(x == 0 for x in vals)


def has_zero_price(pm, keys=("input", "output", "cache_read")):
    """True if any of the given per_mtok keys is 0 in some currency (free tier present,
    possibly alongside a paid tier, e.g. Gemini free+paid)."""
    for k in keys:
        v = (pm or {}).get(k)
        if isinstance(v, dict):
            if any(x == 0 for x in v.values() if x is not None):
                return True
        elif v == 0:
            return True
    return False


def mixed_currency_zero(pm, keys=("input", "output", "cache_read", "cache_write")):
    """Return the per_mtok fields that mix a zero and a positive value across currencies.

    A field such as {"usd": 0, "cny": 0.15} is self-contradictory: 0 means "free", while a
    positive value in the *other* currency proves the model is paid. This happens when a
    CNY-only vendor (domestic page) keeps a stale/fabricated usd=0 from an earlier
    aggregator write; the CNY-only collector then only supplies cny, so update_model_prices
    (which merges per currency and never clears a value) leaves usd=0 stuck forever. The
    correct form for a single-currency vendor is the schema-blessed single-currency entry
    ({"cny": 0.15}) or usd=null -- never 0 (real case: zhipuai glm-4.7-flash).
    """
    out = []
    for k in keys:
        v = (pm or {}).get(k)
        if isinstance(v, dict):
            vals = [x for x in v.values() if x is not None]
            if any(x == 0 for x in vals) and any(x > 0 for x in vals):
                out.append(k)
    return out


# Categories whose OUTPUT side is structurally not billed per token: an embedding/rerank
# model generates nothing, an STT model bills audio seconds, image/video models bill per
# image/second. A 0 in such a row's `output` field therefore means "no output-token charge"
# and is legitimate -- unlike the same 0 on a chat/reasoning row, which asserts "output
# tokens are FREE" next to a positive input price and is really a source's "price not
# published" sentinel that leaked into the value.
ZERO_OUTPUT_CATEGORIES = ("embedding", "rerank", "audio_stt", "audio_tts", "image_gen", "video_gen")


def zero_token_price_fields(pm, billing_model, category=None):
    """Return the per_mtok TOKEN fields carrying usd == 0 on a NON-free model, else [].

    Schema / docs/price-types.md rule: ``null`` = not offered / unknown, ``0`` = genuinely
    free. A model that is not labelled free / subscription_included and publishes
    ``usd: 0`` on ``input`` or ``output`` while another field is positive therefore claims
    "these tokens are free" -- a data-truth violation, and the same class ``audit.py`` already
    hard-fails for ``cache_read``/``cache_write``. The real meaning of such a 0 is "price not
    published by the source" (models.dev's sentinel), i.e. it must be ``null``.

    Real case 2026-09-14: greenpt ``green-s``/``green-s-pro``, azure ``model-router`` and
    privatemode-ai ``voxtral-mini-3b`` all carried ``output: {"usd": 0}`` alongside a positive
    input, every one of them sourced from models.dev ``cost.output = 0``. They were written
    BEFORE sync_modelsdev's ``_u()`` 0->None guard (2026-09-10), and that guard made the stale
    value UNCLEARABLE: the writer now maps the source's 0 to None and ``update_model_prices``
    skips None, so every later 3h sync leaves the 0 in place. Only a hand repair clears it --
    which is exactly why the check lives here and not only in the writer.

    ``output`` is exempted for the structurally-zero-output categories above; ``input`` is
    never exempted (no category bills nothing for its input side).
    """
    bm = billing_model if isinstance(billing_model, list) else ([billing_model] if billing_model else [])
    if any(b in ("free", "subscription_included") for b in bm):
        return []
    if not any_price_positive(pm):
        # An all-zero / all-null price is the free- vs unknown-labelling checks' business.
        return []
    fields = ["input"] if category in ZERO_OUTPUT_CATEGORIES else ["input", "output"]
    out = []
    for k in fields:
        v = (pm or {}).get(k)
        if isinstance(v, dict) and v.get("usd") == 0:
            out.append(k)
    return out


def duplicate_ids(ids):
    """Exact duplicate ids within one provider (the same string appearing twice)."""
    seq = list(ids)
    return {i for i in seq if seq.count(i) > 1}


def case_variant_duplicate_ids(ids):
    """Map casefold(id) -> sorted distinct casings, for ids stored under >1 casing.

    One logical model stored twice under different id casings is a data defect: the two rows
    drift apart, so a consumer reading either id gets a divergent price. An exact-id dup
    check is case-sensitive and never fires on it. Real 2026-09-12: edenai
    `flexai/DeepSeek-V4-Flash-0731` ($0.065/$0.18) vs `flexai/deepseek-v4-flash-0731`
    ($0.03/$0.1), and llmgateway `Qwen3.8-27B` ($0.2/$2) vs `qwen3.8-27b` ($0.42/$3). Only
    the casing the declared source still publishes is kept; the other row is a stale ghost.
    """
    groups = {}
    for i in ids:
        groups.setdefault(str(i).casefold(), set()).add(i)
    return {k: sorted(v) for k, v in groups.items() if len(v) > 1}


def cache_read_exceeds_input(pm, status=None):
    """Return the currencies where cache_read > input on the same model.

    An ``offline`` row (``status="offline"``) is EXEMPT: a retired row keeps its last published
    spec as a historical record on purpose, so a WARN about it can never be actioned -- the same
    rule the limit-pair check applies. Pass the row's status to get that exemption.

    A cache HIT can never cost more than an uncached input token, so `cache_read > input`
    is impossible -- the signature of a parser COLUMN SWAP (a pricing page that renders the
    cache cells "Write before Read" drops the write PREMIUM into cache_read; tier0_anthropic
    once swapped to Read-before-Write). Callers surface this as a WARN, never a hard-fail: an
    aggregation source can itself publish an odd pair (models.dev reports novita-ai
    xiaomimimo/mimo-v2-flash cache_read 0.3 > input 0.1), and a check must not block a sync
    for a value we cannot correctly re-derive. Real stale case surfaced by this guard:
    kilo openai/gpt-oss-20b cache_read 0.03 > input 0.02 (a value its declared source
    models.dev no longer publishes -- update_model_prices never clears a removed value).
    """
    if status == "offline":
        return []
    inp = (pm or {}).get("input")
    cr = (pm or {}).get("cache_read")
    if not isinstance(inp, dict) or not isinstance(cr, dict):
        return []
    bad = []
    for cur in sorted(set(inp) & set(cr)):
        iv, rv = inp.get(cur), cr.get(cur)
        if (isinstance(iv, (int, float)) and not isinstance(iv, bool)
                and isinstance(rv, (int, float)) and not isinstance(rv, bool)
                and iv > 0 and rv > iv):
            bad.append(cur)
    return bad


# ------------------------------------------------------------- price magnitude
# per_mtok / batch values are a price PER 1M TOKENS, so both ends of the scale carry a
# unit-error signature that no real price can produce:
#   - a non-zero value BELOW 1e-4 ($0.0001 per 1M) is the per-token-as-per-M bug
#     (~1e6x too small; OpenRouter's per-token API value once shipped as 2.2e-7);
#   - a value ABOVE 2e3 ($2000 per 1M = $0.002 per token) is the per-1k-as-per-M bug
#     (~1e3x too large; several vendors publish a CNY-per-1k table beside a per-M one).
#     The priciest published per-token API price is $600 per 1M (openai o1-pro output),
#     so the ceiling sits 3.3x beyond it: a value past it is an error, not a new record.
#     (A threshold CANNOT catch a 1e3x mis-scale of a sub-$2/M model -- that lands inside
#     the legitimate range -- but every mis-scale of anything pricier is blocked.)
#     If a vendor ever legitimately publishes above $2000/1M, raise this constant.
PER_MTOK_IMPOSSIBLE_SMALL = 1e-4
PER_MTOK_IMPOSSIBLE_LARGE = 2e3
PER_MTOK_SUSPECT_SMALL = 1e-3
PER_MTOK_SUSPECT_LARGE = 1e3


def per_mtok_magnitude(value):
    """Classify one non-zero $/1M price: None | "too_small" | "too_large" | "suspect".

    ``None`` when the value is null / zero / non-numeric: null means unknown and 0 means
    free, so neither is a magnitude problem. Callers hard-fail "too_small" and "too_large"
    (both are unit/scale errors that no real price can produce) and warn "suspect" (inside
    the narrow band next to a hard boundary -- borderline, possibly real).
    """
    if value is None or isinstance(value, bool):
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    if f == 0:
        return None
    a = abs(f)
    if a < PER_MTOK_IMPOSSIBLE_SMALL:
        return "too_small"
    if a > PER_MTOK_IMPOSSIBLE_LARGE:
        return "too_large"
    if a < PER_MTOK_SUSPECT_SMALL or a > PER_MTOK_SUSPECT_LARGE:
        return "suspect"
    return None


def batch_exceeds_standard(pricing, status=None):
    """Return the batch fields ("input"/"output") whose price exceeds the standard rate.

    An ``offline`` row (``status="offline"``) is EXEMPT, for the same reason as
    ``cache_read_exceeds_input``: a retired row keeps its last published spec on purpose.

    A batch API is a DISCOUNT on the standard rate (OpenAI / Google / Anthropic / xAI batch
    is ~50-80% of standard), so `batch.<field> > per_mtok.<field>` is impossible: it is the
    signature of a stale/shared batch block copied from a DIFFERENT model in the same family,
    or of a unit/scale error. Real 2026-09-13: openai `gpt-5.6-luna` carried batch input 2.5
    against its own standard input 0.2 (12.5x), and `gpt-5.6-terra` batch 2.5 against 2.0 --
    both had inherited gpt-5.5's batch {input 2.5, output 15}. No writer sets `batch` for
    openai (sync_official.parse_openai emits batch=None and tier0_openai omits it), so a
    hand-written stale block survived every 3h sync and `audit.py` never looked at `batch`.

    Callers surface this as a WARN, never a hard-fail: the repo mirrors its declared source,
    and an aggregation source could publish an odd pair (mirrors cache_read_exceeds_input).
    """
    if status == "offline":
        return []
    if not isinstance(pricing, dict):
        return []
    pm = pricing.get("per_mtok") or {}
    bt = pricing.get("batch") or {}
    if not isinstance(pm, dict) or not isinstance(bt, dict):
        return []
    bad = []
    for k in ("input", "output"):
        bv, sv = bt.get(k), pm.get(k)
        if not isinstance(bv, dict) or not isinstance(sv, dict):
            continue
        for cur in sorted(set(bv) & set(sv)):
            b, s = bv.get(cur), sv.get(cur)
            if (isinstance(b, (int, float)) and not isinstance(b, bool)
                    and isinstance(s, (int, float)) and not isinstance(s, bool)
                    and s > 0 and b > s):
                if k not in bad:
                    bad.append(k)
    return bad


# --- off_peak (time-of-day) price contract ---------------------------------------

OFF_PEAK_DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
_OFF_PEAK_UTC_RE = re.compile(r"^\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}$")


def off_peak_violation(pricing):
    """Validate the `off_peak` time-of-day contract; return [(severity, message)].

    `pricing.off_peak` is a DERIVED-price contract, not free-form prose:
    ``off-peak price = per_mtok x multiplier``, with `per_mtok` holding the PEAK
    (standard) tier and `window.peak` defining the hours that are NOT off-peak. So the
    block is only meaningful when (a) there is a per_mtok price to derive from and (b)
    `multiplier` is a genuine DISCOUNT. Both are machine-checkable and neither was
    checked: `schema.json` types `multiplier` as a bare number and `days`/`utc` as bare
    strings, and no audit rule looked at the block at all (real finding 2026-09-14 --
    setting `multiplier: 2.0` and storing the OFF-peak tier in `per_mtok` while still
    declaring 0.5 both passed validate + audit with zero output, so a writer that
    inverted the ratio (2.0 = peak/off-peak instead of 0.5) or halved the price twice
    would publish silently). Same lesson as `max_output_on_non_token_category`: a field
    introduced for a new pricing mechanism needs its invariant encoded as a check, not
    just its shape.

    severity "fail" = the block contradicts the price it derives (impossible, e.g. an
    "off-peak" rate at or above the peak rate, or a discount with no base price to
    discount); "warn" = the contract is present but incomplete/unverifiable. Returns []
    when `off_peak` is absent (most models). The predicate lives here, not inline in
    audit.py, so it is unit-testable.
    """
    if not isinstance(pricing, dict):
        return []
    op = pricing.get("off_peak")
    if op is None:
        return []
    if not isinstance(op, dict):
        return [("fail", "off_peak is not an object")]

    out = []

    # (a) a discount needs a base: off-peak = per_mtok x multiplier.
    pm = pricing.get("per_mtok")
    has_base = False
    if isinstance(pm, dict):
        for _k, _v in pm.items():
            if not isinstance(_v, dict):
                continue
            for _cur, _val in _v.items():
                if _is_number(_val) and _val != 0:
                    has_base = True
                    break
            if has_base:
                break
    if not has_base:
        out.append((
            "fail",
            "off_peak declares a time-of-day discount but per_mtok carries no non-zero "
            "price to derive it from (off-peak = per_mtok x multiplier); an off-peak rate "
            "is not a standalone price",
        ))

    # (b) multiplier must be a real discount (per_mtok is the PEAK tier).
    mult = op.get("multiplier")
    if mult is None:
        out.append(("warn", "off_peak.multiplier is null -- the off-peak rate cannot be derived"))
    elif not _is_number(mult):
        out.append(("fail", f"off_peak.multiplier={mult!r} is not a number"))
    elif not 0.0 < mult < 1.0:
        out.append((
            "fail",
            f"off_peak.multiplier={mult} is not a discount (must satisfy 0 < m < 1; "
            "per_mtok holds the PEAK tier, so m >= 1 publishes an 'off-peak' rate at or "
            "above the peak rate -- signature of storing peak/off-peak inverted)",
        ))

    # (c) window.peak is what defines off-peak (everything outside it).
    window = op.get("window")
    if window is None:
        out.append(("warn", "off_peak.window is missing -- no machine-readable off-peak window"))
    elif not isinstance(window, dict):
        out.append(("fail", "off_peak.window is not an object"))
    else:
        peak = window.get("peak")
        if peak is None:
            out.append(("warn", "off_peak.window.peak is missing -- the peak window defines off-peak"))
        elif not isinstance(peak, dict):
            out.append(("fail", "off_peak.window.peak is not an object"))
        else:
            days = peak.get("days")
            if not isinstance(days, list) or not days:
                out.append(("warn", "off_peak.window.peak.days is empty/absent"))
            else:
                bad_days = [d for d in days if str(d).strip().lower() not in OFF_PEAK_DAYS]
                if bad_days:
                    out.append((
                        "fail",
                        f"off_peak.window.peak.days={bad_days} are not weekday names "
                        f"{list(OFF_PEAK_DAYS)}",
                    ))
            utc = peak.get("utc")
            if not isinstance(utc, list) or not utc:
                out.append(("warn", "off_peak.window.peak.utc is empty/absent"))
            else:
                bad_utc = [u for u in utc if not _OFF_PEAK_UTC_RE.match(str(u).strip())]
                if bad_utc:
                    out.append((
                        "fail",
                        f"off_peak.window.peak.utc={bad_utc} are not HH:MM-HH:MM ranges",
                    ))
        tz = window.get("tz")
        if not isinstance(tz, str) or not tz.strip():
            out.append(("warn", "off_peak.window.tz is missing -- the peak window is ambiguous"))
    return out


def suspicious_max_output(model, limit=10_000_000):
    """Return `max_output` when it is an implausible placeholder value, else None.

    models.dev stores 99999999 as its "this model has no token output" sentinel (video/image
    models with no token context). qiniu-ai/kling-v2-6 carried that sentinel in BOTH limit
    fields; an earlier repair cleared `context_window` but left `max_output`, and
    `max_output_exceeds_context()` could not see it (that pair check needs BOTH fields to be
    ints, and context was null) -- so 1e8 published silently. Mirrors the inline
    context_window sanity check in audit.py so the whole placeholder class is caught.
    """
    mo = model.get("max_output")
    if isinstance(mo, bool) or not isinstance(mo, int):
        return None
    return mo if (mo > limit or mo < 1) else None


def max_output_exceeds_context(model):
    """Return (context_window, max_output) when max_output > context_window, else None.

    Every token a model GENERATES occupies a slot in its own context window (input + output
    share one bounded budget), so `max_output > context_window` is self-contradictory: at least
    one of the two specs is wrong. The pair is the signature of an aggregation source publishing
    an INVERTED limit block, or of a stale spec kept after a context-window shrink
    (`update_model_prices` never clears a value its source stopped publishing).

    Callers surface this as a WARN, never a hard-fail: the repo mirrors its declared source and
    cannot re-derive the pair without the vendor's own model card -- and models.dev DOES publish
    inverted pairs. Real 2026-09-12: models.dev `limit: {context: 524288, output: 1048576}` for
    deepinfra `thinkingmachines/Inkling`, while DeepInfra's own first-party API
    (`https://api.deepinfra.com/v1/openai/models`) reports `context_length` 524288 /
    `max_tokens` 524288 for the same model -- i.e. the repo's pair is wrong and the vendor's own
    endpoint is the anchor that fixes it. A first-party vendor API keeps the invariant
    (191/191 deepinfra rows: max_tokens <= context_length; 0 inverted).
    """
    if not isinstance(model, dict):
        return None
    cw = model.get("context_window")
    mo = model.get("max_output")
    if not _is_number(cw) or not _is_number(mo):
        return None
    if cw <= 0 or mo <= cw:
        return None
    return (cw, mo)


# --- non-token-output categories -------------------------------------------------

# Categories that emit a vector / a score, NOT generated tokens. `max_output` (a
# generated-token limit) does not apply to them and must be null.
NON_TOKEN_OUTPUT_CATEGORIES = ("embedding", "rerank")


def max_output_on_non_token_category(model):
    """Return (category, max_output) when a model that emits NO output tokens carries one.

    `max_output` is the maximum number of tokens a model GENERATES. An embedding or rerank
    model generates no tokens at all -- it returns a vector / a score -- so the field does not
    apply and must be null. models.dev stores the embedding DIMENSION in `limit.output`
    (text-embedding-3-large 3072, ada-002 / 3-small 1536, bge-m3 1024, all-mini-lm-l6-v2 384,
    rerankers 1), and `sync_modelsdev.build_model` copied it verbatim into `max_output`, so 68
    embedding/rerank rows published a vector size as a token limit (real finding 2026-09-14).
    The existing pair check (`max_output > context_window`) saw only the 44 whose dimension
    happened to exceed the context window; the other 24 -- e.g. text-embedding-3-large with
    context 8191 and "max_output" 3072 -- passed silently. A check that fires on only half a
    bug class is itself the bug (policy §15.1), hence this predicate + its audit rule. The
    predicate lives here, not inline, so it is unit-testable.
    """
    if not isinstance(model, dict):
        return None
    cat = str(model.get("category") or "").lower()
    if cat not in NON_TOKEN_OUTPUT_CATEGORIES:
        return None
    mo = model.get("max_output")
    if mo is None:
        return None
    return (cat, mo)


def _is_number(v):
    """True for a real int/float (bool is not a number here)."""
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def model_map(provider):
    return {m["id"]: m for m in provider.get("models", [])}


def load_provider(provider_id):
    path = os.path.join(PROVIDERS, f"{provider_id}.json")
    return read_json(path) if os.path.exists(path) else None


def save_provider(provider):
    write_json(os.path.join(PROVIDERS, f"{provider['provider_id']}.json"), provider)


def _record_surge_skips(provider_id, skips, now, source):
    """Durably surface >5x surge-guard rejections as changelog provenance entries.

    A skipped correction does NOT self-heal: the same >5x gap makes every later sync skip
    again, so the stale value stays published forever with no trace of why. Real case
    (2026-09-11): cortecs `qwen3.8-27b` output stuck at $2.451 while its declared source
    (models.dev) reported $0.4 -- a 6.13x gap the guard silently rejected on every run, so
    the row contradicted its own source indefinitely. Each rejection is now recorded as a
    `kind="verify"`, `field="surge_skip:<field>.<currency>"` entry (old = stored value,
    new = the official value the writer wanted to apply). audit.py flags any recorded skip
    whose stored value is STILL the skipped one -- i.e. still unresolved. Identical pending
    skips are deduped so a 3h sync cannot append a duplicate every run.
    """
    cl = load_changelog()
    pending = set()
    for e in cl.get("entries", [])[:500]:
        if str(e.get("field", "")).startswith("surge_skip:") and e.get("provider_id") == provider_id:
            pending.add((e.get("item_id"), e.get("field"), json.dumps(e.get("old"), sort_keys=True)))
    fresh = []
    for s in skips:
        field = f"surge_skip:{s['field']}.{s['currency']}"
        if (s["model_id"], field, json.dumps({"stored": s["stored"]}, sort_keys=True)) in pending:
            continue
        fresh.append({
            "date": now, "kind": "verify", "scope": "model",
            "provider_id": provider_id, "item_id": s["model_id"], "field": field,
            "old": {"stored": s["stored"]}, "new": {"official": s["official"]},
            "source": source,
        })
    if fresh:
        append_changelog(fresh)
        print(f"  RECORD {provider_id}: {len(fresh)} unresolved >5x surge skip(s) written to changelog")


def record_unseeded_official(provider_id, missing, now, source):
    """Durably surface official model ids that the DB does not contain.

    update_model_prices() never ADDS a model: a parsed id that is absent from the provider
    file is skipped silently (see the `continue` on `if not m`). So a first-party check can
    look green forever while the vendor's live models never enter the DB. Real 2026-09-13:
    stepfun's whole `stepaudio-*` family (6 token-priced models on the official pricing page,
    0 in the DB -- the check regex was `step-`, which silently dropped the family), alibaba
    56 ids, google 6 ids.

    Each unresolved id set is recorded as a `kind="verify"`,
    `field="unseeded_official:<pid>"` changelog entry (new = the parsed ids), and audit.py
    WARNs while those ids are still absent -- the warning drops out automatically once they
    are seeded. Identical pending sets are deduped so a 3h sync cannot append a duplicate.
    """
    if not missing:
        return
    cl = load_changelog()
    for e in cl.get("entries", [])[:500]:
        if e.get("field") == f"unseeded_official:{provider_id}":
            if sorted((e.get("new") or {}).get("ids") or []) == sorted(missing):
                return  # already recorded, still unresolved
            break
    append_changelog([{
        "date": now, "kind": "verify", "scope": "provider",
        "provider_id": provider_id, "item_id": ",".join(sorted(missing)[:3]),
        "field": f"unseeded_official:{provider_id}",
        "new": {"ids": sorted(missing), "count": len(missing)},
        "source": source,
    }])
    print(f"  RECORD {provider_id}: {len(missing)} official model id(s) absent from the DB "
          f"-> changelog (the writer cannot ADD a model)")


def update_model_prices(provider, updates, now, source, surge_factor=5.0):
    """Apply {model_id: {per_mtok: {...}, batch: {...}, notes: str}} updates.
    Only non-None values overwrite. Returns list of changed model ids.
    A price change of more than surge_factor relative to the stored value is treated
    as a likely parsing/layout error: the field is skipped with a warning.
    """
    by_id = model_map(provider)
    changed = []
    surge_skips = []  # >5x guard rejections, surfaced durably (see _record_surge_skips)
    for mid, data in updates.items():
        m = by_id.get(mid)
        if not m:
            continue
        per = data.get("per_mtok") or {}
        pm = m.setdefault("pricing", {}).setdefault("per_mtok", {})
        # per_mtok values are dual-price objects {usd, cny} (schema 26.8); scalars accepted for back-compat.
        for k in ("input", "output", "cache_read", "cache_write"):
            cur_new = per.get(k)
            if cur_new is None:
                continue
            if not isinstance(cur_new, dict):
                cur_new = {"usd": cur_new}
            cur_old = pm.get(k)
            cur_old = dict(cur_old) if isinstance(cur_old, dict) else ({"usd": cur_old} if cur_old is not None else {})
            for currency, nv in cur_new.items():
                if nv is None:
                    continue
                ov = cur_old.get(currency)
                if ov == nv:
                    continue
                # Never let a bare 0 overwrite a real/unknown value: 0 means "free", while an
                # aggregator's 0 usually means "not published" -> that must stay null.
                if nv == 0 and (ov is None or ov != 0):
                    print(f"  SKIP {mid}.{k}.{currency}: refusing to write 0 over {ov!r} (0 means free; unknown must stay null)")
                    continue
                if ov is not None and nv is not None and ov != 0:
                    _ratio = nv / ov
                    if _ratio > surge_factor or _ratio < (1.0 / surge_factor):
                        print(f"  SKIP {mid}.{k}.{currency}: {ov} -> {nv} looks like a parsing error (bidirectional {surge_factor}x surge); keeping old value")
                        surge_skips.append({"model_id": mid, "field": k, "currency": currency, "stored": ov, "official": nv})
                        continue
                cur_old[currency] = nv
                if mid not in changed:
                    changed.append(mid)
            pm[k] = cur_old if cur_old else None
        # billing_model sync: once a model has a real (positive) token price in ANY currency,
        # it is billed per token — correct stale free/subscription/unknown labels.
        if changed and any_price_positive(pm):
            bm = m.get("billing_model") or []
            if "pay_per_token" not in bm:
                m["billing_model"] = ["pay_per_token"]
        if data.get("batch"):
            # schema 26.8+: batch.input/output are dual {usd,cny} objects (lowercase keys).
            # Normalize a scalar batch ({input:20}) from any source so it can't break validate.
            nb = {k: (v if isinstance(v, dict) else ({provider.get("currency", "USD").lower(): v} if v is not None else None))
                  for k, v in data["batch"].items()}
            if m["pricing"].get("batch") != nb:
                m["pricing"]["batch"] = nb
                if mid not in changed:
                    changed.append(mid)
        # Provenance notes. Persist when the price/billing changed, and ALSO to backfill a
        # model that has no note yet: a check that VERIFIES an already-correct price (nothing
        # changed) must still be able to stamp its official source, or a model whose price the
        # aggregator already happened to match stays sourceless forever (real 2026-09-11: the
        # retargeted opencode/opencode-go checks mapped 71 models with a 0-diff price vs the
        # official page, so `mid in changed` was empty and none of them got a note). Never
        # rewrite an EXISTING note on a no-op verify, so an aggregator pass-through cannot
        # clobber a first-party note (no notes tug-of-war).
        _note = data.get("notes")
        if _note:
            _cur = m.get("notes") or ""
            if (mid in changed or not _cur.strip()) and _cur != _note:
                m["notes"] = _note
                if mid not in changed:
                    changed.append(mid)
        new_status = data.get("status")
        if new_status:
            if new_status in ("online", "offline"):
                if m.get("status") != new_status:
                    m["status"] = new_status
                    if mid not in changed:
                        changed.append(mid)
            else:
                # Refuse schema-invalid status values (modelStatus enum = online|offline):
                # a check/collector literal like "retired" would corrupt the file and make
                # validate/audit hard-fail on the next save.
                print(f"  SKIP {mid}.status: invalid value {new_status!r} (only online/offline allowed)")
    if surge_skips:
        _record_surge_skips(provider.get("provider_id"), surge_skips, now, source)
    if changed:
        provider["verified_at"] = now
        provider["updated_at"] = now
        save_provider(provider)
        append_changelog([{
            "date": now, "kind": "update", "scope": "model", "provider_id": provider["provider_id"],
            "item_id": ",".join(changed[:20]), "field": "pricing", "new": {"models": len(changed)},
            "source": source,
        }])
    return changed


# ---------------------------------------------------------------- changelog

def load_changelog():
    p = os.path.join(META, "changelog.json")
    if os.path.exists(p):
        return read_json(p)
    return {"schema_version": SCHEMA_VERSION, "entries": []}


def append_changelog(entries):
    cl = load_changelog()
    # Do NOT truncate: the changelog is an append-only audit trail. The previous
    # [:5000] slice silently dropped the oldest entries on every append once the
    # file passed 5000 records (e.g. the ebcloud entry vanished in PR #154).
    cl["entries"] = entries + cl["entries"]
    write_json(os.path.join(META, "changelog.json"), cl)


# ---------------------------------------------------------------- index/manifest

def load_index():
    p = os.path.join(FEED, "index.json")
    return read_json(p) if os.path.exists(p) else None


def save_index(index):
    write_json(os.path.join(FEED, "index.json"), index)


def load_manifest():
    p = os.path.join(META, "manifest.json")
    return read_json(p) if os.path.exists(p) else None


def save_manifest(manifest):
    write_json(os.path.join(META, "manifest.json"), manifest)


def refresh_index_counts(now=None):
    """Recompute index model counts from actual files."""
    index = load_index()
    changed = False
    for lst in (index["providers"], index["resellers"]):
        for entry in lst:
            path = os.path.join(FEED, entry["file"])
            if os.path.exists(path):
                actual = len(read_json(path).get("models", []))
                if actual != entry["model_count"]:
                    entry["model_count"] = actual
                    if now:
                        entry["updated_at"] = now
                    changed = True
    if changed:
        index["model_count"] = sum(e["model_count"] for e in index["providers"]) + sum(
            e["model_count"] for e in index["resellers"])
        save_index(index)
    return changed
