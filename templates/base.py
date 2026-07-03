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
    parts = []
    for code, icon, title in MODULES:
        parts.append(
            f'<section class="module" id="{code}">'
            f"<h2>{icon} {title}</h2>"
            f'<div class="module-body"><!-- P4 填充 --></div>'
            f"</section>"
        )
    return "\n".join(parts)


# 浅色专业报告风（参考 shanjinki editorial + 现代企业仪表盘）
LIGHT_THEME_CSS = """
:root{
  --bg:#f7f8fa;--surface:#ffffff;--surface-2:#fafbfc;--border:#e4e7eb;--border-strong:#cdd2d8;
  --text:#1f2937;--text-muted:#6b7280;--text-dim:#9ca3af;
  --primary:#1e5baa;--primary-light:#e8f0fb;--primary-dark:#154580;
  --success:#10b981;--warning:#f59e0b;--danger:#ef4444;--purple:#8b5cf6;--orange:#f97316;--cyan:#06b6d4;
  --grad-blue:linear-gradient(90deg,#1e5baa,#3b82f6);
  --shadow-sm:0 1px 2px rgba(0,0,0,.04);--shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);
  --radius:8px;--radius-sm:6px;
}
*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;margin:0;padding:32px;background:var(--bg);color:var(--text);font-size:14px;line-height:1.6;-webkit-font-smoothing:antialiased}
h1{font-size:1.7em;font-weight:700;margin:0 0 8px;color:var(--text);letter-spacing:-.3px}
.subtitle{color:var(--text-muted);font-size:.95em;margin:0 0 24px}
.module{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px;margin-bottom:18px;box-shadow:var(--shadow-sm)}
.module h2{margin:0 0 18px;font-size:1.1em;font-weight:600;color:var(--text);display:flex;align-items:center;gap:10px;padding-bottom:14px;border-bottom:2px solid var(--border)}
.module h2 .icon{width:28px;height:28px;display:inline-flex;align-items:center;justify-content:center;background:var(--primary-light);color:var(--primary);border-radius:6px;font-size:14px}
.module-body{display:flex;flex-direction:column;gap:14px}
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.three-col{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
.full-col{display:grid;grid-template-columns:1fr}
.section-card{background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px 16px;min-width:0;transition:border-color .15s ease,box-shadow .15s ease}
.section-card:hover{border-color:var(--border-strong);box-shadow:var(--shadow)}
.section-card.compact{padding:12px 14px}
.section-title{margin:0 0 10px;font-size:.78em;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.6px;display:flex;align-items:center;gap:6px}
.section-title::before{content:"";display:inline-block;width:3px;height:12px;background:var(--primary);border-radius:2px}
.section-body{min-width:0}
.viz-switch{display:flex;gap:4px;margin-bottom:10px;flex-wrap:wrap}
.viz-btn{padding:5px 10px;min-height:30px;background:var(--surface);border:1px solid var(--border);color:var(--text-muted);border-radius:var(--radius-sm);cursor:pointer;font-size:.82em;transition:all .12s ease}
.viz-btn:hover{border-color:var(--primary);color:var(--primary)}
.viz-btn.active{background:var(--primary);border-color:var(--primary);color:#fff}
.kpi-card{background:#fff;border:1px solid var(--border);border-left:3px solid var(--primary);padding:12px 14px;border-radius:var(--radius-sm);transition:all .15s ease}
.kpi-card:hover{border-color:var(--primary);box-shadow:var(--shadow)}
.kpi-value{font-size:1.6em;font-weight:700;color:var(--text);line-height:1.1;font-feature-settings:"tnum";letter-spacing:-.5px}
.kpi-value.tone-blue{color:var(--primary)}.kpi-value.tone-green{color:var(--success)}.kpi-value.tone-orange{color:var(--orange)}.kpi-value.tone-red{color:var(--danger)}
.kpi-value .unit{font-size:.55em;font-weight:500;color:var(--text-muted);margin-left:4px}
.kpi-sub{color:var(--text-muted);font-size:.8em;margin-top:3px}
.bar-row{display:flex;align-items:center;gap:10px;margin:6px 0}
.bar-label{min-width:120px;color:var(--text);font-size:.88em}
.bar-track{flex:1;background:var(--border);height:8px;border-radius:4px;overflow:hidden}
.bar-fill{background:var(--grad-blue);height:100%;border-radius:4px;transition:width .5s ease}
.bar-value{min-width:90px;text-align:right;color:var(--text-muted);font-size:.82em;font-feature-settings:"tnum"}
.pie-chart{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.pie-legend{flex:1;min-width:160px}
.pie-legend > div{display:flex;align-items:center;gap:8px;margin:3px 0;font-size:.88em}
.pie-legend > div > span:first-child{width:10px;height:10px;border-radius:2px;flex-shrink:0}
.funnel-chart{display:flex;flex-direction:column;align-items:stretch;gap:3px;padding:6px 0}
.funnel-step{background:var(--grad-blue);color:#fff;padding:8px 14px;border-radius:var(--radius-sm);font-weight:500;font-size:.92em;display:flex;justify-content:space-between;align-items:center;font-feature-settings:"tnum";transition:transform .12s ease}
.funnel-step:hover{transform:translateX(4px)}
.progress{margin:8px 0}
.progress-label{display:flex;justify-content:space-between;margin-bottom:5px;font-size:.85em}
.progress-label > span:last-child{color:var(--text-muted);font-feature-settings:"tnum"}
.progress-track{background:var(--border);height:6px;border-radius:3px;overflow:hidden}
.progress-fill{height:100%;border-radius:3px;transition:width .5s ease}
.progress-fill.tone-good{background:var(--success)}.progress-fill.tone-warn{background:var(--warning)}.progress-fill.tone-bad{background:var(--danger)}
.ranking-table{width:100%;border-collapse:collapse;font-size:.9em}
.ranking-table td{padding:6px 10px;border-bottom:1px solid var(--border)}
.ranking-table tr:last-child td{border-bottom:0}
.ranking-table tr:hover td{background:var(--surface-2)}
.rank-badge{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;background:var(--primary);color:#fff;border-radius:50%;font-weight:600;font-size:.8em}
.rank-badge.rank-1{background:var(--success)}.rank-badge.rank-2{background:#34d399}.rank-badge.rank-3{background:#6ee7b7;color:var(--text)}
.hierarchy{padding:2px 0;font-size:.92em}
.hierarchy ul{list-style:none;padding-left:18px;margin:3px 0;border-left:1px dashed var(--border)}
.hierarchy-node{padding:3px 0}
.hierarchy-name{color:var(--text);font-weight:500}
.hierarchy-count{color:var(--text-muted);font-size:.85em;margin-left:4px;font-feature-settings:"tnum"}
.data-table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--border);border-radius:var(--radius-sm);background:#fff}
.data-table{width:100%;border-collapse:collapse;font-size:.88em}
.data-table th{text-align:left;padding:8px 12px;background:var(--surface-2);color:var(--text-muted);font-weight:600;border-bottom:1px solid var(--border);text-transform:uppercase;font-size:.78em;letter-spacing:.5px}
.data-table td{padding:6px 12px;border-bottom:1px solid var(--border);font-feature-settings:"tnum"}
.data-table tbody tr:last-child td{border-bottom:0}
.data-table tbody tr:hover{background:var(--surface-2)}
.drill-btn{padding:8px 14px;min-height:36px;background:transparent;border:1px solid var(--primary);color:var(--primary);border-radius:var(--radius-sm);cursor:pointer;font-size:.85em;font-weight:500;transition:all .12s ease;margin-top:10px}
.drill-btn:hover{background:var(--primary);color:#fff}
.drill-btn:active{transform:scale(.98)}
.drill-panel{margin-top:10px;padding:14px;background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius-sm);display:none;animation:slideDown .18s ease}
@keyframes slideDown{from{opacity:0;transform:translateY(-3px)}to{opacity:1;transform:translateY(0)}}
.empty{color:var(--text-dim);text-align:center;padding:16px;font-style:italic;font-size:.9em}
@media (max-width:980px){body{padding:20px}h1{font-size:1.4em}.module{padding:20px}}
@media (max-width:640px){body{padding:12px;font-size:13px}.module{padding:16px;margin-bottom:14px}.module h2{font-size:1em}.kpi-grid{grid-template-columns:repeat(2,1fr);gap:8px}.two-col,.three-col{grid-template-columns:1fr;gap:12px}.kpi-value{font-size:1.3em}.bar-label{min-width:80px;font-size:.82em}.bar-value{min-width:70px;font-size:.78em}.drill-btn{width:100%}.viz-btn{flex:1;min-width:auto}}
"""


