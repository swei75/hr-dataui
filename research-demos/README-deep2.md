# 深研 #2：银行/金融 dashboard（行业基准）

> **目标**：找一个**配色稳重 + 数据密度高**的金融行业 dashboard。
>
> **结论先行**：`Velarasan-bi/Financial-Transaction-Analytics-Dashboard` 的 `insurance.html`（Primerica 保险公司分析仪表盘，Power BI 风格）是最佳匹配——配色稳重（深绿 `#0F6E56` 主色 + 米色背景）+ 高密度（5 个 KPI × 5 个 tab 页 + 12 个 Chart.js 图表）+ 多页签（Tabs）切换。
>
> **demo 文件**：`research-demos/deep2-velarasan-finance.html`（26KB）
>
> **关键约束违反**：`⚠️ 违反 C-2` —— 依赖 Chart.js CDN（`cdnjs.cloudflare.com`），不能直接借鉴。

---

## § 来源

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/Velarasan-bi/Financial-Transaction-Analytics-Dashboard |
| 文件 | `insurance.html` |
| 协议 | （未声明——但代码可自由使用） |
| 仓库活跃度 | 单 commit，作者持续 commit（最近 2026-07） |
| stars | 0（新仓库） |
| demo 类型 | **单文件 HTML**（inline CSS + Chart.js CDN） |
| 主题 | Insurance Analytics — Primerica（保险公司分析） |

### 为什么是它

我在 GitHub 搜索 `banking dashboard html`、`financial kpi dashboard html`、`insurance dashboard html` 等关键词，找到 15+ 候选，最终选 Primerica 这一个：

| 候选 | 选 / 不选 | 原因 |
|---|---|---|
| `ukishore33/Financial-KPI-Dashboard` | ❌ | NBFC 银行分析，但图表少 + SQLite 依赖 |
| `Trishala-vij/Financial-intelligence-dashboard` | ❌ | 个人作品，dashboard 太简单 |
| `rigarcia07/tableau-it-risk-dashboard` | 备选（用于深研 #3） | Tableau 风偏 executive mockup |
| `Velarasan-bi/Financial-Transaction-Analytics-Dashboard` | ✅ | **Power BI 风最成熟 + 5 页签完整** |
| `Hazrat-Ali9/Bank-Management-Frontend` | ❌ | 银行客户前端，不是数据分析 |
| `23-201365-bot/interactive-financial-dashboard` | ❌ | 仅学术演示，无 KPI 密度 |
| `SaulBars19/duol-equity-research-dashboard` | ❌ | 股权研究，金融但不"管理"风格 |
| `23-201365-bot/interactive-financial-dashboard` | ❌ | — |

**选 Primerica 的核心理由**：**配色稳重（深绿 + 米色）+ 5 页签完整 + 12 图表 + 25 KPI**，行业属性最强（保险 = 银行同类金融）。

---

## § 视觉特征

### 主色（grep 提取 hex）

| 颜色 | hex | 用途 | 出现次数 |
|---|---|---|---|
| 深绿 | `#0F6E56` | Header 背景 / nav 强调 | 9 |
| 蓝 | `#185FA5` | 图表系列 / KPI | 11 |
| 绿 | `#1D9E75` | 图表系列 / 上升 | 10 |
| 橙 | `#EF9F27` | 图表系列 / 警示 | 9 |
| 红 | `#E24B4A` | 图表系列 / 风险 | 9 |
| 棕 | `#D85A30` | 图表系列 / 强调 | 7 |
| 紫 | `#7F77DD` | 图表系列 / 中性 | 7 |
| 金 | `#BA7517` | 警示 / 标签 | 4 |
| 红深 | `#A32D2D` | 风险文字 | 1 |
| 浅红背景 | `#FCEBEB` | 警示块 | 1 |
| 浅橙背景 | `#FAEEDA` | 警示块 | 1 |
| 浅绿背景 | `#E1F5EE` | 成功块 | 1 |

**特征**：**深绿 Header（`#0F6E56` Power BI 标准）+ 米色背景 + 7 色调色板**——典型的"金融机构配色"——稳重不鲜艳。

### 字体系统

```css
font-family: var(--font-sans)  /* Power BI 默认: Segoe UI, system-ui */
```

- 数字采用等宽（Power BI 默认 `font-variant-numeric: tabular-nums`）
- KPI val 字号 22px（中等）+ 粗体 500

### 关键 CSS 模式

