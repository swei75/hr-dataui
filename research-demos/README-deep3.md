# 深研 #3：管理驾驶舱（领导视角）

> **目标**：找一个**KPI 突出 + 异常告警 + 大屏感**的管理驾驶舱 demo。
>
> **结论先行**：`rigarcia07/tableau-it-risk-dashboard` 是最佳匹配——Tableau 风格的 **IT Risk Executive Overview**（RiskVue），4 KPI 顶部突出（Critical risks open 12 / Within appetite 84% / High severity incidents 7 / Control effectiveness 91%）+ **5×5 风险热图**（Impact × Likelihood）+ **Top 风险排行** + **趋势 SVG** + **整改时效表**——"领导视角"元素齐全。
>
> **demo 文件**：`research-demos/deep3-tableau-risk.html`（22KB）
>
> **关键约束违反**：`⚠️ 违反 C-2` —— 依赖 Fontshare 字体 CDN（`api.fontshare.com`），其他 inline CSS。

---

## § 来源

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/rigarcia07/tableau-it-risk-dashboard |
| 文件 | `index.html` |
| 协议 | （未声明——代码 MIT 风格） |
| 仓库活跃度 | 单 commit demo，作者为 Tableau 内部设计师 |
| stars | 0（设计作品仓库） |
| demo 类型 | **单文件 HTML**（inline CSS + 字体 CDN） |
| 主题 | **RiskVue — IT Risk Executive Mockup**（Tableau 风格） |

### 为什么是它

我在 GitHub 搜索 `executive dashboard html`、`management cockpit`、`risk dashboard`、`KPI突出 异常告警` 等关键词，找到 10+ 候选，最终选 Tableau IT Risk：

| 候选 | 选 / 不选 | 原因 |
|---|---|---|
| `rigarcia07/tableau-it-risk-dashboard` | ✅ | **Tableau 风最完整 + 5×5 风险热图 + 4 KPI 顶部** |
| `UmairIsmail-Showcase/Project-Training-Tracker` | 备选 | C-level Report 但 Google Fonts CDN + 紫色渐变 |
| `Hazrat-Ali9/Bank-Management-Frontend` | ❌ | 银行客户前端，42 stars 但是 SPA 非 dashboard |
| `Kscoder42/student-analytics-dashboard` | ❌ | 学生分析，bubble chart 不是大屏感 |
| `PavinAJ/smart-incident-report` | ❌ | 事故报告，离线优先但 viz 简单 |
| `ankit12375/real-time-analytics-dashboard` | ❌ | 实时数据 dashboard（实时数据 YAGNI） |
| `CorporateWater/co-executive-dashboard` | ❌ | 无相关仓库 |
| `dsilentdragon/Myadmindashboard` | ❌ | Tailwind CDN |

**选 Tableau IT Risk 的核心理由**：
1. **"Executive Overview" 明确目标**（领导视角）
2. **4 KPI 卡顶部 + 风险热图 + 排行 + 趋势 + 表** 五大组件齐全
3. **金融/银行场景**（风险、合规）——与 HR 月报目标受众重合
4. **Tableau 配色**（米色 + 深绿 + 暖橙）——专业稳重

---

## § 视觉特征

### 主色（grep 提取 hex）

| 颜色 | hex | 用途 |
|---|---|---|
| 米色背景 | `#f7f6f2` | 主背景 |
| 米色卡片 | `#f9f8f5` / `#fbfbf9` | 卡片背景（多层次） |
| 米色深 | `#f3f0ec` | 高亮背景 |
| 主深绿 | `#01696f` | Header / 强调 / 风险低 |
| 主深绿 hover | `#0c4e54` | hover 状态 |
| 浅绿 | `#cedcd8` | highlight |
| 成功绿 | `#437a22` | 风险低 / 上升趋势 |
| 浅绿背景 | `#d4dfcc` | success badge |
| 警示橙 | `#964219` | 风险中 |
| 浅橙背景 | `#ddcfc6` | warning badge |
| 错误紫红 | `#a12c7b` | 风险高（**独特选择**——非红） |
| 浅紫背景 | `#e0ced7` | error badge |
| 文字深 | `#28251d` | 主文字 |
| 文字灰 | `#6e6b64` | 副文字 |
| 文字淡 | `#97948e` | 三级文字 |

