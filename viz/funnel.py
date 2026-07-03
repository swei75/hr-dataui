"""漏斗图。data: [{label, value}]"""


def render(data, options):
    if not data:
        return '<div class="funnel-empty">无数据</div>'
    max_v = max((d.get("value", 0) or 0) for d in data)
    if max_v == 0:
        return '<div class="funnel-empty">最大值为 0</div>'
    parts = []
    for i, d in enumerate(data):
        v = d.get("value", 0) or 0
        w = (v / max_v) * 100
        color = f"hsl({210 - i * 20}, 60%, 45%)"
        parts.append(
            f'<div class="funnel-step" style="margin:4px 0;width:{w:.1f}%;'
            f'background:{color};color:#fff;padding:8px 12px;'
            f'border-radius:4px;min-width:120px;">'
            f'{d.get("label", "")} <span style="float:right;">{v:,}</span></div>'
        )
    return f'<div class="funnel-chart" style="display:flex;flex-direction:column;align-items:center;">{"".join(parts)}</div>'
