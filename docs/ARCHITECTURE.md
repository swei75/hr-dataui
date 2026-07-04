# 技术选型与架构设计

> **目的**：记录本项目的技术选型决策与架构设计，方便未来回溯与持续迭代。
>
> **维护原则**：
> - 每次架构变更必须同步更新本文件
> - 新决策追加 §5 ADR 章节（编号递增，不修改历史 ADR）
> - 旧决策**不删除**——加 "Superseded by ADR-NNN" 标记
>
> **当前版本**：v1.3（2026-07-04）

---

## 0. 项目概览

### 0.1 一句话

**银行 HR 月度管理驾驶舱**——维护 1 个 Excel（8 sheets）→ 跑 `python build.py` → 生成单文件 HTML 仪表盘。

### 0.2 架构总览

```
┌─────────────────────────────────────────────────────────────────┐
│  Excel (.xlsx, 8 sheets)                                         │
│  └─ 配置 + 6 模块 + 1 多列表                                     │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ pandas.read_excel()
┌─────────────────────────────────────────────────────────────────┐
│  extractors/                                                      │
│  ├─ reader.py    读 Excel → 原始 dict                            │
│  └─ mapping.py   sheet→模块 + viz 配置 + 字段映射                 │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ apply_mapping()
┌─────────────────────────────────────────────────────────────────┐
│  composer.py                                                      │
│  ├─ 按"分组"结构自动选 viz（KPI/donut/bar/table）                │
│  └─ 组装 6 模块 HTML 片段                                       │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ render()
┌─────────────────────────────────────────────────────────────────┐
│  templates/base.py                                                │
│  ├─ Python f-string 模板（不用 Jinja2）                           │
│  └─ inline CSS（自研 + 继承 shanjinki）                          │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ write
┌─────────────────────────────────────────────────────────────────┐
│  output/index.html                                                │
│  └─ 单文件，~69KB，0 外部依赖，file:// 可双击                    │
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
| C-5 | **体积目标 ≤ 50KB** | 邮件附件友好（实际 ~69KB，已超目标但可接受） |

> **违反 C-1 ~ C-5 任一条 = 推翻整个项目目标。** 需要用户明确批准 + 量化数据证明问题。

---

## 2. GitHub 调研记录

> 调研时间：v1.1（2026-07-03）+ v1.2（2026-07-04）
> 调研产物：`research-demos/`（4 个实物 HTML demo + 分析笔记）

### 2.1 shanjinki/excel-to-html-slides ⭐ 主要参考

**仓库**：https://github.com/shanjinki/excel-to-html-slides
**协议**：MIT
**核心价值**：Python 生成单文件 HTML 仪表盘 + 18 种视觉风格 + 完整中文 HR demo

#### 三个 demo 实物对比（v1.1）

| Demo | 文件 | 视觉风格 | 关键学习 |
|---|---|---|---|
| `shanjinki-HR-demo.html` | 32KB | Editorial Brief（米色 + 红棕） | ⭐ 重点参考，最像我们要做的 |
| `shanjinki-finance.html` | 36KB | Boardroom Light（深蓝 + 浅灰） | 同架构不同配色 |
| `shanjinki-sales.html` | 43KB | Command Center（深色 + 青色） | 深色主题对比 |

#### shanjinki-HR-demo 详细观察（13 条）

1. **完全离线** — Ctrl+U 看全是 inline CSS+JS，0 外部请求
2. **中文优先** — 标题"HR 人员运营分析报告"，UI 全中文
3. **3 断点响应式**（980px / 640px）
4. **KPI 卡顶部 3px 彩条**（按类别分色）
5. **2 栏布局**（关键洞察 + 口径假设）
6. **部门柱图 = 纯 CSS**（div + width %），不是 SVG/Canvas
7. **章节编号** 01, 02, 03...
8. **canvas 背景动画**（演示用，不适合打印 → 我们不用）
9. 5 个 KPI 卡：员工数 / 记录数 / 平均绩效 / 异常 / 高工时
10. 风险清单 = 2 列卡片（标题 + 详情 + 行动建议）
11. 表格横向滚动在移动端（不折断）
12. 无交互（不下钻、不切视图）
13. 图表是 CSS 静态条形（无法缩放）

#### 我们的取舍

- ✅ **借鉴**：CSS 静态图表、KPI 卡 + 彩条、章节编号、3 断点响应式、2 栏布局
- ❌ **不借鉴**：canvas 背景动画（不适合 HR 月报严肃场景）

### 2.2 Sven-Bo/pyecharts-dashboard（对比验证）

**仓库**：https://github.com/Sven-Bo/pyecharts-dashboard
**核心价值**：ECharts 真图表 + Tab 切换验证

#### 关键发现

| 维度 | 评估 |
|---|---|
| 图表质量 | ✅ ECharts 完整，hover/tooltip |
| Tab 切换 | ✅ vanilla JS 实现（验证可行） |
| **CDN 依赖** | ❌ `<script src="https://assets.pyecharts.org/...">` 断网打不开 |
| 响应式 | ❌ 写死 `width:900px; height:500px;` |
| 架构 | 单 sheet，无多模块 |

#### 我们的取舍

- ❌ **否决整体方案**——CDN 致命违反 C-2 / C-3
- ✅ **学到**：Tab 切换可用 vanilla JS 实现（不强制 Alpine.js）
- ✅ **学到**：复杂图表（漏斗、桑基）需要 ECharts，但需控制范围

### 2.3 shadcn / Linear（视觉参考，**调研记录待补**）

> ⚠️ **已知缺口**：v1.2 视觉调研时参考了 shadcn 和 Linear 的设计系统，
> 但当时**没有形成文档化的分析笔记**——只影响了 v1.2 的视觉实现
> （CSS variables + 12-col grid + 4-tone + 9 viz）。
>
> **下一步**：在 `research-demos/` 下补充 `README-shadcn.md` / `README-linear.md`。
> 当前可参考 v1.2 实施代码 + git 历史 commit `6a8c2cb`。

### 2.4 否决的候选

| 候选 | 否决原因 | 否决时间 |
|---|---|---|
| `StructuredLabs/preswald` | Pyodide + WASM 单文件包（10-20MB runtime），首屏加载 > 3s，违反 C-1 / C-5 | v1.1 |
| `sqlinsights/st-static-export` | 把 Streamlit 导出静态 HTML，客户端架构违反单文件约束 | v1.1 |

### 2.5 否决的技术方案

| 方案 | 来源 | 否决原因 |
|---|---|---|
| ECharts 5（图表） | v1.0 | 体积 ~1MB，CDN 或 inline 都违反 C-1 / C-5 |
| Pico.css 2（样式） | v1.0 | 风格固定，无法定制专业风；体积 ~10KB 但要 CSS 重新覆盖 |
| Jinja2（模板） | v1.0 | 引入额外依赖；shanjinki 用 f-string 已够用 |
| Alpine.js（前端框架） | v1.0 → v1.2 → v1.3 ❌ | v1.2 引入但 v1.3 移除（见 ADR-009） |

---

## 3. 选型历程 v1.0 → v1.3

| 版本 | 日期 | 关键变更 | 用户评价 |
|---|---|---|---|
| **v1.0** | 2026-07-03 前 | ECharts + Pico.css + Jinja2 + Alpine.js 重型方案 | （未实际发布） |
| **v1.1** | 2026-07-03 | GitHub 调研 → fork shanjinki；CSS 静态图表；自研 CSS | 选型定型 |
| **v1.2** | 2026-07-03 | mapping 配置 + 8 viz + Alpine.js 钻取（43KB） | "不专业、单调" |
| **v1.3** | **2026-07-04** | **Excel SOT + 分组驱动 + 自动 viz + 浅色专业风** | **当前** |

### 3.1 v1.2 → v1.3 的关键教训

v1.2 在工程上"做完了"，但用户评价"不专业"。根因：
1. **过度工程化**——8 个 viz registry 强制选择，配置项太多
2. **样式贫乏**——shadcn/Linear 只学了皮毛，缺乏设计系统
3. **图表表达力不足**——"总数 vs 部分"的组成关系没有图形化表达

v1.3 的转向：
- ✅ 移除 viz registry 强制选择（用户不指定图表类型）
- ✅ composer 按分组结构**自动选 viz**（1 行 KPI / 2-3 行 donut / 4+ 行 bar）
- ✅ 引入 Excel 作为 source of truth（用户每月只改数值列）
- ✅ 浅色专业风 + 4 级 tone + 12px 圆角

---

## 4. 架构设计

### 4.1 数据流（详细）

```
[Excel .xlsx]
    │  openpyxl 读
    ▼
