"""按 mapping 渲染模块 - 智能 viz 选择 + 紧凑布局。

数据类型自动检测：
- 占比分布（4+ 行 + 百分比）→ 紧凑水平柱图
- 占比少（2-3 行）→ 紧凑圆环
- 单值 vs 目标 → 紧凑进度条
- 多列结构 → 表格
- 排名（数字 + 描述）→ 排名列表
"""
from typing import Any

from viz import VIZ_REGISTRY


# ====== 数据类型检测 ======

def _is_pct(v) -> bool:
    """检测是否为百分比。"""
    if isinstance(v, float) and 0 <= v <= 1:
        return True
    if isinstance(v, str) and v.endswith("%"):
        try:
            float(v.rstrip("%"))
            return True
        except ValueError:
            return False
    return False


def _to_pct(v) -> float:
    """统一转为 0-1 浮点。"""
    if isinstance(v, float):
        return v
    if isinstance(v, str) and v.endswith("%"):
        return float(v.rstrip("%")) / 100
    return 0.0


def _infer_chart_type(rows: list[dict]) -> str:
    """根据数据形状推断最适合的 viz。"""
    if not rows:
        return "empty"

    # 排名数据优先
    if _is_rank_data(rows):
        return "rank"

    # 2 项 → pie
    if len(rows) == 2:
        return "pie"

    # 3-12 项数字 → bar
    if 3 <= len(rows) <= 14:
        return "bar"

    # 14+ → list（太多放不下 bar）
    return "list"


def _format_value(v) -> str:
    if v is None or v == "":
        return "—"
    if isinstance(v, float):
        if 0 < v < 1:
            return f"{v * 100:.2f}%"
        return f"{v:,.2f}"
    if isinstance(v, int):
        return f"{v:,}"
    return str(v)


def _is_rank_data(rows: list[dict]) -> bool:
    """检测是否为排名数据（含 Top/Bottom 关键词或大百分比）。"""
    for r in rows:
        label = str(r.get("label", ""))
        if any(kw in label for kw in ["Top", "Bottom", "序时"]):
            return True
    return False


# ====== Viz 渲染（紧凑版）======

def _render_mini_bar(rows: list[dict]) -> str:
    """紧凑水平柱图：label | bar | value。bar 宽度按值归一化。"""
    # 提取数值
    nums = []
    for r in rows:
        v = r.get("value", 0)
        if isinstance(v, (int, float)):
            nums.append(float(v))
        elif _is_pct(v):
            nums.append(_to_pct(v) * 100)
        else:
            nums.append(1)
    max_v = max(nums) if nums else 1
    items = []
    for r, v in zip(rows, nums):
        label = r.get("label", "")
        value = r.get("value", "")
        sub = r.get("sub", "")
        width = (v / max_v * 100) if max_v > 0 else 0
        items.append(
            f'<div class="mini-bar-row">'
            f'<span class="mini-bar-label" title="{label}">{label}</span>'
            f'<span class="mini-bar-track"><span class="mini-bar-fill" style="width:{width:.1f}%"></span></span>'
            f'<span class="mini-bar-value">{_format_value(value)}</span>'
            f'<span class="mini-bar-sub">{sub}</span>'
            f"</div>"
        )
    return f'<div class="mini-bar">{"".join(items)}</div>'


def _render_mini_pie(rows: list[dict]) -> str:
    """紧凑圆环：SVG + 图例。"""
    import math

    nums = []
    for r in rows:
        v = r.get("value", 0)
        if isinstance(v, (int, float)):
            nums.append(float(v))
        elif _is_pct(v):
            nums.append(_to_pct(v) * 100)
        else:
            nums.append(1)
    total = sum(nums) or 1
    palette = ["#1e5baa", "#f97316", "#10b981", "#8b5cf6", "#06b6d4", "#f59e0b", "#ef4444", "#84cc16"]

    cx, cy, r_outer, r_inner = 50, 50, 42, 26
    parts = []
    cum = 0.0
    for i, (r, v) in enumerate(zip(rows, nums)):
        if v <= 0:
            continue
        cum += v
        a1 = (cum - v) / total * 2 * math.pi
        a2 = cum / total * 2 * math.pi
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
        parts.append(
            f'<path d="{path}" fill="{color}"><title>{r.get("label","")}: {v/max(nums)*100 if max(nums) else 0:.1f}%</title></path>'
        )

    legend = "".join(
        f'<div class="mini-pie-leg-item">'
        f'<span class="mini-pie-dot" style="background:{palette[i%len(palette)]}"></span>'
        f'<span class="mini-pie-leg-label">{r.get("label","")}</span>'
        f'<span class="mini-pie-leg-value">{_format_value(r.get("value",0))}</span>'
        f"</div>"
        for i, r in enumerate(rows)
    )

    return (
        f'<div class="mini-pie">'
        f'<svg width="100" height="100" viewBox="0 0 100 100">{"".join(parts)}</svg>'
        f'<div class="mini-pie-legend">{legend}</div>'
        f"</div>"
    )