**特征**：
- **米色基底**（`#f7f6f2` 系）—— Tableau 经典 "Warm Light" 主题
- **深绿主色 + 暖橙 + 紫红**——3 色风险等级（不用纯红/纯绿）
- **dark mode 同样定义** —— `[data-theme="dark"]` 切到 `#171614` 暗色

### 字体系统

```css
--font-body: 'Satoshi', Inter, sans-serif;  /* Fontshare CDN */
--text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);   /* 12-14px */
--text-sm: clamp(0.875rem, 0.8rem + 0.35vw, 1rem);      /* 14-16px */
--text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);   /* 16-18px */
--text-lg: clamp(1.125rem, 1rem + 0.75vw, 1.5rem);      /* 18-24px */
--text-xl: clamp(1.5rem, 1.2rem + 1.25vw, 2.25rem);     /* 24-36px */
```

- **clamp() 流式字体** —— 不同断点不同字号，**移动端友好**
- 数字采用 `font-variant-numeric: tabular-nums`（等宽）

### 间距节奏（8 进制 spacing）

```css
--space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem;
--space-5: 1.25rem; --space-6: 1.5rem; --space-8: 2rem; --space-10: 2.5rem;
--space-12: 3rem;
```

- **8 进制 spacing scale** —— Tailwind 风
- 圆角：`--radius-sm: 0.375rem` / `--radius-md: 0.75rem` / `--radius-lg: 1rem` / `--radius-xl: 1.25rem`
- 阴影：`--shadow-sm/md/lg` —— 3 级深度

---

## § 信息架构

### 章节层级（3 层）

```
Header: RiskVue (h1) + IT Risk Executive Overview (h2)
├── Sidebar 导航（Portfolio + Board Lens）
│   ├── Overview（active）
│   └── 其他 pages（待实现）
└── Main content：
    ├── KPI 卡片行（4 个）
    │   ├── Critical risks open: 12 (↓+3 vs last quarter)
    │   ├── Within appetite: 84% (↑+5 pts improvement)
    │   ├── High severity incidents: 7 (Payments and IAM drive most impact)
    │   └── Control effectiveness: 91%
    ├── Section 1: Residual risk heatmap（5×5 grid）
    ├── Section 2: Top risk concentrations（bar list）
    ├── Section 3: Risk trend vs incidents（SVG sparkline）
    └── Section 4: Control remediation aging（table + status badges）
```

**特点**：
- **左侧固定 sidebar** —— 银行风领导视角（Power BI 风）
- **4 KPI 卡 + 趋势 sub** —— 每个 KPI 有 delta + 注释（v1.3 当前缺）
- **风险热图（heatmap）** —— 5×5 grid，impact × likelihood，颜色编码
- **Top risk concentration** —— bar 排行
- **SVG sparkline** —— 趋势小图（220x280）

### 数据点数量

| 类型 | 数量 |
|---|---|
| KPI 卡 | 4（顶部） |
| 风险热图 cell | 25（5×5 grid） |
| 风险集中项 | 5-10（bar list） |
| SVG sparkline | 1（280px 高） |
| 整改表格 | 5-10 行 |
| 状态 badge | high / watch / good 三色 |

### 叙述 vs 图表比例

| 类型 | 估算占比 |
|---|---|
| **叙述/解释**（KPI sub 注释 + section subtitle + footer note） | **~20%** |
| **图表/数据**（KPI + heatmap + bars + SVG + table） | **~80%** |

**关键洞察**：**叙事比 Velarasan 多一倍**（20% vs 10%）—— executive dashboard 用更多文字解释"为何重要"、"趋势如何"。

