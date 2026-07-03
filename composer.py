"""按 mapping 渲染模块 - 现代仪表盘 viz。

数据驱动 + 类型检测：
- 2 项占比 → donut
- 3-14 项数字 → bar-list（带 tone 配色）
- 含 Top/Bottom 关键词 → rank-list
- 进度型 → progress bar
- 表格型 → data-table
- 大量同类项 → grid-list
"""
from typing import Any
import math


# ====== 通用 helpers ======

def _format(v) -> str:
    if v is None or v == "":
        return "—"
    if isinstance(v, float):
        if 0 < v < 1:
            return f"{v * 100:.2f}%"
        if abs(v) >= 1000:
            return f"{v:,.0f}"
        return f"{v:,.2f}"
    if isinstance(v, int):
        return f"{v:,}"
    return str(v)


def _to_num(v) -> float:
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.rstrip("%").strip()
        try:
            n = float(s)
            if v.endswith("%"):
                return n / 100
            return n
        except ValueError:
            return 0.0
    return 0.0


def _is_rank(rows: list[dict]) -> bool:
    for r in rows:
        if any(kw in str(r.get("label", "")) for kw in ["Top", "Bottom", "序时"]):
            return True
    return False


def _get_filtered(data: Any, data_key: str) -> list[dict]:
    if isinstance(data, list) and data and isinstance(data[0], dict) and "section" in data[0]:
        return [r for r in data if r.get("section") == data_key]
    return []


# ====== Viz 渲染函数 ======

def _render_bar_list(rows: list[dict]) -> str:
    """横向 bar list：label | bar | value。bar 长度按值归一化。"""
    nums = [_to_num(r.get("value")) for r in rows]
    max_v = max(nums) if nums else 1
    tones = ["", "tone-orange", "tone-green", "tone-purple", "tone-cyan"]
    items = []
    for idx, (r, v) in enumerate(zip(rows, nums)):
        label = r.get("label", "")
        value = r.get("value", "")
        sub = r.get("sub", "")
        width = (v / max_v * 100) if max_v > 0 else 0
        tone = tones[idx % len(tones)]
        items.append(
            f'<div class="bar-row">'
            f'<span class="bar-row-label" title="{label}">{label}</span>'
            f'<span class="bar-row-track"><span class="bar-row-fill {tone}" style="width:{width:.1f}%"></span></span>'
            f'<span class="bar-row-value">{_format(value)}</span>'
            f"</div>"
        )
        if sub:
            items.append(f'<div class="bar-row-sub">{sub}</div>')
    return f'<div class="bar-list">{"".join(items)}</div>'


def _render_donut(rows: list[dict]) -> str:
    """圆环图 + 图例。"""
    nums = [_to_num(r.get("value")) for r in rows]
    total = sum(nums) or 1
    palette = ["#4f46e5", "#f97316", "#10b981", "#8b5cf6", "#06b6d4", "#ec4899", "#f59e0b", "#ef4444"]

    cx, cy, r_outer, r_inner = 60, 60, 50, 32
    parts = []
    cum = 0.0
    for i, (r, v) in enumerate(zip(rows, nums)):
        if v <= 0:
            continue
        cum += v
        a1 = (cum - v) / total * 2 * math.pi - math.pi / 2
        a2 = cum / total * 2 * math.pi - math.pi / 2
        x1o, y1o = cx + r_outer * math.cos(a1), cy + r_outer * math.sin(a1)
        x2o, y2o = cx + r_outer * math.cos(a2), cy + r_outer * math.sin(a2)
        x1i, y1i = cx + r_inner * math.cos(a1), cy + r_inner * math.sin(a1)
        x2i, y2i = cx + r_inner * math.cos(a2), cy + r_inner * math.sin(a2)
        large = 1 if v / total > 0.5 else 0
        color = palette[i % len(palette)]
        path = (
            f"M {x1o:.1f} {y1o:.1f} A {r_outer} {r_outer} 0 {large} 1 {x2o:.1f} {y2o:.1f} "
            f"L {x2i:.1f} {y2i:.1f} A {r_inner} {r_inner} 0 {large} 0 {x1i:.1f} {y1i:.1f} Z"
        )
        parts.append(f'<path d="{path}" fill="{color}"><title>{r.get("label","")}: {v/total*100:.1f}%</title></path>')

    legend = "".join(
        f'<div class="donut-leg-row">'
        f'<span class="donut-leg-dot" style="background:{palette[i%len(palette)]}"></span>'
        f'<span class="donut-leg-label">{r.get("label","")}</span>'
        f'<span class="donut-leg-value">{_format(r.get("value",0))}</span>'
        f"</div>"
        for i, r in enumerate(rows)
    )

    total_label = _format(rows[0].get("value")) if len(rows) == 2 else f"{len(rows)} 项"
    return (
        f'<div class="donut-wrap">'
        f'<svg class="donut-svg" viewBox="0 0 120 120">'
        f'<circle cx="60" cy="60" r="50" fill="#f4f4f5"/>'
        f'{"".join(parts)}'
        f'<text class="donut-center" x="60" y="58" text-anchor="middle">{total_label}</text>'
        f'<text class="donut-center-sub" x="60" y="74" text-anchor="middle">合计</text>'
        f"</svg>"
        f'<div class="donut-legend">{legend}</div>'
        f"</div>"
    )


