"""KPI 单数字卡。data: {value, sub, tone}"""

TONE_COLORS = {
    "blue": "#1E5BAA",
    "green": "#2E7D32",
    "orange": "#E07B39",
    "red": "#C62828",
}


def render(data: dict, options: dict) -> str:
    value = data.get("value", "-") if isinstance(data, dict) else data
    sub = data.get("sub", "") if isinstance(data, dict) else ""
    tone = data.get("tone", "blue") if isinstance(data, dict) else "blue"
    color = TONE_COLORS.get(tone, TONE_COLORS["blue"])
    return (
        f'<div class="kpi-card" style="border-left:4px solid {color};'
        f'padding:12px 16px;background:#fafafa;border-radius:6px;">'
        f'<div class="kpi-value" style="font-size:2em;font-weight:600;'
        f'color:{color};">{value}</div>'
        f'<div class="kpi-sub" style="color:#666;font-size:0.9em;">{sub}</div>'
        f"</div>"
    )
