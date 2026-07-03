"""KPI 单数字卡。data: {value, sub, tone}"""

TONE_COLORS = {
    "blue": "var(--primary)",
    "green": "var(--success)",
    "orange": "var(--orange)",
    "red": "var(--danger)",
}


def render(data, options):
    if isinstance(data, dict):
        value = data.get("value", "-")
        sub = data.get("sub", "")
        tone = data.get("tone", "blue")
    else:
        value = data
        sub = ""
        tone = "blue"
    color_class = f"tone-{tone}"
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-value {color_class}">{value}</div>'
        f'<div class="kpi-sub">{sub}</div>'
        f"</div>"
    )