def _render_progress(rows: list[dict]) -> str:
    """进度条列表。"""
    items = []
    for r in rows:
        label = r.get("label", "")
        value = r.get("value", "")
        sub = r.get("sub", "")
        pct = _to_num(value) if (isinstance(value, str) and value.endswith("%")) else 0
        if pct == 0 and isinstance(value, (int, float)) and value <= 1:
            pct = value
        tone = "tone-good" if pct >= 0.8 else ("tone-warn" if pct >= 0.5 else "tone-bad")
        items.append(
            f'<div class="prog-row">'
            f'<div class="prog-row-head">'
            f'<span class="prog-row-label" title="{label}">{label}</span>'
            f'<span class="prog-row-value">{_format(value)}</span>'
            f"</div>"
            f'<div class="prog-row-bar"><span class="prog-row-fill {tone}" style="width:{pct*100:.1f}%"></span></div>'
            f"</div>"
        )
    return f'<div class="prog-list">{"".join(items)}</div>'


def _render_rank(rows: list[dict]) -> str:
    """排名列表（gold/silver/bronze badge）。"""
    items = []
    for i, r in enumerate(rows):
        rank = i + 1
        badge_class = {1: "gold", 2: "silver", 3: "bronze"}.get(rank, "")
        items.append(
            f'<div class="rank-row">'
            f'<span class="rank-badge {badge_class}">{rank}</span>'
            f'<span class="rank-label">{r.get("label","")}</span>'
            f'<span class="rank-value">{_format(r.get("value",""))}</span>'
            f"</div>"
        )
    return f'<div class="rank-list">{"".join(items)}</div>'


def _render_grid_list(rows: list[dict]) -> str:
    """网格列表（适合网点等多同类项）。"""
    items = "".join(
        f'<div class="grid-item">'
        f'<span class="grid-item-label">{r.get("label","")}</span>'
        f'<span class="grid-item-value">{_format(r.get("value",0))}</span>'
        f"</div>"
        for r in rows
    )
    return f'<div class="grid-list">{items}</div>'


def _render_stat_cards(rows: list[dict]) -> str:
    """Stat 卡片组（适合 3-4 个核心数字）。"""
    if not rows:
        return ""
    inner = "".join(
        f'<div class="stat-card">'
        f'<div class="stat-card-label">{r.get("label","")}</div>'
        f'<div class="stat-card-value">{_format(r.get("value",0))}</div>'
        f'<div class="stat-card-sub">{r.get("sub","")}</div>'
        f"</div>"
        for r in rows
    )
    return f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px">{inner}</div>'


def _render_table(data_key: str, full_data: list) -> str:
    """表格。"""
    rows = _get_filtered(full_data, data_key)
    if not rows:
        return ""
    cols = [k for k in rows[0].keys() if k != "section"]
    head = "".join(f"<th>{c}</th>" for c in cols)
    body = "".join(
        "<tr>" + "".join(f"<td>{_format(r.get(c))}</td>" for c in cols) + "</tr>"
        for r in rows
    )
    return f'<div style="overflow-x:auto;-webkit-overflow-scrolling:touch"><table class="data-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


# ====== Section 渲染主逻辑 ======

def render_section(section: dict, data: Any) -> str:
    """根据 section + data 自动选 viz。"""
    data_key = section.get("data_key", "")
    section_type = section.get("type", "stats")
    title = section.get("title", "")
    span = section.get("span", 6)

    rows = _get_filtered(data, data_key) if section_type != "table" else []

    if section_type == "table":
        body = _render_table(data_key, data if isinstance(data, list) else [])
        if not body:
            return ""
    elif section_type == "hierarchy" or (rows and len(rows) >= 12 and all(isinstance(r.get("value"), (int, float)) for r in rows)):
        body = _render_grid_list(rows)
    elif _is_rank(rows):
        body = _render_rank(rows)
    elif len(rows) == 2:
        body = _render_donut(rows)
    elif 3 <= len(rows) <= 4 and all(str(r.get("value", "")).endswith("%") for r in rows):
        body = _render_progress(rows)
    elif 3 <= len(rows) <= 14:
        body = _render_bar_list(rows)
    else:
        body = _render_stat_cards(rows) if rows else ""

    if not body:
        return ""

    return (
        f'<div class="section span-{span}">'
        f'<div class="section-head">'
        f'<span class="section-title"><span class="section-title-dot"></span>{title}</span>'
        f'<span class="section-meta">{len(rows)} 项</span>'
        f"</div>"
        f"{body}"
        f"</div>"
    )


def render_module(module_key: str, module_cfg: dict, module_data: Any) -> str:
    sections_html = []
    for section in module_cfg.get("sections", []):
        rendered = render_section(section, module_data)
        if rendered:
            sections_html.append(rendered)
    icon = module_cfg.get("icon", "")
    title = module_cfg.get("title", "")
    sub = module_cfg.get("sub", "")
    return (
        f'<section class="module">'
        f'<div class="module-head">'
        f'<div class="module-icon">{icon}</div>'
        f'<div><div class="module-title">{title}</div>'
        f'<div class="module-sub">{sub}</div>'
        f"</div>"
        f"</div>"
        f'<div class="module-body">{"".join(sections_html)}</div>'
        f"</section>"
    )


def render_kpi_strip(kpis: list[dict]) -> str:
    """顶部 KPI 长条。"""
    if not kpis:
        return ""
    cards = "".join(
        f'<div class="kpi-strip-card">'
        f'<div class="kpi-strip-label">{k.get("label","")}</div>'
        f'<div class="kpi-strip-value">{_format(k.get("value",0))}</div>'
        f'<div class="kpi-strip-sub">{k.get("sub","")}</div>'
        f"</div>"
        for k in kpis
    )
    return f'<div class="kpi-strip">{cards}</div>'