[reader.read_workbook(path)]
    │  返回 dict {"组织架构": [records], "员工情况": [...], ...}
    │  records = [{分组, 名称, 数值, 单位, 备注, 排序, is_total}, ...]
    ▼
[mapping.apply(raw_data)]
    │  按 MODULES 配置 → 标准化数据
    │  加上 模块标题/icon/order
    ▼
[composer.compose(modules)]
    │  对每个模块 → 按"分组"切分数据
    │  每个分组 → 自动选 viz（_pick_viz(group)）
    │  viz_registry[type].render(data, options) → HTML 片段
    │  拼装进 base template
    ▼
[base.render_page()]
    │  Python f-string 渲染（不用 Jinja2）
    │  inline CSS（自研 + shanjinki 风格）
    │  inline JSON（window.HR_DATA）
    │  inline JS（vanilla，少量交互）
    ▼
[output/index.html]   单文件 ~69KB
```

### 4.2 模块划分

```
hr-dataui/
├── build.py                  # 入口
├── requirements.txt          # pandas + openpyxl
├── CLAUDE.md                 # 行为准则 + 选型 + Anti-Patterns
├── README.md                 # 项目介绍
│
├── data/
│   └── test.xlsx             # 8 sheets source of truth
│
├── extractors/
│   ├── reader.py             # Excel → dict
│   ├── mapping.py            # sheet→模块 + viz 配置
│   └── drills.py             # 钻取数据加载（备用）
│
├── viz/                      # 8 个 viz 函数（composer 自动选）
│   ├── kpi.py bar.py pie.py funnel.py
│   └── progress.py ranking.py hierarchy.py table.py
│
├── composer.py               # 自动选 viz + 拼装 6 模块
├── templates/base.py         # f-string 模板 + CSS
│
├── tests/
│   ├── _make_test_xlsx.py    # 生成测试 Excel
│   └── test_build_e2e.py     # 6 个 E2E 用例
│
├── docs/
│   ├── REQUIREMENTS.md       # v1.0 需求
│   ├── ARCHITECTURE.md       # ← 本文档
│   ├── MONTHLY-WORKFLOW.md   # 月度操作手册
│   └── superpowers/{specs,plans}/
│
├── research-demos/           # GitHub 调研 demo + 分析
└── output/index.html         # 最终产物（git ignore）
```

### 4.3 数据契约

每个数据 sheet **7 列**：

| 列 | 含义 | 决定什么 |
|---|---|---|
| 分组 | 数据分类 | **决定 viz 类型**（1 行 → KPI，2-3 行 → donut，4+ 行 → bar） |
| 名称 | 显示名 | 图表/表格中显示 |
| 数值 | 主要数字 | 柱长、饼大小 |
| 单位 | 显示单位 | 数字后缀 |
| 备注 | 可选说明 | 鼠标悬停或表格列 |
| 排序 | 显示顺序 | 数字越小越靠前 |
| is_total | 是否总数行 | 用于 KPI+bar 组合展示 |

**约定**：
- 占比统一 0-1 浮点（`0.2586` = 25.86%）
- 缺失值 = 空 cell（**不写** "N/A" / "无" / "-"）
- 千分位统一 `,`（`5,901`）
- 时段字段从 `配置` sheet 读

### 4.4 自动 viz 选择策略

```
对每个分组的 records:
    if len(records) == 1:
        → KPI 卡（突出单一数字）
    elif len(records) in (2, 3) and 有 is_total 行:
        → Donut（组成关系，总数 = 各部分之和）
    elif len(records) >= 4:
        → Bar（分布对比）
    else:
        → Table（详细数据）