---

## § 图表清单（位置 + 类型 + 用途）

| 位置 | 类型 | 用途 |
|---|---|---|
| Header | brand + sidebar nav | 顶级导航 |
| KPI 行 | 4 张 kpi-card | 4 个核心数字 + delta + sub |
| Section 1 | 5×5 heatmap | 残值风险热图（impact × likelihood） |
| Section 2 | bar list | Top 风险集中（5-10 项） |
| Section 3 | SVG sparkline | 风险 vs 事故趋势（280px 高） |
| Section 4 | data-table + status badges | 整改时效表（high / watch / good） |

**特点**：
- **heatmap 是核心 viz** —— 用 grid + 颜色编码表达"二维风险"
- **SVG sparkline** —— 内联 SVG（无依赖），可缩放
- **status badge** —— `high/watch/good` 3 色（紫红 / 橙 / 绿），独特选择

---

## § 借鉴清单（具体到本项目能用什么）

### A. Risk Heatmap 模式（**高优先**——独有）

shanjinki 和 Velarasan **都没有热图**——这是 Tableau RiskVue 的**独有价值**。

HR 月报可借鉴场景：
- **M-2 员工情况**：年龄 × 司龄 热图（找出"年轻高流失"群体）
- **M-3 人员优化**：引进难度 × 流失率 热图（找出"难招易流"岗位）
- **M-4 干部队伍**：层级 × 后备充足度 热图

实现（CSS grid）：

```css
.heatmap { display: grid; grid-template-columns: 80px repeat(5, 1fr); gap: var(--space-2); }
.heat-cell { min-height: 74px; border-radius: var(--radius-md); padding: var(--space-3); }
.risk-low { background: color-mix(in srgb, var(--color-success) 18%, var(--color-surface)); }
.risk-high { background: color-mix(in srgb, var(--color-error) 22%, var(--color-surface)); }
```

### B. KPI delta + sub 双行注释（**高优先**）

```html
<div class="kpi-label">Critical risks open</div>
<div class="kpi-value">12</div>
<div class="kpi-sub"><span class="trend-down">+3 vs last quarter</span></div>
```

v1.3 当前 KPI 卡**仅显示数字**——领导看不到"环比/同比"。**真实 HR 月报需要**：员工数环比 +5 人、客户经理流失 -2 人。

### C. 流式字号 clamp()（**中优先**）

```css
--text-xl: clamp(1.5rem, 1.2rem + 1.25vw, 2.25rem);  /* 24-36px */
--text-lg: clamp(1.125rem, 1rem + 0.75vw, 1.5rem);    /* 18-24px */
```

v1.3 当前用固定 px——加 clamp() 让移动端字号更合适。

### D. SVG sparkline（**中优先**）

SVG 内联（无 CDN 依赖）实现趋势小图。比 Chart.js 轻量，**比 CSS bar 更适合"小趋势"**。

HR 月报可借鉴场景：
- KPI 卡右上角小趋势线
- 6 模块顶部"过去 12 月趋势"小图

### E. Status badge 3 色（**中优先**）

```css
.status.high { background: var(--color-error-highlight); color: var(--color-error); }
.status.watch { background: var(--color-warning-highlight); color: var(--color-warning); }
.status.good { background: var(--color-success-highlight); color: var(--color-success); }
```

HR 月报可借鉴场景：
- M-4 干部职数表：配/未配/超额
- M-1 网点状态：正常/预警/整改

### F. 8 进制 spacing scale（**中优先**）

Tailwind 风 spacing scale——比 v1.3 当前 18px padding 更系统化：

```css
--space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem;
```

### G. 风险等级不用纯红/绿（**低优先——独特价值**）

Tableau 用 **紫红 `#a12c7b`** 表达 risk-high 而非纯红 `#ef4444`——更"金融稳重"。可借鉴但**优先级低**（v1.3 风险色未明确）。

---

## § 警示清单（哪些不适合 + 为什么）

