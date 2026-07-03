"""按分组 + is_total 渲染模块。

新数据流（来自重构后的 Excel）：
- 每个 sheet 是 1 个模块的多分组数据
- 每行：{分组, 名称, 数值, 单位, 备注, 排序, is_total}
- 相同分组 = 同一逻辑组
- is_total=TRUE = 该组总数行

自动 viz 选择：
- 1 行（is_total） → KPI 卡
- 2-3 行（无 is_total） → donut（组成关系）
- 4+ 行（无 is_total） → horizontal bar
- 含 is_total + 子项 → KPI 总数 + bar 子项
- 多列 table sheet → data-table
"""
import math
from typing import Any
from collections import defaultdict


# ====== Helpers ======

def _fmt(v) -> str:
    """格式化数值。"""
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
        try:
            return float(v.rstrip("%").replace(",", ""))
        except (ValueError, AttributeError):
            return 0.0
    return 0.0


def _group_by(rows: list[dict], key: str) -> dict[str, list[dict]]:
    groups = defaultdict(list)
    for r in rows:
        groups[r.get(key, "")].append(r)
    return dict(groups)


def _sort_key(r: dict) -> tuple:
    """按排序字段排序（同序则按名称）。"""
    s = r.get("排序", 0)
    try:
        s = int(s) if s != "" else 0
    except (ValueError, TypeError):
        s = 0
    return (s, r.get("名称", ""))


# ====== Viz 渲染 ======

def _render_kpi(rows: list[dict]) -> str:
    """KPI 卡（1 行 or 多个 is_total）。"""
    if not rows:
        return ""
    items = []
    for r in rows:
        items.append(
            f'<div class="kpi-card">'
            f'<div class="kpi-card-label">{r.get("名称", "")}</div>'
            f'<div class="kpi-card-value">{_fmt(r.get("数值"))}</div>'
            f'<div class="kpi-card-sub">{r.get("备注", "")}</div>'
            f"</div>"
        )
    return f'<div class="kpi-strip-inner">{"".join(items)}</div>'


def _render_donut(rows: list[dict]) -> str:
    """圆环图（2-5 项组成）。"""
    nums = [_to_num(r.get("数值")) for r in rows]
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
        parts.append(f'<path d="{path}" fill="{color}"><title>{r.get("名称","")}: {v/total*100:.1f}%</title></path>')

    legend = "".join(
        f'<div class="donut-leg-row">'
        f'<span class="donut-leg-dot" style="background:{palette[i%len(palette)]}"></span>'
        f'<span class="donut-leg-label">{r.get("名称","")}</span>'
        f'<span class="donut-leg-value">{_fmt(r.get("数值"))}</span>'
        f"</div>"
        for i, r in enumerate(rows)
    )

    return (
        f'<div class="donut-wrap">'
        f'<svg class="donut-svg" viewBox="0 0 120 120">'
        f'<circle cx="60" cy="60" r="50" fill="#f4f4f5"/>'
        f'{"".join(parts)}'
        f'<text x="60" y="58" text-anchor="middle" class="donut-center">{_fmt(rows[0].get("数值"))}</text>'
        f'<text x="60" y="74" text-anchor="middle" class="donut-center-sub">合计</text>'
        f"</svg>"
        f'<div class="donut-legend">{legend}</div>'
        f"</div>"
    )


def _render_bar(rows: list[dict]) -> str:
    """横向柱图（4+ 项）。"""
    nums = [_to_num(r.get("数值")) for r in rows]
    max_v = max(nums) if nums else 1
    tones = ["", "tone-orange", "tone-green", "tone-purple", "tone-cyan", "tone-pink"]
    items = []
    for idx, (r, v) in enumerate(zip(rows, nums)):
        label = r.get("名称", "")
        value = r.get("数值", "")
        unit = r.get("单位", "")
        sub = r.get("备注", "")
        width = (v / max_v * 100) if max_v > 0 else 0
        tone = tones[idx % len(tones)]
        val_str = _fmt(value)
        if unit and not val_str.endswith("%"):
            val_str = f"{val_str} {unit}"
        items.append(
            f'<div class="bar-row">'
            f'<span class="bar-row-label" title="{label}">{label}</span>'
            f'<span class="bar-row-track"><span class="bar-row-fill {tone}" style="width:{width:.1f}%"></span></span>'
            f'<span class="bar-row-value">{val_str}</span>'
            f"</div>"
        )
        if sub:
            items.append(f'<div class="bar-row-sub">{sub}</div>')
    return f'<div class="bar-list">{"".join(items)}</div>'