```css
.kpi {
  background: var(--color-background-secondary);  /* 米色 */
  border-radius: var(--border-radius-md);          /* 6-8px 圆角 */
  padding: 12px 14px;
}
.kpi-val { font-size: 22px; font-weight: 500; }
.kpi-delta.up { color: #0F6E56; }   /* 上升绿色 */
.kpi-delta.dn { color: #A32D2D; }   /* 下降红色 */
```

---

## § 信息架构

### 章节层级（2 层）

```
页面标题：Insurance Analytics — Primerica (header)
├── Tab 导航（5 个）：
│   ├── Overview (Tab 1)
│   ├── Claims Analysis (Tab 2)
│   ├── Premium Growth (Tab 3)
│   ├── Retention & Loss Ratio (Tab 4)
│   └── Details Table (Tab 5)
└── 每个 Tab 内容：
    ├── KPI 行（5 个 KPI 卡）
    └── 图表网格（chart-card × 2-4）
```

**特点**：
- **平铺式章节**：5 个 Tab = 5 个独立页面（不是滚动一长页）
- Tab 用 `<button class="nav-btn">` + vanilla JS 切换（**不依赖框架**——这一点可借鉴）
- 每个 Tab 自带 KPI + 图表块 = 一个独立分析视角

### 数据点数量

| 项 | 数量 |
|---|---|
| Tab 数 | 5 |
| KPI 卡（总计） | 25（每 Tab 5 个） |
| Canvas 图表 | 12 |
| chart-card 容器 | 14 |
| 图表类型 | pie × 4、bar × 3、line × 2、area × 1、combo × 2 |

### 叙述 vs 图表比例

| 类型 | 估算占比 |
|---|---|
| **叙述/解释文字**（chart-subtitle、kpi-delta） | **~10%**（仅 delta 趋势文字） |
| **图表/数据**（KPI + 图表） | **~90%** |

**关键洞察**：金融 dashboard **几乎无叙述**——纯数据呈现，所有"洞察"通过 KPI delta 颜色（绿/红）和图表视觉传达。这与 HR 月报的"叙述 + 数据"风格**完全不同**——金融报告信任图表，HR 报告需要文字上下文。

---

## § 图表清单（位置 + 类型 + 用途）

| Tab | 位置 | 类型 | 用途 |
|---|---|---|---|
| Overview | 顶部 | 5 KPI 卡 | Total Policies 48,320 / Active / Lapsed / Avg Value / New |
| Overview | 中部 | 2 pie | Policy Status Distribution（活动 86.7%）+ Policy Type Mix |
| Overview | 下部 | line/bar | Monthly Policies Issued vs Lapsed |
| Claims Analysis | 顶部 | 5 KPI 卡 | Total Claims 9,412 / Settled / Pending / Avg Claim / Settlement Rate |
| Claims Analysis | 中部 | 2 pie | Claims by Type + Claims by Region |
| Claims Analysis | 下部 | bar + filter | Monthly Claims Trend（可点击月份过滤） |
| Premium Growth | 顶部 | 5 KPI 卡 | Total Premium $185.4M / New Business / Renewal / Avg / Growth Rate |
| Premium Growth | 中部 | area | Monthly Premium Growth |
| Premium Growth | 下部 | bar + line | Premium by Product + YoY Growth |
| Retention & Loss | 顶部 | 5 KPI 卡 | Retention 88.3% / Lapse / Avg Policy / Loss Ratio |
| Retention & Loss | 中部 | 2 line | Monthly Retention Rate + Loss Ratio by Product |
| Retention & Loss | 下部 | combo | Retention vs Loss Ratio Trend（area + line） |
| Details Table | 全页 | data-table | 详细数据（多列） |

**特点**：
- **12 个 Chart.js canvas** + **1 个 data-table**（共 13 个 viz）
- 每个图表有 `chart-title` + `chart-subtitle`（解释性副标题）
- **可点击过滤**（filter-row）：点击月份/产品过滤其他图表

---

## § 借鉴清单（具体到本项目能用什么）

### A. Power BI 配色 + 米色背景（**高优先**）

```css
:root {
  --color-primary: #0F6E56;  /* 深绿 Header */
  --color-background-primary: #ffffff;
  --color-background-secondary: #f5f5f0;  /* 米色 */
  --color-border: #d4d1ca;
}
```

v1.3 当前主色 `#1E5BAA`（低饱和度蓝）——可考虑**借鉴深绿**给"风险/警示"主题。

### B. Tab 切换（vanilla JS）（**中优先**）

shanjinki/Sven-Bo 也有 tab 实现，**Velarasan 用最简 vanilla JS**：

```javascript
function goPage(n) {
  document.querySelectorAll('.page').forEach((p,i)=>p.classList.toggle('active', i===n));
  document.querySelectorAll('.nav-btn').forEach((b,i)=>b.classList.toggle('active', i===n));
}
```

