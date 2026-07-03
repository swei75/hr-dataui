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
    "组织架构",
    "员工情况",
    "人员优化",
    "干部队伍",
    "考核薪酬",
    "培训赋能",
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


# 深色业务仪表盘主题（GitHub Primer / Linear 风格）
# 关键：保持 ≤ 50KB 总产物
DARK_THEME_CSS = """
:root{--bg:#0d1117;--bg-elev:#161b22;--bg-card:#1c2128;--border:#30363d;--border-subtle:#21262d;--text:#e6edf3;--text-muted:#8b949e;--text-dim:#6e7681;--primary:#58a6ff;--primary-glow:rgba(88,166,255,.15);--success:#3fb950;--warning:#d29922;--danger:#f85149;--purple:#bc8cff;--orange:#f78166;--cyan:#39c5cf;--grad-blue:linear-gradient(90deg,#58a6ff,#3fb950);--grad-warm:linear-gradient(90deg,#f78166,#d29922);--shadow:0 4px 14px rgba(0,0,0,.4);--radius:10px;--radius-sm:6px;}
*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;margin:0;padding:24px;background:var(--bg);color:var(--text);font-size:14px;line-height:1.6}
h1{font-size:1.6em;font-weight:700;margin:0 0 24px;background:var(--grad-blue);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:-.5px}
.module{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:24px;margin-bottom:20px;box-shadow:var(--shadow);transition:border-color .2s ease}
.module:hover{border-color:var(--primary)}
.module h2{margin:0 0 20px;font-size:1.15em;font-weight:600;color:var(--text);display:flex;align-items:center;gap:8px;padding-bottom:12px;border-bottom:1px solid var(--border-subtle)}
.module h2::before{content:"";display:inline-block;width:4px;height:16px;background:var(--primary);border-radius:2px}
.module-body{display:flex;flex-direction:column;gap:18px}
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.full-col{display:grid;grid-template-columns:1fr}
.section-card{background:var(--bg-elev);border:1px solid var(--border-subtle);border-radius:var(--radius-sm);padding:16px 18px;min-width:0;transition:border-color .2s ease}
.section-card:hover{border-color:var(--border)}
.section-title{margin:0 0 12px;font-size:.85em;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.6px}
.section-body{min-width:0}
.viz-switch{display:flex;gap:4px;margin-bottom:12px;flex-wrap:wrap}
.viz-btn{padding:6px 12px;min-height:32px;background:var(--bg-elev);border:1px solid var(--border);color:var(--text-muted);border-radius:var(--radius-sm);cursor:pointer;font-size:.85em;transition:all .15s ease}
.viz-btn:hover{border-color:var(--primary);color:var(--text)}
.viz-btn.active{background:var(--primary-glow);border-color:var(--primary);color:var(--primary)}
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.kpi-card{background:var(--bg-elev);border:1px solid var(--border);border-left:3px solid var(--primary);padding:14px 18px;border-radius:var(--radius-sm);transition:transform .15s ease,border-color .2s ease}
.kpi-card:hover{transform:translateY(-1px);border-color:var(--primary)}
.kpi-value{font-size:1.9em;font-weight:700;color:var(--text);line-height:1.1;font-feature-settings:"tnum"}
.kpi-value.tone-blue{color:var(--primary)}.kpi-value.tone-green{color:var(--success)}.kpi-value.tone-orange{color:var(--orange)}.kpi-value.tone-red{color:var(--danger)}
.kpi-sub{color:var(--text-muted);font-size:.85em;margin-top:4px}
.bar-row{display:flex;align-items:center;gap:12px;margin:8px 0;padding:4px 0}
.bar-label{min-width:140px;color:var(--text-muted);font-size:.9em}
.bar-track{flex:1;background:var(--bg-elev);height:10px;border-radius:5px;overflow:hidden;position:relative}
.bar-fill{background:var(--grad-blue);height:100%;border-radius:5px;transition:width .6s ease;box-shadow:0 0 8px var(--primary-glow)}
.bar-value{min-width:100px;text-align:right;color:var(--text);font-size:.9em;font-feature-settings:"tnum"}
.pie-chart{display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.pie-legend{flex:1;min-width:200px}
.pie-legend > div{display:flex;align-items:center;gap:8px;margin:4px 0;font-size:.9em}
.pie-legend > div > span:first-child{width:12px;height:12px;border-radius:3px;flex-shrink:0}
.funnel-chart{display:flex;flex-direction:column;align-items:stretch;gap:4px;padding:8px 0}
.funnel-step{background:var(--grad-warm);color:#0d1117;padding:10px 16px;border-radius:var(--radius-sm);font-weight:500;display:flex;justify-content:space-between;align-items:center;font-feature-settings:"tnum"}
.progress{margin:10px 0}
.progress-label{display:flex;justify-content:space-between;margin-bottom:6px;font-size:.9em}
.progress-label > span:last-child{color:var(--text-muted);font-feature-settings:"tnum"}
.progress-track{background:var(--bg-elev);height:8px;border-radius:4px;overflow:hidden}
.progress-fill{height:100%;border-radius:4px;transition:width .6s ease;box-shadow:0 0 6px currentColor}
.progress-fill.tone-good{background:var(--success);color:var(--success)}
.progress-fill.tone-warn{background:var(--warning);color:var(--warning)}
.progress-fill.tone-bad{background:var(--danger);color:var(--danger)}
.ranking-table{width:100%;border-collapse:collapse}
.ranking-table td{padding:8px 12px;border-bottom:1px solid var(--border-subtle)}
.ranking-table tr:hover td{background:var(--bg-elev)}
.rank-badge{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;background:var(--primary-glow);color:var(--primary);border-radius:50%;font-weight:600;font-size:.85em}
.hierarchy{padding:4px 0}
.hierarchy ul{list-style:none;padding-left:20px;margin:4px 0;border-left:1px dashed var(--border)}
.hierarchy-node{padding:6px 0}
.hierarchy-name{color:var(--text);font-weight:500}
.hierarchy-count{color:var(--text-muted);font-size:.85em;margin-left:4px}
.data-table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--border);border-radius:var(--radius-sm)}
.data-table{width:100%;border-collapse:collapse;font-size:.9em}
.data-table th{text-align:left;padding:10px 14px;background:var(--bg-elev);color:var(--text-muted);font-weight:600;border-bottom:1px solid var(--border);text-transform:uppercase;font-size:.8em;letter-spacing:.5px}
.data-table td{padding:8px 14px;border-bottom:1px solid var(--border-subtle);font-feature-settings:"tnum"}
.data-table tbody tr:hover{background:var(--bg-elev)}
.drill-btn{padding:10px 18px;min-height:44px;background:transparent;border:1px solid var(--primary);color:var(--primary);border-radius:var(--radius-sm);cursor:pointer;font-size:.9em;font-weight:500;transition:all .15s ease}
.drill-btn:hover{background:var(--primary-glow);box-shadow:0 0 0 3px var(--primary-glow)}
.drill-btn:active{transform:scale(.98)}
.drill-panel{margin-top:12px;padding:16px;background:var(--bg-elev);border:1px solid var(--border);border-radius:var(--radius-sm);display:none;animation:slideDown .2s ease}
@keyframes slideDown{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}
.empty{color:var(--text-dim);text-align:center;padding:20px;font-style:italic}
@media (max-width:980px){body{padding:16px}.module{padding:20px}h1{font-size:1.4em}}
@media (max-width:640px){body{padding:12px;font-size:13px}.module{padding:16px;margin-bottom:14px;border-radius:8px}.module h2{font-size:1.05em}.kpi-grid{grid-template-columns:1fr 1fr;gap:8px}.two-col{grid-template-columns:1fr;gap:12px}.kpi-value{font-size:1.5em}.bar-label{min-width:90px;font-size:.85em}.bar-value{min-width:80px;font-size:.85em}.drill-btn{width:100%}.viz-btn{flex:1;min-width:auto}}
"""


