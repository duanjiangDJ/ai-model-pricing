"""Generate human-readable Markdown (EN default + zh-CN) from machine-readable data.

Usage: python scripts/build_human.py
Output:
  data/human/README.md, data/human/providers/*.md, data/human/plans.md   (English, default)
  data/human/zh-CN/README.md, data/human/zh-CN/providers/*.md, data/human/zh-CN/plans.md (中文)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HUMAN, MACHINE, PROVIDERS, read_json  # noqa: E402

CHANNEL_LABEL = {
    "first_party": "First-party",
    "cloud": "Cloud-hosted",
    "hosted": "Inference host",
    "aggregator": "Aggregator",
    "reseller": "Reseller",
}
CHANNEL_LABEL_ZH = {
    "first_party": "官方直供",
    "cloud": "云平台托管",
    "hosted": "推理托管",
    "aggregator": "聚合站",
    "reseller": "中转站",
}

L10N = {
    "en": {
        "channel": "Channel",
        "homepage": "Homepage",
        "pricing_page": "Pricing page",
        "currency": "Currency",
        "currency_note": " (non-USD, see notes)",
        "updated": "Data updated",
        "verified": "Verified",
        "models_count": "**{}** models in total.",
        "model": "Model",
        "category": "Category",
        "context": "Context",
        "input": "Input $/MTok",
        "output": "Output $/MTok",
        "cache_read": "Cache read",
        "cache_write": "Cache write",
        "batch": "Batch (in/out)",
        "other": "Other billing",
        "notes": "Notes",
        "reseller_note": "OpenRouter reseller price",
        "plans_title": "Subscription & Coding Plans",
        "plans_count": "**{}** plans in total. Updated: {}",
        "product": "Product",
        "plan": "Plan",
        "billing": "Billing",
        "price": "Price (USD)",
        "limits": "Limits",
        "includes": "Includes",
        "url": "URL",
        "verified_at": "Verified",
        "index_title": "AI Model Pricing — Human-Readable Index",
        "index_note1": "Data sources: official pricing pages & public APIs. Machine-readable version: [`data/machine/`](../machine/).",
        "index_note2": "Auto-updated daily by GitHub Actions (see `.github/workflows/daily-check.yml`).",
        "index_updated": "Generated",
        "index_models": "Models total",
        "index_plans": "Plans total",
        "index_providers": "Providers",
        "providers_header": "Providers",
        "file": "File",
        "plans_link": "Plans",
        "docs_links": ["Other docs", "Provider landscape", "Price types", "Machine format spec", "Guide for AI agents"],
        "docs_files": ["../docs/providers.md", "../docs/price-types.md", "../FORMAT.md", "../AGENTS.md"],
        "misc": "Misc",
    },
    "zh-CN": {
        "channel": "渠道",
        "homepage": "官网",
        "pricing_page": "定价页",
        "currency": "币种",
        "currency_note": "（非 USD，注意换算）",
        "updated": "数据更新时间",
        "verified": "核实时间",
        "models_count": "共 **{}** 个模型。",
        "model": "模型",
        "category": "类别",
        "context": "上下文",
        "input": "输入 $/MTok",
        "output": "输出 $/MTok",
        "cache_read": "缓存读",
        "cache_write": "缓存写",
        "batch": "批处理(入/出)",
        "other": "其他计费",
        "notes": "备注",
        "reseller_note": "OpenRouter 转售价",
        "plans_title": "订阅与编码工具计划（Plans）",
        "plans_count": "共 **{}** 个计划。更新时间: {}",
        "product": "产品",
        "plan": "计划",
        "billing": "计费",
        "price": "价格(USD)",
        "limits": "用量限制",
        "includes": "包含内容",
        "url": "定价页",
        "verified_at": "核实时间",
        "index_title": "AI Model Pricing — 人类可读索引",
        "index_note1": "数据来源于各厂商官方定价页与公开 API，机器可读版本见 [`data/machine/`](../machine/)。",
        "index_note2": "更新机制：GitHub Actions 每日自动检查（见 `.github/workflows/daily-check.yml`）。",
        "index_updated": "数据更新时间",
        "index_models": "模型总数",
        "index_plans": "订阅计划数",
        "index_providers": "覆盖渠道",
        "providers_header": "供应商列表",
        "file": "文件",
        "plans_link": "订阅计划",
        "docs_links": ["其他文档", "供应商全景", "收费形式口径", "机器格式规范", "Agent 指南"],
        "docs_files": ["../docs/providers.md", "../docs/price-types.md", "../FORMAT.md", "../AGENTS.md"],
        "misc": "其他",
    },
}


def fmt(v, currency="USD", suffix=""):
    if v is None:
        return "—"
    if isinstance(v, str):
        return v
    return f"${v:g}{suffix}"


def num_fmt(v):
    if v is None:
        return "—"
    if v >= 1_000_000:
        return f"{v / 1_000_000:g}M"
    if v >= 1000:
        return f"{v / 1000:g}K"
    return str(v)


def build_provider_md(provider, lang, channel_labels):
    t = L10N[lang]
    cur = provider.get("currency", "USD")
    lines = [
        f"# {provider['name']}",
        "",
        f"- provider_id: `{provider['provider_id']}`",
        f"- {t['channel']}: {channel_labels.get(provider['channel'], provider['channel'])}",
        f"- {t['homepage']}: {provider.get('homepage', '—')}",
        f"- {t['pricing_page']}: {provider.get('pricing_page') or '—'}",
        f"- {t['currency']}: {cur}" + (t["currency_note"] if cur != "USD" else ""),
        f"- {t['updated']}: {provider.get('updated_at', '—')}",
        f"- {t['verified']}: {provider.get('verified_at', '—')}",
        "",
        t["models_count"].format(len(provider["models"])),
        "",
        f"| {t['model']} | {t['category']} | {t['context']} | {t['input']} | {t['output']} | {t['cache_read']} | {t['cache_write']} | {t['batch']} | {t['other']} |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for m in provider["models"]:
        p = m.get("pricing") or {}
        mt = p.get("per_mtok") or {}
        batch = p.get("batch") or {}
        other = []
        if p.get("per_image"):
            other.append("per-image")
        if p.get("per_request"):
            other.append(f"per-request ${p['per_request']:g}")
        if p.get("per_audio_second"):
            other.append("per-audio-sec")
        if p.get("credits"):
            other.append(f"credits({p['credits'].get('unit_name', 'credits')})")
        if p.get("gpu"):
            other.append("GPU-based")
        if p.get("finetune"):
            other.append("finetune")
        if p.get("neuron_second"):
            other.append("neuron-sec")
        lines.append(
            "| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                f"`{m['id']}`",
                m.get("category", "—"),
                num_fmt(m.get("context_window")),
                fmt(mt.get("input"), cur),
                fmt(mt.get("output"), cur),
                fmt(mt.get("cache_read"), cur),
                fmt(mt.get("cache_write"), cur),
                f"{fmt(batch.get('input'), cur)}/{fmt(batch.get('output'), cur)}",
                "; ".join(other) or "—",
            )
        )
    return "\n".join(lines) + "\n"


def build_plans_md(plans_data, lang):
    t = L10N[lang]
    plans = plans_data.get("plans", [])
    lines = [
        f"# {t['plans_title']}",
        "",
        t["plans_count"].format(len(plans), plans_data.get("updated_at", "—")),
        "",
        f"| {t['product']} | {t['plan']} | {t['category']} | {t['billing']} | {t['price']} | {t['limits']} | {t['includes']} | {t['url']} | {t['verified_at']} |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for p in plans:
        lines.append(
            "| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                p["product"],
                p["plan"],
                p["category"],
                p.get("billing") or "—",
                fmt(p.get("price_usd")),
                (p.get("limits") or "—").replace("|", "\\|"),
                "; ".join(p.get("includes") or []).replace("|", "\\|") or "—",
                f"[link]({p['url']})" if p.get("url") else "—",
                p.get("verified_at", "—"),
            )
        )
    return "\n".join(lines) + "\n"


def build_index_md(index, entries, plans_count, lang, channel_labels):
    t = L10N[lang]
    model_total = sum(len(p["models"]) for p, _ in entries)
    lines = [
        f"# {t['index_title']}",
        "",
        f"> {t['index_note1']}",
        f"> {t['index_note2']}",
        "",
        f"- {t['index_updated']}: {index.get('generated_at')}",
        f"- {t['index_providers']}: {len(entries)}",
        f"- {t['index_models']}: {model_total}",
        f"- {t['index_plans']}: {plans_count}",
        "",
        f"## {t['providers_header']}",
        "",
        f"| {t['product']} | {t['channel']} | {t['index_models']} | {t['file']} | {t['updated']} |",
        "|---|---|---|---|---|",
    ]
    for p, entry in entries:
        lines.append(
            "| [{}](providers/{}.md) | {} | {} | `{}` | {} |".format(
                p["name"], p["provider_id"], channel_labels.get(p["channel"], p["channel"]),
                len(p["models"]), entry["file"], p.get("updated_at", "—"),
            )
        )
    lines += [
        "",
        f"## {t['plans_link']}",
        "",
        f"[plans.md](plans.md) — {t['plans_count'].format(plans_count, '—')}",
        "",
        f"## {t['misc']}",
        "",
    ]
    for i, (label, fpath) in enumerate(zip(t["docs_links"], t["docs_files"])):
        lines.append(f"- [{label}]({fpath})")
    return "\n".join(lines) + "\n"


def main():
    index = read_json(os.path.join(MACHINE, "index.json"))
    plans_data = read_json(os.path.join(MACHINE, "plans.json"))
    plans = plans_data.get("plans", [])

    for lang in ("en", "zh-CN"):
        labels = CHANNEL_LABEL if lang == "en" else CHANNEL_LABEL_ZH
        out_root = os.path.join(HUMAN, "" if lang == "en" else lang)
        os.makedirs(os.path.join(out_root, "providers"), exist_ok=True)

        entries = []
        for entry in index["providers"] + index["resellers"]:
            fpath = os.path.join(MACHINE, entry["file"])
            if not os.path.exists(fpath):
                continue
            provider = read_json(fpath)
            md = build_provider_md(provider, lang, labels)
            with open(os.path.join(out_root, "providers", f"{provider['provider_id']}.md"), "w", encoding="utf-8") as f:
                f.write(md)
            entries.append((provider, entry))

        with open(os.path.join(out_root, "plans.md"), "w", encoding="utf-8") as f:
            f.write(build_plans_md(plans_data, lang))
        with open(os.path.join(out_root, "README.md"), "w", encoding="utf-8") as f:
            f.write(build_index_md(index, entries, len(plans), lang, labels))
        print(f"human pages [{lang}]: {len(entries)} providers, {len(plans)} plans")


if __name__ == "__main__":
    main()
