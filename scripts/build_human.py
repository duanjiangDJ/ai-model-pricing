"""Generate human-readable Markdown from machine-readable data.

Usage: python scripts/build_human.py
Output: data/human/README.md, data/human/providers/*.md, data/human/plans.md
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HUMAN, MACHINE, PROVIDERS, read_json, write_json  # noqa: E402

CHANNEL_LABEL = {
    "first_party": "官方直供",
    "cloud": "云平台托管",
    "hosted": "推理托管",
    "aggregator": "聚合站",
    "reseller": "中转站",
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


def build_provider_md(provider, index_entry):
    cur = provider.get("currency", "USD")
    lines = [
        f"# {provider['name']}",
        "",
        f"- provider_id: `{provider['provider_id']}`",
        f"- 渠道: {CHANNEL_LABEL.get(provider['channel'], provider['channel'])}",
        f"- 官网: {provider.get('homepage', '—')}",
        f"- 定价页: {provider.get('pricing_page') or '—'}",
        f"- 币种: {cur}" + ("（非 USD，注意换算）" if cur != "USD" else ""),
        f"- 数据更新时间: {provider.get('updated_at', '—')}",
        f"- 核实时间: {provider.get('verified_at', '—')}",
        "",
        f"共 **{len(provider['models'])}** 个模型。",
        "",
        "| 模型 | 类别 | 上下文 | 输入 $/MTok | 输出 $/MTok | 缓存读 | 缓存写 | 批处理(入/出) | 其他计费 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for m in provider["models"]:
        p = m.get("pricing") or {}
        mt = p.get("per_mtok") or {}
        batch = p.get("batch") or {}
        other = []
        if p.get("per_image"):
            other.append("按张计费")
        if p.get("per_request"):
            other.append(f"按请求 ${p['per_request']:g}")
        if p.get("per_audio_second"):
            other.append("按音频秒")
        if p.get("credits"):
            other.append(f"点数({p['credits'].get('unit_name', 'credits')})")
        if p.get("gpu"):
            other.append("按GPU计费")
        if p.get("finetune"):
            other.append("微调收费")
        if p.get("neuron_second"):
            other.append("神经元秒")
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
    notes = [f"- {m['id']}: {m['notes']}" for m in provider["models"] if m.get("notes") and "reseller" in m["notes"]]
    if notes:
        lines += ["", "## 备注", ""] + notes[:20]
    return "\n".join(lines) + "\n"


def main():
    index = read_json(os.path.join(MACHINE, "index.json"))
    os.makedirs(os.path.join(HUMAN, "providers"), exist_ok=True)

    # provider pages
    entries = []
    for entry in index["providers"] + index["resellers"]:
        fpath = os.path.join(MACHINE, entry["file"])
        if not os.path.exists(fpath):
            continue
        provider = read_json(fpath)
        slug = provider["provider_id"]
        md = build_provider_md(provider, entry)
        with open(os.path.join(HUMAN, "providers", f"{slug}.md"), "w", encoding="utf-8") as f:
            f.write(md)
        entries.append((provider, entry))

    # plans page
    plans_data = read_json(os.path.join(MACHINE, "plans.json"))
    plans = plans_data.get("plans", [])
    plans_lines = [
        "# 订阅与编码工具计划（Plans）",
        "",
        f"共 **{len(plans)}** 个计划。更新时间: {plans_data.get('updated_at', '—')}",
        "",
        "| 产品 | 计划 | 类别 | 计费 | 价格(USD) | 用量限制 | 包含内容 | 定价页 | 核实时间 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for p in plans:
        plans_lines.append(
            "| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                p["product"],
                p["plan"],
                p["category"],
                p.get("billing") or "—",
                fmt(p.get("price_usd")),
                (p.get("limits") or "—").replace("|", "\\|"),
                "; ".join(p.get("includes") or []).replace("|", "\\|") or "—",
                f"[链接]({p['url']})" if p.get("url") else "—",
                p.get("verified_at", "—"),
            )
        )
    with open(os.path.join(HUMAN, "plans.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(plans_lines) + "\n")

    # index README
    model_total = sum(len(p["models"]) for p, _ in entries)
    lines = [
        "# AI Model Pricing — 人类可读索引",
        "",
        "> 数据来源于各厂商官方定价页与公开 API，机器可读版本见 [`data/machine/`](../machine/)。",
        "> 更新机制：GitHub Actions 每日自动检查（见 `.github/workflows/daily-check.yml`）。",
        "",
        f"- 数据更新时间: {index.get('generated_at')}",
        f"- 覆盖渠道: {len(entries)} 个（含 OpenRouter 聚合 419 个模型）",
        f"- 模型总数: {model_total}",
        f"- 订阅计划数: {len(plans)}",
        "",
        "## 供应商列表",
        "",
        "| Provider | 渠道 | 模型数 | 文件 | 更新时间 |",
        "|---|---|---|---|---|",
    ]
    for p, entry in entries:
        lines.append(
            "| [{}](providers/{}.md) | {} | {} | `{}` | {} |".format(
                p["name"], p["provider_id"], CHANNEL_LABEL.get(p["channel"], p["channel"]),
                len(p["models"]), entry["file"], p.get("updated_at", "—"),
            )
        )
    lines += ["", "## 订阅计划", "", f"[plans.md](plans.md) — 共 {len(plans)} 个计划", "",
              "## 其他文档", "",
              "- [供应商全景](../docs/providers.md)",
              "- [收费形式口径](../docs/price-types.md)",
              "- [机器格式规范](../FORMAT.md)"]
    with open(os.path.join(HUMAN, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"human pages: {len(entries)} providers, {len(plans)} plans")


if __name__ == "__main__":
    main()