def render_page(
    body: str,
    title: str = "人力资源管理数据驾驶舱",
    alpine: str = "",
    drill_data: str = "{}",
) -> str:
    """渲染完整 HTML 页面。"""
    # ~2KB vanilla JS：钻取面板 toggle + 数据渲染
    inline_js = """<script>document.addEventListener('click',function(e){if(e.target.classList.contains('drill-btn')){var p=e.target.nextElementSibling;if(p){var open=p.style.display==='block';p.style.display=open?'none':'block';if(!open&&p.innerHTML===''){var k=e.target.getAttribute('data-key');var d=window.HR_DRILL_DATA&&window.HR_DRILL_DATA[k];p.innerHTML=d?renderDrill(d):'<div class="empty">无数据</div>';}}}}});function renderDrill(d){if(!d||!d.rows||!d.rows.length)return'<div class="empty">无数据</div>';var cols=Object.keys(d.rows[0]);var h='<div class="data-table-wrap"><table class="data-table"><thead><tr>';cols.forEach(function(c){h+='<th>'+c+'</th>';});h+='</tr></thead><tbody>';d.rows.slice(0,50).forEach(function(r){h+='<tr>';cols.forEach(function(c){var v=r[c];if(typeof v==='number')v=v.toLocaleString();h+='<td>'+(v==null?'':v)+'</td>';});h+='</tr>';});if(d.rows.length>50)h+='<tr><td colspan="'+cols.length+'" style="text-align:center;color:var(--text-muted)">仅显示前 50 / '+d.rows.length+' 条</td></tr>';return h+'</tbody></table></div>';}</script>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{DARK_THEME_CSS}</style>
</head>
<body>
<h1>{title}</h1>
{body}
<script>window.HR_DRILL_DATA = {drill_data};</script>
{inline_js}
</body>
</html>"""
