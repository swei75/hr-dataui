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

# v1.4 风险等级色（前后对比覆盖 v1.3 的 --success/--warning/--danger 浅绿色）
# v1.3 colors kept for unrelated usages; v1.4 ADDS stronger semantic tokens.
# 注：v1.4 plan 要求 #16A34A / #D97706 / #DC2626；用 -fg 作为前景文字色。
DESIGN_TOKENS = """
:root{
  --bg:#fbf4e9;--surface:#fefcf7;--surface-2:#f4eadb;--surface-hover:#fef6e6;
  --border:#e8d8c3;--border-strong:#d4b896;--border-muted:#ead9c3;
  --text:#241b15;--text-muted:#7b6653;--text-dim:#a89880;--text-faint:#d4c4ad;
  --primary:#9f6b44;--primary-light:#ead9c3;--primary-hover:#6b4423;
  /* v1.4 risk tokens (米色红棕风格) */
  --success:#4a7c59;--success-foreground:#FFFFFF;
  --warning:#a04030;--warning-foreground:#FFFFFF;
  --danger:#8b2e2e;--danger-foreground:#FFFFFF;
  --success-soft:#4a7c59;--success-light:#d4dfcc;
  --warning-soft:#a04030;--warning-light:#ddcfc6;
  --danger-soft:#8b2e2e;--danger-light:#e0ced7;
  --info:#5d7b8e;--info-light:#d6e0e6;
  --purple:#8b5e83;--orange:#c47a3d;--cyan:#5d8a8e;--pink:#a45878;
  /* v1.5.21: 顶部 hero 区广银化（不污染 6 模块） */
  --hero-red:#c8102e;--hero-red-deep:#a40e25;--hero-gold:#f5b500;--hero-gold-soft:#fff3cd;--hero-text-on-red:#fff;--hero-bg-warm:#fff8e6;
  /* v1.4 8 进制 spacing scale */
  --space-1:8px;--space-2:16px;--space-3:24px;--space-4:32px;--space-5:48px;--space-6:64px;
  --shadow-sm:0 1px 2px 0 rgb(36 27 21 / .06);
  --shadow:0 2px 6px 0 rgb(36 27 21 / .08), 0 1px 2px -1px rgb(36 27 21 / .04);
  --shadow-md:0 6px 14px -2px rgb(36 27 21 / .10), 0 3px 6px -2px rgb(36 27 21 / .06);
  --radius:14px;--radius-sm:10px;--radius-xs:6px;--radius-pill:9999px;
}
body{counter-reset:module}
*::selection{background:var(--primary-light);color:var(--primary-hover)}
*::-webkit-scrollbar{width:8px;height:8px}
*::-webkit-scrollbar-thumb{background:var(--border-strong);border-radius:8px}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Inter","Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
  margin:0;padding:0;background:var(--bg);color:var(--text);
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased;font-feature-settings:"cv02","cv03","cv11","ss01";
  font-variant-numeric:tabular-nums;
}
a{color:var(--primary);text-decoration:none}
h1,h2,h3,h4{margin:0;font-weight:600;letter-spacing:-.01em}

/* ============ Hero（v1.5.21: 广银红+金招牌） ============ */
.hero{background:linear-gradient(135deg,var(--hero-red) 0%,var(--hero-red-deep) 100%);padding:40px 36px 24px;border-bottom:3px solid var(--hero-gold);color:var(--hero-text-on-red)}
.hero-inner{max-width:1400px;margin:0 auto;display:flex;align-items:flex-end;justify-content:space-between;gap:24px;flex-wrap:wrap}
.hero-title{font-size:3.4em;font-weight:800;letter-spacing:-.03em;color:var(--hero-text-on-red);line-height:1.15;text-shadow:0 2px 8px rgb(0 0 0 / .15)}
.hero-subtitle{color:var(--hero-gold-soft);font-size:1.1em;margin-top:12px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.hero-subtitle .badge{background:var(--hero-gold);color:var(--hero-red-deep);padding:4px 16px;border-radius:var(--radius-pill);font-size:.95em;font-weight:700;border:1px solid rgb(255 255 255 / .3)}
.hero-meta{text-align:right;color:var(--hero-gold-soft);font-size:1.02em}
.hero-meta strong{color:var(--hero-text-on-red);font-weight:700;font-size:1.15em}

/* ============ KPI strip ============ */
.kpi-strip{max-width:1400px;margin:18px auto 0;padding:0 36px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}
.kpi-strip-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow-sm);transition:all .15s ease;position:relative;overflow:hidden}
.kpi-strip-card::before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:var(--primary);opacity:0;transition:opacity .15s ease}
.kpi-strip-card:hover{box-shadow:var(--shadow);transform:translateY(-1px);border-color:var(--border-strong)}
.kpi-strip-card:hover::before{opacity:1}
.kpi-strip-card .kpi-strip-label{font-size:.95em;color:var(--text-muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px}
.kpi-strip-card .kpi-strip-value{font-size:2.7em;font-weight:800;color:var(--text);line-height:1.1;margin-top:6px;letter-spacing:-.03em}
.kpi-strip-card .kpi-strip-sub{font-size:.92em;color:var(--text-muted);margin-top:6px;display:flex;align-items:center;gap:5px}

/* ============ v1.5.19: Dashboard 顶部 v_hero 数字塔（区别于模块内 KPI 卡） ============ */
.kpi-hero{max-width:1400px;margin:18px auto 0;padding:0 36px;display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
.kpi-hero-card{background:var(--hero-text-on-red);border:1px solid var(--border);border-radius:var(--radius);padding:18px 20px;display:flex;align-items:center;gap:14px;box-shadow:var(--shadow-sm);position:relative;overflow:hidden;transition:transform .15s ease, box-shadow .15s ease;color:var(--text)}
.kpi-hero-card:hover{transform:translateY(-2px);box-shadow:var(--shadow-md)}
.kpi-hero-card::after{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--primary)}
.kpi-hero-card:nth-child(1)::after{background:var(--hero-red)}
.kpi-hero-card:nth-child(2)::after{background:var(--hero-red-deep)}
.kpi-hero-card:nth-child(3)::after{background:var(--hero-gold)}
.kpi-hero-card:nth-child(4)::after{background:#e63946}
.kpi-hero-card:nth-child(5)::after{background:#d62828}
.kpi-hero-card:nth-child(6)::after{background:#9d0208}
.kpi-hero-icon{width:48px;height:48px;background:var(--hero-red-deep);color:var(--hero-text-on-red);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0;border:1px solid var(--hero-gold)}
.kpi-hero-body{flex:1;min-width:0}
.kpi-hero-label{font-size:.78em;color:var(--text-muted);font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin-bottom:2px}
.kpi-hero-value{font-size:1.85em;font-weight:800;color:var(--text);line-height:1.1;letter-spacing:-.025em;font-variant-numeric:tabular-nums;display:flex;align-items:baseline;gap:3px;min-width:0;flex-wrap:nowrap;white-space:nowrap;overflow:hidden}
.kpi-hero-card{min-width:0}
.kpi-hero-num{white-space:nowrap}
.kpi-hero-unit{font-size:.4em;color:var(--text-muted);font-weight:700;margin-left:0;flex-shrink:0}
.kpi-hero-unit{font-size:.4em;color:var(--text-muted);font-weight:700;margin-left:2px}
.kpi-hero-sub{font-size:.78em;color:var(--text-muted);margin-top:4px;line-height:1.4}
.kpi-hero-bar{display:none}

/* ============ v1.5.3: M-1 KPI Cards (v1 design) ============ */
.kpi-cards-row{grid-column:1 / -1;display:grid;grid-template-columns:repeat(6,1fr);gap:14px;padding:8px 0 4px}
.kpi-card-m1{background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius);padding:22px 18px;position:relative;overflow:hidden;transition:all .15s ease}
.kpi-card-m1::before{content:"";position:absolute;top:0;left:0;right:0;height:5px;background:var(--primary)}
.kpi-card-m1[data-category="success"]::before{background:var(--success)}
.kpi-card-m1[data-category="warning"]::before{background:var(--warning)}
.kpi-card-m1[data-category="danger"]::before{background:var(--danger)}
.kpi-card-m1:hover{transform:translateY(-2px);box-shadow:var(--shadow-md)}
.kpi-card-m1-label{font-size:.95em;color:var(--text-muted);font-weight:700;margin-bottom:12px;letter-spacing:.3px}
.kpi-card-m1-value{font-size:3em;font-weight:800;color:var(--text);line-height:1;letter-spacing:-.035em;margin-bottom:8px;font-feature-settings:"tnum";display:flex;align-items:baseline;gap:4px;white-space:nowrap;min-width:0}
.kpi-card-m1-unit{font-size:.45em;color:var(--text-muted);font-weight:700;margin-left:4px;flex-shrink:0}
.kpi-card-m1-sub{font-size:.92em;color:var(--text-muted);line-height:1.45}

/* ============ v1.5.9: M-2 v11 风格 (4 KPI + 5 段 stacked 卡片 + 8 客户/客服网格) ============ */
.kpi-row.v11{grid-column:1 / -1;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:18px;padding:0}
.kpi.v11{background:var(--primary);color:#fefcf7;border-radius:var(--radius);padding:22px 20px;position:relative;overflow:hidden;border:none;box-shadow:var(--shadow-sm)}
.kpi.v11.alt{background:var(--primary-hover)}
.kpi.v11.acc{background:var(--warning)}
.kpi.v11.ok{background:var(--success)}
.kpi.v11::before{content:"";position:absolute;top:0;right:0;width:120px;height:120px;background:rgba(255,255,255,.06);border-radius:50%;transform:translate(40px,-40px)}
.kpi.v11 .glyph{font-size:22px;opacity:.85;margin-bottom:8px}
.kpi.v11 .label{font-size:.85em;letter-spacing:.04em;opacity:.85;margin-bottom:8px;font-weight:600}
.kpi.v11 .big{font-size:2.6em;font-weight:800;line-height:1;font-variant-numeric:tabular-nums}
.kpi.v11 .unit{font-size:.4em;opacity:.75;margin-left:4px;font-weight:600}
.kpi.v11 .sub{font-size:.82em;margin-top:8px;padding-top:8px;border-top:1px solid rgba(255,255,255,.2);opacity:.85}

.section-title{grid-column:1 / -1;display:flex;align-items:center;gap:10px;margin:16px 0 12px}
.section-title h3{margin:0;font-size:1.1em;color:var(--primary-hover);font-weight:700}
.section-title .pill{font-size:.75em;letter-spacing:.06em;background:var(--primary-light);color:var(--primary-hover);padding:4px 10px;border-radius:999px;font-weight:700}

.dim-grid{grid-column:1 / -1;display:grid;grid-template-columns:.8fr 1.1fr 1.05fr 1.05fr 1.05fr;gap:14px;margin-bottom:16px;padding:0}
.dim-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;border-top:4px solid var(--primary);box-shadow:var(--shadow-sm)}
.dim-card.b{border-top-color:var(--primary-hover)}
.dim-card.c{border-top-color:var(--warning)}
.dim-card.d{border-top-color:var(--success)}
.dim-card.e{border-top-color:#c9a883}
.dim-card .head{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.dim-card .head h4{margin:0;font-size:1em;color:var(--primary-hover);font-weight:700}
.dim-card .head .ttl{font-size:.78em;color:var(--text-muted);letter-spacing:.06em;font-weight:600}
.stacked-bar{height:38px;display:flex;border-radius:6px;overflow:hidden;background:var(--surface-2);margin-bottom:12px}
.stacked-bar .seg{display:flex;align-items:center;justify-content:center;color:#fefcf7;font-size:.78em;font-weight:700;padding:0 4px;white-space:nowrap;overflow:hidden}
.stacked-bar .s1{background:var(--primary-hover)}.stacked-bar .s2{background:var(--primary)}.stacked-bar .s3{background:var(--warning)}.stacked-bar .s4{background:#c9a883}.stacked-bar .s5{background:var(--success)}
.dim-list{display:flex;flex-direction:column;gap:5px}
.dim-list .row{display:grid;grid-template-columns:14px minmax(0,1fr) auto;font-size:.88em;color:var(--text);align-items:center;gap:6px;min-width:0}
.dim-list .row .dot{width:10px;height:10px;border-radius:3px}
.dim-list .row .vl{color:var(--text-muted);font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap}
.dim-list .row>*:not(.dot){white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dot1{background:var(--primary-hover)}.dot2{background:var(--primary)}.dot3{background:var(--warning)}.dot4{background:#c9a883}.dot5{background:var(--success)}

.cs-grid{grid-column:1 / -1;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:16px;padding:0}
.cs-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;border-left:5px solid var(--primary);box-shadow:var(--shadow-sm)}
.cs-card.b{border-left-color:var(--primary-hover)}
.cs-card.c{border-left-color:var(--warning)}
.cs-card.d{border-left-color:var(--success)}
.cs-card .tag{font-size:.78em;color:var(--primary);letter-spacing:.06em;font-weight:700;margin-bottom:6px}
.cs-card .num{font-size:2em;font-weight:800;color:var(--text);font-variant-numeric:tabular-nums;line-height:1;display:flex;align-items:baseline;gap:4px;white-space:nowrap;min-width:0}
.cs-card .num small{font-size:.5em;color:var(--text-muted);margin-left:4px;font-weight:600;flex-shrink:0}
.cs-card .name{font-size:1em;color:var(--text);font-weight:600;margin:8px 0 4px}
.cs-card .meta{font-size:.85em;color:var(--text-muted);line-height:1.6}
.cs-card .mini-stk{height:8px;display:flex;border-radius:4px;overflow:hidden;background:var(--surface-2);margin-top:10px}

/* ============ v1.5.10: M-3 v_hr 风格 (gauge + flow + dual-bar + ranks) ============ */
.gauge-grid{grid-column:1 / -1;display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:16px;padding:0}
.gauge-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:22px 18px;text-align:center;position:relative;box-shadow:var(--shadow-sm)}
.gauge-svg{display:block;margin:0 auto 10px}
.gauge-card .ring-bg{fill:none;stroke:var(--surface-2);stroke-width:10}
.gauge-card .ring-fg{fill:none;stroke-width:10;stroke-linecap:round;transition:stroke-dasharray .8s ease}
.gauge-card .ring-num{font-size:32px;font-weight:800;fill:var(--text);font-variant-numeric:tabular-nums}
.gauge-card .ring-unit{font-size:13px;fill:var(--text-muted)}
.gauge-card .lbl{font-size:1em;color:var(--primary-hover);font-weight:700;margin-bottom:4px}
.gauge-card .sub{font-size:.85em;color:var(--text-muted);line-height:1.5}

.prog-row{grid-column:1 / -1;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:22px 24px;margin-bottom:16px;box-shadow:var(--shadow-sm)}
.prog-row h4{margin:0 0 14px;font-size:1.05em;color:var(--primary-hover);display:flex;justify-content:space-between;align-items:center;font-weight:700}
.prog-row h4 .target{font-size:.85em;color:var(--text-muted);font-weight:500}
.month-bar{display:grid;grid-template-columns:60px 1fr 90px;gap:14px;align-items:center;margin-bottom:10px}
.month-bar:last-child{margin-bottom:0}
.month-bar .m-lbl{font-size:.92em;color:var(--text);font-weight:600}
.month-bar .m-track{height:22px;background:var(--surface-2);border-radius:6px;overflow:hidden;position:relative}
.month-bar .m-fill{height:100%;background:linear-gradient(90deg,var(--primary),var(--primary-hover));border-radius:6px;display:flex;align-items:center;padding-left:8px;color:var(--surface);font-size:.78em;font-weight:700}
.month-bar .m-val{font-size:.92em;color:var(--text);text-align:right;font-variant-numeric:tabular-nums;font-weight:700}

.timeline-wrap{grid-column:1 / -1;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px 28px;margin-bottom:16px;position:relative;box-shadow:var(--shadow-sm)}
.timeline-wrap h4{margin:0 0 18px;font-size:1.05em;color:var(--primary-hover);font-weight:700}
.timeline{position:relative;padding:18px 0 0}
.timeline::before{content:"";position:absolute;left:0;right:0;top:42px;height:3px;background:linear-gradient(90deg,var(--primary) 0%,var(--primary) 41%,var(--warning) 41%,var(--warning) 100%);border-radius:2px}
.tl-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:0}
.tl-node{position:relative;text-align:center;padding-top:0}
.tl-dot{width:18px;height:18px;border-radius:50%;background:var(--primary);border:3px solid var(--bg);margin:34px auto 10px;position:relative;z-index:2;box-shadow:0 0 0 2px var(--primary)}
.tl-dot.warn{background:var(--warning);box-shadow:0 0 0 2px var(--warning)}
.tl-month{font-size:.92em;color:var(--primary-hover);font-weight:700;margin-bottom:4px}
.tl-event{font-size:.85em;color:var(--text);line-height:1.5;padding:0 4px}
.tl-event b{color:var(--primary-hover);font-weight:700;display:block;font-size:.95em;margin-bottom:2px}

.flow-grid{grid-column:1 / -1;display:flex;align-items:stretch;justify-content:space-between;gap:0;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px 28px;margin-bottom:16px;box-shadow:var(--shadow-sm)}
.flow-node{flex:1;background:var(--surface);border:2px solid var(--primary);border-radius:10px;padding:14px 10px;text-align:center;position:relative;min-height:140px}
.flow-node.in{border-color:var(--success)}
.flow-node.out{border-color:var(--warning)}
.flow-node .flow-icon{width:48px;height:48px;background:var(--primary);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;margin:0 auto 8px;box-shadow:var(--shadow-sm)}
.flow-node.in .flow-icon{background:var(--success)}
.flow-node.out .flow-icon{background:var(--warning)}
.flow-node .flow-title{font-size:.92em;color:var(--primary-hover);font-weight:700;margin-bottom:6px;letter-spacing:.04em}
.flow-node .flow-metric{font-size:2em;font-weight:800;color:var(--text);font-variant-numeric:tabular-nums;line-height:1}
.flow-node.in .flow-metric{color:var(--success)}
.flow-node.out .flow-metric{color:var(--warning)}
.flow-node .flow-unit{font-size:.4em;color:var(--text-muted);font-weight:700;margin-left:3px}
.flow-node .flow-sub{font-size:.78em;color:var(--text-muted);margin-top:6px;line-height:1.4}
.flow-arrow{display:flex;align-items:center;justify-content:center;color:var(--primary);font-size:28px;font-weight:700;padding:0 6px;flex:0 0 auto;min-height:140px}

.dual-grid{grid-column:1 / -1;display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:16px;padding:0;align-items:start}
.dual-bars-area{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.dual-bar{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px 22px;box-shadow:var(--shadow-sm)}
.dual-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.dual-head h4{margin:0;font-size:1.05em;color:var(--primary-hover);font-weight:700}
.dual-pct{font-size:1.6em;font-weight:800;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.dual-rows{display:flex;flex-direction:column;gap:10px}
.dual-row{display:grid;grid-template-columns:50px 1fr 60px;align-items:center;gap:10px}
.dual-lbl{font-size:.85em;color:var(--text-muted);font-weight:600}
.dual-track{height:22px;background:var(--surface-2);border-radius:6px;overflow:hidden;position:relative}
.dual-fill{height:100%;border-radius:6px;display:flex;align-items:center;padding-left:8px;color:var(--surface);font-size:.78em;font-weight:700;transition:width .8s ease}
.dual-fill.target{background:#c9a883}
.dual-val{font-size:.92em;color:var(--text);text-align:right;font-variant-numeric:tabular-nums;font-weight:700}

.dual-summary{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px 22px;box-shadow:var(--shadow-sm);position:sticky;top:14px}
.dual-summary .summary-title{margin:0 0 14px;font-size:1.1em;color:var(--primary-hover);font-weight:700;display:flex;align-items:center;gap:8px}
.dual-summary .summary-kpis{display:grid;grid-template-columns:1fr;gap:12px;margin-bottom:18px;padding-bottom:18px;border-bottom:1px dashed var(--border-muted)}
.dual-summary .summary-kpi{text-align:center;padding:8px;background:var(--surface-2);border-radius:var(--radius-sm)}
.dual-summary .summary-lbl{font-size:.78em;color:var(--text-muted);font-weight:600;margin-bottom:4px;letter-spacing:.04em}
.dual-summary .summary-val{font-size:2em;font-weight:800;line-height:1;font-variant-numeric:tabular-nums;letter-spacing:-.025em}
.dual-summary .summary-unit{font-size:.4em;font-weight:700;margin-left:3px;opacity:.7}
.dual-summary .summary-sub{font-size:.78em;color:var(--text-muted);margin-top:4px;line-height:1.4}
.dual-summary .summary-prog-head{font-size:.85em;color:var(--primary-hover);font-weight:700;margin-bottom:10px}
.dual-summary .summary-prog-row{display:grid;grid-template-columns:70px 1fr 50px;align-items:center;gap:8px;margin-bottom:8px;font-size:.82em}
.dual-summary .summary-prog-lbl{color:var(--text);font-weight:600}
.dual-summary .summary-prog-track{height:14px;background:var(--surface-2);border-radius:4px;overflow:hidden}
.dual-summary .summary-prog-fill{height:100%;border-radius:4px;transition:width .6s ease}
.dual-summary .summary-prog-val{color:var(--text);text-align:right;font-variant-numeric:tabular-nums;font-weight:700}

.rank-grid{grid-column:1 / -1;display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px;padding:0}
.rank-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px 22px;box-shadow:var(--shadow-sm)}
.rank-card.ok{border-top:4px solid var(--success)}
.rank-card.bad{border-top:4px solid var(--warning)}
.rank-card h4{margin:0 0 12px;font-size:1em;color:var(--primary-hover);display:flex;justify-content:space-between;align-items:center;font-weight:700}
.rank-card h4 .pill-s{font-size:.78em;background:var(--primary-light);color:var(--primary-hover);padding:3px 8px;border-radius:999px;font-weight:700}
.rank-list{display:flex;flex-direction:column;gap:6px}
.rank-list .r-row{display:grid;grid-template-columns:24px 1fr auto;font-size:.88em;color:var(--text);align-items:center;gap:8px}
.rank-list .r-row .pos{width:22px;height:22px;border-radius:6px;background:var(--primary);color:var(--surface);display:flex;align-items:center;justify-content:center;font-size:.78em;font-weight:800}
.rank-list .r-row .pos.bad{background:var(--warning)}
.rank-list .r-row .name{font-weight:600}
.rank-list .r-row .vl{color:var(--text-muted);font-variant-numeric:tabular-nums;font-weight:700}

.podium{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px;min-height:80px}
.pod-col{display:flex;flex-direction:column;align-items:center;min-width:0}
.pod-bar{width:100%;background:linear-gradient(0deg,var(--primary),#c9a883);border-radius:6px 6px 0 0;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:8px 4px;color:var(--surface);font-weight:700;min-height:60px}
.pod-bar.bad{background:linear-gradient(0deg,var(--warning),#c08a7e)}
.pod-bar .pct{font-size:18px;font-variant-numeric:tabular-nums}
.pod-bar .lbl{font-size:10px;letter-spacing:.04em;margin-top:2px}
.pod-name{margin-top:6px;font-size:13px;color:var(--text);font-weight:700;text-align:center}
.pod-name small{display:block;font-size:10px;color:var(--text-muted);font-weight:500;margin-top:2px}
.rank-tbl{width:100%;border-collapse:collapse;font-size:12px;margin-top:8px}
.rank-tbl th{text-align:left;color:var(--text-muted);font-weight:600;padding:4px 6px;border-bottom:1px solid var(--border)}
.rank-tbl td{padding:5px 6px;border-bottom:1px solid var(--surface-2);color:var(--text)}
.rank-tbl td.num{text-align:right;font-variant-numeric:tabular-nums;font-weight:700;color:var(--primary)}
.rank-tbl td.num.bad{color:var(--warning)}

.exit-grid{grid-column:1 / -1;display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-bottom:16px;padding:0}
.exit-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px 22px;box-shadow:var(--shadow-sm)}
.exit-card h4{margin:0 0 12px;font-size:1em;color:var(--primary-hover);display:flex;justify-content:space-between;font-weight:700}
.exit-card h4 .pill-s{font-size:.78em;background:var(--primary-light);color:var(--primary-hover);padding:3px 8px;border-radius:999px;font-weight:700}
.exit-rows{display:flex;flex-direction:column;gap:8px}
.exit-rows .er{display:grid;grid-template-columns:90px 1fr 50px;font-size:.88em;align-items:center;gap:8px}
.exit-rows .er .nm{color:var(--text);font-weight:600}
.exit-rows .er .trk{height:18px;background:var(--surface-2);border-radius:4px;overflow:hidden}
.exit-rows .er .fl{height:100%;background:var(--primary);display:flex;align-items:center;padding-left:6px;color:var(--surface);font-size:.78em;font-weight:700}
.exit-rows .er .vl{color:var(--text);text-align:right;font-variant-numeric:tabular-nums;font-weight:700}

.case-grid{grid-column:1 / -1;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:16px;padding:0}
.case-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;border-left:5px solid #c9a883;box-shadow:var(--shadow-sm)}
.case-card.win{border-left-color:var(--success)}
.case-card.lose{border-left-color:var(--warning)}
.case-card .tag{font-size:.78em;color:var(--primary);letter-spacing:.06em;font-weight:700;margin-bottom:6px}
.case-card.win .tag{color:var(--success)}
.case-card.lose .tag{color:var(--warning)}
.case-card .ttl{font-size:1em;color:var(--text);font-weight:700;margin-bottom:4px}
.case-card .meta{font-size:.85em;color:var(--text-muted);line-height:1.5}

/* ============ v1.5.13: M-4 v2 分类树 ============ */
.tree-wrap{grid-column:1 / -1;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px 28px;margin-bottom:16px;overflow-x:auto;box-shadow:var(--shadow-sm)}
.tree{display:flex;flex-direction:column;align-items:center;gap:0}
.tn{display:inline-flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;border-radius:12px;padding:14px 18px;position:relative;min-width:140px}
.tn .t-label{font-size:11px;letter-spacing:.06em;color:var(--text-muted);margin-bottom:4px;font-weight:600}
.tn .t-num{font-size:28px;font-weight:800;line-height:1;color:var(--text);font-variant-numeric:tabular-nums}
.tn .t-num small{font-size:13px;color:var(--text-muted);font-weight:500;margin-left:3px}
.tn .t-sub{font-size:11px;color:var(--text-muted);margin-top:4px;line-height:1.4}
.tn.root{background:var(--primary-hover);color:var(--surface);border:3px solid var(--primary-hover);padding:20px 32px;min-width:240px;box-shadow:var(--shadow-md)}
.tn.root .t-label{color:var(--primary-light)}
.tn.root .t-num{color:var(--surface)}
.tn.root .t-num small{color:var(--primary-light)}
.tn.root .t-sub{color:var(--primary-light)}
.tn.branch{background:var(--primary);color:var(--surface);border:2px solid var(--primary)}
.tn.branch .t-label,.tn.branch .t-num,.tn.branch .t-num small,.tn.branch .t-sub{color:var(--surface)}
.tn.branch.alert{background:var(--warning);border-color:var(--warning)}
.tn.branch.core{background:var(--primary-hover);border-color:var(--primary-hover);border-width:3px;padding:18px 24px;min-width:180px;box-shadow:var(--shadow-md)}
.tn.leaf{background:var(--surface);color:var(--text);border:1.5px solid var(--primary)}
.tn.leaf.ok{border-color:var(--success)}
.tn.leaf.warn{border-color:var(--warning)}
.tn .fill-bar{margin-top:8px;width:100%;height:6px;background:var(--surface-2);border-radius:3px;overflow:hidden}
.tn .fill-bar i{display:block;height:100%;background:var(--success)}
.tn.warn .fill-bar i{background:var(--warning)}
.vline{width:2px;height:22px;background:var(--primary);margin:0 auto}
.tree-row{display:flex;gap:14px;align-items:flex-start;justify-content:center;width:100%;flex-wrap:wrap;margin-bottom:14px}
.tree-row.level2-row{margin-top:6px}
.branch-l1{display:flex;flex-direction:column;align-items:center}
.branch-l2{display:flex;gap:10px;justify-content:center;align-items:flex-start;margin-top:6px;flex-wrap:wrap}
.title-row{display:flex;justify-content:center;margin:8px 0;font-size:11px;color:var(--text-muted);letter-spacing:.06em;text-transform:uppercase;font-weight:700}
.legend{display:flex;justify-content:center;gap:18px;margin-top:18px;padding-top:14px;border-top:1px dashed var(--border);font-size:11px;color:var(--text-muted);flex-wrap:wrap}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;vertical-align:middle;margin-right:5px}

/* ============ v1.5.14: M-5 v1 财务大卡 ============ */
.fc-grid{grid-column:1 / -1;display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:16px;padding:0}
.fc{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px 18px 14px;position:relative;overflow:hidden;box-shadow:var(--shadow-sm)}
.fc::after{content:"";position:absolute;bottom:0;left:0;right:0;height:3px;background:var(--primary)}
.fc.b::after{background:var(--primary-hover)}
.fc.c::after{background:var(--warning)}
.fc.d::after{background:var(--success)}
.fc.e::after{background:#c9a883}
.fc-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.fc-ico{width:36px;height:36px;border-radius:8px;background:var(--surface-2);color:var(--primary-hover);display:flex;align-items:center;justify-content:center;font-size:18px}
.fc-lbl{font-size:.92em;color:var(--text-muted);letter-spacing:.04em;font-weight:600}
.fc-num{font-size:2.4em;font-weight:800;line-height:1;color:var(--text);font-variant-numeric:tabular-nums;margin-bottom:6px;letter-spacing:-.025em}
.fc-num small{font-size:.45em;color:var(--text-muted);font-weight:700;margin-left:3px}
.fc-sub{font-size:.85em;color:var(--text-muted);margin-bottom:10px;line-height:1.5}
.fc-spark{width:100%;height:36px;display:block;margin-top:6px}
.fc-legend{display:flex;justify-content:space-between;font-size:.75em;color:var(--text-muted);margin-top:6px;padding-top:6px;border-top:1px solid var(--border-muted)}

/* ============ v1.5.17: M-6 v_train 风格 (v1 顶部 + v8 主体) ============ */
.card-wall-m6{grid-column:1 / -1;display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:16px;padding:0}
.kpi-card-m6{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px 16px;position:relative;box-shadow:var(--shadow-sm);transition:transform .15s ease}
.kpi-card-m6:hover{transform:translateY(-2px);box-shadow:var(--shadow-md)}
.kpi-card-m6 .hd{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.kpi-card-m6 .hd .left{display:flex;align-items:center;gap:8px}
.kpi-card-m6 .ic{width:32px;height:32px;background:var(--surface-2);color:var(--primary-hover);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px}
.kpi-card-m6 .ttl{font-size:.9em;color:var(--primary-hover);font-weight:700;letter-spacing:.03em}
.kpi-card-m6 .delta{position:absolute;top:18px;right:14px;display:inline-flex;align-items:center;gap:3px;padding:3px 8px;border-radius:12px;font-size:.78em;font-weight:600}
.kpi-card-m6 .delta.up{background:rgba(74,124,89,.13);color:var(--success)}
.kpi-card-m6 .delta.flat{background:rgba(123,102,83,.13);color:var(--text-muted)}
.kpi-card-m6 .delta.warn{background:rgba(160,64,48,.13);color:var(--warning)}
.kpi-card-m6 .num-row{display:flex;align-items:baseline;gap:6px;margin:6px 0 8px}
.kpi-card-m6 .num{font-size:2.2em;font-weight:800;color:var(--text);line-height:1;font-variant-numeric:tabular-nums;letter-spacing:-.025em}
.kpi-card-m6 .unit{font-size:.5em;color:var(--text-muted);font-weight:700;margin-left:2px}
.kpi-card-m6 .ft{display:flex;align-items:center;justify-content:space-between;margin-top:6px;padding-top:6px;border-top:1px dashed var(--border-muted);font-size:.78em;color:var(--text-muted)}
.kpi-card-m6 .ft .tag{font-weight:600}
.kpi-card-m6 .ft .tag-good{color:var(--success)}
.kpi-card-m6 .ft .tag-warn{color:var(--warning)}
.kpi-card-m6 .ft .tag-flat{color:var(--text-muted)}

.heatmap-block{grid-column:1 / -1;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px 24px;margin-bottom:16px;box-shadow:var(--shadow-sm)}
.heatmap-block .block-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;padding-bottom:10px;border-bottom:1px dashed var(--border-muted)}
.heatmap-block .block-head h3{font-size:1.05em;font-weight:700;color:var(--primary-hover);letter-spacing:.04em;display:flex;align-items:center;gap:8px;margin:0}
.heatmap-block .block-head h3 .pill{font-size:.7em;padding:2px 8px;border-radius:8px;background:var(--surface-2);color:var(--primary-hover);font-weight:600}
.heatmap-block .block-head .hint{font-size:.78em;color:var(--text-muted)}
.heat-grid{display:grid;grid-template-columns:60px repeat(12,1fr) 8px;gap:6px;align-items:center}
.heat-grid .yl{font-size:.78em;color:var(--text-muted);text-align:right;padding-right:8px;letter-spacing:.04em}
.heat-grid .month{height:64px;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;font-variant-numeric:tabular-nums;border:1px solid rgba(107,68,35,.08)}
.heat-grid .month .m{font-size:.78em;font-weight:700;letter-spacing:.05em;opacity:.85}
.heat-grid .month .v{font-size:1em;font-weight:800;line-height:1}
.heat-grid .month.heat1{background:#e2c79f;color:var(--primary-hover)}
.heat-grid .month.heat1 .v,.heat-grid .month.heat1 .m{color:var(--primary-hover)}
.heat-grid .month.heat3{background:#9f6b44;color:#fefcf7}
.heat-grid .month.heat3 .v,.heat-grid .month.heat3 .m{color:#fefcf7}
.heat-grid .month.heat4{background:#6b4423;color:#fefcf7}
.heat-grid .month.heat4 .v,.heat-grid .month.heat4 .m{color:#fefcf7}
.heat-grid .month.unknown{background:repeating-linear-gradient(135deg,var(--surface-2) 0,var(--surface-2) 5px,rgba(123,102,83,.06) 5px,rgba(123,102,83,.06) 10px)}
.heat-grid .month.unknown .v{color:var(--text-muted);font-size:.85em;font-weight:600}
.heat-grid .month.unknown .m{color:var(--text-muted)}

.dept-pair{grid-column:1 / -1;display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px;padding:0}
.dept-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 20px;box-shadow:var(--shadow-sm)}
.dept-card h4{font-size:1em;font-weight:700;color:var(--primary-hover);margin:0 0 10px;display:flex;align-items:center;gap:8px;letter-spacing:.04em}
.dept-card h4 .pill{font-size:.78em;font-weight:700;padding:2px 8px;border-radius:10px;background:var(--surface-2);color:var(--primary-hover)}
.dept-card.good h4 .pill{background:rgba(74,124,89,.14);color:var(--success)}
.dept-card.warn h4 .pill{background:rgba(160,64,48,.14);color:var(--warning)}
.dept-tags{display:flex;flex-wrap:wrap;gap:6px}
.dept-tags span{font-size:.78em;padding:2px 8px;border-radius:4px;background:var(--surface-2);color:var(--primary-hover);border:1px solid var(--border);letter-spacing:.02em}
.dept-card.warn .dept-tags span{background:rgba(160,64,48,.08);border-color:rgba(160,64,48,.25);color:var(--warning)}
.dept-card.good .dept-tags span{background:rgba(74,124,89,.10);border-color:rgba(74,124,89,.25);color:var(--success)}

.rail-block{grid-column:1 / -1;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px 24px;margin-bottom:16px;box-shadow:var(--shadow-sm)}
.rail-block .block-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;padding-bottom:10px;border-bottom:1px dashed var(--border-muted)}
.rail-block .block-head h3{font-size:1.05em;font-weight:700;color:var(--primary-hover);letter-spacing:.04em;display:flex;align-items:center;gap:8px;margin:0}
.rail-block .block-head h3 .pill{font-size:.7em;padding:2px 8px;border-radius:8px;background:var(--surface-2);color:var(--primary-hover);font-weight:600}
.rail-block .block-head .hint{font-size:.78em;color:var(--text-muted)}
.rail-svg{width:100%;height:240px;display:block}
.trend-up{color:var(--success);font-weight:600}
.trend-down{color:var(--danger);font-weight:600}
.trend-flat{color:var(--text-dim)}

/* ============ Main grid ============ */
.dashboard{max-width:1400px;margin:14px auto;padding:0 32px 40px}
.module{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:14px;box-shadow:var(--shadow-sm);overflow:hidden}
.module[data-featured="true"]{border:2px solid var(--primary);box-shadow:var(--shadow-md);background:var(--surface)}
.module-head{padding:16px 26px;border-bottom:1px solid var(--border-muted);display:flex;align-items:center;gap:14px;background:var(--surface)}
.module-head-hidden{display:none}
.module-head-featured{padding:0;border-bottom:0;background:transparent;gap:18px;display:none}
.module-head-featured .module-icon{width:56px;height:56px;font-size:28px;background:var(--primary);color:#fff;box-shadow:var(--shadow-md)}
.module-head-featured .module-title,.module-head-featured .module-sub{display:none}
.module-icon{width:48px;height:48px;background:var(--primary-light);color:var(--primary-hover);border-radius:var(--radius-sm);display:inline-flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0}
.module-title{font-size:2em;font-weight:800;color:var(--text);letter-spacing:-.025em;line-height:1.2}
.module[data-featured="true"] .module-title{font-size:2.6em;color:var(--primary-hover)}
.module-sub{font-size:1em;color:var(--text-muted);margin-left:12px}
.module-narrative{padding:14px 26px 16px;margin:0;color:var(--text);font-size:1.05em;line-height:1.75;background:linear-gradient(180deg,var(--primary-light) 0%,var(--surface) 100%);border-bottom:1px solid var(--border-muted)}
.module-narrative-head{padding:20px 26px 14px;display:flex;align-items:center;gap:14px;background:transparent}
.module-narrative-head .narrative-h2{font-size:2em;font-weight:800;color:var(--primary-hover);margin:0;display:flex;align-items:center;gap:12px;letter-spacing:-.025em}
.module-narrative-head .narrative-icon{display:inline-flex;align-items:center;justify-content:center;width:56px;height:56px;background:var(--primary);color:#fff;border-radius:14px;font-size:28px;flex-shrink:0;box-shadow:var(--shadow-sm)}
.module-narrative-head .narrative-badge{display:inline-flex;align-items:center;justify-content:center;min-width:40px;height:34px;border-radius:999px;background:var(--primary-light);color:var(--primary-hover);font-size:1.1em;font-weight:800}
.module-narrative-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px 30px;margin:0 26px 20px;font-size:1.05em;line-height:1.8;color:var(--text);border-left:6px solid var(--primary);box-shadow:var(--shadow-sm)}
.module-narrative-card p{margin:0 0 12px}
.module-narrative-card p:last-child{margin-bottom:0}
.module-narrative-card strong{color:var(--primary-hover);font-weight:700}
.module-body{padding:16px 26px;display:grid;grid-template-columns:repeat(12,1fr);gap:14px}
.section{grid-column:span 6;min-width:0}
.section.span-12{grid-column:span 12}
.section.span-4{grid-column:span 4}
.section.span-8{grid-column:span 8}
.section-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;padding-bottom:6px;border-bottom:1px dashed var(--border-muted)}
.section-title{font-size:1.2em;font-weight:700;color:var(--text);display:flex;align-items:center;gap:8px;letter-spacing:-.01em}
.section-title-dot{width:8px;height:8px;border-radius:50%;background:var(--primary);flex-shrink:0}
.section-meta{font-size:.88em;color:var(--text-dim);font-weight:600}

/* ============ Viz: Stat card ============ */
.stat-card{background:var(--surface-2);border:1px solid var(--border-muted);border-radius:var(--radius-sm);padding:12px 14px}
.stat-card-label{font-size:.78em;color:var(--text-muted);font-weight:500;margin-bottom:2px}
.stat-card-value{font-size:1.4em;font-weight:700;color:var(--text);letter-spacing:-.02em}
.stat-card-value.tone-blue{color:var(--primary)}.stat-card-value.tone-green{color:var(--success)}.stat-card-value.tone-orange{color:var(--orange)}.stat-card-value.tone-red{color:var(--danger)}
.stat-card-sub{font-size:.78em;color:var(--text-dim);margin-top:2px}

/* ============ Viz: Plain text list (v1.4.1: 去掉色条) ============ */
.bar-list{display:flex;flex-direction:column;gap:4px}
.bar-row{display:flex;justify-content:space-between;align-items:baseline;gap:16px;font-size:.88em;padding:6px 0;border-bottom:1px solid var(--border-muted)}
.bar-row:last-of-type{border-bottom:0}
.bar-row-label{color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;min-width:0}
.bar-row-value{color:var(--text);font-weight:600;text-align:right;font-size:.95em;white-space:nowrap;font-feature-settings:"tnum"}
.bar-row-sub{color:var(--text-dim);font-size:.78em;margin-top:-4px;padding-left:0}

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
  /* v1.5.21.3b: 17 个内部 grid 自适应（保留多列 + 超容器宽时横向滚动） */
  .kpi-hero{grid-template-columns:repeat(6,minmax(180px,1fr));overflow-x:auto}
  .kpi-cards-row{grid-template-columns:repeat(6,minmax(160px,1fr));overflow-x:auto}
  .kpi-row.v11{grid-template-columns:repeat(4,minmax(200px,1fr));overflow-x:auto}
  .dim-grid{grid-template-columns:repeat(5,minmax(160px,1fr));overflow-x:auto}
  .cs-grid{grid-template-columns:repeat(4,minmax(200px,1fr));overflow-x:auto}
  .gauge-grid{grid-template-columns:repeat(3,minmax(220px,1fr));overflow-x:auto}
  .dual-grid{grid-template-columns:repeat(2,minmax(300px,1fr));overflow-x:auto}
  .dual-bars-area{grid-template-columns:repeat(2,minmax(280px,1fr));overflow-x:auto}
  .rank-grid{grid-template-columns:repeat(2,minmax(280px,1fr));overflow-x:auto}
  .exit-grid{grid-template-columns:repeat(2,minmax(280px,1fr));overflow-x:auto}
  .case-grid{grid-template-columns:repeat(4,minmax(220px,1fr));overflow-x:auto}
  .podium{grid-template-columns:repeat(3,minmax(150px,1fr));overflow-x:auto}
  .fc-grid{grid-template-columns:repeat(5,minmax(200px,1fr));overflow-x:auto}
  .card-wall-m6{grid-template-columns:repeat(6,minmax(160px,1fr));overflow-x:auto}
  .tl-grid{grid-template-columns:repeat(5,minmax(150px,1fr));overflow-x:auto}
  .dept-pair{grid-template-columns:repeat(2,minmax(280px,1fr));overflow-x:auto}
  .narrative-grid{grid-template-columns:repeat(2,minmax(280px,1fr));overflow-x:auto}
  .heat-grid{grid-template-columns:60px repeat(12,minmax(45px,1fr)) 8px;overflow-x:auto}
  /* viz 硬编码宽度兜底（覆盖 viz/*.py 内联 min-width:120） */
  .bar-label,.funnel-row{min-width:0;max-width:100%}
  .donut-svg{width:80px;height:80px;flex-shrink:0}
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
  .module-body{padding:12px 10px}
  .module-narrative-card{padding:14px 12px}
  .tn,.tn.root,.tn.branch.core{min-width:100%;width:100%}
  /* viz 硬编码宽度 override（覆盖 viz/*.py 内联 min-width:120px） */
  .bar-label,.funnel-row{min-width:0;max-width:100%}
  .donut-svg{width:80px;height:80px;flex-shrink:0}
}

/* ============ v1.4: KPI card (模块内 KPI) + 3px 彩条 + delta + note ============ */
.kpi-strip-inner{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:var(--space-2);padding:var(--space-2) 0}
.kpi-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:var(--space-2) var(--space-3);position:relative;overflow:hidden;border-top:3px solid var(--primary)}
.kpi-card[data-category="success"]{border-top-color:var(--success)}
.kpi-card[data-category="warning"]{border-top-color:var(--warning)}
.kpi-card[data-category="danger"]{border-top-color:var(--danger)}
.kpi-card-label{font-size:.78em;color:var(--text-muted);font-weight:500;text-transform:uppercase;letter-spacing:.4px}
.kpi-card-value{font-size:1.5em;font-weight:700;color:var(--text);line-height:1.1;margin-top:4px;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.kpi-card-sub{font-size:.78em;color:var(--text-muted);margin-top:4px;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.kpi-card-delta{font-weight:600;padding:1px 6px;border-radius:var(--radius-pill);background:var(--surface-2)}
.kpi-card-delta.trend-up{color:var(--success)}
.kpi-card-delta.trend-down{color:var(--danger)}
.kpi-card-delta.trend-flat{color:var(--text-dim)}
.kpi-note{font-size:12px;color:var(--text-muted);margin-top:var(--space-1);line-height:1.45;border-top:1px dashed var(--border-muted);padding-top:var(--space-1)}

/* ============ v1.4: Narrative 2 栏 ============ */
.narrative-grid{display:grid;grid-template-columns:1.4fr 1fr;gap:var(--space-3);margin:0 var(--space-3) var(--space-3);padding:var(--space-3);background:linear-gradient(180deg,var(--primary-light) 0%,#f0f9ff 100%);border:1px solid var(--border);border-radius:var(--radius-sm)}
.narrative-col h3.narrative-h{font-size:.85em;color:var(--primary-hover);margin-bottom:var(--space-1);font-weight:600}
.narrative-col p{font-size:.85em;color:var(--text);line-height:1.55;margin:0;overflow-wrap:break-word;word-break:break-word;max-width:100%}
.narrative-muted{color:var(--text-muted)!important}

/* ============ v1.4: Module 章节编号 01/02/03 (CSS counter) ============ */
.module{counter-increment:module}
.module h2.module-title::before{content:counter(module,decimal-leading-zero) " · ";color:var(--primary);font-feature-settings:"tnum"}

/* ============ v1.4: Heatmap ============ */
.heatmap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.heatmap-table{border-collapse:separate;border-spacing:4px;width:100%}
.heatmap-table th,.heatmap-table td{padding:10px 14px;text-align:center;font-size:.85em;border-radius:var(--radius-xs);font-variant-numeric:tabular-nums}
.heatmap-col-label,.heatmap-row-label{background:var(--surface-2);color:var(--text-muted);font-weight:600;font-size:.78em}
.heatmap-row-label{text-align:left;white-space:nowrap}
.heatmap-cell{background:var(--surface-2);color:var(--text);font-weight:600;border:1px solid var(--border-muted)}
.heatmap-cell[data-level="success"]{background:rgba(22,163,74,.18);color:var(--success);border-color:rgba(22,163,74,.3)}
.heatmap-cell[data-level="warning"]{background:rgba(217,119,6,.18);color:var(--warning);border-color:rgba(217,119,6,.3)}
.heatmap-cell[data-level="danger"]{background:rgba(220,38,38,.18);color:var(--danger);border-color:rgba(220,38,38,.3)}
.heatmap-empty{padding:var(--space-3);text-align:center;color:var(--text-muted)}

/* ============ v1.4: 8 进制 spacing 应用于模块级 padding/margin ============ */
.module-body{padding:var(--space-3) var(--space-4)}
.module-head{padding:var(--space-2) var(--space-4)}
.hero{padding:var(--space-4) var(--space-5) var(--space-3)}
.kpi-strip{margin:var(--space-3) auto 0;padding:0 var(--space-5)}
.dashboard{margin:var(--space-3) auto;padding:0 var(--space-5) var(--space-6)}
.module{margin-bottom:var(--space-3)}
.kpi-strip-inner{padding:var(--space-2) 0;gap:var(--space-2)}
.kpi-card{padding:var(--space-2) var(--space-3);margin-bottom:var(--space-1)}
.kpi-note{margin-top:var(--space-1);padding-top:var(--space-1)}
.narrative-grid{margin:0 var(--space-3) var(--space-3);padding:var(--space-3);gap:var(--space-3)}
.section-head{margin-bottom:var(--space-1);padding-bottom:var(--space-1)}
.section-title{gap:var(--space-1)}
.donut-wrap{gap:var(--space-3)}
.bar-list{gap:var(--space-2)}
.bar-row{gap:var(--space-2)}
.prog-row-head{gap:var(--space-1)}
.heatmap-table th,.heatmap-table td{padding:var(--space-2) var(--space-3)}
.heatmap-table{border-spacing:var(--space-1)}
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