```

**Why**：用户不需要懂图表类型——只需保证数据按"分组"组织好就行。
简化心智负担 + 视觉一致性。

---

## 5. 决策记录（ADR）

每个 ADR 包含：**Status / Date / Context / Decision / Consequences**。

---

### ADR-001: 单 Excel 数据源（8 sheets）

- **Status**: Accepted
- **Date**: 2026-07-03（v1.1）→ 强化于 2026-07-04（v1.3）

**Context**：HR 每月维护一份数据。多种方案：
- (a) 6 个 Excel 文件（每个模块一个）
- (b) 1 个 Excel 多 sheet
- (c) 1 个 Excel 1 sheet（结构化）
- (d) 数据库 / 后端

**Decision**：采用 (b) ——**1 个 .xlsx / 8 sheets**：
1 个 `配置` sheet + 6 个模块 sheet + 1 个 `M-4 干部职数表`（多列结构）

**Consequences**：
- ✅ 用户只维护 1 个文件，备份/分发简单
- ✅ 8 sheets 总和可控在 ~200 行
- ❌ 大数据量（>1000 行/模块）会变慢——但 HR 月报场景不超此量
- ❌ 多人协作困难——但本项目是单人维护

**Alternatives Considered**：
- (a) 6 文件：HR 要管理 6 个文件，容易漏更新某模块 → 否决
- (d) 数据库：违反 C-2 / C-3（离线分发）→ 否决

---

### ADR-002: 7 列数据契约

- **Status**: Superseded by [ADR-011](#adr-011-9-列数据契约修订加-delta--sub_text--metric_note)（2026-07-04）
- **Date**: 2026-07-04（v1.3）

**Context**：v1.2 用复杂 mapping 配置（`data_key`、`alt_types`、`drillable`），用户难以维护。v1.3 转向"数据驱动"——让 Excel 结构本身决定渲染。

**Decision**：每个数据 sheet 用 **7 列固定结构**：`分组 / 名称 / 数值 / 单位 / 备注 / 排序 / is_total`

**Consequences**：
- ✅ 用户只需懂 7 个列名，无需懂 viz / data_key 等概念
- ✅ composer 可以 100% 自动选 viz（不需要人配）
- ❌ 7 列表达力有限——超复杂结构（多维交叉）需要预先 pivot
- ❌ 异构数据（不同 sheet 列数不同）不支持——但本项目 6 模块都是同构

---

### ADR-003: CSS 静态图表（v1.0 基础）+ ECharts 仅可选

- **Status**: Accepted
- **Date**: 2026-07-03（v1.1）

**Context**：图表方案选择——图表库通常功能强但体积大；纯 CSS 图表轻但表达力弱。

**Decision**：默认 **CSS 静态图表**（div + width %），ECharts **仅作可选升级路径**

**Consequences**：
- ✅ 体积可控（CSS 图表 ~5KB）
- ✅ 完全离线，0 依赖
- ❌ 无交互（hover/tooltip/缩放）
- ❌ 复杂图表（漏斗、桑基、地图）不支持——但本项目 6 模块用不到

**Alternatives Considered**：
- ECharts：~1MB，inline 或 CDN 都违反 C-1 / C-5 → 默认否决
- Chart.js：~200KB，仍偏大 → 否决
- D3.js：API 复杂，本项目无定制需求 → 否决

---

### ADR-004: 自研 CSS（继承 shanjinki 18 styles）

- **Status**: Accepted
- **Date**: 2026-07-03（v1.1）→ 强化于 2026-07-04（v1.3）

**Context**：样式方案——CSS 框架（Pico.css、Tailwind、Bulma）vs 自研。

**Decision**：**自研 CSS**——基础借鉴 shanjinki 18 styles，主题用 CSS variables（v1.3 强化）。

**Consequences**：
- ✅ 体积最小（~10KB）
- ✅ 完全控制视觉细节（银行专业风）
- ✅ 无框架升级负担
- ❌ 开发量更大——但一次性投入，复用多年
- ❌ 无社区组件库——但本项目 UI 简单，无需复杂组件

**Alternatives Considered**：
- Pico.css：风格 classless 不可定制 → 否决
- Tailwind：~3MB JIT（CDN 模式），违反 C-5 → 否决
- shadcn / Linear：作为**视觉参考**而非代码引入（见 §2.3 缺口）

---

### ADR-005: Python f-string（不用 Jinja2）

- **Status**: Accepted
- **Date**: 2026-07-03（v1.1）

**Context**：模板引擎选择——Jinja2（标准）vs f-string（Python 内置）。

**Decision**：**Python f-string**——`templates/base.py` 是 .py 文件，不是 .j2。

**Consequences**：
- ✅ 零依赖（Python 标准库）
- ✅ 模板里可以调函数、做循环
- ❌ HTML 转义需手动——但本项目所有数据都来自 Excel，无 XSS 风险
- ❌ 模板和逻辑耦合——但项目小，可控

**Alternatives Considered**：
- Jinja2：~500KB 依赖，HTML 转义更严格 → 收益不抵成本

---

### ADR-006: composer 自动选 viz（取代 viz registry 强制选择）

- **Status**: Accepted
- **Date**: 2026-07-04（v1.3）

**Context**：v1.2 有 8 个 viz 文件 + `VIZ_REGISTRY` + `mapping.py` 配 `type` 字段。问题：
- 用户要在 mapping.py 选 viz 类型——心智负担
- viz 类型选择不当导致视觉不一致（用户选 `bar` 表达组成关系）

**Decision**：v1.3 改为**完全自动**——`composer._pick_viz(group)` 按行数自动选：
- 1 行 → KPI
- 2-3 行 + is_total → donut
- 4+ 行 → bar
- 多列 → table

**Consequences**：
- ✅ 用户 0 心智负担（只需组织好数据）
- ✅ 视觉一致性 100% 保证
- ❌ 失去 viz 切换能力（v1.2 的 `alt_types` 取消）——但用户决策 YAGNI
- ❌ 特殊场景（如要漏斗）需要手动覆盖——但 6 模块用不到

**Alternatives Considered**：
- viz registry + alt_types（v1.2 方案）：灵活但复杂 → 否决
- 用户在 Excel 里指定 viz 类型：心智负担回到原点 → 否决

---

### ADR-007: 浅色专业风 + CSS variables + 4 级 tone

- **Status**: Superseded by [ADR-012](#adr-012-3-色风险等级编码修订)（2026-07-04）
- **Date**: 2026-07-04（v1.3）

**Context**：视觉风格——v1.2 试过 dark theme（GitHub Primer + Linear 风格），用户评价"不专业"。
v1.3 改用浅色专业风。

**Decision**：
- 主色：低饱和度蓝（`#1E5BAA`，银行稳重感）
- 4 级 tone：浅 → 深（用于 KPI 卡、bar 渐变、表格 hover）
- 12px 圆角（现代但不轻浮）
- CSS variables 主题（`--primary-50` ~ `--primary-900`）

