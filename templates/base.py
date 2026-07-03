"""HTML base template functions (f-string, NOT Jinja2)."""

MODULES = [
    ("M-1", "🏛", "组织架构"),
    ("M-2", "👥", "员工情况"),
    ("M-3", "📉", "人员优化"),
    ("M-4", "🎖", "干部队伍"),
    ("M-5", "💰", "考核薪酬"),
    ("M-6", "📚", "培训赋能"),
]

MODULES_ORDER = [
    "组织架构", "员工情况", "人员优化", "干部队伍", "考核薪酬", "培训赋能",
]


def render_module_placeholders() -> str:
    """渲染 6 个空模块占位符。"""
    parts = []
    for code, icon, title in MODULES:
        parts.append(
            f'<section class="module" id="{code}">'
            f"<h2>{icon} {title}</h2>"
            f'<div class="module-body"><!-- P4 填充 --></div>'
            f"</section>"
        )
    return "\n".join(parts)


def render_page(
    body: str,
    title: str = "人力资源管理数据驾驶舱",
    alpine: str = "",
    drill_data: str = "{}",
) -> str:
    """渲染完整 HTML 页面。

    alpine 参数保留以兼容 build.py 调用，但实际使用内置 vanilla JS（更小）。
    """
    # ~2KB vanilla JS：钻取面板 toggle + 数据渲染（替代 Alpine.js 43KB）
    inline_js = """<script>function toggleDrill(btn){var p=btn.nextElementSibling;if(!p)return;p.style.display=p.style.display==='none'?'block':'none';}function renderDrill(d){if(!d||!d.rows)return'<div class="empty">无数据</div>';var h='<table style="width:100%;border-collapse:collapse;font-size:0.9em;"><thead><tr><th style="text-align:left;padding:6px;border-bottom:1px solid #ccc;">#</th>';var cols=Object.keys(d.rows[0]||{});cols.forEach(function(c){h+='<th style="text-align:left;padding:6px;border-bottom:1px solid #ccc;">'+c+'</th>';});h+='</tr></thead><tbody>';d.rows.forEach(function(r,i){h+='<tr><td style="padding:4px 6px;color:#999;">'+(i+1)+'</td>';cols.forEach(function(c){h+='<td style="padding:4px 6px;">'+r[c]+'</td>';});h+='</tr>';});return h+'</tbody></table>';}document.addEventListener('click',function(e){if(e.target.classList.contains('drill-btn')){toggleDrill(e.target);}});</script>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body {{ font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; margin: 0; padding: 16px; color: #222; }}
.module {{ margin-bottom: 24px; padding: 16px; border: 1px solid #eee; border-radius: 8px; background: #fff; }}
.module h2 {{ margin: 0 0 12px 0; font-size: 1.3em; color: #1E5BAA; }}
.drill-btn {{ padding: 12px 16px; min-height: 44px; min-width: 44px; background: #1E5BAA; color: #fff; border: 0; border-radius: 6px; cursor: pointer; font-size: 1em; }}
.drill-btn:hover {{ background: #154580; }}
.drill-panel {{ margin-top: 12px; padding: 12px; background: #f5f5f5; border-radius: 4px; display: none; }}
.viz-btn {{ padding: 8px 12px; min-height: 44px; background: #fff; border: 1px solid #1E5BAA; color: #1E5BAA; border-radius: 4px; cursor: pointer; }}
.viz-btn.active {{ background: #1E5BAA; color: #fff; }}
.kpi-card {{ border-left: 4px solid #1E5BAA; padding: 12px 16px; background: #fafafa; border-radius: 6px; }}
.kpi-value {{ font-size: 2em; font-weight: 600; color: #1E5BAA; }}
.kpi-sub {{ color: #666; font-size: 0.9em; }}
.data-table-wrap {{ overflow-x: auto; -webkit-overflow-scrolling: touch; }}
@media (max-width: 980px) {{ .module h2 {{ font-size: 1.2em; }} }}
@media (max-width: 640px) {{
  body {{ padding: 8px; }}
  .module {{ padding: 12px; margin-bottom: 16px; }}
  .module h2 {{ font-size: 1.1em; }}
  .drill-btn {{ width: 100%; }}
  .viz-btn {{ flex: 1; }}
  .viz-switch {{ display: flex; gap: 4px; }}
  .kpi-value {{ font-size: 1.5em; }}
}}
</style>
</head>
<body>
<h1>{title}</h1>
{body}
<script>window.HR_DRILL_DATA = {drill_data};</script>
{inline_js}
</body>
</html>"""
