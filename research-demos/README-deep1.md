# 深研 #1：中文 HR 月报 demo（最像真实银行 HR 月报）

> **目标**：找一个**信息架构上最像真实银行 HR 月报**的 demo（叙述 + 排名 + 多列对比表）。
>
> **结论先行**：搜索 GitHub/Tableau/帆软公开 demo 后，**找到的"中文 HR 月报 HTML demo"中，shanjinki-HR-demo.html 是唯一高度匹配的实物**。它已经是 v1.1 调研的产物，本次重新审视并扩充分析（重点关注"叙述 + 排名 + 对比表"三大要素是否对齐真实 .docx 月报）。
>
> **demo 文件**：`research-demos/deep1-shanjinki-HR.html`（32KB，从 `shanjinki-HR-demo.html` 复制）

---

## § 来源

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/shanjinki/excel-to-html-slides |
| 路径 | `examples/sample_hr_report.html` |
| 协议 | MIT |
| 仓库活跃度 | v1.1 调研时 stars 较少但作者持续维护；最近 commit 2026-06 |
| demo 类型 | **单文件 HTML**（inline CSS+JS），Ctrl+U 看完全无外部请求 |
| 与 v1.1 关系 | v1.1 已用作主参考，本次作为**深研基线** |

### 为什么是它

我在 GitHub 二次搜索了 `hr dashboard html`、`human resources dashboard html template`、`workforce analytics dashboard html` 等 10+ 关键词，**找到的中文 HR 月报 HTML demo 几乎都缺**：

| GitHub 候选 | 不选原因 |
|---|---|
| `teenucaroline04-dot/HR-Analytics-Dashboard` | 仅 3KB 模板，无 HR 月报叙述结构 |
| `Rohini-hub05/CodeAlpha_HR_Analytics` | IBM HR Analytics 数据集（员工流失），不是月报 |
| `sohampatil333/Ai-Powered-HR-Analytics-Dashboard` | 流失率分析，Python+Plotly 不在浏览器运行 |
| `pruthvimamania528/Using-AI-GoogleStitch-tasknova-hr-dashboard-ui` | 招聘分析，UI 设计稿非月报 |
| `DineshPolisetti/workforce-dashboard` | 员工管理 SPA，HR 操作面板 ≠ 月报 |

**问题根源**：国内银行 HR 月报基本都是内部材料，公开 demo 极少；GitHub 上的 HR demo 多为"员工流失/招聘"主题，没有中文月报叙事+排名+多列对比表的形态。

**Fallback**：用 shanjinki-HR-demo.html 作为**最像的实物**，辅以 `docs/范例：人力资源管理数据驾驶舱（2026年5月）V2.docx` 作概念参照。

---

## § 视觉特征

### 主色（用 grep 提取 hex）

| 颜色 | hex | 用途 | 出现次数 |
|---|---|---|---|
| accent 蓝 | `#38bdf8` | 强调色 / 链接 | 4 |
| 琥珀 | `#f59e0b` | KPI 卡顶部彩条 / 警示 | 3 |
| 翠绿 | `#34d399` | 成功 / 正向趋势 | 3 |
| 红色 | `#ef4444` | 风险 / 警示 | 2 |
| 背景米色 | `#fbf4e9` / `#fff7ed` / `#fff1e7` | 多层次米色背景 | 各 1 |
| 卡片色 | `#f4eadb` / `#e8d8c3` | 卡片背景（米色系） | 各 1 |

**特征**：**米色系**（`#fbf4e9` 系）+ **红棕色点缀** + **彩色 KPI 彩条**——经典"Editorial Brief"风格。

### 字体系统

```css
font-family: "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
```

- 中文优先（PingFang SC + 微软雅黑）
- 数字未单独定义字体（fallback 到 Arial）

### 主题结构

