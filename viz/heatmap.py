"""v1.4 heatmap viz（员工 × 司龄 等二维矩阵）。

CSS classes: success / warning / danger 映射 --success / --warning / --danger。
"""


def render_heatmap(records: list[dict], options: dict | None = None) -> str:
    """渲染二维 heatmap grid。

    Args:
        records: [{'row': '员工-产品经理', 'col': '司龄-3-5年', 'value': 0.85, 'level': 'success'}, ...]
                 每个 record 渲染 1 个 cell（不聚合）。
        options: 预留。{'row_labels': [...], 'col_labels': [...]}

    Returns:
        HTML 字符串。
    """
    options = options or {}
    if not records:
        return '<div class="heatmap-empty">无数据</div>'

    # 不做聚合：每个 record 直接渲染 1 个 cell
    # 行/列顺序：按输入 records 顺序去重
    rows_seen: list[str] = []
    cols_seen: list[str] = []
    grid: dict[tuple[str, str], dict] = {}
    for r in records:
        row_key = r.get("row", "")
        col_key = r.get("col", "")
        if row_key not in rows_seen:
            rows_seen.append(row_key)
        if col_key not in cols_seen:
            cols_seen.append(col_key)
        grid[(row_key, col_key)] = r

    # 表头
    header_cells = "".join(f'<th class="heatmap-col-label">{c}</th>' for c in cols_seen)

    # 行
    rows_html = []
    for row_key in rows_seen:
        row_cells = []
        for c in cols_seen:
            cell = grid.get((row_key, c))
            if cell:
                level = cell.get("level", "warning")
                val = cell.get("value", 0)
                row_cells.append(
                    f'<td class="heatmap-cell" data-level="{level}">{val:.2f}</td>'
                )
            else:
                row_cells.append('<td class="heatmap-cell" data-level="warning">—</td>')
        rows_html.append(f'<tr><th class="heatmap-row-label">{row_key}</th>{"".join(row_cells)}</tr>')

    return (
        '<div class="heatmap">'
        '<table class="heatmap-table">'
        f'<thead><tr><th></th>{header_cells}</tr></thead>'
        f'<tbody>{"".join(rows_html)}</tbody>'
        '</table>'
        '</div>'
    )
