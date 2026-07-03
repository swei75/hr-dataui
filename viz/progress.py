"""进度条。data: {label, current, target, pct}"""


def render(data, options):
    if not isinstance(data, dict):
        return '<div class="progress-empty">无数据</div>'
    label = data.get("label", "")
    current = data.get("current", 0) or 0
    target = data.get("target", 0) or 0
    pct = data.get("pct", 0) or 0
    color = "#2E7D32" if pct >= 0.8 else ("#E07B39" if pct >= 0.5 else "#C62828")
    return (
        f'<div class="progress" style="margin:8px 0;">'
        f'<div class="progress-label" style="display:flex;'
        f'justify-content:space-between;margin-bottom:4px;">'
        f"<span>{label}</span>"
        f"<span>{current:,}/{target:,} ({pct * 100:.1f}%)</span></div>"
        f'<div class="progress-track" style="background:#eee;height:20px;'
        f'border-radius:4px;overflow:hidden;">'
        f'<div class="progress-fill" style="width:{pct * 100:.1f}%;'
        f"background:{color};height:100%;\"></div></div></div>"
    )
