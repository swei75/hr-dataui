"""层级树。data: [{region, count, children: [...]}]"""


def _render_node(node):
    region = node.get("region", node.get("name", ""))
    count = node.get("count", 0)
    children = node.get("children", [])
    child_html = ""
    if children:
        child_html = "<ul>" + "".join(f"<li>{_render_node(c)}</li>" for c in children) + "</ul>"
    return (
        f'<div class="hierarchy-node">'
        f'<span class="hierarchy-name">{region}</span> '
        f'<span class="hierarchy-count">({count:,})</span>'
        f"{child_html}</div>"
    )


def render(data, options):
    if not data:
        return '<div class="hierarchy-empty">无数据</div>'
    return f'<div class="hierarchy">{"".join(_render_node(n) for n in data)}</div>'