**Consequences**：
- ✅ 符合银行/金融场景的"稳重"预期
- ✅ 打印友好（白底黑字）
- ❌ 不适合大屏演示（深色更好）——但本场景是月报分发，不是大屏

**Alternatives Considered**：
- dark theme：演示好看但打印/邮件不友好 → 否决
- 高饱和度色：年轻但不专业 → 否决

---

### ADR-008: 12-col grid + 3 断点（1100/768/480）

- **Status**: Accepted
- **Date**: 2026-07-04（v1.3）

**Context**：响应式布局方案——断点数量和栅格选择影响开发成本和视觉密度。

**Decision**：
- **12-col grid**（CSS Grid 实现）
- 3 个断点：1100px（桌面）/ 768px（平板）/ 480px（手机）
- 触屏按钮 ≥ 44×44px（Apple HIG）

**Consequences**：
- ✅ 桌面/平板/手机都有合适密度
- ✅ 12-col 灵活组合（3+3+3+3、6+6、4+8 等）
- ❌ 中间断点（768-1100）密度变化大——但 HR 报告场景多在桌面或手机看

**Alternatives Considered**：
- 2 断点（980/640）：缺少平板细分 → 否决
- 4 断点：开发成本翻倍，收益边际 → 否决

---

### ADR-009: 钻取交互 YAGNI（v1.2 Alpine.js 钻取在 v1.3 移除）