def _render_progress(rows: list[dict]) -> str:
    """进度条：单行 (label) + bar + 数字。"""
    items = []
    for r in rows:
        label = r.get("label", "")
        value = r.get("value", "")
        sub = r.get("sub", "")
        pct = _to_pct(value) if _is_pct(value) else 0
        tone = "good" if pct >= 0.8 else ("warn" if pct >= 0.5 else "bad")
        items.append(
            f'<div class="prog-row">'
            f'<span class="prog-label">{label}</span>'
            f'<span class="prog-track"><span class="prog-fill tone-{tone}" style="width:{pct*100:.1f}%"></span></span>'
            f'<span class="prog-value">{_format_value(value)}</span>'
            f'<span class="prog-sub">{sub}</span>'
            f"</div>"
        )
    return f'<div class="prog">{"".join(items)}</div>'


def _render_ranking(rows: list[dict]) -> str:
    """排名列表：rank badge + label + value。"""
    items = []
    for i, r in enumerate(rows):
        rank = i + 1
        badge_class = f"rank-{min(rank, 3)}"
        items.append(
            f'<div class="rank-row">'
            f'<span class="rank-badge {badge_class}">{rank}</span>'
            f'<span class="rank-label">{r.get("label","")}</span>'
            f'<span class="rank-value">{_format_value(r.get("value",""))}</span>'
            f'<span class="rank-sub">{r.get("sub","")}</span>'
            f"</div>"
        )
    return f'<div class="rank">{"".join(items)}</div>'


def _render_list(rows: list[dict]) -> str:
    """纯列表（无百分比或特殊模式）。"""
    items = []
    for r in rows:
        items.append(
            f'<div class="list-row">'
            f'<span class="list-label">{r.get("label","")}</span>'
            f'<span class="list-value">{_format_value(r.get("value",""))}</span>'
            f'<span class="list-sub">{r.get("sub","")}</span>'
            f"</div>"
        )
    return f'<div class="list">{"".join(items)}</div>'


def _render_table(data_key: str, full_data: list) -> str:
    """表格（多列结构）。"""
    rows = [r for r in full_data if r.get("section") == data_key]
    if not rows:
        return ""
    cols = [k for k in rows[0].keys() if k != "section"]
    head = "".join(f"<th>{c}</th>" for c in cols)
    body = "".join(
        "<tr>" + "".join(f"<td>{_format_value(r.get(c))}</td>" for c in cols) + "</tr>"
        for r in rows
    )
    return f'<div class="table-wrap"><table class="data-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


# ====== Section 渲染主逻辑 ======

def render_section(section: dict, data: Any) -> str:
    """渲染 section：根据数据自动选 viz。"""
    data_key = section.get("data_key", "")
    section_type = section.get("type", "stats")
    title = section.get("title", "")

    if isinstance(data, list) and data and isinstance(data[0], dict) and "section" in data[0]:
        rows = [r for r in data if r.get("section") == data_key]
    else:
        rows = []

    if not rows:
        return ""

    if section_type == "table":
        body = _render_table(data_key, data)
    elif section_type == "hierarchy":
        items = "".join(
            f'<div class="h-row">'
            f'<span class="h-name">{r.get("label","")}</span>'
            f'<span class="h-count">{_format_value(r.get("value",0))}</span>'
            f'<span class="h-sub">{r.get("sub","")}</span>'
            f"</div>"
            for r in rows
        )
        body = f'<div class="h-list">{items}</div>'
    else:
        # 智能选 viz
        chart_type = _infer_chart_type(rows)
        if _is_rank_data(rows):
            body = _render_ranking(rows)
        elif chart_type == "pie":
            body = _render_mini_pie(rows)
        elif chart_type == "bar":
            body = _render_mini_bar(rows)
        elif chart_type == "list":
            body = _render_list(rows)
        else:
            body = _render_list(rows)

    return f'<div class="section"><h3 class="section-title">{title}</h3>{body}</div>'


def render_module(module_key: str, module_cfg: dict, module_data: Any) -> str:
    sections_html = []
    for section in module_cfg.get("sections", []):
        rendered = render_section(section, module_data)
        if rendered:
            sections_html.append(rendered)
    icon = module_cfg.get("icon", "")
    title = module_cfg.get("title", "")
    return (
        f'<section class="module" id="M-{module_cfg.get("order","?")}">'
        f"<h2><span class='icon'>{icon}</span>{title}</h2>"
        f'<div class="module-body">{"".join(sections_html)}</div>'
        f"</section>"
    )