def render_page(
    body: str,
    title: str = "人力资源管理数据驾驶舱",
    alpine: str = "",
    drill_data: str = "{}",
) -> str:
    inline_js = """<script>document.addEventListener('click',function(e){if(e.target.classList.contains('drill-btn')){var p=e.target.nextElementSibling;if(p){var open=p.style.display==='block';p.style.display=open?'none':'block';if(!open&&p.innerHTML===''){var k=e.target.getAttribute('data-key');var d=window.HR_DRILL_DATA&&window.HR_DRILL_DATA[k];p.innerHTML=d?renderDrill(d):'<div class="empty">无数据</div>';}}}}});function renderDrill(d){if(!d||!d.rows||!d.rows.length)return'<div class="empty">无数据</div>';var cols=Object.keys(d.rows[0]);var h='<div class="data-table-wrap"><table class="data-table"><thead><tr>';cols.forEach(function(c){h+='<th>'+c+'</th>';});h+='</tr></thead><tbody>';d.rows.slice(0,50).forEach(function(r){h+='<tr>';cols.forEach(function(c){var v=r[c];if(typeof v==='number')v=v.toLocaleString();h+='<td>'+(v==null?'':v)+'</td>';});h+='</tr>';});if(d.rows.length>50)h+='<tr><td colspan="'+cols.length+'" style="text-align:center;color:var(--text-muted)">仅显示前 50 / '+d.rows.length+' 条</td></tr>';return h+'</tbody></table></div>';}</script>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{LIGHT_THEME_CSS}</style>
</head>
<body>
<h1>{title}</h1>
<p class="subtitle">报告期：{title.split('（')[-1].rstrip('）') if '（' in title else ''}</p>
{body}
<script>window.HR_DRILL_DATA = {drill_data};</script>
{inline_js}
</body>
</html>"""
