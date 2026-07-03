"""Top/Bottom N 排名。data: [{rank, name, value}]"""


def render(data, options):
    if not data:
        return '<div class="ranking-empty">无数据</div>'
    rows = []
    for d in data:
        rank = d.get("rank", "")
        name = d.get("name", "")
        value = d.get("value", 0)
        rows.append(
            f'<tr><td style="padding:6px 12px;">'
            f'<span class="rank-badge" style="display:inline-block;'
            f'width:24px;height:24px;line-height:24px;text-align:center;'
            f'background:#1E5BAA;color:#fff;border-radius:50%;">{rank}</span></td>'
            f'<td style="padding:6px 12px;">{name}</td>'
            f'<td style="padding:6px 12px;text-align:right;">{value:,}</td></tr>'
        )
    return (
        f'<table class="ranking-table" style="width:100%;border-collapse:collapse;">'
        f'{"".join(rows)}</table>'
    )
