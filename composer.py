"""字段映射 + viz 配置。

按 .docx 内容比重设计：
- size="compact" → 关键数字（KPI 行，多列小卡）
- size="half" → 并排显示
- size="full" → 占满（重要表/排名）
"""
from typing import Any

from viz import VIZ_REGISTRY


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


def _adapt_and_render(render_fn, viz_type: str, data: Any, options: dict, data_key: str = "") -> str:
    if data is None:
        return '<div class="empty">无数据</div>'

    # 数据切片：按 data_key 过滤 section 列
    if isinstance(data, list) and data and isinstance(data[0], dict) and "section" in data[0]:
        filtered = [r for r in data if r.get("section") == data_key]
        if filtered:
            data = filtered

    expected = VIZ_SHAPE.get(viz_type, "list")

    if expected == "dict" and isinstance(data, list):
        if not data:
            return '<div class="empty">无数据</div>'
        first = data[0]
        if viz_type == "kpi":
            num = first.get("value")
            sub = first.get("sub") or first.get("label") or ""
            return render_fn({"value": num, "sub": sub, "tone": "blue"}, options)
        if viz_type == "progress":
            label = first.get("label") or ""
            current = first.get("value") or 0
            target_str = first.get("sub", "")
            # 尝试从 sub 提取数字（如 "全年任务 410"）
            target = 0
            for word in str(target_str).split():
                try:
                    target = int(word)
                    break
                except ValueError:
                    pass
            # 计算 pct
            if target > 0:
                pct = current / target
            elif "pct" in first or "完成率" in str(first.get("label", "")):
                pct = first.get("value", 0) if isinstance(first.get("value"), float) and first.get("value", 0) <= 1 else 0
            else:
                pct = 0
            return render_fn({"label": label, "current": current, "target": target, "pct": pct}, options)

    if expected == "list" and isinstance(data, dict):
        return render_fn([data], options)

    return render_fn(data, options)


def _render_section_body(section: dict, data: Any) -> str:
    render_fn = VIZ_REGISTRY[section["type"]]
    return _adapt_and_render(render_fn, section["type"], data, {}, section.get("data_key", ""))


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
    size = section.get("size", "")
    body = _render_section_body(section, data)
    compact = " compact" if size == "compact" else ""
    return (
        f'<div class="section-card{compact}" data-section="{section["key"]}">'
        f'{_section_title_html(section.get("title", ""))}'
        f'<div class="section-body">{body}</div>'
        f"{_section_drill_html(drillable, data_key)}"
        f"</div>"
    )


def _layout_sections(sections: list[tuple[dict, Any]]) -> str:
    """布局策略：
    - size="compact" → kpi-grid（多列）
    - size="half" → two-col
    - size="full" → full-col
    - 默认：kpi 进 kpi-grid，其他成对进 two-col
    """
    parts = []
    i = 0
    n = len(sections)
    while i < n:
        section, data = sections[i]
        size = section.get("size", "")

        # 显式 compact：单 section 单独放，标记为 compact；多个连续 compact 才合并
        if size == "compact":
            kpi_group = []
            while i < n and sections[i][0].get("size") == "compact":
                kpi_group.append(_build_section_card(*sections[i]))
                i += 1
            if len(kpi_group) >= 2:
                parts.append(f'<div class="kpi-grid">{"".join(kpi_group)}</div>')
            else:
                parts.append(f'<div class="kpi-grid">{"".join(kpi_group)}</div>')
            continue

        # 显式 full
        if size == "full":
            parts.append(f'<div class="full-col">{_build_section_card(*sections[i])}</div>')
            i += 1
            continue

        # 显式 half → 与下一个 half 配对
        if size == "half":
            a = _build_section_card(*sections[i])
            if i + 1 < n and sections[i + 1][0].get("size") == "half":
                b = _build_section_card(*sections[i + 1])
                parts.append(f'<div class="two-col">{a}{b}</div>')
                i += 2
            else:
                parts.append(f'<div class="two-col">{a}</div>')
                i += 1
            continue

        # 默认：kpi 进 grid，其他两两配对
        if section["type"] == "kpi":
            kpi_group = []
            while i < n and (sections[i][0]["type"] == "kpi" or sections[i][0].get("size") == "compact"):
                kpi_group.append(_build_section_card(*sections[i]))
                i += 1
            parts.append(f'<div class="kpi-grid">{"".join(kpi_group)}</div>')
            continue

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
    sections = []
    for section in module_cfg.get("sections", []):
        data_key = section.get("data_key")
        if isinstance(module_data, dict) and data_key:
            data = module_data.get(data_key)
        else:
            data = module_data
        sections.append((section, data))

    body = _layout_sections(sections)
    icon = module_cfg.get("icon", "")
    title = module_cfg.get("title", "")
    return f"""<section class="module" id="M-{module_cfg.get('order', '?')}">
<h2><span class="icon">{icon}</span> {title}</h2>
<div class="module-body">
{body}
</div>
</section>"""