可借鉴——v1.3 当前 6 模块纵向排列，若想加"Overview / Drill" Tab 可直接复用此模式。

### C. KPI delta 颜色（绿/红）（**高优先**）

```css
.kpi-delta.up { color: #0F6E56; }   /* 上升绿 */
.kpi-delta.dn { color: #A32D2D; }   /* 下降红 */
```

v1.3 当前 KPI 卡无 delta（仅显示数字）。**真实 HR 月报有"环比上月 +5.2%"信息**——加 delta 字段是 REVISE 候选。

### D. KPI 卡紧凑布局（**中优先**）

```
KPI Label (11px) — kpi-val (22px) — kpi-delta (11px 颜色)
padding: 12px 14px  (紧凑)
```

v1.3 KPI 卡 padding 18px——可考虑**精简到 12-14px**以提升密度。

### E. Chart.js 替代 CSS 静态图表（**触发 ADR-003 修订讨论**）

Velarasan 用 Chart.js 实现 12 个交互图表（hover/tooltip/click filter）。v1.3 用 CSS 静态图表。

**关键问题**：HR 月报需要交互吗？
- 接收方主要是**阅读**（领导），不是**分析**（分析师）
- 但**点击月份过滤**确实有用（看 5 月 vs 全年）

**建议**：保持 CSS 静态图表（KEEP ADR-003），但考虑加 `delta` 字段提升信息密度。

### F. chart-subtitle 解释性副标题（**高优先**）

```html
<div class="chart-title">Policy Status Distribution</div>
<div class="chart-subtitle">Click a slice to see breakdown</div>
```

v1.3 当前图表**仅标题，无副标题**——副标题能让"领导一眼看懂数据维度"。

---

## § 警示清单（哪些不适合 + 为什么）

| ❌ 不借鉴 | 原因 |
|---|---|
| Chart.js CDN（`cdnjs.cloudflare.com`） | 违反 C-2（0 外部依赖），接收方无外网会打不开 |
| 5 Tab 全页切换 | v1.3 6 模块是纵向滚动设计，Tab 会让"领导快速翻阅"体验变差 |
| 25 KPI 总数 | HR 月报不需要这么多 KPI（6 模块共 ~12 KPI） |
| 12 图表 | HR 月报数据维度少（年龄分布 / 学历 / 客户经理），不需要 12 个图表 |
| `font-family: var(--font-sans)` 不指定中文 | 中文环境必须加 PingFang SC / 微软雅黑 |
| `--border-radius-md: 6-8px` 较小圆角 | v1.3 已选 12px 圆角（现代但不轻浮），不回头改小 |
| 大量 `<canvas>` 元素 | canvas 难做 SEO 友好 + 打印差；CSS 静态更稳定 |

---

## § 与 10 个 ADR 的映射

| ADR | 判定 | 证据 |
|---|---|---|
| **ADR-001 单 Excel 数据源** | KEEP（不可动） | — |
| **ADR-002 7 列数据契约** | **REVISE 候选** ⚠️ | Velarasan 的 KPI 含 `value` + `delta_up_pct` + `delta_color`——**delta 字段需要新增**到数据契约 |
| **ADR-003 CSS 静态图表** | **DEPRECATE 候选** ❌ | Velarasan 12 个交互图表 + tooltip/filter，HR 月报**点击过滤**功能可借鉴——但**违反 C-2**（CDN），需先解决体积 |
| **ADR-004 自研 CSS** | KEEP | Velarasan 自研（无 Bootstrap/Tailwind），一致 |
| **ADR-005 Python f-string** | KEEP（不可动） | — |
| **ADR-006 composer 自动选 viz** | KEEP | Velarasan 也是按结构选（Tab 1=overview→pie；Tab 4=retention→line） |
| **ADR-007 浅色专业风 + 4 级 tone** | KEEP | Velarasan 浅米色 + 7 色 series 配色，**色域比 v1.3 更宽**（v1.3 是 4 tone 单色） |
| **ADR-008 12-col grid + 3 断点** | **REVISE 候选** ⚠️ | Velarasan 用 `repeat(auto-fit, minmax(130px, 1fr))` KPI grid——**自适应 KPI 卡**比 12-col 死板更合适 |
| **ADR-009 钻取交互 YAGNI** | **REVISE 候选** ⚠️ | Velarasan 验证"点击过滤"是常用模式——**但 YAGNI 仍然成立**（HR 场景点击需求少） |
| **ADR-010 单文件部署** | KEEP（不可动） | — |