- `body class="theme-editorial"` — Editorial Brief 主题（18 个主题之一）
- CSS variables 驱动，浅色 + 米色 + 红棕色系
- **canvas 背景动画**（右上角光晕）——演示用，**不适合打印**

---

## § 信息架构

### 章节层级（3 层）

```
页面标题：HR 人员运营分析报告 (h1)
├── 01 全局概览 (h2)
│   └── 5 个 KPI 卡 (h3 / kpi-label)
├── 02 关键洞察 (h2, card-title)
│   └── N 条洞察列表 (insight)
├── 03 口径假设 (h2, card-title)
│   └── N 条假设 (assumption)
├── 04 需求生命周期漏斗 / GMV 趋势 / 季度趋势 (h2)
│   └── funnel + bar 列表
├── 05 各一级分类交付健康度 / 主体表现 / 品类贡献 (h2)
│   └── cat-grid（多 cat-card）
├── 06 专项下钻 / 渠道贡献 / 结构贡献 (h2)
│   └── special-grid 或 cat-grid
├── 07 退货分析 / 异常与风险明细 (h2)
│   └── kpi-grid + data-table
└── 90 风险清单与行动建议 (h2, 编号 90 突出)
    └── risk-grid（risk-card × N）
```

**关键发现**：
- 章节用 `01, 02, 03, ...` + `90` 编号（风险段独立编号为 90，避免与前面混）
- 卡片标题用 `<span>02</span><h2>` 形式，编号 + 标题并列
- **2 列布局**：02 关键洞察 与 03 口径假设 横向并排（`section two-col`）

### 数据点数量

| 类型 | 数量 | 备注 |
|---|---|---|
| KPI 卡 | 5（顶部 `kpi-grid`） | 员工数/记录数/平均绩效/异常/高工时 |
| 章节编号 | 7+1（90 风险） | 编号递增 + 末尾 90 突出 |
| 表格 | 4 个 `<table>` | 季度趋势 / 异常与风险 / 退货分析等 |
| 柱状条目 | 5（funnel） + 多 bar-item | CSS div 实现 |
| 风险卡 | 1 grid（多张卡） | 每张卡有标题 + 详情 + 行动建议 |
| cat-card | 多张 | 每张：分类名 + 健康度 + 4 个 mini 数据点 + 经办人 |

### 叙述 vs 图表比例

| 类型 | 估算占比 |
|---|---|
| **叙述/解释文字**（section-title + insight + assumption + risk.action） | **~35%** |
| **图表/数据**（KPI + bar + funnel + table + cat-card） | **~65%** |

**关键洞察**：**叙述占比 35%，比 v1.3 当前高很多**——v1.3 几乎是 0% 叙述（仅数据 + 章节标题）。这是与 .docx 月报差距最大的点。

---

## § 图表清单（位置 + 类型 + 用途）

| 章节编号 | 位置 | 类型 | 用途 |
|---|---|---|---|
| 01 | 顶部 `kpi-grid` | 5 个 KPI 卡 | 全局数字快照（员工数/记录数等） |
| 02 | 关键洞察 | 文字段落列表 | 业务洞察（叙述） |
| 03 | 口径假设 | 文字段落列表 | 数据定义说明（叙述） |
| 04 | 漏斗 / 趋势 | CSS funnel + bar-item | 时间序列 + 漏斗（多数据系列） |
| 05 | 各分类 | cat-grid（多 cat-card） | 分类对比（每张卡：4 个 mini 数据） |
| 06 | 专项下钻 | special-grid | 子项明细（标题 + 4 meta + 4 sample） |
| 07 | 异常与风险 | data-table | 多列对比（主体 / 期间 / 原因 / 营收 / 净利润 / 负债率） |
| 90 | 风险清单 | risk-grid | 行动建议卡（标题 + 详情 + 行动） |

