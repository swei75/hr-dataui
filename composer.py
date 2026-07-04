"""按分组 + is_total 渲染模块。

新数据流（来自重构后的 Excel）：
- 每个 sheet 是 1 个模块的多分组数据
- 每行：{分组, 名称, 数值, 单位, 备注, 排序, is_total, delta?, sub_text?, metric_note?}
- 相同分组 = 同一逻辑组
- is_total=TRUE = 该组总数行

v1.4 新增：
- delta 自动计算（基于 _prev sheet）
- sub_text → 2 栏 narrative 渲染
- metric_note → KPI 卡底部说明
- 完成率 → data-category 风险等级
- M-2 含"员工 × 司龄" → heatmap

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


# ====== v1.4 delta 计算 ======

def calc_delta(current: float, prev: float | None) -> dict | None:
    """v1.4: 计算环比 delta。

    Returns: {"abs": diff, "pct": ratio, "direction": up/down/flat, "display": "+25.0%"} or None.
    """
    if prev is None or prev == 0:
        return None
    diff = current - prev
    pct = diff / abs(prev)
    if diff > 0:
        direction = "up"
        display = f"+{pct * 100:.1f}%"
    elif diff < 0:
        direction = "down"
        display = f"{pct * 100:.1f}%"
    else:
        direction = "flat"
        display = "0.0%"
    return {"abs": diff, "pct": pct, "direction": direction, "display": display}


def classify_rate(value: float, target: float = 100.0) -> str:
    """v1.4: 完成率分级（spec §3.3）。

    - value >= 100% → success（达成）
    - value >= 90% 且 < 100% → warning（接近）
    - value < 90% → danger（异常）
    """
    if value >= target:
        return "success"
    if value >= target * 0.9:
        return "warning"
    return "danger"


def _infer_target(value: float, unit: str) -> float | None:
    """推断完成率目标值。单位 "%" 或 名称含 "完成率" → 目标 = 100%. """
    if unit and "%" in str(unit):
        return 100.0
    return None


# ====== Viz 渲染 ======

def _render_kpi(rows: list[dict]) -> str:
    """KPI 卡（1 行 or 多个 is_total）。

    v1.4: data-category 风险等级 + metric_note + delta 徽章。
    """
    if not rows:
        return ""
    items = []
    for r in rows:
        value = _to_num(r.get("数值"))
        unit = r.get("单位", "")
        target = _infer_target(value, unit)
        category = ""
        if target is not None and str(r.get("is_total", "")).upper() == "TRUE":
            category = classify_rate(value, target)
        delta_html = ""
        delta = r.get("delta")
        if isinstance(delta, dict):
            direction = delta.get("direction", "flat")
            css_class = f"trend-{direction}"
            delta_html = f'<span class="{css_class} kpi-card-delta">{delta.get("display","")}</span>'
        note_html = ""
        if r.get("metric_note"):
            note_html = f'<p class="kpi-note">{r["metric_note"]}</p>'
        attrs = f' data-category="{category}"' if category else ""
        items.append(
            f'<div class="kpi-card"{attrs}>'
            f'<div class="kpi-card-label">{r.get("名称", "")}</div>'
            f'<div class="kpi-card-value">{_fmt(r.get("数值"))}</div>'
            f'<div class="kpi-card-sub">{r.get("备注", "")}{delta_html}</div>'
            f"{note_html}"
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
    """纯文本列表（v1.4.1：去掉色条，避免视觉干扰）。"""
    items = []
    for r in rows:
        label = r.get("名称", "")
        value = r.get("数值", "")
        unit = r.get("单位", "")
        sub = r.get("备注", "")
        val_str = _fmt(value)
        if unit and not val_str.endswith("%"):
            val_str = f"{val_str} {unit}"
        items.append(
            f'<div class="bar-row">'
            f'<span class="bar-row-label">{label}</span>'
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


# ====== v1.4 Heatmap（员工 × 司龄 二维） ======

def _try_render_heatmap(group_name: str, rows: list[dict]) -> str | None:
    """M-2 含 '员工 × 司龄' 二维数据时调用 render_heatmap（lazy import）。"""
    if "员工" not in group_name or "司龄" not in group_name:
        return None
    try:
        from viz.heatmap import render_heatmap
    except ImportError:
        return None
    # 期望 records: [{'row': '员工-产品经理', 'col': '司龄-3-5年', 'value': 0.85, 'level': 'success'}, ...]
    cells = []
    for r in rows:
        value = _to_num(r.get("数值"))
        if value <= 1:  # 0-1 浮点占比
            level = classify_rate(value * 100, 100)
        else:
            level = classify_rate(value, 100)
        cells.append({
            "row": f"员工-{r.get('名称','')}",
            "col": group_name,
            "value": value,
            "level": level,
        })
    return render_heatmap(cells, {"row_labels": [c["row"] for c in cells], "col_labels": [group_name]})


# ====== 自动 viz 选择 ======

def _pick_viz(rows: list[dict], group_name: str = "") -> str:
    """根据分组结构选择 viz。"""
    if not rows:
        return "empty"

    # v1.4: M-2 员工 × 司龄 → heatmap
    if group_name and "员工" in group_name and "司龄" in group_name:
        heatmap = _try_render_heatmap(group_name, rows)
        if heatmap:
            return "heatmap"

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

    # 2-5 项 → donut（v1.4.2：扩展范围，>5 项才走纯文本）
    if 2 <= len(rows) <= 5:
        return "donut"

    # 6+ 项 → 纯文本列表（v1.4.1：_render_bar 已输出纯文本）
    return "bar"


# ====== Section 渲染 ======

def render_group(group_name: str, rows: list[dict], span: int = 6) -> str:
    """渲染单个分组 section。"""
    if not rows:
        return ""
    rows = sorted(rows, key=_sort_key)
    viz = _pick_viz(rows, group_name)

    # 渲染 body
    if viz == "heatmap":
        heatmap_html = _try_render_heatmap(group_name, rows) or ""
        body = heatmap_html
    elif viz == "kpi":
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
    """v1.5.19: 顶部 KPI 长条（v_hero 数字塔风格，与模块内 KPI 卡区分）。"""
    if not kpis:
        return ""
    cards = "".join(
        f'<div class="kpi-hero-card">'
        f'<div class="kpi-hero-icon">{k.get("icon","")}</div>'
        f'<div class="kpi-hero-body">'
        f'<div class="kpi-hero-label">{k.get("label","")}</div>'
        f'<div class="kpi-hero-value">{_fmt(k.get("value",0))}<span class="kpi-hero-unit">{k.get("unit","")}</span></div>'
        f'<div class="kpi-hero-sub">{k.get("sub","")}</div>'
        f'</div>'
        f'<div class="kpi-hero-bar"></div>'
        f"</div>"
        for k in kpis
    )
    return f'<section class="kpi-hero">{cards}</section>'


def render_narrative_block(sub_text: str) -> str:
    """v1.4: 2 栏 narrative 渲染（关键洞察 / 口径假设）。"""
    if not sub_text:
        return ""
    return (
        f'<div class="narrative-grid">'
        f'<div class="narrative-col">'
        f'<h3 class="narrative-h">关键洞察</h3>'
        f'<p>{sub_text}</p>'
        f"</div>"
        f'<div class="narrative-col">'
        f'<h3 class="narrative-h">口径假设</h3>'
        f'<p class="narrative-muted">以当期披露口径为准；合并/剔除项详见数据契约 §8。</p>'
        f"</div>"
        f"</div>"
    )


def _extract_module_sub_text(module_data: list[dict]) -> str:
    """从模块数据中提取首个非空 sub_text。"""
    for r in module_data:
        sub = r.get("sub_text")
        if sub:
            return str(sub)
    return ""


def _apply_deltas(module_data: list[dict], prev_records: list[dict]) -> None:
    """v1.4: 计算并写入 delta。"""
    if not prev_records:
        return
    # 按 (名称, 单位) 索引 prev
    prev_index = {}
    for p in prev_records:
        key = (p.get("名称", ""), p.get("单位", ""))
        prev_index[key] = _to_num(p.get("数值"))
    for r in module_data:
        key = (r.get("名称", ""), r.get("单位", ""))
        prev_value = prev_index.get(key)
        current = _to_num(r.get("数值"))
        if prev_value is not None:
            r["delta"] = calc_delta(current, prev_value)


def render_module(module_key: str, module_cfg: dict, module_data: list[dict], extra_sheets: dict[str, list[dict]] | None = None, prev_records: list[dict] | None = None) -> str:
    """渲染模块。

    v1.4 新增：
    - prev_records: 上期数据 → 计算 delta
    - 模块内首个 sub_text → 顶部 narrative
    """
    extra_sheets = extra_sheets or {}

    # 应用 delta
    _apply_deltas(module_data, prev_records or [])

    groups = _group_by(module_data, "分组")

    # v1.5.2: KPI 卡优先（M-1 用 v1 设计：6 KPI + 段落，跳过分组渲染）
    kpi_cards_html = ""
    kpi_cards_cfg = module_cfg.get("kpi_cards", [])
    if kpi_cards_cfg:
        cards = []
        for card in kpi_cards_cfg:
            category = card.get("category", "")
            cat_attr = f' data-category="{category}"' if category else ""
            cards.append(
                f'<article class="kpi-card-m1"{cat_attr}>'
                f'<div class="kpi-card-m1-label">{card.get("label","")}</div>'
                f'<div class="kpi-card-m1-value">{card.get("value","")}<span class="kpi-card-m1-unit">{card.get("unit","")}</span></div>'
                f'<div class="kpi-card-m1-sub">{card.get("sub","")}</div>'
                f"</article>"
            )
        kpi_cards_html = f'<div class="kpi-cards-row">{"".join(cards)}</div>'

    sections_html = []
    # 主分组（按 mapping 顺序）— kpi_cards 模块跳过
    if not kpi_cards_cfg:
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
    featured_attr = ' data-featured="true"' if module_cfg.get("featured") else ""

    # v1.4 narrative 块
    narrative = render_narrative_block(_extract_module_sub_text(module_data))

    # v1.5: 模块级段落叙述（嵌在 module-head 后）
    sub_text_for_narrative = _extract_module_sub_text(module_data)

    # v1.5.4: v1 风格 narrative 卡片（M-1 用：独立米色卡片 + h2 + 多段 strong 文字）
    module_narrative_cfg = module_cfg.get("narrative")
    is_v1_style = isinstance(module_narrative_cfg, list) and module_narrative_cfg

    # v1.5.9: v11 风格数据检测（M-2 用：4 KPI + 5 段 stacked 卡片 + 8 客户/客服网格）
    kpi_quad = module_cfg.get("kpi_quad", [])
    dim_cards = module_cfg.get("dim_cards", [])
    cs_grid = module_cfg.get("cs_grid", [])
    is_v11_style = bool(module_narrative_cfg) and bool(kpi_quad) and bool(dim_cards) and bool(cs_grid)

    # v1.5.10: v_hr 风格检测（M-3 用：v1 gauge + v2 整体 + v3 双轴对比）
    gauges = module_cfg.get("gauges", [])
    flow_nodes = module_cfg.get("flow_nodes", [])
    dual_bars = module_cfg.get("dual_bars", [])
    rank_top3 = module_cfg.get("rank_top3", {})
    rank_bottom3 = module_cfg.get("rank_bottom3", {})
    exit_bars = module_cfg.get("exit_bars", [])
    case_cards = module_cfg.get("case_cards", [])
    is_v_hr_style = bool(module_narrative_cfg) and (bool(gauges) or bool(flow_nodes) or bool(dual_bars))

    # v1.5.13: v2 分类树风格检测（M-4 用）
    tree = module_cfg.get("tree", {})
    is_v_tree_style = bool(module_narrative_cfg) and bool(tree)

    # v1.5.14: v1 财务大卡风格检测（M-5 用）
    fc_cards = module_cfg.get("fc_cards", [])
    is_v_fc_style = bool(module_narrative_cfg) and bool(fc_cards)

    # v1.5.17: v_train 风格检测（M-6 用：v1 顶部 6 大卡 + v8 主体）
    kpi_cards_v1 = module_cfg.get("kpi_cards_v1", [])
    heatmap_months = module_cfg.get("heatmap_months", [])
    is_v_train_style = bool(module_narrative_cfg) and bool(kpi_cards_v1)

    module_intro = ""
    module_body_content = ""
    module_head_html = ""

    if is_v_train_style:
        # v1.5.17: v_train（v1 顶部 6 大卡 + v8 热力图 + 时间线 + 部门对）
        if "、" in title:
            badge, rest = title.split("、", 1)
            h2_content = f'<span class="narrative-icon">{icon}</span><span class="narrative-badge">{badge}</span>、{rest}'
        else:
            h2_content = f'<span class="narrative-icon">{icon}</span>{title}'
        paras = "".join(f"<p>{p}</p>" for p in module_narrative_cfg)
        narrative_card_html = f'<section class="module-narrative-card">{paras}</section>'
        module_intro = (
            f'<div class="module-narrative-head">'
            f'<h2 class="narrative-h2">{h2_content}</h2>'
            f'</div>'
            f'{narrative_card_html}'
        )

        # v1 风格 6 大卡
        v1_cards_html = []
        for c in kpi_cards_v1:
            v1_cards_html.append(
                f'<article class="kpi-card-m6">'
                f'<div class="hd"><div class="left"><span class="ic">{c.get("ic","")}</span><span class="ttl">{c.get("ttl","")}</span></div></div>'
                f'<span class="delta {c.get("delta","")}">{c.get("delta_text","")}</span>'
                f'<div class="num-row"><span class="num">{c.get("num","")}</span><span class="unit">{c.get("unit","")}</span></div>'
                f'<div class="ft"><span>累计</span><span class="tag {c.get("ft_tag","")}">{c.get("ft_text","")}</span></div>'
                f'</article>'
            )
        v1_section = f'<section class="card-wall-m6">{"".join(v1_cards_html)}</section>'

        # v8 热力图
        heat_cells = "".join(
            f'<div class="month {m["heat"]}"><div class="m">{m["m"]}</div><div class="v">{m["v"]}</div></div>'
            for m in heatmap_months
        )
        heatmap_html = (
            f'<section class="heatmap-block">'
            f'<div class="block-head"><h3>月度培训热力图 <span class="pill">1-12 月</span></h3><span class="hint">颜色越深 = 培训场次越多</span></div>'
            f'<div class="heat-grid"><div class="yl">培训场次</div>{heat_cells}</div>'
            f'</section>'
        )

        # v8 时间线 SVG（12 月里程碑）
        rail_svg = '''<svg class="rail-svg" viewBox="0 0 1100 240" xmlns="http://www.w3.org/2000/svg">
<line x1="40" y1="130" x2="1060" y2="130" stroke="#6b4423" stroke-width="2.5"/>
<g font-family="SF Mono,Consolas,monospace" font-size="11" fill="#7b6653" text-anchor="middle">
<line x1="80" y1="125" x2="80" y2="135" stroke="#7b6653" stroke-width="1"/><text x="80" y="148">1</text>
<line x1="165" y1="125" x2="165" y2="135" stroke="#7b6653" stroke-width="1"/><text x="165" y="148">2</text>
<line x1="250" y1="125" x2="250" y2="135" stroke="#7b6653" stroke-width="1"/><text x="250" y="148">3</text>
<line x1="335" y1="125" x2="335" y2="135" stroke="#7b6653" stroke-width="1"/><text x="335" y="148">4</text>
<line x1="420" y1="125" x2="420" y2="135" stroke="#7b6653" stroke-width="1"/><text x="420" y="148">5</text>
<line x1="505" y1="125" x2="505" y2="135" stroke="#7b6653" stroke-width="1"/><text x="505" y="148">6</text>
<line x1="590" y1="125" x2="590" y2="135" stroke="#7b6653" stroke-width="1"/><text x="590" y="148">7</text>
<line x1="675" y1="125" x2="675" y2="135" stroke="#7b6653" stroke-width="1"/><text x="675" y="148">8</text>
<line x1="760" y1="125" x2="760" y2="135" stroke="#7b6653" stroke-width="1"/><text x="760" y="148">9</text>
<line x1="845" y1="125" x2="845" y2="135" stroke="#7b6653" stroke-width="1"/><text x="845" y="148">10</text>
<line x1="930" y1="125" x2="930" y2="135" stroke="#7b6653" stroke-width="1"/><text x="930" y="148">11</text>
<line x1="1015" y1="125" x2="1015" y2="135" stroke="#7b6653" stroke-width="1"/><text x="1015" y="148">12</text>
</g>
<line x1="420" y1="115" x2="420" y2="145" stroke="#c9b299" stroke-width="1" stroke-dasharray="2,2"/>
<line x1="760" y1="115" x2="760" y2="145" stroke="#c9b299" stroke-width="1" stroke-dasharray="2,2"/>
<g font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="10" fill="#9f6b44" text-anchor="middle" font-weight="600">
<text x="420" y="170">H1</text><text x="760" y="170">H2</text>
</g>
<line x1="80" y1="130" x2="80" y2="70" stroke="#6b4423" stroke-width="1.5"/>
<circle cx="80" cy="60" r="6" fill="#6b4423" stroke="#fefcf7" stroke-width="2"/>
<text x="80" y="42" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="11" fill="#241b15" text-anchor="middle" font-weight="600">5 期 广银大讲堂</text>
<text x="80" y="55" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="9.5" fill="#7b6653" text-anchor="middle">Q1 季度排</text>
<line x1="250" y1="130" x2="250" y2="70" stroke="#6b4423" stroke-width="1.5"/>
<circle cx="250" cy="60" r="6" fill="#6b4423" stroke="#fefcf7" stroke-width="2"/>
<text x="250" y="42" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="11" fill="#241b15" text-anchor="middle" font-weight="600">2 期 对公特训营</text>
<text x="250" y="55" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="9.5" fill="#7b6653" text-anchor="middle">3 月</text>
<line x1="335" y1="130" x2="335" y2="70" stroke="#6b4423" stroke-width="1.5"/>
<circle cx="335" cy="60" r="6" fill="#6b4423" stroke="#fefcf7" stroke-width="2"/>
<text x="335" y="42" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="11" fill="#241b15" text-anchor="middle" font-weight="600">4 期 办贷火线班</text>
<text x="335" y="55" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="9.5" fill="#7b6653" text-anchor="middle">4 月</text>
<line x1="420" y1="130" x2="420" y2="70" stroke="#6b4423" stroke-width="1.5"/>
<circle cx="420" cy="60" r="6" fill="#6b4423" stroke="#fefcf7" stroke-width="2"/>
<text x="420" y="42" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="11" fill="#241b15" text-anchor="middle" font-weight="600">3 期 个贷铁军</text>
<text x="420" y="55" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="9.5" fill="#7b6653" text-anchor="middle">5 月</text>
<line x1="505" y1="130" x2="505" y2="70" stroke="#6b4423" stroke-width="1.5"/>
<circle cx="505" cy="60" r="6" fill="#6b4423" stroke="#fefcf7" stroke-width="2"/>
<text x="505" y="42" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="11" fill="#241b15" text-anchor="middle" font-weight="600">1 期 校招新员工</text>
<text x="505" y="55" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="9.5" fill="#7b6653" text-anchor="middle">6 月</text>
<line x1="590" y1="130" x2="590" y2="200" stroke="#a04030" stroke-width="1.5" stroke-dasharray="3,2"/>
<circle cx="590" cy="210" r="6" fill="#a04030" stroke="#fefcf7" stroke-width="2"/>
<text x="590" y="228" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="11" fill="#a04030" text-anchor="middle" font-weight="600">走进华为 2.0 [待填]</text>
<rect x="80" y="92" width="935" height="22" fill="rgba(159,107,68,.10)" stroke="#9f6b44" stroke-width="1" stroke-dasharray="3,2" rx="4"/>
<text x="540" y="107" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="10.5" fill="#6b4423" text-anchor="middle" font-weight="600">资格考 35 场 · 8 大岗位 · 全行累计 1,878 人次</text>
<text x="40" y="225" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="10" fill="#7b6653">● 实色 pin = 已完成 ·</text>
<text x="170" y="225" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="10" fill="#a04030">○ 虚线 pin = 计划启动</text>
</svg>'''
        rail_html = (
            f'<section class="rail-block">'
            f'<div class="block-head"><h3>12 月培训里程碑时间线 <span class="pill">重点 55 项 · 资格考 35 场</span></h3><span class="hint">pin = 重点培训项目 · 阴影 = 资格考覆盖</span></div>'
            f'{rail_svg}'
            f'</section>'
        )

        # v8 部门对
        good_tags = "".join(f'<span>{d}</span>' for d in module_cfg.get("dept_good", []))
        warn_tags = "".join(f'<span>{d}</span>' for d in module_cfg.get("dept_warn", []))
        dept_html = (
            f'<section class="dept-pair">'
            f'<div class="dept-card good"><h4>100% 完成 <span class="pill">8 / 24</span></h4><div class="dept-tags">{good_tags}</div></div>'
            f'<div class="dept-card warn"><h4>末位警示 <span class="pill">后 3 位</span></h4><div class="dept-tags">{warn_tags}</div></div>'
            f'</section>'
        )

        module_body_content = v1_section + heatmap_html + rail_html + dept_html
    elif is_v_fc_style:
        # v1.5.14: v1 财务大卡（5 子方向 + sparkline 折线）
        if "、" in title:
            badge, rest = title.split("、", 1)
            h2_content = f'<span class="narrative-icon">{icon}</span><span class="narrative-badge">{badge}</span>、{rest}'
        else:
            h2_content = f'<span class="narrative-icon">{icon}</span>{title}'
        paras = "".join(f"<p>{p}</p>" for p in module_narrative_cfg)
        narrative_card_html = f'<section class="module-narrative-card">{paras}</section>'
        module_intro = (
            f'<div class="module-narrative-head">'
            f'<h2 class="narrative-h2">{h2_content}</h2>'
            f'</div>'
            f'{narrative_card_html}'
        )

        fc_html = []
        for fc in fc_cards:
            color_cls = f' {fc.get("color","")}' if fc.get("color") else ""
            legend_html = "".join(f'<span>{l}</span>' for l in fc.get("legend", []))
            fc_html.append(
                f'<article class="fc{color_cls}">'
                f'<div class="fc-head"><span class="fc-ico">{fc.get("icon","")}</span><span class="fc-lbl">{fc.get("label","")}</span></div>'
                f'<div class="fc-num">{fc.get("num","")}<small>{fc.get("unit","")}</small></div>'
                f'<div class="fc-sub">{fc.get("sub","")}</div>'
                f'<svg class="fc-spark" viewBox="0 0 200 36" preserveAspectRatio="none">'
                f'<polyline fill="none" stroke="{fc.get("spark_color","#9f6b44")}" stroke-width="1.6" points="{fc.get("spark_points","")}"/>'
                f'<line x1="0" y1="{fc.get("baseline_y",30)}" x2="200" y2="{fc.get("baseline_y",30)}" stroke="#f4eadb" stroke-width="0.5"/>'
                f'</svg>'
                f'<div class="fc-legend">{legend_html}</div>'
                f'</article>'
            )
        fc_section = (
            f'<div class="section-title"><h3>5 子方向 · 财务大卡 + 折线趋势</h3><span class="pill">5/5 子方向</span></div>'
            f'<section class="fc-grid">{"".join(fc_html)}</section>'
        )
        module_body_content = fc_section
    elif is_v_tree_style:
        # v1.5.13: v2 分类树（干部队伍建设总览 + 4 大类平级 + 中层核心 + 总行/经营 + 正/副职）
        if "、" in title:
            badge, rest = title.split("、", 1)
            h2_content = f'<span class="narrative-icon">{icon}</span><span class="narrative-badge">{badge}</span>、{rest}'
        else:
            h2_content = f'<span class="narrative-icon">{icon}</span>{title}'
        paras = "".join(f"<p>{p}</p>" for p in module_narrative_cfg)
        narrative_card_html = f'<section class="module-narrative-card">{paras}</section>'
        module_intro = (
            f'<div class="module-narrative-head">'
            f'<h2 class="narrative-h2">{h2_content}</h2>'
            f'</div>'
            f'{narrative_card_html}'
        )

        # 渲染分类树
        def render_tn(n, is_root=False):
            # v1.5.16: root 节点不加 leaf/branch class（避免 .tn.leaf 覆盖 .tn.root）
            if is_root:
                kind = ""
            else:
                kind = n.get("kind", "leaf")
            extra_class = f" {kind}" if kind else ""
            label = n.get("label", "")
            num = n.get("num", "")
            unit = n.get("unit", "")
            sub = n.get("sub", "")
            pct = n.get("pct", "")
            root_class = " root" if is_root else ""
            pct_html = ""
            if pct:
                pct_html = f'<div class="t-num">{pct}</div><div class="fill-bar"><i style="width:{pct}"></i></div>'
            num_html = f'<div class="t-num">{num}<small>{unit}</small></div>' if num else ""
            sub_html = f'<div class="t-sub">{sub}</div>' if sub else ""
            return (
                f'<div class="tn{root_class}{extra_class}">'
                f'<div class="t-label">{label}</div>'
                f'{num_html}'
                f'{sub_html}'
                f'{pct_html}'
                f'</div>'
            )

        tree_html_parts = []
        # 根
        tree_html_parts.append(render_tn(tree.get("root", {}), is_root=True))
        tree_html_parts.append('<div class="vline"></div>')

        # 一级 4 大类
        level1_html = []
        for n in tree.get("level1", []):
            kind = n.get("kind", "leaf")
            if "pct" in n:
                level1_html.append(f'<div class="branch-l1">{render_tn(n)}</div>')
            else:
                level1_html.append(f'<div class="branch-l1">{render_tn(n)}</div>')
        mid_html = f'<div class="branch-l1">{render_tn(tree.get("mid", {}))}</div>'
        level1_html.append(mid_html)
        tree_html_parts.append(f'<div class="tree-row level1-row">{"".join(level1_html)}</div>')

        # 中层子分支
        mid = tree.get("mid", {})
        level2_html = []
        for n2 in tree.get("level2", []):
            n2_html = render_tn(n2)
            l3_html = "".join(render_tn(n3) for n3 in n2.get("level3", []))
            level2_html.append(
                f'<div class="branch-l1">'
                f'{n2_html}'
                f'<div class="vline"></div>'
                f'<div class="branch-l2">{l3_html}</div>'
                f'</div>'
            )
        tree_html_parts.append(
            f'<div class="title-row">中层干部 · 按机构拆分</div>'
            f'<div class="tree-row level2-row">{"".join(level2_html)}</div>'
        )

        tree_html = (
            f'<div class="section-title"><h3>干部职数组织架构树</h3><span class="pill">4 大类 · 13 节点</span></div>'
            f'<section class="tree-wrap"><div class="tree">{"".join(tree_html_parts)}</div>'
            f'<div class="legend">'
            f'<span><i style="background:#6b4423"></i>根节点（总览）</span>'
            f'<span><i style="background:#9f6b44"></i>分支节点</span>'
            f'<span><i style="background:#a04030"></i>警示分支</span>'
            f'<span><i style="background:#fefcf7;border:1px solid #4a7c59"></i>健康叶</span>'
            f'<span><i style="background:#fefcf7;border:1px solid #a04030"></i>警示叶</span>'
            f'</div>'
            f'</section>'
        )
        module_body_content = tree_html
    elif is_v_hr_style:
        # v1.5.10: v_hr 风格 — narrative + gauges + progress + timeline + flow + dual-bars + ranks
        # narrative head + card
        if "、" in title:
            badge, rest = title.split("、", 1)
            h2_content = f'<span class="narrative-icon">{icon}</span><span class="narrative-badge">{badge}</span>、{rest}'
        else:
            h2_content = f'<span class="narrative-icon">{icon}</span>{title}'
        paras = "".join(f"<p>{p}</p>" for p in module_narrative_cfg)
        narrative_card_html = f'<section class="module-narrative-card">{paras}</section>'
        module_intro = (
            f'<div class="module-narrative-head">'
            f'<h2 class="narrative-h2">{h2_content}</h2>'
            f'</div>'
            f'{narrative_card_html}'
        )

        sections = []

        # 1. gauge 仪表盘（v1）
        if gauges:
            gauge_html = []
            for g in gauges:
                stroke = 389.56
                offset = stroke * (g["pct"] / 100)
                if offset > stroke: offset = stroke
                if offset < 0: offset = 0
                gauge_html.append(
                    f'<article class="gauge-card">'
                    f'<svg class="gauge-svg" width="160" height="100" viewBox="0 0 160 100">'
                    f'<circle class="ring-bg" cx="80" cy="80" r="62"/>'
                    f'<circle class="ring-fg" cx="80" cy="80" r="62" stroke="{g["color"]}" stroke-dasharray="{offset:.2f} {stroke:.2f}" transform="rotate(-90 80 80)"/>'
                    f'<text class="ring-num" x="80" y="78" text-anchor="middle">{g["num"]}</text>'
                    f'<text class="ring-unit" x="80" y="94" text-anchor="middle">{g["unit"]}</text>'
                    f'</svg>'
                    f'<div class="lbl">{g["lbl"]}</div>'
                    f'<div class="sub">{g["sub"]}</div>'
                    f'</article>'
                )
            sections.append(
                f'<div class="section-title"><h3>核心指标 · 三个仪表盘</h3><span class="pill">gauge × 3</span></div>'
                f'<section class="gauge-grid">{"".join(gauge_html)}</section>'
            )

        # 2. 流程图（v2）
        if flow_nodes:
            flow_html = []
            for i, f in enumerate(flow_nodes):
                arrow = '<div class="flow-arrow">▶</div>' if i < len(flow_nodes) - 1 else ''
                kind_class = f" {f['kind']}" if f.get('kind') else ''
                flow_html.append(
                    f'<div class="flow-node{kind_class}">'
                    f'<div class="flow-icon">{f["icon"]}</div>'
                    f'<div class="flow-title">{f["title"]}</div>'
                    f'<div class="flow-metric">{f["metric"]}<span class="flow-unit">{f["unit"]}</span></div>'
                    f'<div class="flow-sub">{f["sub"]}</div>'
                    f'</div>{arrow}'
                )
            sections.append(
                f'<div class="section-title"><h3>端到端流程 · 人才引进 → 人员退出</h3><span class="pill">flow × 4 节点</span></div>'
                f'<section class="flow-grid">{"".join(flow_html)}</section>'
            )

        # 3. 双轴对比柱（v3）+ 右侧 summary 摘要（v1.5.12）
        if dual_bars:
            max_v = max((d["actual"] for d in dual_bars), default=1)
            max_v = max(max_v, max((d["target"] for d in dual_bars), default=0))
            db_html = []
            for d in dual_bars:
                actual_w = (d["actual"] / max_v * 100) if max_v > 0 else 0
                target_w = (d["target"] / max_v * 100) if max_v > 0 else 0
                pct = d["pct"]
                bar_color = "#4a7c59" if pct >= 100 else ("#9f6b44" if pct >= 50 else "#a04030")
                db_html.append(
                    f'<article class="dual-bar">'
                    f'<div class="dual-head"><h4>{d["name"]}</h4><span class="dual-pct" style="color:{bar_color}">{pct}%</span></div>'
                    f'<div class="dual-rows">'
                    f'<div class="dual-row"><span class="dual-lbl">实际</span><div class="dual-track"><div class="dual-fill" style="width:{actual_w}%;background:{d["color"]}"></div><span class="dual-val">{d["actual"]}</span></div></div>'
                    f'<div class="dual-row"><span class="dual-lbl">目标</span><div class="dual-track"><div class="dual-fill target" style="width:{target_w}%;background:#c9a883"></div><span class="dual-val">{d["target"]}</span></div></div>'
                    f'</div>'
                    f'</article>'
                )
            dual_section = f'<div class="dual-bars-area">{"".join(db_html)}</div>'

            # 右侧 summary 卡
            dual_summary = module_cfg.get("dual_summary", {})
            summary_html = ""
            if dual_summary:
                kpis_html = "".join(
                    f'<div class="summary-kpi">'
                    f'<div class="summary-lbl">{k.get("lbl","")}</div>'
                    f'<div class="summary-val" style="color:{k.get("color","#9f6b44")}">{k.get("val","")}<span class="summary-unit">{k.get("unit","")}</span></div>'
                    f'<div class="summary-sub">{k.get("sub","")}</div>'
                    f'</div>'
                    for k in dual_summary.get("kpis", [])
                )
                prog_html = "".join(
                    f'<div class="summary-prog-row">'
                    f'<span class="summary-prog-lbl">{p["lbl"]}</span>'
                    f'<div class="summary-prog-track"><div class="summary-prog-fill" style="width:{min(p["pct"],100)}%;background:{p["color"]}"></div></div>'
                    f'<span class="summary-prog-val">{p["pct"]}%</span>'
                    f'</div>'
                    for p in dual_summary.get("progress", [])
                )
                summary_html = (
                    f'<aside class="dual-summary">'
                    f'<h4 class="summary-title">{dual_summary.get("title","")}</h4>'
                    f'<div class="summary-kpis">{kpis_html}</div>'
                    f'<div class="summary-progress"><div class="summary-prog-head">5 大任务线完成率</div>{prog_html}</div>'
                    f'</aside>'
                )
            sections.append(
                f'<div class="section-title"><h3>双轴对比 · 全年目标 vs 1-5 月实际</h3><span class="pill">dual-bar × 6</span></div>'
                f'<section class="dual-grid">{dual_section}{summary_html}</section>'
            )

        # 4. 颁奖台 Top 3 / Bottom 3 + 任务完成量 Top 3（v2）
        if rank_top3 and rank_bottom3:
            def render_podium(rank):
                pod_html = "".join(
                    f'<div class="pod-col"><div class="pod-bar{" bad" if rank["kind"] == "bad" else ""}" style="height:{p["h"]}px">'
                    f'<span class="pct">{p["pct"]}</span><span class="lbl">{p["lbl"]}</span></div>'
                    f'<div class="pod-name">{p["name"]}<small>{p["sub"]}</small></div></div>'
                    for p in rank["podium"]
                )
                tbl_html = "".join(
                    f'<tr><td>{t["rank"]}</td><td>{t["name"]}</td><td class="num{" bad" if rank["kind"] == "bad" else ""}">{t["val"]}</td></tr>'
                    for t in rank["table"]
                )
                return (
                    f'<article class="rank-card {rank["kind"]}">'
                    f'<h4>{rank["title"]}</h4>'
                    f'<div class="podium">{pod_html}</div>'
                    f'<table class="rank-tbl"><tr><th>排名</th><th>分行</th><th>{("完成率" if "%" in rank["table"][0]["val"] else "退出量")}</th></tr>{tbl_html}</table>'
                    f'</article>'
                )
            rank_volume = module_cfg.get("rank_volume", {})
            volume_html = render_podium(rank_volume) if rank_volume else ""
            sections.append(
                f'<div class="section-title"><h3>排名榜 · 颁奖台 + 退出类型</h3><span class="pill">podium + exit-bar</span></div>'
                f'<section class="rank-grid">{render_podium(rank_top3)}{render_podium(rank_bottom3)}{volume_html}</section>'
            )

        # 5. 退出类型（v2）
        if exit_bars:
            ex_html = []
            for e in exit_bars:
                rows_html = "".join(
                    f'<div class="er"><span class="nm">{r["nm"]}</span><div class="trk"><div class="fl" style="width:{r["pct"]}%;background:{r["bg"]}">{r["label"]}</div></div><span class="vl">{r["label"]}</span></div>'
                    for r in e["rows"]
                )
                ex_html.append(
                    f'<article class="exit-card">'
                    f'<h4>{e["title"]} <span class="pill-s">总 202</span></h4>'
                    f'<div class="exit-rows">{rows_html}</div>'
                    f'</article>'
                )
            sections.append(
                f'<div class="section-title"><h3>退出类型 · 机构 + 职级</h3><span class="pill">exit-bar × 6</span></div>'
                f'<section class="exit-grid">{"".join(ex_html)}</section>'
            )

        # 6. 4 案例卡（v2）
        if case_cards:
            case_html = "".join(
                f'<article class="case-card {c["kind"]}">'
                f'<div class="tag">{c["tag"]}</div>'
                f'<div class="ttl">{c["title"]}</div>'
                f'<div class="meta">{c["meta"]}</div>'
                f'</article>'
                for c in case_cards
            )
            sections.append(
                f'<div class="section-title"><h3>劳动仲裁 · 4 案例卡</h3><span class="pill">case × 4</span></div>'
                f'<section class="case-grid">{case_html}</section>'
            )

        module_body_content = "".join(sections)
    elif is_v11_style:
        # v11 风格：4 KPI + 5 段 stacked 卡片 + 8 客户/客服网格
        kpi_html = "".join(
            f'<article class="kpi v11 {k.get("variant","")}">'
            f'<div class="glyph">{k.get("glyph","")}</div>'
            f'<div class="label">{k.get("label","")}</div>'
            f'<div class="big">{k.get("big","")}<span class="unit">{k.get("unit","")}</span></div>'
            f'<div class="sub">{k.get("sub","")}</div>'
            f"</article>"
            for k in kpi_quad
        )
        kpi_row_html = f'<section class="kpi-row v11">{kpi_html}</section>'

        dim_html = []
        for d in dim_cards:
            segs = "".join(
                f'<div class="seg {cls}" style="width:{w}%">{label}</div>'
                for label, w, cls in d["segments"]
            )
            rows = "".join(
                f'<div class="row"><span class="dot {dot}"></span><span>{name}</span><span class="vl">{vl}</span></div>'
                for dot, name, vl in d["rows"]
            )
            dim_html.append(
                f'<article class="dim-card {d.get("color","")}">'
                f'<div class="head"><h4>{d["head_icon"]} {d["head_title"]}</h4><span class="ttl">{d["ttl"]}</span></div>'
                f'<div class="stacked-bar">{segs}</div>'
                f'<div class="dim-list">{rows}</div>'
                f"</article>"
            )
        dim_section_html = (
            f'<div class="section-title"><h3>中部 5 维度 · stacked-bar 卡片</h3><span class="pill">5/5 维度</span></div>'
            f'<section class="dim-grid">{"".join(dim_html)}</section>'
        )

        cs_html = []
        for c in cs_grid:
            mini = "".join(
                f'<div style="width:{w}%;background:{col}"></div>'
                for w, col in c["mini"]
            )
            cs_html.append(
                f'<article class="cs-card {c.get("color","")}">'
                f'<div class="tag">{c["tag"]}</div>'
                f'<div class="num">{c["num"]}<small>{c["unit"]}</small></div>'
                f'<div class="name">{c["name"]}</div>'
                f'<div class="meta">{c["meta"]}</div>'
                f'<div class="mini-stk">{mini}</div>'
                f"</article>"
            )
        cs_section_html = (
            f'<div class="section-title"><h3>底部 8 项 · 客户/客服经理细分</h3><span class="pill">8 项</span></div>'
            f'<section class="cs-grid">{"".join(cs_html)}</section>'
        )

        if "、" in title:
            badge, rest = title.split("、", 1)
            h2_content = f'<span class="narrative-icon">{icon}</span><span class="narrative-badge">{badge}</span>、{rest}'
        else:
            h2_content = f'<span class="narrative-icon">{icon}</span>{title}'

        paras = "".join(f"<p>{p}</p>" for p in module_narrative_cfg)
        module_intro = (
            f'<div class="module-narrative-head">'
            f'<h2 class="narrative-h2">{h2_content}</h2>'
            f'</div>'
            f'<section class="module-narrative-card">{paras}</section>'
        )
        module_body_content = kpi_row_html + dim_section_html + cs_section_html
    elif is_v1_style:
        # v1.5.8: icon + 标题移到 narrative-card 上方
        if "、" in title:
            badge, rest = title.split("、", 1)
            h2_content = f'<span class="narrative-icon">{icon}</span><span class="narrative-badge">{badge}</span>、{rest}'
        else:
            h2_content = f'<span class="narrative-icon">{icon}</span>{title}'
        paras = "".join(f"<p>{p}</p>" for p in module_narrative_cfg)
        module_intro = (
            f'<div class="module-narrative-head">'
            f'<h2 class="narrative-h2">{h2_content}</h2>'
            f'</div>'
            f'<section class="module-narrative-card">'
            f'{paras}'
            f"</section>"
        )
        module_body_content = "".join(sections_html) + kpi_cards_html
    elif sub_text_for_narrative:
        # v1.5 风格：单段叙述
        module_intro = (
            f'<p class="module-narrative">{sub_text_for_narrative}</p>'
        )
        module_body_content = "".join(sections_html) + kpi_cards_html
    else:
        module_body_content = "".join(sections_html) + kpi_cards_html

    # 非 v1/v11/v_tree/v_fc/v_hr 风格模块：保留 module-head
    if not is_v1_style and not is_v11_style and not is_v_tree_style and not is_v_fc_style and not is_v_hr_style:
        module_head_html = (
            f'<div class="module-head">'
            f'<div class="module-icon">{icon}</div>'
            f'<div><div class="module-title">{title}</div>'
            f'<div class="module-sub">{sub}</div>'
            f"</div>"
            f"</div>"
        )
    elif is_v1_style:
        # v1 风格：保留 module-head 但 CSS 隐藏 title/sub（让 icon 单独显示在 .module-head-featured 中；实际 icon 已移到 narrative h2）
        module_head_html = (
            f'<div class="module-head module-head-featured">'
            f'<div class="module-icon">{icon}</div>'
            f'<div><div class="module-title">{title}</div>'
            f'<div class="module-sub">{sub}</div>'
            f"</div>"
            f"</div>"
        )

    return (
        f'<section class="module"{featured_attr} data-index="{module_cfg.get("order", 0):02d}">'
        f"{module_head_html}"
        f"{module_intro}"
        f'<div class="module-body">{module_body_content}</div>'
        f"</section>"
    )
