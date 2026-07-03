"""HTML base template - 紧凑响应式风格。

设计目标：
- 信息密度最大化（每行一个数据点）
- 桌面 2-3 列 / 平板 2 列 / 手机 1 列
- 紧凑间距，无大卡片
- 50KB 总预算
"""

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
    parts = []
    for code, icon, title in MODULES:
        parts.append(
            f'<section class="module" id="{code}">'
            f"<h2><span class='icon'>{icon}</span>{title}</h2>"
            f'<div class="module-body"></div></section>'
        )
    return "\n".join(parts)


# 紧凑响应式 CSS
COMPACT_CSS = """
:root{--bg:#f7f8fa;--surface:#fff;--surface-2:#fafbfc;--border:#e4e7eb;--border-strong:#cdd2d8;--text:#1f2937;--text-muted:#6b7280;--text-dim:#9ca3af;--primary:#1e5baa;--primary-light:#e8f0fb;--success:#10b981;--warning:#f59e0b;--danger:#ef4444;--orange:#f97316;--cyan:#06b6d4;--radius:6px;}
*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;margin:0;padding:20px 24px;background:var(--bg);color:var(--text);font-size:13.5px;line-height:1.5;-webkit-font-smoothing:antialiased}
h1{font-size:1.5em;font-weight:700;margin:0 0 4px;color:var(--text);letter-spacing:-.3px}
.subtitle{color:var(--text-muted);font-size:.88em;margin:0 0 18px}
.module{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 18px;margin-bottom:12px}
.module h2{margin:0 0 12px;font-size:1em;font-weight:600;color:var(--text);display:flex;align-items:center;gap:8px;padding-bottom:8px;border-bottom:1px solid var(--border)}
.module h2 .icon{font-size:14px}
.module-body{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:8px 24px;align-items:start}
.module-body > .section{break-inside:avoid}
.section{min-width:0}
.section-title{margin:0 0 4px;font-size:.72em;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;padding-top:2px}
.section-title:first-child{margin-top:0}
.stat-list{display:flex;flex-direction:column;gap:1px}
.stat-row{display:grid;grid-template-columns:1fr auto auto 1.2fr;gap:10px;align-items:center;padding:4px 8px;border-radius:4px;font-size:.92em;min-height:26px}
.stat-row:hover{background:var(--surface-2)}
.stat-label{color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.stat-value{color:var(--text);font-weight:600;font-feature-settings:"tnum";white-space:nowrap;text-align:right;min-width:60px}
.stat-bar{height:6px;background:var(--border);border-radius:3px;overflow:hidden;min-width:40px}
.stat-bar-fill{height:100%;background:var(--primary);border-radius:3px;transition:width .4s ease}
.stat-sub{color:var(--text-dim);font-size:.82em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:right}
/* Mini Bar */
.mini-bar{display:flex;flex-direction:column;gap:1px}
.mini-bar-row{display:grid;grid-template-columns:1fr 1.2fr auto 1fr;gap:8px;align-items:center;padding:5px 8px;border-radius:4px;font-size:.9em;min-height:28px}
.mini-bar-row:hover{background:var(--surface-2)}
.mini-bar-label{color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mini-bar-track{height:8px;background:var(--border);border-radius:4px;overflow:hidden;min-width:50px}
.mini-bar-fill{height:100%;background:linear-gradient(90deg,#1e5baa,#3b82f6);border-radius:4px;transition:width .5s ease}
.mini-bar-value{color:var(--text);font-weight:600;font-feature-settings:"tnum";text-align:right;min-width:50px}
.mini-bar-sub{color:var(--text-dim);font-size:.82em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
/* Mini Pie */
.mini-pie{display:flex;align-items:center;gap:14px;padding:6px}
.mini-pie svg{flex-shrink:0}
.mini-pie-legend{flex:1;display:flex;flex-direction:column;gap:3px;min-width:0}
.mini-pie-leg-item{display:flex;align-items:center;gap:6px;font-size:.88em;min-width:0}
.mini-pie-dot{width:10px;height:10px;border-radius:2px;flex-shrink:0}
.mini-pie-leg-label{color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;min-width:0}
.mini-pie-leg-value{color:var(--text-muted);font-feature-settings:"tnum";font-weight:500;white-space:nowrap}
/* Progress */
.prog{display:flex;flex-direction:column;gap:2px}
.prog-row{display:grid;grid-template-columns:1.2fr 1.5fr auto 1fr;gap:8px;align-items:center;padding:5px 8px;border-radius:4px;font-size:.9em}
.prog-row:hover{background:var(--surface-2)}
.prog-label{color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.prog-track{height:8px;background:var(--border);border-radius:4px;overflow:hidden}
.prog-fill{height:100%;border-radius:4px;transition:width .5s ease}
.prog-fill.tone-good{background:linear-gradient(90deg,#10b981,#34d399)}.prog-fill.tone-warn{background:linear-gradient(90deg,#f59e0b,#fbbf24)}.prog-fill.tone-bad{background:linear-gradient(90deg,#ef4444,#f87171)}
.prog-value{color:var(--text);font-weight:600;font-feature-settings:"tnum";white-space:nowrap;min-width:60px;text-align:right}
.prog-sub{color:var(--text-dim);font-size:.82em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
/* Ranking */
.rank{display:flex;flex-direction:column;gap:1px}
.rank-row{display:grid;grid-template-columns:24px 1fr auto 1fr;gap:10px;align-items:center;padding:5px 8px;border-radius:4px;font-size:.9em;min-height:28px}
.rank-row:hover{background:var(--surface-2)}
.rank-badge{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;background:#cbd5e1;color:#475569;border-radius:50%;font-weight:600;font-size:.78em}
.rank-badge.rank-1{background:linear-gradient(135deg,#fbbf24,#f59e0b);color:#fff;box-shadow:0 1px 3px rgba(245,158,11,.3)}
.rank-badge.rank-2{background:linear-gradient(135deg,#d1d5db,#9ca3af);color:#fff}
.rank-badge.rank-3{background:linear-gradient(135deg,#fed7aa,#fb923c);color:#fff}
.rank-label{color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rank-value{color:var(--text);font-weight:600;font-feature-settings:"tnum";text-align:right;min-width:60px}
.rank-sub{color:var(--text-dim);font-size:.82em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
/* Plain List */
.list{display:flex;flex-direction:column;gap:1px}
.list-row{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:center;padding:4px 8px;border-radius:4px;font-size:.9em;min-height:24px}
.list-row:hover{background:var(--surface-2)}
.list-label{color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.list-value{color:var(--text);font-weight:600;font-feature-settings:"tnum";text-align:right;min-width:60px}
.list-sub{color:var(--text-dim);font-size:.82em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:right}
.hierarchy-list{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:2px 16px}
.hierarchy-list li{display:flex;justify-content:space-between;align-items:baseline;padding:3px 8px;border-radius:4px;font-size:.92em}
.hierarchy-list li:hover{background:var(--surface-2)}
.h-name{color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-right:8px}
.h-count{color:var(--text-muted);font-feature-settings:"tnum";font-weight:500;white-space:nowrap}
.table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--border);border-radius:4px;background:#fff;margin-top:4px}
.data-table{width:100%;border-collapse:collapse;font-size:.88em}
.data-table th{text-align:left;padding:6px 10px;background:var(--surface-2);color:var(--text-muted);font-weight:600;border-bottom:1px solid var(--border);text-transform:uppercase;font-size:.78em;letter-spacing:.4px;white-space:nowrap}
.data-table td{padding:5px 10px;border-bottom:1px solid var(--border);font-feature-settings:"tnum";color:var(--text)}
.data-table tbody tr:last-child td{border-bottom:0}
.data-table tbody tr:hover{background:var(--surface-2)}
.empty{color:var(--text-dim);font-style:italic;font-size:.85em}
@media (max-width:1100px){body{padding:16px 18px}.module-body{grid-template-columns:1fr 1fr}}
@media (max-width:760px){body{padding:12px;font-size:13px}.module{padding:12px 14px;margin-bottom:10px}.module h2{font-size:.95em}.module-body{grid-template-columns:1fr;gap:8px}.stat-row{grid-template-columns:1fr auto auto;font-size:.95em;padding:5px 4px}.stat-sub{display:none}.hierarchy-list{grid-template-columns:1fr 1fr}}
@media (max-width:480px){body{padding:10px;font-size:12.5px}.stat-row{grid-template-columns:1fr auto;font-size:.92em}.hierarchy-list{grid-template-columns:1fr}}
"""


def render_page(body: str, title: str = "人力资源管理数据驾驶舱", drill_data: str = "{}") -> str:
    inline_js = ""  # 当前无钻取
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{COMPACT_CSS}</style>
</head>
<body>
<h1>{title}</h1>
{body}
</body>
</html>"""
