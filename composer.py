"""字段映射 - 按 .docx 内容分组。

每模块的 sections 数量匹配数据点组数。
所有 section 渲染为紧凑 stat rows，无大卡片。
"""
from typing import Any

from viz import VIZ_REGISTRY


# viz 期望的 data 形状
VIZ_SHAPE = {
    "kpi": "dict", "bar": "list", "pie": "list", "funnel": "list",
    "progress": "dict", "ranking": "list", "hierarchy": "list", "table": "list",
}


def _adapt(render_fn, viz_type: str, data: Any, data_key: str) -> str:
    """适配数据 → 调用 viz render。"""
    if data is None:
        return ""

    # 按 section 字段过滤
    if isinstance(data, list) and data and isinstance(data[0], dict) and "section" in data[0]:
        filtered = [r for r in data if r.get("section") == data_key]
        if filtered:
            data = filtered

    if not data:
        return ""

    expected = VIZ_SHAPE.get(viz_type, "list")

    if expected == "dict" and isinstance(data, list):
        first = data[0]
        if viz_type == "kpi":
            return render_fn(
                {"value": first.get("value", "-"), "sub": first.get("label", ""), "tone": "blue"},
                {},
            )
        if viz_type == "progress":
            label = first.get("label", "")
            current = first.get("value", 0) or 0
            sub = str(first.get("sub", ""))
            target = 0
            for w in sub.split():
                try:
                    target = int(w)
                    break
                except ValueError:
                    pass
            pct = current / target if target > 0 else 0
            return render_fn(
                {"label": label, "current": current, "target": target, "pct": pct}, {}
            )

    if expected == "list" and isinstance(data, dict):
        return render_fn([data], {})

    return render_fn(data, {})


def _format_value(v) -> str:
    """数值格式化。"""
    if v is None:
        return "—"
    if isinstance(v, float):
        if 0 < v < 1:
            return f"{v * 100:.2f}%"
        return f"{v:,.2f}"
    if isinstance(v, int):
        return f"{v:,}"
    return str(v)


def _render_compact_stat_row(r: dict, max_pct: float = 0) -> str:
    """渲染一行紧凑 stat: label | value (with inline bar) | sub"""
    label = r.get("label", "")
    value = r.get("value", "")
    sub = r.get("sub", "")

    # 检测是否有占比可用于 inline bar
    pct = 0
    if isinstance(value, float) and 0 < value < 1:
        pct = value
    elif isinstance(value, str) and value.endswith("%"):
        try:
            pct = float(value.rstrip("%")) / 100
        except ValueError:
            pct = 0

    bar_html = ""
    if pct > 0 and max_pct > 0:
        width = (pct / max_pct) * 100
        bar_html = f'<span class="stat-bar"><span class="stat-bar-fill" style="width:{width:.1f}%"></span></span>'

    return (
        f'<div class="stat-row">'
        f'<span class="stat-label">{label}</span>'
        f'<span class="stat-value">{_format_value(value)}</span>'
        f"{bar_html}"
        f'<span class="stat-sub">{sub}</span>'
        f"</div>"
    )


def _render_table(section: dict, data: Any) -> str:
    """渲染紧凑表格。"""
    if isinstance(data, list) and data and isinstance(data[0], dict) and "section" in data[0]:
        filtered = [r for r in data if r.get("section") == section.get("data_key")]
    else:
        filtered = data if isinstance(data, list) else []
    if not filtered:
        return ""

    # 收集列名（排除 section 列）
    cols = [k for k in filtered[0].keys() if k != "section"]
    head = "".join(f"<th>{c}</th>" for c in cols)
    rows = "".join(
        "<tr>" + "".join(f"<td>{_format_value(r.get(c))}</td>" for c in cols) + "</tr>"
        for r in filtered
    )
    return f'<div class="table-wrap"><table class="data-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'


def render_section(section: dict, data: Any) -> str:
    """渲染 section：紧凑 stat rows 或 table。"""
    data_key = section.get("data_key", "")
    section_type = section.get("type", "")
    title = section.get("title", "")

    # 过滤数据
    if isinstance(data, list) and data and isinstance(data[0], dict) and "section" in data[0]:
        rows = [r for r in data if r.get("section") == data_key]
    else:
        rows = []

    if not rows:
        return ""

    # table 类型
    if section_type == "table":
        table_html = _render_table(section, data)
        return f'<div class="section"><h3 class="section-title">{title}</h3>{table_html}</div>'

    # hierarchy 类型：父子结构
    if section_type == "hierarchy":
        items = "".join(
            f'<li><span class="h-name">{r.get("label", "")}</span> '
            f'<span class="h-count">{_format_value(r.get("value"))}</span></li>'
            for r in rows
        )
        return f'<div class="section"><h3 class="section-title">{title}</h3><ul class="hierarchy-list">{items}</ul></div>'

    # 其他：紧凑 stat rows
    # 计算 max pct 用于归一化
    pcts = []
    for r in rows:
        v = r.get("value")
        if isinstance(v, float) and 0 < v < 1:
            pcts.append(v)
        elif isinstance(v, str) and v.endswith("%"):
            try:
                pcts.append(float(v.rstrip("%")) / 100)
            except ValueError:
                pass
    max_pct = max(pcts) if pcts else 0

    rows_html = "".join(_render_compact_stat_row(r, max_pct) for r in rows)
    return f'<div class="section"><h3 class="section-title">{title}</h3><div class="stat-list">{rows_html}</div></div>'


def render_module(module_key: str, module_cfg: dict, module_data: Any) -> str:
    """渲染模块：所有 sections 紧凑排列。"""
    sections_html = []
    for section in module_cfg.get("sections", []):
        rendered = render_section(section, module_data)
        if rendered:
            sections_html.append(rendered)

    icon = module_cfg.get("icon", "")
    title = module_cfg.get("title", "")
    return f"""<section class="module" id="M-{module_cfg.get('order', '?')}">
<h2><span class="icon">{icon}</span> {title}</h2>
<div class="module-body">{"".join(sections_html)}</div>
</section>"""