**特点**：
- 所有图表 = **纯 CSS**（div + width %），非 SVG/Canvas（除背景动画）
- cat-card 是核心组件——比单卡 KPI 信息密度高 3-4 倍
- 风险卡 = 业务级叙述（标题 + 详情 + 行动）三段式，最像 .docx 段落

---

## § 借鉴清单（具体到本项目能用什么）

### A. 章节编号 + 标题并列（**高优先**）

shanjinki 用 `<span>02</span><h2>` 形式编号 + 标题并列。**v1.3 当前只显示标题文字**，可以加编号让 6 模块结构更清晰：

```python
# composer.py 改动
def render_module_title(num: int, title: str) -> str:
    return f'<div class="section-title"><span>{num:02d}</span><h2>{title}</h2></div>'
```

### B. 2 列"洞察 + 假设"布局（**高优先**）

shanjinki 02 关键洞察 / 03 口径假设 并排。当前 v1.3 缺"业务叙述"段——可在每个模块顶部加一栏**关键发现**（来自数据自动生成），提升"专业感"。

### C. cat-card 模式（**中优先**）

每张卡 4 个 mini 数据点 + 1 个经办人。比单 KPI 卡信息密度高 3-4 倍，适合**分类对比**场景（如 M-2 客户经理分类、M-1 网点层级）。

### D. risk-card = 标题 + 详情 + 行动（**高优先**）

直接对应真实 HR 月报的"风险清单"段落。v1.3 当前没有这种**业务叙述卡**——这是 v1.3 最缺的元素。

### E. KPI 卡顶部彩条（**已借鉴**）

v1.3 已借鉴（4-tone 顶部条）。

### F. CSS bar 实现（**已借鉴**）

v1.3 已借鉴（div + width %）。

### G. canvas 背景动画（**不借鉴**）

演示效果，HR 月报严肃场景不需要，反而显得"花哨"。

---

## § 警示清单（哪些不适合 + 为什么）

| ❌ 不借鉴 | 原因 |
|---|---|
| 章节编号 90（风险段独立） | 编号应连续递增，90 不符合逻辑 |
| canvas 背景动画 | 演示好看但打印/邮件分发不友好 |
| 大量 emoji（漏斗/箭头） | 不专业 |
| `style="width:${w}%"` 内联 | 违反关注点分离（但 shanjinki 是单文件可接受） |
| 18 种主题切换 | 本项目不需要；用户只关心一个主题 |

---

## § 与 10 个 ADR 的映射

| ADR | 判定 | 证据 |
|---|---|---|
| **ADR-001 单 Excel 数据源** | KEEP（不可动） | — |
| **ADR-002 7 列数据契约** | **REVISE 候选** ⚠️ | shanjinki 用 `categories[].{name, rate, health, owners, mini-grid}` **嵌套结构**——表达力远超 7 列扁平结构。需要增加 `narrative` / `description` 字段？ |
| **ADR-003 CSS 静态图表** | KEEP | 与 shanjinki 一致 |
| **ADR-004 自研 CSS** | KEEP | 与 shanjinki 一致 |
| **ADR-005 Python f-string** | KEEP（不可动） | — |
| **ADR-006 composer 自动选 viz** | KEEP | shanjinki 也是"按结构自动选"（KPI/funnel/cat-grid/data-table） |
| **ADR-007 浅色专业风 + 4 级 tone** | KEEP | shanjinki editorial-brief 是浅色 + 米色 + 4 tone 的最佳实现 |
| **ADR-008 12-col grid + 3 断点** | KEEP | — |
| **ADR-009 钻取交互 YAGNI** | KEEP | shanjinki 也无交互 |
| **ADR-010 单文件部署** | KEEP（不可动） | — |

### 重点关注：ADR-002 修订方向

**触发条件**：shanjinki demo 用嵌套 JSON（`categories[].mini-grid[4]`、`specials[].items[4]`）描述"分类对比 + 子项明细 + 样本"，表达力远超 7 列扁平结构。