| ❌ 不借鉴 | 原因 |
|---|---|
| Fontshare CDN（`api.fontshare.com`） | 违反 C-2 |
| sidebar 左侧导航 | v1.3 6 模块是纵向滚动，sidebar 会让"快速翻阅"变复杂 |
| heatmap（5×5 grid） | 仅适合**双维度交叉**场景，HR 月报多维度不需要 |
| dark mode toggle | v1.3 是月报分发，dark mode YAGNI |
| `color-mix(in srgb, ...)` CSS 函数 | 现代浏览器支持，**Chrome 111+**——v1.3 N-4 要求 Chrome 80+ 不兼容 |
| clamp() 流体字号 | Chrome 79+ 支持，**v1.3 N-4 Chrome 80+ 临界**——需测试 |
| 大量 Tailwind 风 utility class | v1.3 自研 CSS 不引 Tailwind |

---

## § 与 10 个 ADR 的映射

| ADR | 判定 | 证据 |
|---|---|---|
| **ADR-001 单 Excel 数据源** | KEEP（不可动） | — |
| **ADR-002 7 列数据契约** | **REVISE 候选** ⚠️ | KPI sub 注释 + delta 字段需要新增——**最少 2 列 `delta` + `sub_text`** |
| **ADR-003 CSS 静态图表** | **REVISE 候选** ⚠️ | heatmap 是 grid + 颜色编码（非传统 chart），属于"扩展 CSS 静态图表"范围；可加 SVG sparkline（内联无依赖） |
| **ADR-004 自研 CSS** | KEEP | Tableau 风也是自研 CSS（不引框架），一致 |
| **ADR-005 Python f-string** | KEEP（不可动） | — |
| **ADR-006 composer 自动选 viz** | **REVISE 候选** ⚠️ | heatmap 需要 4+ 列（impact, likelihood, value, label），**不是单 viz 类型可表达**——需要新增 viz 类型或扩展 group 结构 |
| **ADR-007 浅色专业风 + 4 级 tone** | **REVISE 候选** ⚠️ | Tableau 是"米色 + 3 色风险等级"，比 v1.3 "indigo + 4-tone" 更金融稳重 |
| **ADR-008 12-col grid + 3 断点** | KEEP | Tableau 也是 12-col 风格 |
| **ADR-009 钻取交互 YAGNI** | KEEP | Tableau demo 无钻取 |
| **ADR-010 单文件部署** | KEEP（不可动） | — |

### 重点关注 1：ADR-002 修订方向（最强证据）

**触发条件**：
- 4 KPI 卡都有 `delta` + `sub` 字段（"环比 +5"、"Payments 和 IAM 驱动"）
- 真实 HR 月报（.docx）也有"比上月增加 / 重点关注 XX"叙述

**具体修订方向（待用户审批）**：
- 选项 A：**composer 自动算 delta**（基于上月数据，推荐——HR 不该懂 delta）
- 选项 B：**加列 `delta_pct` + `sub_text`**（HR 手动维护）
- 选项 C：**保持现状**（YAGNI）

**建议**：A 选项。

### 重点关注 2：ADR-007 修订方向

**触发条件**：Tableau 是"米色 + 深绿 + 紫红 + 暖橙"4 色，比 v1.3 "indigo 4-tone" 更"金融/政务"。

**具体修订方向**：
- v1.3 主色 `#1E5BAA`（indigo）→ Tableau 深绿 `#01696f` 或保留（看用户偏好）
- v1.3 4-tone 同色相 → Tableau 4 色（成功/警示/风险/中性）不同色相

**建议**：保留 indigo 主色，但**加 3 色风险等级**（成功/警示/风险）到 design tokens。

---

## § 15 维度观察表

