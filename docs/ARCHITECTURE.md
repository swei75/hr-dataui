# 技术选型与架构设计

> **目的**：记录本项目的技术选型决策与架构设计，方便未来回溯与持续迭代。
>
> **维护原则**：
> - 每次架构变更必须同步更新本文件
> - 新决策追加 §5 ADR 章节（编号递增，不修改历史 ADR）
> - 旧决策**不删除**——加 "Superseded by ADR-NNN" 标记
>
> **当前版本**：v1.5（2026-07-04）

---

## 0. 项目概览

### 0.1 一句话

**银行 HR 月度管理驾驶舱**——维护 1 个 Excel（9 sheets）→ 跑 `python build.py` → 生成 ~98KB 单文件 HTML 仪表盘。

### 0.2 架构总览（v1.5：每模块独立 viz）

```
┌─────────────────────────────────────────────────────────────────┐
│  Excel (.xlsx, 9 sheets)                                         │
│  └─ 配置 + 6 模块 + 1 多列 + 1 _prev 快照                       │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ pandas.read_excel()
┌─────────────────────────────────────────────────────────────────┐
│  extractors/                                                      │
│  ├─ reader.py    读 Excel → 原始 dict（含 _prev）               │
│  └─ mapping.py   sheet→模块 + viz_style 字段 + 字段映射         │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ apply_mapping()
┌─────────────────────────────────────────────────────────────────┐
│  composer.py                                                      │
│  ├─ render_kpi_strip()      Dashboard 顶 6 KPI（v_hero 数字塔）  │
│  ├─ render_module()         模块渲染主函数                     │
│  │  └─ 6 风格分支（is_v_*_style dispatch）：                    │
│  │     ├─ is_v1_style     → M-1 / M-5 (6 KPI + 段落 / 5 财务大卡)│
│  │     ├─ is_v11_style    → M-2 员工情况                       │
│  │     ├─ is_v_hr_style   → M-3 人员优化 (gauge + flow + dual-bar)│
│  │     ├─ is_v_tree_style → M-4 干部队伍 (分类树)              │
│  │     ├─ is_v_fc_style   → M-5 考核薪酬 (5 财务大卡)         │
│  │     └─ is_v_train_style→ M-6 培训赋能 (v1 顶 + v8 主体)   │
│  └─ 维护 _prev 快照（自动算 delta）                              │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ render()
┌─────────────────────────────────────────────────────────────────┐
│  templates/base.py                                                │
│  ├─ Python f-string 模板（不用 Jinja2）                          │
│  ├─ inline CSS（v1.5 视觉系统：#9f6b44 / 16px / 加大字阶）       │
│  └─ 7 套 viz 样式（.kpi-hero / .kpi-card-m1 / .kpi-card /     │
│       .stacked-bar / .gauge-card / .fc-card-m6 / .tree-wrap /   │
│       .rail-block / .dual-bar / .rank-card 等）                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  output/index.html                                                │
│  └─ 单文件，~98KB，0 外部依赖，file:// 可双击                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. 核心约束（不可妥协）

以下 5 条贯穿所有版本，**任何方案讨论前先看这一节**：

| # | 约束 | 为什么不可妥协 |
|---|---|---|
| C-1 | **单文件 HTML** | 邮件附件、U 盘、内网分发是核心场景 |
| C-2 | **0 外部依赖** | 接收方无技术背景，不能要求"装个 Node"或"开 VPN" |
| C-3 | **完全离线 / file:// 可用** | 必须避开 CORS；任何 CDN/fetch 都是负担 |
| C-4 | **多端响应式** | 领导可能在手机上看 |
| C-5 | **体积目标 ≤ 50KB（实际 98KB 可接受）** | 邮件附件友好 |

> **违反 C-1 ~ C-5 任一条 = 推翻整个项目目标。** 需要用户明确批准 + 量化数据证明问题。

---

## 2. v1.5 模块 viz 风格详解（核心创新）

v1.4 是统一默认风格；v1.5 改为**每模块独立 viz**，表达力最大化。

| 模块 | viz 风格 | 实现位置 | 主要组件 | 触发条件 |
|---|---|---|---|---|
| Dashboard 顶部 | **v_hero 数字塔** | `composer.py: render_kpi_strip()` | 6 项指标横向 icon + 6 色左侧 border | composer 总是渲染（每个 dashboard 顶部） |
| M-1 组织架构 | **v1（6 KPI + 段落）** | `composer.py: render_module()` `is_v1_style` 分支 | 6 个 KPI 卡 + sub_text 段落 | `is_v1_style=True` |
| M-2 员工情况 | **v11（4 KPI + 5 stacked + 8 grid）** | `composer.py: render_module()` `is_v11_style` 分支 | 4 个核心 KPI + 5 个 stacked bar + 8 个 grid 子项 | `is_v11_style=True` |
| M-3 人员优化 | **v_hr 融合** | `composer.py: render_module()` `is_v_hr_style` 分支 | gauge（引入率）+ flow（退出流向）+ dual-bar（腾笼换鸟）+ 3 排名（含任务完成量 Top 3，v1.5.20 补） | `is_v_hr_style=True` |
| M-4 干部队伍 | **v2 分类树** | `composer.py: render_module()` `is_v_tree_style` 分支（含 `render_tn` 内部函数）| 4 大类（按职级）+ 中层分支（按分行/部门）| `is_v_tree_style=True` |
| M-5 考核薪酬 | **v1（5 财务大卡 + sparkline）** | `composer.py: render_module()` `is_v_fc_style` 分支 | 5 个财务大卡（工资/年金/补充医疗等）+ sparkline 趋势 | `is_v_fc_style=True` |
| M-6 培训赋能 | **v_train（v1 顶 + v8 主体）** | `composer.py: render_module()` `is_v_train_style` 分支 | v1 风格的顶部 KPI 卡 + v8 风格的主体进度条/列表 | `is_v_train_style=True` |

**实施机制**：
- `extractors/mapping.py` 每个模块配置项含 `kpi_cards_v1` / `dim_cards` / `tree` / `gauges` / `fc_cards` / `kpi_cards_v1` 等风格字段
- `composer.py: render_module()` 根据上述字段检测 `is_v_*_style=True`，dispatch 到对应 `elif` 分支
- 各 viz 风格在 `render_module()` 函数内独立实现（约 100-200 行/风格），**互不耦合**
- Dashboard 顶部走 `render_kpi_strip()` 函数（独立于 `render_module`）

---

## 3. v1.5 视觉系统

| 维度 | v1.4 | v1.5 |
|---|---|---|
| 主色 | `#1E5BAA` indigo | **`#9f6b44` 米色红棕** |
| 深主色 | — | `#6b4423` |
| 警告 | — | `#a04030` |
| 成功 | — | `#4a7c59` |
| body font-size | 14px | **16px** |
| hero | — | **3.4em** |
| module-title | 1.5em | **2em** |
| kpi-card | — | **2.4em** |
| 字号阶梯 | 14/16/24px | 16/24/32px + 加大 hero/kpi |
| 整体气质 | 银行稳重（冷色调） | 米色红棕（温暖专业，参考 shanjinki Editorial Brief） |

