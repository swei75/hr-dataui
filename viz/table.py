"""数据表。data: list[dict] (col names from keys)"""


def render(data, options):
    if not data:
        return '<div class="table-empty">无数据</div>'
    cols = list(data[0].keys())
    head = "".join(
        f'<th style="padding:8px 12px;text-align:left;border-bottom:2px solid #1E5BAA;">{c}</th>'
        for c in cols
    )
    rows = []
    for row in data:
        cells = "".join(
            f'<td style="padding:6px 12px;border-bottom:1px solid #eee;">{row.get(c, "")}</td>'
            for c in cols
        )
        rows.append(f"<tr>{cells}</tr>")
    return (
        '<div class="data-table-wrap" style="overflow-x:auto;">'
        '<table class="data-table" style="width:100%;border-collapse:collapse;">'
        f"<thead><tr>{head}</tr></thead>"
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )
