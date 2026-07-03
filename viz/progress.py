"""进度条。data: {label, current, target, pct}"""


def render(data, options):
    if not isinstance(data, dict):
        return '<div class="empty">无数据</div>'
    label = data.get("label", "")
    current = data.get("current", 0) or 0
    target = data.get("target", 0) or 0
    pct = data.get("pct", 0) or 0
    if pct >= 0.8:
        tone = "good"
    elif pct >= 0.5:
        tone = "warn"
    else:
        tone = "bad"
    return (
        f'<div class="progress">'
        f'<div class="progress-label">'
        f"<span>{label}</span>"
        f"<span>{current:,}/{target:,} ({pct * 100:.1f}%)</span></div>"
        f'<div class="progress-track">'
        f'<div class="progress-fill tone-{tone}" style="width:{pct * 100:.1f}%;"></div>'
        f"</div></div>"
    )