---

## 4. GitHub 调研记录（v1.4 → v1.5）

> 调研时间：v1.1（2026-07-03）+ v1.4（2026-07-04 redesign research）
> 调研产物：`research-demos/`（4 个实物 HTML demo + 3 深研 + 8 广扫描 + 决策映射）

### 4.1 shanjinki/excel-to-html-slides ⭐ 主要参考

**仓库**：https://github.com/shanjinki/excel-to-html-slides
**协议**：MIT
**核心价值**：Python 生成单文件 HTML 仪表盘 + 18 种视觉风格 + 完整中文 HR demo

**v1.5 直接借鉴**：shanjinki-HR-demo 的 **Editorial Brief 风格**（米色 + 红棕）→ v1.5 主色 `#9f6b44`。

### 4.2 v1.4 重新设计调研（已完成）

调研产出（`research-demos/`）：
- 3 个深研 README（中文 HR 月报 / 银行 dashboard / 管理驾驶舱）
- 8 个广扫描矩阵（Tableau / PowerBI / FineBI / Smartbi / Superset / Metabase）
- 决策映射表（10 个 ADR 判定）
- ARCHITECTURE.md 修订建议

调研结论：每模块独立 viz 风格表达力最强 → 落地为 v1.5。

### 4.3 否决的候选