**具体修订方向（待用户审批）**：
- 选项 A：**加 1 列 `narrative` 到 7 列**（轻量——只加叙述文本，不改结构）
- 选项 B：**扩展为 9 列**（narrative + impact 评级 + 行动建议）
- 选项 C：**保持 7 列，用 is_total/排序/分组 字段的组合模拟嵌套**（最简——但表达力受限）

**建议**：A 选项——最小代价（1 列）+ 最大收益（叙述文字是 .docx 月报灵魂）。

---

## § 15 维度观察表

| # | 维度 | 描述 | 分值 (1-5) | 备注 |
|---|---|---|---|---|
| 1 | 结构层级 | 模块 / 章节 / 小节 / 数据点 | 4 | 3 层（标题 → 章节 → 数据） |
| 2 | 叙述 vs 数据比例 | 文字段落 vs 图表/数字 | 35/65 | 叙述 35% 是 .docx 月报典型形态 |
| 3 | 图表类型清单 | KPI / bar / funnel / cat-grid / table / risk-card | 6 类 | 全部 CSS 实现 |
| 4 | KPI 展示 | 5 个 KPI 卡 + 顶部 3px 彩条 | 4 | 顶部彩条分色清晰 |
| 5 | 排名展示 | cat-card grid（按 health 颜色分）+ risk-card | 4 | 颜色编码隐含排名 |
| 6 | 对比手法 | cat-grid（多分类对比）+ data-table（多列对比） | 4 | 表格列多列对比典型 |
| 7 | 配色方案 | 米色 + 红棕 + 4-tone accent | 4 | editorial 经典 |
| 8 | 字体系统 | PingFang SC + Microsoft YaHei + Arial | 4 | 中文优先；数字未单独 |
| 9 | 间距节奏 | 模块 24px / 卡片 16px / 数据 8px | 4 | 呼吸感足 |
| 10 | 强调手段 | 颜色（4-tone）+ 编号（01-90）+ 彩条 | 4 | 三重强调 |
| 11 | 表格用法 | 异常明细 / 季度趋势 / 退货分析 | 4 | 6-7 列对比 |
| 12 | 模块标题样式 | 编号 + 标题并列（`<span>02</span><h2>`） | 5 | 视觉锚点强 |
| 13 | 留白比例 | 米色背景 + 大间距 + 卡片分离 | 4 | 偏松（不是密集） |
| 14 | 银行/政务感 | 浅米色 + 红棕 = "出版物"风格 | 3 | 偏编辑风，非纯银行 |
| 15 | 整体印象 | 3 个形容词 | — | **专业、编辑感、信息密度高** |

---

## § 1 句话核心发现

shanjinki-HR-demo 的 **章节编号 + 2 列叙述 + cat-card + risk-card** 4 个元素是真实银行 HR 月报（.docx）的最小可视化骨架；**v1.3 当前缺叙述 + 排名 + 多列对比表三大块**，导致用户评价"不专业"。

---

## § 兜底说明

- **找到 HTML demo**：✅（shanjinki-HR-demo.html）
- **找到更优 demo**：❌（GitHub 无其他中文 HR 月报 demo 接近）
- **概念参考**：`docs/范例：人力资源管理数据驾驶舱（2026年5月）V2.docx`（已存在的真实月报）

---

## § 验证建议

如需对照真实 .docx 阅读：
1. 打开 `deep1-shanjinki-HR.html` 在浏览器
2. 打开 `docs/范例：人力资源管理数据驾驶舱（2026年5月）V2.docx`
3. 对比：
   - .docx 有"关键发现"段落 → shanjinki 02 关键洞察 → v1.3 ❌
   - .docx 有"风险清单" → shanjinki 90 风险清单 → v1.3 ❌
   - .docx 有"排名对比表" → shanjinki data-table → v1.3 部分有

**结论**：v1.3 → v1.4 修订方向应**优先增加叙述段 + 风险卡**。