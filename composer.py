"""按 mapping 组合 6 模块 HTML。

布局策略：
- 连续 kpi section → kpi-grid（多列 KPI）
- 其他 section 两两一组 → two-col grid
- 奇数尾 section 占满整行
"""
from typing import Any

from viz import VIZ_REGISTRY


# 每个 viz 期望的 data 形状：dict / list[dict]
VIZ_SHAPE = {
    "kpi": "dict",
    "bar": "list",
    "pie": "list",
    "funnel": "list",
    "progress": "dict",
    "ranking": "list",
    "hierarchy": "list",
    "table": "list",
}


def _adapt_and_render(render_fn, viz_type: str, data: Any, options: dict) -> str:
    """根据 viz 期望形状适配 data，返回渲染 HTML。"""
    if data is None:
        return '<div class="empty">无数据</div>'

    expected = VIZ_SHAPE.get(viz_type, "list")

    if expected == "dict" and isinstance(data, list):
        if not data:
            return '<div class="empty">无数据</div>'
        first = data[0]
        if viz_type == "kpi":
            num = first.get("数量") or first.get("实际") or first.get("value")
            sub = first.get("指标") or first.get("分类") or first.get("类别") or "合计"
            return render_fn({"value": num, "sub": sub, "tone": "blue"}, options)
        if viz_type == "progress":
            label = first.get("指标") or first.get("分类") or first.get("部门/项目") or ""
            current = first.get("实际") or first.get("完成") or 0
            target = first.get("计划") or 0
            pct = first.get("完成率") or first.get("百分比") or 0
            return render_fn({"label": label, "current": current, "target": target, "pct": pct}, options)

    if expected == "list" and isinstance(data, dict):
        return render_fn([data], options)

    return render_fn(data, options)


def _render_section_body(section: dict, data: Any) -> str:
    """渲染 section body（不含布局包装）。"""
    render_fn = VIZ_REGISTRY[section["type"]]
    return _adapt_and_render(render_fn, section["type"], data, {})


def _section_title_html(title: str) -> str:
    if not title:
        return ""
    return f'<h3 class="section-title">{title}</h3>'


def _section_drill_html(drillable: bool, data_key: str) -> str:
    if not drillable:
        return ""
    return (
        '<div class="drill-wrap">'
        f'<button class="drill-btn" data-key="{data_key}">查看详情</button>'
        f'<div class="drill-panel" data-key="{data_key}"></div>'
        "</div>"
    )


def _build_section_card(section: dict, data: Any) -> str:
    """单个 section 卡片（含 title + viz + 可选 drill）。"""
    drillable = section.get("drillable", False)
    data_key = section.get("data_key", "")
    body = _render_section_body(section, data)
    return (
        f'<div class="section-card" data-section="{section["key"]}">'
        f'{_section_title_html(section.get("title", ""))}'
        f'<div class="section-body">{body}</div>'
        f"{_section_drill_html(drillable, data_key)}"
        f"</div>"
    )


def _layout_sections(sections: list[tuple[dict, Any]]) -> str:
    """布局策略：把 sections 排成网格。

    - 连续 kpi → kpi-grid row
    - 其余两两一组 → two-col row
    - 奇数尾 → full width
    """
    parts = []
    i = 0
    n = len(sections)
    while i < n:
        section, data = sections[i]
        # 收集连续 kpi
        if section["type"] == "kpi":
            kpi_group = []
            while i < n and sections[i][0]["type"] == "kpi":
                kpi_group.append(_build_section_card(*sections[i]))
                i += 1
            parts.append(f'<div class="kpi-grid">{"".join(kpi_group)}</div>')
            continue

        # 其他 viz：两两一组
        if i + 1 < n and sections[i + 1][0]["type"] != "kpi":
            a = _build_section_card(*sections[i])
            b = _build_section_card(*sections[i + 1])
            parts.append(f'<div class="two-col">{a}{b}</div>')
            i += 2
        else:
            parts.append(f'<div class="full-col">{_build_section_card(*sections[i])}</div>')
            i += 1
    return "".join(parts)


def render_module(module_key: str, module_cfg: dict, module_data: Any) -> str:
    """渲染单模块：智能网格布局。"""
    sections = []
    for section in module_cfg.get("sections", []):
        data_key = section.get("data_key")
        if isinstance(module_data, dict) and data_key:
            data = module_data.get(data_key)
        else:
            data = module_data
        sections.append((section, data))

    body = _layout_sections(sections)
    return f"""<section class="module" id="M-{module_cfg.get('order', '?')}">
<h2>{module_cfg['icon']} {module_cfg['title']}</h2>
<div class="module-body">
{body}
</div>
</section>"""