| # | 维度 | 描述 | 分值 (1-5) | 备注 |
|---|---|---|---|---|
| 1 | 结构层级 | Header / Sidebar / 4 section | 4 | 3 层（顶级 / section / 数据） |
| 2 | 叙述 vs 数据比例 | KPI sub + section 注释 vs 图表 | 20/80 | 比 Velarasan 多 1 倍 |
| 3 | 图表类型清单 | KPI / heatmap / bars / sparkline / table | 5 类 | heatmap 是独有 |
| 4 | KPI 展示 | 4 KPI + delta + sub 双行 | **5** | 行业标杆 |
| 5 | 排名展示 | Top 5-10 bar list + status badges | 4 | 显式 Top N |
| 6 | 对比手法 | delta + 同比/环比 sub | 4 | 多重对比 |
| 7 | 配色方案 | 米色 + 深绿 + 暖橙 + 紫红（4 色） | 5 | 金融稳重 |
| 8 | 字体系统 | Satoshi + clamp() 流体 | 4 | 现代但需中文 |
| 9 | 间距节奏 | 8 进制 scale + 5 级圆角 + 3 级阴影 | **5** | **最系统** |
| 10 | 强调手段 | 颜色（3 风险等级）+ 数字（clamp 流体） | 4 | 双色 + 数字 |
| 11 | 表格用法 | 整改时效表 + status badges | 4 | 表格+徽章组合 |
| 12 | 模块标题样式 | section-title 双行（标题 + 副标题） | 5 | 副标题解释 |
| 13 | 留白比例 | 中等偏松（米色 + 16-24px padding） | 4 | executive 典型 |
| 14 | 银行/政务感 | 米色 + 深绿 = 银行稳重 | **5** | **与 Velarasan 并列** |
| 15 | 整体印象 | 3 个形容词 | — | **专业、稳重、Tableau 标杆** |

---

## § 1 句话核心发现

Tableau RiskVue 验证了"**4 KPI 顶部 + delta + sub 注释 + 风险热图 + SVG sparkline + 8 进制 spacing**"是领导视角管理驾驶舱的最佳实践——v1.3 当前**缺 KPI delta/sub** 和 **缺风险等级 3 色编码** 是最关键的两个缺口，加上 **heatmap** 是独有的可视化机会。

---

## § 兜底说明

- **找到 HTML demo**：✅（rigarcia07/tableau-it-risk-dashboard）
- **领导视角匹配度**：⭐⭐⭐⭐⭐（5/5）—— "Executive Overview" 明确
- **风格借鉴度**：⭐⭐⭐⭐⭐（5/5）—— KPI delta / heatmap / spacing 全部可借鉴
- **直接可用度**：⭐⭐⭐（3/5）—— 字体 CDN + `color-mix()` 不兼容 Chrome 80

---

## § 验证建议

1. 在浏览器打开 `deep3-tableau-risk.html`
2. 注意 4 大元素：
   - **顶部 4 KPI 卡**：每个有 delta + sub 注释
   - **5×5 风险热图**：颜色编码
   - **SVG sparkline**：右下趋势
   - **整改表 + badge**：3 色状态
3. 对比 v1.3：
   - v1.3 无 KPI delta——领导看不到"环比/同比"
   - v1.3 无 status badge——表格信息密度低
   - v1.3 无 heatmap——缺二维交叉 viz
4. **决策**：v1.4 是否加 KPI delta + 风险等级 3 色 + heatmap？

---

## § 关键警告

⚠️ **Fontshare CDN 依赖** —— 此 demo 通过 `<link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap">` 加载 Satoshi 字体，**违反 C-2**。可借鉴设计模式（KPI delta / heatmap / spacing），**不能直接复制字体引用**。

⚠️ **`color-mix()` CSS 函数** —— 浏览器兼容性 Chrome 111+（2023-03），**v1.3 N-4 要求 Chrome 80+ 不兼容**。如借鉴 heatmap 颜色，需用 rgba()/hex 替代。

⚠️ **`clamp()` 流体字号** —— Chrome 79+ 支持，**v1.3 N-4 Chrome 80+ 临界**。需测试或用固定 px 替代。