- **Status**: Accepted
- **Date**: 2026-07-04（v1.3）

**Context**：v1.2 实现了 Alpine.js 钻取（M-1 网点层级 / M-2 客户经理分类 / M-3 退出多维共 3 处）。
用户决策 v1.3 移除——HR 月报场景不需要下钻。

**Decision**：**不实现钻取**——所有数据平铺在 dashboard 上。

**Consequences**：
- ✅ 移除 Alpine.js（~15KB）→ 节省体积
- ✅ 实现更简单（无状态管理）
- ❌ 数据量大时 dashboard 会变长——但 6 模块共 ~188 行，可控

**Why YAGNI**：
- HR 月报读者主要看趋势/对比，不需要下钻到个体
- 真要下钻，浏览器搜索 + Ctrl+F 够用
- 钻取是 v1.2 的过度设计——v1.3 回归 Simplicity First

---

### ADR-010: 单文件部署（拒绝拆 SPA / 后端）

- **Status**: Accepted（重申 C-1）
- **Date**: 2026-07-03（v1.1）

**Context**：是否拆分（多文件 SPA / 后端 API / 静态资源 + 异步加载）。

**Decision**：**单文件**——所有 HTML / CSS / JS / JSON 都 inline 进 `output/index.html`。

**Consequences**：
- ✅ 极致可移植（邮件、U 盘、内网）
- ✅ 0 CORS 问题（file:// 可用）
- ❌ 体积上限 ~100KB（性能拐点）——当前 69KB 安全
- ❌ 不能用代码分割/懒加载——但本项目不需要

