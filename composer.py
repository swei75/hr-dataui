"""按 mapping 组合 6 模块 HTML。"""
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

    # 实际是 list，期望是 dict（kpi / progress）→ 找匹配的列
    if expected == "dict" and isinstance(data, list):
        if not data:
            return '<div class="empty">无数据</div>'
        first = data[0]
        # kpi: 找 数量 / value 字段
        if viz_type == "kpi":
            num = first.get("数量") or first.get("实际") or first.get("value")
            sub = first.get("指标") or first.get("分类") or first.get("类别") or "合计"
            return render_fn({"value": num, "sub": sub, "tone": "blue"}, options)
        # progress: 找 计划 / 实际 / 完成率
        if viz_type == "progress":
            label = first.get("指标") or first.get("分类") or first.get("部门/项目") or ""
            current = first.get("实际") or first.get("完成") or 0
            target = first.get("计划") or 0
            pct = first.get("完成率") or first.get("百分比") or 0
            return render_fn({"label": label, "current": current, "target": target, "pct": pct}, options)

    # 实际是 dict，期望是 list → 包成 list
    if expected == "list" and isinstance(data, dict):
        return render_fn([data], options)

    return render_fn(data, options)


def render_section(section: dict, data: Any, options: dict | None = None) -> str:
    """渲染单个 section。"""
    options = options or {}
    viz_type = section["type"]
    alt_types = section.get("alt_types", [])
    drillable = section.get("drillable", False)
    data_key = section.get("data_key", "")

    render_fn = VIZ_REGISTRY[viz_type]
    # 智能数据形状适配：list → 转为 viz 期望的形状
    body = _adapt_and_render(render_fn, viz_type, data, options)

    # viz switch
    switch_html = ""
    if alt_types:
        switch_html = (
            '<div class="viz-switch" '
            'style="display:flex;gap:4px;margin-bottom:8px;flex-wrap:wrap;">'
        )
        switch_html += (
            f'<button class="viz-btn active" data-viz="{viz_type}">{viz_type}</button>'
        )
        for alt in alt_types:
            switch_html += f'<button class="viz-btn" data-viz="{alt}">{alt}</button>'
        switch_html += "</div>"

    # drill button (vanilla JS - 替代 Alpine.js)
    drill_html = ""
    if drillable:
        drill_html = (
            '<div style="margin-top:8px;">'
            f'<button class="drill-btn" data-key="{data_key}">查看详情</button>'
            f'<div class="drill-panel" data-key="{data_key}"></div>'
            "</div>"
        )

    title_html = ""
    if section.get("title"):
        title_html = f'<h3 style="margin:16px 0 8px 0;">{section["title"]}</h3>'

    return f"""<div class="section" id="sec-{section['key']}">
{title_html}
{switch_html}
{body}
{drill_html}
</div>"""


def render_module(module_key: str, module_cfg: dict, module_data: Any) -> str:
    """渲染单模块（多个 section 拼装）。

    module_data: list[dict]（原始 sheet rows）或 dict[section_key, data]
    """
    sections_html = []
    for section in module_cfg.get("sections", []):
        data_key = section.get("data_key")
        if isinstance(module_data, dict) and data_key:
            data = module_data.get(data_key)
        else:
            data = module_data  # list 形式：所有 section 共用
        sections_html.append(render_section(section, data))

    return f"""<section class="module" id="M-{module_cfg.get('order', '?')}">
<h2>{module_cfg['icon']} {module_cfg['title']}</h2>
<div class="module-body">
{''.join(sections_html)}
</div>
</section>"""