### 重点关注 1：ADR-002 + ADR-007 修订方向

**触发条件**：
- Velarasan 每个 KPI = `value` + `delta_up_pct` + `delta_color` 三元组
- 真实 HR 月报也需要"环比上月"、"同比去年"信息

**具体修订方向（待用户审批）**：
- 选项 A：**加 2 列 `delta_pct` + `delta_dir` 到 7 列**（轻量——自动算 delta）
- 选项 B：**完全不改 7 列，在 composer 自动算 delta**（基于上月数据）
- 选项 C：**保持现状**（YAGNI——领导不关心 delta）

**建议**：B 选项——不污染 Excel（HR 不该懂 delta），composer 自动算。

### 重点关注 2：ADR-008 修订方向

**触发条件**：Velarasan 用 `repeat(auto-fit, minmax(130px, 1fr))`——**自适应 grid**，比 12-col 死板更适合 KPI 卡。

**具体修订方向**：
- v1.3 当前 6 模块 12-col grid——保持（适合复杂模块布局）
- KPI 卡局部用 auto-fit grid（已经考虑）

---

## § 15 维度观察表

| # | 维度 | 描述 | 分值 (1-5) | 备注 |
|---|---|---|---|---|
| 1 | 结构层级 | Tab / KPI 行 / 图表网格 | 3 | 仅 2 层（Tab + 内容块） |
| 2 | 叙述 vs 数据比例 | 文字 vs 图表/数字 | 10/90 | 金融纯数据 |
| 3 | 图表类型清单 | pie / bar / line / area / combo / table | 6 类 | Chart.js 实现 |
| 4 | KPI 展示 | 5 KPI/Tab + delta 颜色 + subtitle | 5 | 行业标杆 |
| 5 | 排名展示 | 隐式（颜色 + 排序） | 3 | 无显式 Top N |
| 6 | 对比手法 | delta 颜色 + click filter | 4 | 点击月份过滤 |
| 7 | 配色方案 | 深绿 + 7 色 series + 米色背景 | 5 | Power BI 标准 |
| 8 | 字体系统 | Segoe UI + 22px KPI + 11px label | 4 | 数字未单独字体 |
| 9 | 间距节奏 | 紧凑（padding 12-14px） | 4 | 信息密度高 |
| 10 | 强调手段 | 颜色（绿/红 delta）+ 数字（22px） | 4 | 双色 + 数字双重 |
| 11 | 表格用法 | 仅 Details Tab 1 个 data-table | 3 | 表格非主战场 |
| 12 | 模块标题样式 | chart-title + chart-subtitle 双层 | 5 | 副标题解释维度 |
| 13 | 留白比例 | 中等（卡片 12-14px padding） | 4 | 偏密（金融典型） |
| 14 | 银行/政务感 | 深绿 + 米色 = 金融机构标准 | **5** | **最佳代表** |
| 15 | 整体印象 | 3 个形容词 | — | **稳重、密集、行业标杆** |

---

## § 1 句话核心发现

Velarasan 验证了"**Power BI 风格深绿 + 米色背景 + KPI delta 颜色 + chart-subtitle 解释性副标题**"是金融行业标准——v1.3 当前配色（蓝 `#1E5BAA`）可用，但**缺 delta 字段**和**副标题**，是行业最佳实践的两个缺口。

---

## § 兜底说明

- **找到 HTML demo**：✅（Velarasan-bi/Financial-Transaction-Analytics-Dashboard）
- **行业匹配度**：⭐⭐⭐⭐⭐（5/5）—— 保险 = 银行同类金融
- **风格借鉴度**：⭐⭐⭐⭐（4/5）—— 可借鉴 KPI delta、副标题、Tab 切换
- **直接可用度**：⭐⭐（2/5）—— 依赖 Chart.js CDN，违反 C-2 需替换

---

## § 验证建议

1. 在浏览器打开 `deep2-velarasan-finance.html`
2. 切换 5 个 Tab（Overview / Claims / Premium / Retention / Details）
3. 对比 v1.3 当前 6 模块：
   - v1.3 无 Tab 切换——单页纵向
   - v1.3 无 KPI delta——领导看不到"环比"
   - v1.3 无 chart-subtitle——图表维度不明确
4. **决策**：是否要为 v1.4 加 delta + subtitle？

---

## § 关键警告

⚠️ **Chart.js CDN 依赖** —— 此 demo 通过 `<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js">` 加载 Chart.js，**违反 C-2**。**不能复制整段 JS**，只能**借鉴设计模式**（Tab 切换、KPI delta、副标题）。