**Alternatives Considered**：
- 多文件 + fetch JSON：fetch 在 file:// 下 CORS 失败 → 否决
- CDN + 异步加载：违反 C-3 → 否决
- 后端 API：违反 C-2 → 否决

---

### ADR-011: 9 列数据契约（修订：加 delta + sub_text + metric_note）

- **Status**: Accepted
- **Date**: 2026-07-04（v1.4 候选，基于 S1 调研）

**Context**：v1.3 的 7 列契约（ADR-002）经过 S1 调研（3 深研 + 8 广扫描 + shadcn/Linear 笔记）发现 3 个核心缺口：

1. **缺 delta 字段** — 3 深研全部触发（深 #1 KPI 看图说话 / 深 #2 Velarasan KPI delta / 深 #3 Tableau RiskVue delta）+ 4/8 国内 BI 标配
2. **缺 sub_text 叙述字段** — 深 #1 shanjinki 30+ 字叙述 + 深 #3 Tableau RiskVue sub 注释
3. **缺 metric_note 字段** — 4/8 国内 BI（FineBI HR + 银行 + Smartbi + Superset）标配"KPI 下方 12-16 字看图说话"

**Decision**：在 ADR-002 的 7 列基础上扩展为 9 列：

| 列 | 含义 | 来源 |
|---|---|---|
| 分组 | 数据分类 | ADR-002 保留 |
| 名称 | 显示名 | ADR-002 保留 |
| 数值 | 主要数字 | ADR-002 保留 |
| 单位 | 显示单位 | ADR-002 保留 |
| 备注 | 可选说明 | ADR-002 保留 |
| 排序 | 显示顺序 | ADR-002 保留 |
| is_total | 是否总数行 | ADR-002 保留 |
| **delta**（新） | 同比 / 环比 / 绝对差，**composer 自动算**（不污染 Excel） | Q1+Q2 ✅ |
| **sub_text**（新） | 模块/分组级叙述（如"本月净增 50 人，主要来自校园招聘"），可选 | Q3 ✅ |
| **metric_note**（新） | KPI 卡下方 12-16 字"看图说话"，可选 | 广扫描触发 |

