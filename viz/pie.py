"""圆环图。data: [{label, value, pct}]"""
import math

PALETTE = [
    "#1E5BAA",
    "#E07B39",
    "#2E7D32",
    "#C62828",
    "#6A1B9A",
    "#00838F",
    "#F9A825",
    "#5D4037",
]


def render(data, options):
    if not data:
        return '<div class="pie-empty">无数据</div>'
    total = sum((d.get("value", 0) or 0) for d in data)
    if total == 0:
        return '<div class="pie-empty">总和为 0</div>'

    cx, cy, r_outer, r_inner = 100, 100, 80, 50
    parts = []
    cum_pct = 0.0
    for i, d in enumerate(data):
        pct = (d.get("value", 0) or 0) / total
        cum_pct += pct
        a1 = (cum_pct - pct) * 2 * math.pi
        a2 = cum_pct * 2 * math.pi
        x1o, y1o = cx + r_outer * math.cos(a1), cy + r_outer * math.sin(a1)
        x2o, y2o = cx + r_outer * math.cos(a2), cy + r_outer * math.sin(a2)
        x1i, y1i = cx + r_inner * math.cos(a1), cy + r_inner * math.sin(a1)
        x2i, y2i = cx + r_inner * math.cos(a2), cy + r_inner * math.sin(a2)
        large = 1 if pct > 0.5 else 0
        color = PALETTE[i % len(PALETTE)]
        path = (
            f"M {x1o:.1f} {y1o:.1f} A {r_outer} {r_outer} 0 {large} 1 {x2o:.1f} {y2o:.1f} "
            f"L {x2i:.1f} {y2i:.1f} A {r_inner} {r_inner} 0 {large} 0 {x1i:.1f} {y1i:.1f} Z"
        )
        parts.append(
            f'<path d="{path}" fill="{color}">'
            f"<title>{d.get('label', '')}: {(pct * 100):.2f}%</title></path>"
        )

    legend = "".join(
        f'<div style="display:flex;align-items:center;gap:6px;margin:2px 0;">'
        f'<span style="width:12px;height:12px;background:{PALETTE[i % len(PALETTE)]};'
        f'display:inline-block;"></span>'
        f'<span>{d.get("label", "")}: {d.get("value", 0):,}</span></div>'
        for i, d in enumerate(data)
    )

    return (
        '<div class="pie-chart" style="display:flex;align-items:center;'
        'gap:16px;flex-wrap:wrap;">'
        f'<svg width="200" height="200" viewBox="0 0 200 200">{"".join(parts)}</svg>'
        f'<div class="pie-legend" style="flex:1;min-width:200px;">{legend}</div>'
        "</div>"
    )
