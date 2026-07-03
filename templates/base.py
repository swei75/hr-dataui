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