def _render_table(rows: list[dict]) -> str:
    """多列表（从多列 sheet 来）。"""
    if not rows:
        return ""
    cols = list(rows[0].keys())
    head = "".join(f"<th>{c}</th>" for c in cols)
    body = "".join(
        "<tr>" + "".join(f"<td>{_fmt(r.get(c))}</td>" for c in cols) + "</tr>"
        for r in rows
    )
    return f'<div style="overflow-x:auto;-webkit-overflow-scrolling:touch"><table class="data-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def _render_total_with_sub(total_rows: list[dict], sub_rows: list[dict]) -> str:
    """KPI 总数 + 子项 bar。"""
    kpi = _render_kpi(total_rows)
    bar = _render_bar(sub_rows) if sub_rows else ""
    return f'<div class="total-with-sub">{kpi}{bar}</div>'


# ====== 自动 viz 选择 ======

def _pick_viz(rows: list[dict]) -> str:
    """根据分组结构选择 viz。"""
    if not rows:
        return "empty"

    total_rows = [r for r in rows if str(r.get("is_total", "")).upper() == "TRUE"]
    sub_rows = [r for r in rows if str(r.get("is_total", "")).upper() != "TRUE"]

    # 全部 is_total → KPI
    if total_rows and not sub_rows:
        return "kpi"

    # 有 is_total + sub → KPI + bar
    if total_rows and sub_rows:
        return "total_sub"

    # 1 项（无 is_total）→ KPI
    if len(rows) == 1:
        return "kpi"

    # 2-3 项 → donut
    if 2 <= len(rows) <= 3:
        return "donut"

    # 4+ 项 → bar
    return "bar"


# ====== Section 渲染 ======

def render_group(group_name: str, rows: list[dict], span: int = 6) -> str:
    """渲染单个分组 section。"""
    if not rows:
        return ""
    rows = sorted(rows, key=_sort_key)
    viz = _pick_viz(rows)

    # 渲染 body
    if viz == "kpi":
        body = _render_kpi(rows)
    elif viz == "donut":
        body = _render_donut(rows)
    elif viz == "bar":
        body = _render_bar(rows)
    elif viz == "total_sub":
        total_rows = [r for r in rows if str(r.get("is_total", "")).upper() == "TRUE"]
        sub_rows = [r for r in rows if str(r.get("is_total", "")).upper() != "TRUE"]
        body = _render_total_with_sub(total_rows, sub_rows)
    else:
        body = ""

    return (
        f'<div class="section span-{span}">'
        f'<div class="section-head">'
        f'<span class="section-title"><span class="section-title-dot"></span>{group_name}</span>'
        f'<span class="section-meta">{len(rows)} 项</span>'
        f"</div>"
        f"{body}"
        f"</div>"
    )


def render_table_sheet(rows: list[dict], title: str, span: int = 12) -> str:
    """渲染多列 sheet 为表格。"""
    if not rows:
        return ""
    body = _render_table(rows)
    return (
        f'<div class="section span-{span}">'
        f'<div class="section-head">'
        f'<span class="section-title"><span class="section-title-dot"></span>{title}</span>'
        f'<span class="section-meta">{len(rows)} 行</span>'
        f"</div>"
        f"{body}"
        f"</div>"
    )


def render_kpi_strip(kpis: list[dict]) -> str:
    """顶部 KPI 长条。"""
    if not kpis:
        return ""
    cards = "".join(
        f'<div class="kpi-strip-card">'
        f'<div class="kpi-strip-label">{k.get("label","")}</div>'
        f'<div class="kpi-strip-value">{_fmt(k.get("value",0))}</div>'
        f'<div class="kpi-strip-sub">{k.get("sub","")}</div>'
        f"</div>"
        for k in kpis
    )
    return f'<div class="kpi-strip">{cards}</div>'


def render_module(module_key: str, module_cfg: dict, module_data: list[dict], extra_sheets: dict[str, list[dict]] | None = None) -> str:
    """渲染模块。"""
    extra_sheets = extra_sheets or {}
    groups = _group_by(module_data, "分组")

    sections_html = []
    # 主分组（按 mapping 顺序）
    for group_cfg in module_cfg.get("groups", []):
        gname = group_cfg["name"]
        gspan = group_cfg.get("span", 6)
        rows = groups.get(gname, [])
        rendered = render_group(gname, rows, gspan)
        if rendered:
            sections_html.append(rendered)

    # 额外 sheet（多列表等）
    for sheet_name, span in module_cfg.get("extra_sheets", []):
        rows = extra_sheets.get(sheet_name, [])
        rendered = render_table_sheet(rows, sheet_name.split(" ", 1)[-1] if " " in sheet_name else sheet_name, span)
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