| 候选 | 否决原因 | 否决时间 |
|---|---|---|
| `StructuredLabs/preswald` | Pyodide + WASM 单文件包（10-20MB runtime） | v1.1 |
| `sqlinsights/st-static-export` | 把 Streamlit 导出静态 HTML | v1.1 |
| ECharts 5（图表） | 体积 ~1MB | v1.0 |
| Pico.css 2（样式） | 风格固定，无法定制 | v1.0 |
| Jinja2（模板） | 引入额外依赖 | v1.0 |
| Alpine.js（前端框架） | v1.2 引入但 v1.3 移除 | v1.3 |
| 统一 viz 风格（v1.4） | 表达力不足，每模块独立 viz 更优 | v1.5 |

---

## 5. 决策记录（ADR）

每个 ADR 包含：**Status / Date / Context / Decision / Consequences**。

### ADR-001: 单 Excel 数据源（9 sheets）

- **Status**: Accepted
- **Date**: 2026-07-03（v1.1）→ 强化于 2026-07-04（v1.5）

**Decision**：1 个 .xlsx / 9 sheets = 配置 + 6 模块 + M-4 多列 + _prev 快照。

**Consequences**：用户只维护 1 个文件；_prev 自动维护不污染 Excel。

---

### ADR-002: 7 列数据契约

