"""HTML base template - 现代 HR 仪表盘风格。

设计参考：
- shanjinki 真实 HR 报告（多 card 嵌套 + 主题色 + 圆角 12-18px）
- shadcn/Vercel 风格（中性灰 + 蓝色点缀 + 8px 网格 + 微阴影）
- Linear 风格（subtle 边框 + 紧凑 padding + Inter 字体）
"""

# 模块元数据
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


# ============ 设计系统 tokens ============
# 中性灰阶（zinc/gray 色系）
# 单一蓝色主色（indigo-600 #4f46e5 风格）
# 状态色：success / warn / danger

DESIGN_TOKENS = """
:root{
  --bg:#fafafa;--surface:#ffffff;--surface-2:#f4f4f5;--surface-hover:#f9fafb;
  --border:#e4e4e7;--border-strong:#d4d4d8;--border-muted:#f4f4f5;
  --text:#18181b;--text-muted:#52525b;--text-dim:#a1a1aa;--text-faint:#d4d4d8;
  --primary:#4f46e5;--primary-light:#eef2ff;--primary-hover:#4338ca;
  --success:#10b981;--success-light:#d1fae5;
  --warning:#f59e0b;--warning-light:#fef3c7;
  --danger:#ef4444;--danger-light:#fee2e2;
  --info:#0ea5e9;--info-light:#e0f2fe;
  --purple:#8b5cf6;--orange:#f97316;--cyan:#06b6d4;--pink:#ec4899;
  --shadow-sm:0 1px 2px 0 rgb(0 0 0 / .05);
  --shadow:0 1px 3px 0 rgb(0 0 0 / .08), 0 1px 2px -1px rgb(0 0 0 / .05);
  --shadow-md:0 4px 6px -1px rgb(0 0 0 / .07), 0 2px 4px -2px rgb(0 0 0 / .05);
  --radius:12px;--radius-sm:8px;--radius-xs:4px;--radius-pill:9999px;
}
*::selection{background:var(--primary-light);color:var(--primary-hover)}
*::-webkit-scrollbar{width:8px;height:8px}
*::-webkit-scrollbar-thumb{background:var(--border-strong);border-radius:8px}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Inter","Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
  margin:0;padding:0;background:var(--bg);color:var(--text);
  font-size:14px;line-height:1.55;-webkit-font-smoothing:antialiased;font-feature-settings:"cv02","cv03","cv11","ss01";
  font-variant-numeric:tabular-nums;
}
a{color:var(--primary);text-decoration:none}
h1,h2,h3,h4{margin:0;font-weight:600;letter-spacing:-.01em}

/* ============ Hero ============ */
.hero{background:linear-gradient(180deg,#fff 0%,var(--bg) 100%);padding:32px 40px 24px;border-bottom:1px solid var(--border)}
.hero-inner{max-width:1400px;margin:0 auto;display:flex;align-items:flex-end;justify-content:space-between;gap:24px;flex-wrap:wrap}
.hero-title{font-size:1.75em;font-weight:700;letter-spacing:-.02em;color:var(--text);line-height:1.2}
.hero-subtitle{color:var(--text-muted);font-size:.92em;margin-top:6px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.hero-subtitle .badge{background:var(--primary-light);color:var(--primary);padding:2px 10px;border-radius:var(--radius-pill);font-size:.78em;font-weight:500}
.hero-meta{text-align:right;color:var(--text-muted);font-size:.82em}
.hero-meta strong{color:var(--text);font-weight:600}

/* ============ KPI strip ============ */
.kpi-strip{max-width:1400px;margin:24px auto 0;padding:0 40px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}
.kpi-strip-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow-sm);transition:all .15s ease;position:relative;overflow:hidden}
.kpi-strip-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--primary);opacity:0;transition:opacity .15s ease}
.kpi-strip-card:hover{box-shadow:var(--shadow);transform:translateY(-1px);border-color:var(--border-strong)}
.kpi-strip-card:hover::before{opacity:1}
.kpi-strip-card .kpi-strip-label{font-size:.78em;color:var(--text-muted);font-weight:500;text-transform:uppercase;letter-spacing:.4px}
.kpi-strip-card .kpi-strip-value{font-size:1.65em;font-weight:700;color:var(--text);line-height:1.1;margin-top:4px;letter-spacing:-.02em}
.kpi-strip-card .kpi-strip-sub{font-size:.78em;color:var(--text-muted);margin-top:4px;display:flex;align-items:center;gap:4px}
.trend-up{color:var(--success);font-weight:600}
.trend-down{color:var(--danger);font-weight:600}
.trend-flat{color:var(--text-dim)}

/* ============ Main grid ============ */
.dashboard{max-width:1400px;margin:24px auto;padding:0 40px 60px}
.module{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:18px;box-shadow:var(--shadow-sm);overflow:hidden}
.module-head{padding:16px 24px;border-bottom:1px solid var(--border-muted);display:flex;align-items:center;gap:12px;background:var(--surface)}
.module-icon{width:36px;height:36px;background:var(--primary-light);color:var(--primary);border-radius:var(--radius-sm);display:inline-flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.module-title{font-size:1.05em;font-weight:600;color:var(--text)}
.module-sub{font-size:.78em;color:var(--text-muted);margin-left:8px}
.module-body{padding:20px 24px;display:grid;grid-template-columns:repeat(12,1fr);gap:16px}
.section{grid-column:span 6;min-width:0}
.section.span-12{grid-column:span 12}
.section.span-4{grid-column:span 4}
.section.span-8{grid-column:span 8}
.section-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;padding-bottom:8px;border-bottom:1px dashed var(--border-muted)}
.section-title{font-size:.85em;font-weight:600;color:var(--text);display:flex;align-items:center;gap:6px}
.section-title-dot{width:6px;height:6px;border-radius:50%;background:var(--primary);flex-shrink:0}
.section-meta{font-size:.72em;color:var(--text-dim);font-weight:500}

/* ============ Viz: Stat card ============ */
.stat-card{background:var(--surface-2);border:1px solid var(--border-muted);border-radius:var(--radius-sm);padding:12px 14px}
.stat-card-label{font-size:.78em;color:var(--text-muted);font-weight:500;margin-bottom:2px}
.stat-card-value{font-size:1.4em;font-weight:700;color:var(--text);letter-spacing:-.02em}
.stat-card-value.tone-blue{color:var(--primary)}.stat-card-value.tone-green{color:var(--success)}.stat-card-value.tone-orange{color:var(--orange)}.stat-card-value.tone-red{color:var(--danger)}
.stat-card-sub{font-size:.78em;color:var(--text-dim);margin-top:2px}

/* ============ Viz: Horizontal bar list ============ */
.bar-list{display:flex;flex-direction:column;gap:8px}
.bar-row{display:grid;grid-template-columns:120px 1fr 80px;gap:10px;align-items:center;font-size:.88em}
.bar-row-label{color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bar-row-track{height:8px;background:var(--surface-2);border-radius:var(--radius-pill);overflow:hidden;position:relative;border:1px solid var(--border-muted)}
.bar-row-fill{height:100%;background:var(--primary);border-radius:var(--radius-pill);transition:width .6s cubic-bezier(.4,0,.2,1)}
.bar-row-fill.tone-orange{background:var(--orange)}
.bar-row-fill.tone-green{background:var(--success)}
.bar-row-fill.tone-purple{background:var(--purple)}
.bar-row-fill.tone-cyan{background:var(--cyan)}
.bar-row-value{color:var(--text-muted);font-weight:600;text-align:right;font-size:.92em;white-space:nowrap}
.bar-row-sub{grid-column:2 / 4;color:var(--text-dim);font-size:.78em;margin-top:-4px;padding-left:2px}

/* ============ Viz: Donut ============ */
.donut-wrap{display:flex;align-items:center;gap:16px}
.donut-svg{width:120px;height:120px;flex-shrink:0}
.donut-center{font-size:1.4em;font-weight:700;fill:var(--text)}
.donut-center-sub{font-size:.7em;fill:var(--text-muted);font-weight:500}
.donut-legend{flex:1;display:flex;flex-direction:column;gap:6px;min-width:0}
.donut-leg-row{display:flex;align-items:center;gap:8px;font-size:.85em;padding:4px 8px;border-radius:var(--radius-xs);transition:background .12s}
.donut-leg-row:hover{background:var(--surface-2)}
.donut-leg-dot{width:10px;height:10px;border-radius:3px;flex-shrink:0}
.donut-leg-label{color:var(--text);flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.donut-leg-value{color:var(--text-muted);font-weight:600;font-feature-settings:"tnum";white-space:nowrap}

/* ============ Viz: Progress ============ */
.prog-list{display:flex;flex-direction:column;gap:12px}
.prog-row{display:flex;flex-direction:column;gap:5px}
.prog-row-head{display:flex;justify-content:space-between;align-items:baseline;font-size:.88em}
.prog-row-label{color:var(--text);font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.prog-row-value{color:var(--text-muted);font-weight:600;font-feature-settings:"tnum";font-size:.95em}
.prog-row-value .tone-good{color:var(--success)}.prog-row-value .tone-warn{color:var(--warning)}.prog-row-value .tone-bad{color:var(--danger)}
.prog-row-bar{height:10px;background:var(--surface-2);border-radius:var(--radius-pill);overflow:hidden;border:1px solid var(--border-muted);position:relative}
.prog-row-fill{height:100%;border-radius:var(--radius-pill);transition:width .7s cubic-bezier(.4,0,.2,1)}
.prog-row-fill.tone-good{background:linear-gradient(90deg,#10b981,#34d399)}
.prog-row-fill.tone-warn{background:linear-gradient(90deg,#f59e0b,#fbbf24)}
.prog-row-fill.tone-bad{background:linear-gradient(90deg,#ef4444,#f87171)}

/* ============ Viz: Rank list ============ */
.rank-list{display:flex;flex-direction:column;gap:6px}
.rank-row{display:grid;grid-template-columns:28px 1fr auto;gap:10px;align-items:center;padding:6px 10px;border-radius:var(--radius-sm);transition:background .12s;font-size:.88em}
.rank-row:hover{background:var(--surface-2)}
.rank-badge{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;background:var(--surface-2);color:var(--text-muted);border:1px solid var(--border);border-radius:50%;font-weight:600;font-size:.8em;font-feature-settings:"tnum"}
.rank-badge.gold{background:linear-gradient(135deg,#fde68a,#f59e0b);color:#fff;border-color:transparent;box-shadow:0 1px 3px rgb(245 158 11 / .3)}
.rank-badge.silver{background:linear-gradient(135deg,#e5e7eb,#9ca3af);color:#fff;border-color:transparent}
.rank-badge.bronze{background:linear-gradient(135deg,#fed7aa,#fb923c);color:#fff;border-color:transparent}
.rank-label{color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rank-value{color:var(--text-muted);font-weight:600;font-feature-settings:"tnum";font-size:.95em;white-space:nowrap}

/* ============ Viz: Table ============ */
.data-table{width:100%;border-collapse:collapse;font-size:.88em}
.data-table th{text-align:left;padding:8px 12px;background:var(--surface-2);color:var(--text-muted);font-weight:600;border-bottom:1px solid var(--border);text-transform:uppercase;font-size:.74em;letter-spacing:.5px;white-space:nowrap}
.data-table td{padding:8px 12px;border-bottom:1px solid var(--border-muted);font-feature-settings:"tnum";color:var(--text)}
.data-table tbody tr:last-child td{border-bottom:0}
.data-table tbody tr:hover{background:var(--surface-hover)}
.data-table .num{text-align:right;font-weight:600}
.data-table .pct{color:var(--text-muted);font-size:.95em}

/* ============ Viz: Grid (网点等) ============ */
.grid-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:6px}
.grid-item{display:flex;justify-content:space-between;align-items:baseline;padding:6px 10px;background:var(--surface-2);border:1px solid var(--border-muted);border-radius:var(--radius-xs);font-size:.85em;transition:all .12s}
.grid-item:hover{background:var(--surface-hover);border-color:var(--border)}
.grid-item-label{color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-right:6px}
.grid-item-value{color:var(--text-muted);font-weight:600;font-feature-settings:"tnum";white-space:nowrap}

/* ============ Insight callout ============ */
.insight{background:linear-gradient(135deg,var(--primary-light) 0%,#f0f9ff 100%);border:1px solid var(--primary);border-radius:var(--radius-sm);padding:12px 16px;display:flex;gap:10px;font-size:.88em;align-items:flex-start}
.insight-icon{width:20px;height:20px;background:var(--primary);color:#fff;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0}
.insight-body{color:var(--text);line-height:1.5}
.insight-body strong{color:var(--primary-hover)}

/* ============ Responsive ============ */
@media (max-width:1100px){
  .hero{padding:24px}
  .kpi-strip,.dashboard{padding-left:24px;padding-right:24px}
  .module-body{grid-template-columns:repeat(6,1fr);gap:14px}
  .section{grid-column:span 6}
  .section.span-4{grid-column:span 6}
  .section.span-8{grid-column:span 6}
}
@media (max-width:768px){
  body{font-size:13.5px}
  .hero{padding:20px 16px 16px}
  .hero-title{font-size:1.4em}
  .hero-inner{flex-direction:column;align-items:flex-start;gap:8px}
  .hero-meta{text-align:left}
  .kpi-strip,.dashboard{padding-left:16px;padding-right:16px;margin-top:16px}
  .kpi-strip{grid-template-columns:repeat(2,1fr);gap:10px}
  .kpi-strip-card{padding:12px 14px}
  .kpi-strip-card .kpi-strip-value{font-size:1.3em}
  .module{margin-bottom:14px;border-radius:var(--radius-sm)}
  .module-head{padding:12px 16px}
  .module-body{grid-template-columns:1fr;gap:14px;padding:14px 16px}
  .section,.section.span-4,.section.span-8,.section.span-12{grid-column:1}
  .bar-row{grid-template-columns:90px 1fr 70px;font-size:.85em}
  .donut-wrap{flex-direction:column;align-items:flex-start;gap:12px}
  .grid-list{grid-template-columns:repeat(2,1fr)}
}
@media (max-width:480px){
  body{font-size:13px}
  .kpi-strip{grid-template-columns:1fr 1fr}
  .bar-row{grid-template-columns:80px 1fr 60px}
  .grid-list{grid-template-columns:1fr}
}
"""


def render_page(body: str, title: str = "人力资源管理数据驾驶舱", subtitle: str = "", report_date: str = "2026年5月") -> str:
    """渲染完整页面。"""
    hero = f"""
<header class="hero">
  <div class="hero-inner">
    <div>
      <h1 class="hero-title">{title}</h1>
      <p class="hero-subtitle"><span class="badge">月度报告</span> 报告期：{report_date} · 数据截至月末</p>
    </div>
    <div class="hero-meta">
      <strong>XX 银行 · 人力资源部</strong><br>
      <span>报告生成：2026-07-03</span>
    </div>
  </div>
</header>
"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{DESIGN_TOKENS}</style>
</head>
<body>
{hero}
<main class="dashboard">
{body}
</main>
</body>
</html>"""


def render_module_placeholders() -> str:
    return "\n".join(
        f'<section class="module"><div class="module-head"><div class="module-icon">{icon}</div><div><div class="module-title">{title}</div></div></div><div class="module-body"></div></section>'
        for _, icon, title in MODULES
    )