**delta 字段详细设计**（Q2 = b 自动算）：
- Excel 仍只放本期数据（不污染）
- composer 维护 `_prev` 历史快照 sheet（首次构建时创建 + 每月覆盖）
- delta 由 composer 按 is_total 行 + 当前 sheet vs `_prev` sheet 自动算
- 显示规则：
  - delta 非空 + is_total=True → KPI 卡右下角"vs 上月"绿（涨）/ 红（跌）文字
  - delta 非空 + is_total=False → bar 末端"vs 上月"徽章
  - delta 空 → 不显示（与 v1.3 一致）

**Consequences**：
- ✅ 用户只填本期数据（不污染 Excel），composer 自动算 delta
- ✅ KPI 卡"vs 上月"是行业最佳实践（深 #2 + 深 #3 + 4/8 广扫描验证）
- ✅ 叙述字段让 dashboard 更接近真实 .docx HR 月报（深 #1 + 深 #3 验证）
- ❌ 需要维护 `_prev` sheet → composer 多一点代码（v1.4 spec 内容）
- ❌ 9 列比 7 列多 28% → Excel 略宽，但可控

**Alternatives Considered**：
- 7 列不变：用户评价"不专业"根因之一是 KPI 没对比 → 否决
- delta 手动填：用户每月多填一列，违反"只改数值列"原则 → 否决

---

### ADR-012: 3 色风险等级编码（修订）

- **Status**: Accepted
- **Date**: 2026-07-04（v1.4 候选，基于 S1 调研）

**Context**：v1.3 的浅色专业风（ADR-007）只用了"主色 indigo + 4 级 tone"，缺**风险等级语义编码**。S1 调研发现：

- 深 #3 Tableau RiskVue：3 色风险（绿/橙/红）+ 5×5 热图
- 广扫描 FineBI 银行：深蓝 #0A1F3D + 金色 #D4AF37（5/5 银行感）→ v2.0 候选

但银行/政务场景实际是"完成率<80% 红色警示 / 80-100% 橙色 / ≥100% 绿色"，**3 色风险等级**是行业标配。

**Decision**：在 v1.3 的 `--primary` + 4 级 tone 基础上增加 3 色风险 token：

```css
--success:        #16A34A;  /* 绿，完成率 ≥ 100% */
--warning:        #D97706;  /* 橙，完成率 80-100% */
--danger:         #DC2626;  /* 红，完成率 < 80% */
--success-foreground: #FFFFFF;
--warning-foreground: #FFFFFF;
--danger-foreground:  #FFFFFF;
```

**v1.4 实施**：composer 识别"完成率"类数据时自动用对应风险色（无需用户配）。

**v2.0 候选**（不进 v1.4）：`bank-dark` style（深蓝 #0A1F3D + 金色 #D4AF37），用户后续可选启用。

**Consequences**：
- ✅ 完成率类数据自动有"绿/橙/红"语义（领导视角一目了然）
- ✅ 与 ADR-007 的浅色基调不冲突（3 色作为 accent，主色不变）
- ✅ 符合深 #3 Tableau RiskVue + FineBI 银行实践
- ❌ 多 3 个 CSS variable → 体积 +200B，可忽略

**Alternatives Considered**：
- 只用文字"达标/未达标"：领导视角不直观 → 否决
- 用 emoji 图标（✅⚠️❌）：违反"专业"基调 → 否决

---

## 6. 经验教训

### 6.1 v1.2 为什么被否（即使"做完了"）

**表层原因**：用户评价"不专业、单调"。
**深层原因**：
1. **过度工程化**：8 viz registry + mapping 配置 = 用户要懂 viz 类型 + data_key + alt_types + drillable
2. **样式贫乏**：抄了 shadcn/Linear 皮毛（dark + 12-col），没有真正理解设计系统
3. **表达力不足**：bar/pie 都用来表达"总数 vs 部分"，但用户视觉上分不清