- **Status**: Superseded by [ADR-011](#adr-011-9-列数据契约修订加-delta--sub_text--metric_note)（2026-07-04）
- **Date**: 2026-07-04（v1.3）

**Decision**：7 列固定结构 → 已被 ADR-011 取代。

---

### ADR-003: CSS 静态图表（v1.0 基础）+ ECharts 仅可选

- **Status**: Accepted → 部分 Superseded by ADR-013
- **Date**: 2026-07-03（v1.1）

**Decision**：默认 CSS 静态图表，ECharts 仅作可选升级路径。

---

### ADR-004: 自研 CSS（继承 shanjinki 18 styles）

- **Status**: Accepted → 强化于 v1.5
- **Date**: 2026-07-03（v1.1）

**Decision**：自研 CSS，v1.5 强化为 7 套 viz 风格的 CSS。

---

### ADR-005: Python f-string（不用 Jinja2）

- **Status**: Accepted
- **Date**: 2026-07-03（v1.1）

**Decision**：Python f-string，`templates/base.py` 是 .py 文件。

---

### ADR-006: composer 自动选 viz（取代 viz registry 强制选择）

- **Status**: Superseded by [ADR-013](#adr-013-每模块独立-viz-风格v15-革新)（2026-07-04）
- **Date**: 2026-07-04（v1.3）

**Decision**：v1.3 自动选 viz → v1.5 改为每模块独立 viz。

---

### ADR-007: 浅色专业风 + CSS variables + 4 级 tone

- **Status**: Superseded by [ADR-014](#adr-014-米色红棕视觉系统v15)（2026-07-04）
- **Date**: 2026-07-04（v1.3）

**Decision**：v1.3 主色 indigo → v1.5 改为米色红棕。

---

### ADR-008: 12-col grid + 3 断点（1100/768/480）

- **Status**: Accepted
- **Date**: 2026-07-04（v1.3）

**Decision**：12-col grid + 3 断点 + 触屏按钮 ≥ 44×44px。

---

### ADR-009: 钻取交互 YAGNI（v1.2 Alpine.js 钻取在 v1.3 移除）

- **Status**: Accepted
- **Date**: 2026-07-04（v1.3）

**Decision**：不实现钻取，所有数据平铺。

---

### ADR-010: 单文件部署（拒绝拆 SPA / 后端）

- **Status**: Accepted
- **Date**: 2026-07-03（v1.1）

**Decision**：所有 HTML/CSS/JS/JSON inline 进 `output/index.html`。

---

### ADR-011: 9/10 列数据契约（修订：加 delta + sub_text + metric_note）

- **Status**: Accepted
- **Date**: 2026-07-04（v1.4，基于 S1 调研）

**Decision**：在 ADR-002 的 7 列基础上扩展为 10 列：

| # | 列 | 来源 |
|---|---|---|
| 1 | 分组 | ADR-002 保留 |
| 2 | 名称 | ADR-002 保留 |
| 3 | 数值 | ADR-002 保留 |
| 4 | 单位 | ADR-002 保留 |
| 5 | 备注 | ADR-002 保留 |
| 6 | 排序 | ADR-002 保留 |
| 7 | is_total | ADR-002 保留 |
| 8 | **delta** | v1.4 新（composer 自动算） |
| 9 | **sub_text** | v1.4 新（模块级叙述） |
| 10 | **metric_note** | v1.4 新（KPI 下方 12-16 字看图说话） |

**delta 字段**：Excel 仍只放本期数据（不污染），composer 维护 `_prev` 快照计算环比。

---

### ADR-012: 3 色风险等级编码（修订）

- **Status**: Accepted
- **Date**: 2026-07-04（v1.4，基于 S1 调研）

**Decision**：在 v1.3 `--primary` + 4 级 tone 基础上增加 3 色风险 token：

```css
--success: #16A34A;  /* 绿 */
--warning: #D97706;  /* 橙 */
--danger:  #DC2626;  /* 红 */
```

**v1.5 强化**：3 色 token 与米色红棕主色协调搭配使用。

---

### ADR-013: 每模块独立 viz 风格（v1.5 革新）

- **Status**: Accepted
- **Date**: 2026-07-04（v1.5）

**Context**：v1.4 是统一默认风格，调研发现每模块独立 viz 表达力更强：
- M-1 组织架构：6 KPI + 段落（v1）比 donut 更直观
- M-2 员工情况：4 KPI + 5 stacked + 8 grid（v11）能容纳多维构成
- M-3 人员优化：gauge + flow + dual-bar + 3 排名（v_hr 融合）比单一图表更能表达多维流程
- M-4 干部队伍：分类树（v2）天然契合层级关系
- M-5 考核薪酬：财务大卡 + sparkline（v1）突出金额主体
- M-6 培训赋能：复合 viz（v_train）能同时展示 KPI + 进度

**Decision**：v1.5 取消 ADR-006 的"composer 自动选 viz"，改为**每模块独立 viz**：

| 模块 | viz 风格 | composer 风格分支 | viz 函数 |
|---|---|---|---|
| Dashboard 顶 | v_hero 数字塔 | `is_v_hero_style` | `viz/v_hero.py` |
| M-1 组织架构 | v1（6 KPI + 段落） | `is_v1_style` | `viz/v1.py` |
| M-2 员工情况 | v11（4 KPI + 5 stacked + 8 grid） | `is_v11_style` | `viz/v11.py` |
| M-3 人员优化 | v_hr 融合 | `is_v_hr_style` | `viz/v_hr.py` |
| M-4 干部队伍 | v2 分类树 | `is_v2_style` | `viz/v2.py` |
| M-5 考核薪酬 | v1 财务大卡 + sparkline | `is_v1_style` | `viz/v1.py` |
| M-6 培训赋能 | v_train（v1 顶 + v8 主体） | `is_v_train_style` | `viz/v_train.py` |

**Consequences**：
- ✅ 表达力最大化（每模块用最适合的 viz）
- ✅ 视觉丰富度提升（用户反馈从"单调"→"专业"）
- ✅ 100% 覆盖 .docx 范例 77/77 关键数据点
- ❌ viz 函数数量从 1（统一默认）→ 7（每模块独立），维护成本上升
- ❌ 输出文件 69KB → 98KB（仍 ≤ 100KB 上限）
- ❌ 用户不可切换 viz 风格（mapping.py 写死）

**Why YAGNI 不再适用**：v1.3 时期用户评价"单调"，表明 viz 风格的"灵活性"反而是负担——用户不需要切换，只需要"对的风格"。

---

### ADR-014: 米色红棕视觉系统（v1.5）

- **Status**: Accepted
- **Date**: 2026-07-04（v1.5）

**Context**：v1.4 主色 `#1E5BAA` indigo（银行稳重感），用户反馈"偏冷"，与 .docx 范例 HR 月报的温暖气质不匹配。

调研发现 shanjinki-HR-demo 的 **Editorial Brief 风格**（米色 + 红棕）更符合 HR 月报的"温暖专业"基调。

**Decision**：v1.5 视觉系统升级：

| 维度 | v1.4 | v1.5 |
|---|---|---|
| 主色 | `#1E5BAA` indigo | `#9f6b44` 米色红棕 |
| 深主色 | — | `#6b4423` |
| 警告 | — | `#a04030` |
| 成功 | — | `#4a7c59` |
| body font-size | 14px | **16px** |
| hero | — | **3.4em** |
| module-title | 1.5em | **2em** |
| kpi-card | — | **2.4em** |

**Consequences**：
- ✅ 视觉更温暖专业，符合 HR 月报气质
- ✅ 加大字号提升可读性（领导可能在手机看）
- ✅ 借鉴 shanjinki-HR-demo Editorial Brief 风格（MIT 协议合规）
- ❌ 主色变更需要同步更新 CSS variables（已迁移）
- ❌ 字号变大导致文件 +29KB（69KB → 98KB）

---

## 6. 数据契约（v1.5：10 列）

每个数据 sheet **10 列**：

| # | 列 | 含义 | 决定什么 |
|---|---|---|---|
| 1 | 分组 | 数据分类 | viz 风格（映射到 viz_style 字段） |
| 2 | 名称 | 显示名 | 图表/表格中显示 |
| 3 | 数值 | 主要数字 | 柱长、饼大小、KPI 主数字 |
| 4 | 单位 | 显示单位 | 数字后缀 |
| 5 | 备注 | 可选说明 | 鼠标悬停或表格列 |
| 6 | 排序 | 显示顺序 | 数字越小越靠前 |
| 7 | is_total | 是否总数行 | 用于 KPI+bar 组合 |
| 8 | delta | 环比差 | composer 自动算（来自 _prev） |
| 9 | sub_text | 模块级叙述 | 关键洞察段落 |
| 10 | metric_note | KPI 卡底部说明 | 12-16 字看图说话 |

**约定**：
- 占比统一 0-1 浮点（`0.2586` = 25.86%）
- 缺失值 = 空 cell（**不写** "N/A" / "无" / "-"）
- 千分位统一 `,`（`5,901`）
- 时段字段从 `配置` sheet 读

---

## 7. 模块 viz 实施表（v1.5）

| 模块 | 实施位置 | 风格分支 | viz 函数 | 关键 CSS 类 |
|---|---|---|---|---|
| Dashboard 顶 | `composer.render_dashboard_header()` | `is_v_hero_style` | `viz/v_hero.py` | `.hero-tower`, `.hero-tower__item` |
| M-1 组织架构 | `composer.render_module("M-1")` | `is_v1_style` | `viz/v1.py` | `.v1-kpi-grid`, `.v1-narrative` |
| M-2 员工情况 | `composer.render_module("M-2")` | `is_v11_style` | `viz/v11.py` | `.v11-kpi-row`, `.v11-stacked`, `.v11-grid-8` |
| M-3 人员优化 | `composer.render_module("M-3")` | `is_v_hr_style` | `viz/v_hr.py` | `.v-hr-gauge`, `.v-hr-flow`, `.v-hr-dual-bar`, `.v-hr-ranking` |
| M-4 干部队伍 | `composer.render_module("M-4")` | `is_v2_style` | `viz/v2.py` | `.v2-tree`, `.v2-tree__node` |
| M-5 考核薪酬 | `composer.render_module("M-5")` | `is_v1_style` | `viz/v1.py`（共用 M-1） | `.v1-finance-card`, `.sparkline` |
| M-6 培训赋能 | `composer.render_module("M-6")` | `is_v_train_style` | `viz/v_train.py` | `.v-train-header`, `.v-train-body` |

---

## 8. 经验教训

### 8.1 v1.2 为什么被否（即使"做完了"）

**表层原因**：用户评价"不专业、单调"。
**深层原因**：
1. **过度工程化**：8 viz registry + mapping 配置
2. **样式贫乏**：抄了 shadcn/Linear 皮毛
3. **表达力不足**：bar/pie 表达"总数 vs 部分"不够

**v1.3 → v1.5 的纠偏**：
- v1.3 移除 viz registry（ADR-006）
- v1.5 每模块独立 viz（ADR-013）

### 8.2 "通过" ≠ "全速前进"

v1.3 评审通过后用户继续提需求（v1.4 / v1.5）。**教训**：每个新阶段都要再确认。

### 8.3 调研要形成文档

v1.4 调研形成 `research-demos/` 完整笔记（3 深研 + 8 广扫描 + 决策映射）→ v1.5 直接落地。

### 8.4 viz 灵活性是负担，不是收益

v1.3 自动选 viz 让用户"省心"，但 v1.5 调研发现用户其实需要"对的风格"——预设的固定 viz 反而更好。**教训**：用户说"YAGNI" 时，往往意味着"我也不知道我想要什么"。

---

## 9. 已知缺口（待补充）

| 缺口 | 影响 | 优先级 |
|---|---|---|
| 性能基准测试（构建时间、加载时间、内存峰值） | 回归时无基线 | 🟡 中 |
| 6 模块各自的"业务定义"（什么算客户经理、什么算腾笼换鸟） | 数据契约演化时无参考 | 🟢 低 |

### 9.1 后续维护建议

- **添加新 ADR**：在 §5 末尾追加 `### ADR-NNN: ...`
- **旧决策变更**：不要修改原 ADR，加 "Superseded by ADR-NNN" 标记
- **新调研**：在 `research-demos/` 下加 `README-项目名.md` + 实物 demo
- **新约束**：如发现 C-1~C-5 不够用，先讨论再追加为 C-6 / C-7

---

## 10. 参考资料

| 文档 | 路径 | 说明 |
|---|---|---|
| 需求 v1.5 | `docs/REQUIREMENTS.md` | 当前需求 |
| 月度工作流 | `docs/MONTHLY-WORKFLOW.md` | HR 操作手册 |
| 项目指引 | `CLAUDE.md` | 行为准则 + Anti-Patterns |
| 调研 demo | `research-demos/README.md` | 4 个 GitHub 项目的实物对比 + v1.4 调研 |
| v1.4 spec | `docs/superpowers/specs/2026-07-04-hr-dataui-v1.4-design.md` | v1.4 设计 spec（含 v1.5 演进说明） |
| v1.4 plan | `docs/superpowers/plans/2026-07-04-hr-dataui-v1.4.md` | v1.4 实施计划 |

---

## 变更日志

| 日期 | 变更 | 作者 |
|---|---|---|
| 2026-07-04 | 初始版本，包含 v1.3 全部 ADR（ADR-001 ~ ADR-010） | Claude + 用户协作 |
| 2026-07-04 | S1 调研完成：新增 ADR-011（9 列契约）+ ADR-012（3 色风险等级） | Claude + 用户确认 |
| 2026-07-04 | **v1.5 演进：新增 ADR-013（每模块独立 viz）+ ADR-014（米色红棕视觉系统）；ADR-006 / ADR-007 加 Superseded 标记；视觉系统表格更新；§2 重写为 v1.5 模块 viz 风格详解** | Claude + 用户协作 |
| 2026-07-05 | **v1.5.21**：顶部 hero 区广银红+金（hero-only token 隔离，不污染 `--primary` 主调色板） | Claude + 用户协作 |
| 2026-07-05 | **v1.5.21.2**：5 处排版 bug 修复（kpi-hero 数字+单位、M-1 "2+13 个" 拆行、cs-card 拆行、stacked 列宽分配、legend 拆字、段落右截断、podium 数字可见） | Claude + 用户协作 |
| 2026-07-05 | **v1.5.21.3**：移动端响应式 — 桌面 ≥1100px 完全不动；<1100px 17 grid 自适应（`minmax + overflow-x` 横滚）；移动 scrollbar visible；viz/*.py 硬编码宽度 CSS override 不改源码 | Claude + 用户协作 |