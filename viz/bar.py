"""横向柱图（占比）。data: [{label, value, pct}]"""


def render(data, options):
    if not data:
        return '<div class="bar-empty">无数据</div>'
    max_pct = max((d.get("pct", 0) or 0) for d in data)
    rows = []
    for d in data:
        label = d.get("label", "")
        value = d.get("value", 0)
        pct = d.get("pct", 0) or 0
        width = (pct / max_pct * 100) if max_pct > 0 else 0
        rows.append(
            f'<div class="bar-row" style="display:flex;align-items:center;'
            f'gap:8px;margin:6px 0;">'
            f'<div class="bar-label" style="min-width:120px;">{label}</div>'
            f'<div class="bar-track" style="flex:1;background:#eee;height:18px;'
            f'border-radius:3px;overflow:hidden;">'
            f'<div class="bar-fill" style="width:{width:.1f}%;'
            f'background:#1E5BAA;height:100%;"></div></div>'
            f'<div class="bar-value" style="min-width:80px;text-align:right;">'
            f"{value:,} ({pct * 100:.2f}%)</div></div>"
        )
    return f'<div class="bar-chart">{"".join(rows)}</div>'