**v1.3 的纠偏**：
- 移除 viz 选择（ADR-006）
- 浅色专业风（ADR-007）
- donut 表达组成、bar 表达分布（ADR-006 + §4.4）

### 6.2 不要从零搭——但 fork 后也要真正学

v1.1 fork shanjinki 时，**CSS 借鉴 + 架构借鉴**，但**没学其视觉系统的设计哲学**。
v1.2 抄了 dark theme 没用对场景（HR 月报不是大屏）。
v1.3 才真正理解"专业风 = 浅色 + 4-tone + 留白"。

**教训**：fork 不等于理解，必须做视觉对比 + 用户反馈验证。

### 6.3 "通过" ≠ "全速前进"

需求文档 v1.0 评审"通过"——但用户实际还没决定选型。
CLAUDE.md §5 强调：列假设、列选项，让用户选。
**教训**：评审通过某文档 ≠ 用户对所有细节都满意。每个新阶段都要再确认。

### 6.4 调研要形成文档（不只是 HTML demo）

v1.1 调研 shanjinki / Sven-Bo 形成了 `research-demos/README.md`——13 条详细观察 + 对比表。
v1.2 调研 shadcn / Linear **只留在会话记忆里**——现在回看缺乏材料。

**教训**：每次调研必须产出 markdown 笔记，否则过几天就忘。**已记为下一步补充项**。

---

## 7. 已知缺口（待补充）

| 缺口 | 影响 | 优先级 |
|---|---|---|
| **shadcn / Linear 调研详细记录**（仅在会话日志里提了一句） | v1.3 视觉决策难以回溯 | 🔴 高 |
| v1.0 → v1.1 调研时的具体搜索关键词 | 未来调研时无参考 | 🟡 中 |
| 性能基准测试（构建时间、加载时间、内存峰值） | 回归时无基线 | 🟡 中 |
| viz 函数逐个 ADR（当前只 ADR-006 整体讲了自动选择） | 未来调单个 viz 时无独立决策记录 | 🟢 低 |
| 6 模块各自的"业务定义"（什么算客户经理、什么算腾笼换鸟） | 数据契约演化时无参考 | 🟢 低 |

### 7.1 后续维护建议

- **添加新 ADR**：在 §5 末尾追加 `### ADR-NNN: ...`，不要修改历史 ADR
- **旧决策变更**：不要修改原 ADR，加 "Superseded by ADR-NNN" 标记
- **新调研**：在 `research-demos/` 下加 `README-项目名.md` + 实物 demo
- **新约束**：如发现 C-1~C-5 不够用，先讨论再追加为 C-6 / C-7

---

## 8. 参考资料

| 文档 | 路径 | 说明 |
|---|---|---|
| 需求 v1.0 | `docs/REQUIREMENTS.md` | 初始需求 + 8 个决策点 |
| 设计 spec v1.3 | `docs/superpowers/specs/2026-07-04-hr-dataui-v1.3-design.md` | 当前 spec |
| 实施计划 v1.3 | `docs/superpowers/plans/2026-07-04-hr-dataui-v1.3.md` | 当前 plan |
| 月度工作流 | `docs/MONTHLY-WORKFLOW.md` | HR 操作手册 |
| 项目指引 | `CLAUDE.md` | 行为准则 + Anti-Patterns |
| 调研 demo | `research-demos/README.md` | 4 个 GitHub 项目的实物对比 |
| 项目记忆 | `memory/project-overview.md` | 当前状态摘要 |
| 技术决策记忆 | `memory/tech-decisions.md` | 8 个决策的快速索引 |

---

## 变更日志

| 日期 | 变更 | 作者 |
|---|---|---|
| 2026-07-04 | 初始版本，包含 v1.3 全部 ADR | Claude + 用户协作 |
| 2026-07-04 | S1 调研完成：3 深研 + 8 广扫描 + shadcn/Linear → 新增 ADR-011（9 列契约）+ ADR-012（3 色风险等级）；ADR-002 / ADR-007 加 Superseded 标记 | Claude + 用户确认 |
