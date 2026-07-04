# hr-dataui

> **银行 HR 月度管理驾驶舱** · 单文件 HTML 仪表盘 · 0 外部依赖 · 完全离线

---

## 一句话总结

维护 1 个 Excel（8 sheets）→ 跑 `python build.py` → 生成 ~69KB 的单文件 HTML。
接收方**双击即用**，可邮件、U 盘、内网分发，无任何依赖。

---

## 1. 设计背景

### 1.1 业务场景

银行 HR 每月生成一份管理驾驶舱报告，分发给领导、HR 业务部门，并作为历史档案留存。

| 环节 | 角色 | 操作 |
|---|---|---|
| 数据录入 | HR 月报制作人 | 从 .docx 转 Excel，维护 8 个 sheet |
| 构建 | 同上 | `python build.py` 生成 HTML |
| 分发 | 同上 | 邮件 / U 盘 / 内网 |
| 阅读 | 报告接收方 | 双击 HTML 浏览 6 大模块 |

### 1.2 6 大业务模块

| # | 模块 | 关键数据点 |
|---|---|---|
| M-1 | 组织架构 | 28/2/24/183 网点分布 |
| M-2 | 员工情况 | 5901 员工多维构成（年龄/学历/客户经理…） |
| M-3 | 人员优化 | 引进 / 退出 / 腾笼换鸟 |
| M-4 | 干部队伍 | 211 总职 / 194 配 / 17 空（含职数表） |
| M-5 | 考核薪酬 | 工资总额 / 年金 |
| M-6 | 培训赋能 | 培训场次 / 完成率 |

### 1.3 设计哲学

- **Excel = Source of Truth** — 每月只改 Excel "数值"列，其他 6 列不动
- **分组驱动 + 自动选 viz** — 用户不指定图表类型，composer 按"分组"行数自动选
- **Simplicity First** — 禁止 speculative features；禁止未要求的灵活性配置
- **不要从零搭** — 基于 GitHub fork（shanjinki/excel-to-html-slides）改造

### 1.4 决策历程（v1.0 → v1.3）

| 版本 | 日期 | 关键变更 | 评价 |
|---|---|---|---|
| v1.0 | 弃用 | ECharts + Pico.css + Jinja2 + Alpine.js 重型方案 | 体积大、依赖多 |
| v1.1 | 2026-07-03 | GitHub 调研 → fork shanjinki；CSS 静态图表；自研 CSS | 选型定型 |
| v1.2 | 2026-07-03 | mapping 配置 + 8 viz + Alpine.js 钻取（43KB） | 用户："不专业" |
| **v1.3** | **2026-07-04** | **Excel SOT + 分组驱动 + 自动 viz + 浅色专业风** | **当前** |

调研记录见 [research-demos/README.md](research-demos/README.md)。

---

## 2. 基本要求

### 2.1 功能要求

| # | 要求 | 说明 |
|---|---|---|
| F-1 | 读 1 个 .xlsx | 8 sheets（1 配置 + 6 模块 + 1 多列表） |
| F-2 | 自动 viz 选择 | 1 行 → KPI / 2-3 行 → donut / 4+ 行 → bar / 多列 → table |
| F-3 | 6 模块全显示 | 按 mapping 配置组装 |
| F-4 | 单文件输出 | 0 外部依赖，`file://` 协议双击即开 |
| F-5 | 中文优先 | 表头、UI、报告期、机构名均中文 |

### 2.2 非功能要求

| # | 指标 | 目标 | 当前 |
|---|---|---|---|
| N-1 | 文件大小 | ≤ 50KB 目标 | **69K**（超目标但可接受） |
| N-2 | 外部依赖 | 0（无 CDN、无 fetch） | ✅ |
| N-3 | 加载时间 | < 1s（`file://`） | ✅ |
| N-4 | 浏览器 | Chrome 80+ / Edge / Firefox 70+ / Safari 13+ | ✅ |
| N-5 | 移动端 | iOS Safari / Android Chrome / 微信内置 | ✅ |
| N-6 | 响应式断点 | 1100 / 768 / 480 | ✅ |
| N-7 | E2E 测试 | 全绿 | ✅ 6/6 passed |

### 2.3 数据契约

每个数据 sheet **7 列结构**：

| 列 | 含义 | 示例 |
|---|---|---|
| 分组 | 数据分类（决定 viz） | 客户经理 / 学历 |
| 名称 | 显示名 | 对公客户经理 |
| 数值 | 主要数字 | 870 |
| 单位 | 显示单位 | 人 |
| 备注 | 可选说明 | |
| 排序 | 显示顺序 | 2 |
| is_total | 是否总数行（用于 KPI+bar 组合） | TRUE |

**v1.4 新增列（10 列总）**：

| 列 | 用途 | 示例 |
|---|---|---|
| delta | 环比绝对差（自动） | 20 |
| sub_text | 模块级叙述（关键洞察） | 全行共 28 个一级部门 |
| metric_note | KPI 卡底部说明 | 较上月增加 12 人 |

**约定**：
- 占比统一 0-1 浮点（`0.2586` = 25.86%）
- 缺失值 = 空 cell（**不写** "N/A" / "无" / "-"）
- 千分位统一 `,`（`5,901`）
- 时段字段从 `配置` sheet 读，不写死

---

## 3. 使用用法

### 3.1 环境准备

```bash
cd hr-dataui
pip install -r requirements.txt   # pandas + openpyxl
```

### 3.2 目录速查

```
hr-dataui/
├── build.py                       # 入口：python build.py
├── requirements.txt               # pandas + openpyxl
├── README.md                      # ← 本文档
├── CLAUDE.md                      # 项目指引 + 选型 + Anti-Patterns
│
├── data/                          # Excel 数据源（1 个 .xlsx, 8 sheets）
│   └── test.xlsx                  # 8-sheet source of truth
│
├── extractors/                    # 数据读取 + 字段映射
│   ├── reader.py                  #   read_workbook() 读 Excel → dict
│   ├── mapping.py                 #   sheet→键名 + viz 类型 + 配置
│   └── drills.py                  #   钻取数据加载（备用）
│
├── viz/                           # 8 个 viz 函数（composer 自动选）
│   ├── kpi.py / bar.py / pie.py / funnel.py
│   └── progress.py / ranking.py / hierarchy.py / table.py
│
├── composer.py                    # 按 mapping 组合 6 模块 HTML
├── templates/base.py              # f-string 模板 + CSS
│
├── tests/                         # E2E 测试
│   ├── _make_test_xlsx.py         #   生成测试 Excel
│   └── test_build_e2e.py          #   6 个 E2E 用例
│
├── docs/
│   ├── REQUIREMENTS.md            # v1.0 需求
│   ├── MONTHLY-WORKFLOW.md        # 月度更新流程（HR 操作手册）
│   └── superpowers/{specs,plans}/ # 设计 spec + 实施计划
│
├── research-demos/                # v1.1 GitHub 调研 demo
└── output/                        # 最终产物
    └── index.html                 #   ~69KB 单文件（git ignore）
```

### 3.3 快速上手

```bash
# 1. 编辑 data/人力资源管理数据驾驶舱_YYYY年M月.xlsx（改"数值"列）
# 2. 构建
python build.py
# 3. 验证
open output/index.html
```

**完整月度流程**（HR 操作手册）→ [docs/MONTHLY-WORKFLOW.md](docs/MONTHLY-WORKFLOW.md)

### 3.4 扩展指南

#### 添加新 viz 类型

1. 在 `viz/` 创建 `xxx.py`，函数签名：
   ```python
   def render(data: list, options: dict) -> str:
       """返回 HTML 片段"""
   ```
2. 在 `viz/__init__.py` 的 `VIZ_REGISTRY` 注册
3. 在 `composer.py` 的 `_pick_viz()` 添加选择逻辑
4. 在 `templates/base.py` 添加对应 CSS

#### 添加新模块

1. 在 `data/*.xlsx` 添加新 sheet
2. 在 `extractors/mapping.py` 的 `MODULES` 加配置：
   ```python
   "M-7 新模块": {
       "title": "七、新模块",
       "icon": "🆕",
       "order": 7,
       "sub": "描述",
       "groups": [{"name": "分组1", "span": 6}, ...],
   }
   ```
3. `python build.py`

---

## 4. 项目成果

### 4.1 v1.3 已交付

- ✅ 6 模块 dashboard 跑通
- ✅ Excel source of truth（8 sheets，188 行）
- ✅ 自动 viz 选择（KPI / donut / bar / table）
- ✅ E2E 测试 6/6 passed
- ✅ M-4 干部职数表 bug 修复
- ✅ 月度更新工作流文档化

### 4.2 8 个技术决策（v1.3）

| # | 决策 | 选定方案 |
|---|---|---|
| D-1 | 数据源 | 1 个 .xlsx / 8 sheets |
| D-2 | 数据契约 | 7 列结构 |
| D-3 | 渲染逻辑 | composer 按"分组"结构自动选 viz |
| D-4 | viz 自动选择 | KPI(1行) / donut(2-3行组成) / bar(4+行分布) / table(多列) |
| D-5 | 视觉 | 浅色专业风 + CSS variables + 4 级 tone + 12px 圆角 |
| D-6 | 布局 | 12-col grid，3 断点（1100/768/480） |
| D-7 | 主题栈 | shanjinki fork + Python f-string |
| D-8 | 输出 | 单文件 HTML, 0 外部 CDN |

**Why**：这些决策经过 3 轮迭代验证。核心约束（单文件、离线、轻量）从未变。
**改它需要理由**（详见 [CLAUDE.md §4](CLAUDE.md)），不是反过来。

### 4.3 已弃用方案（**不要回退**）

| ❌ 弃用 | 原因 |
|---|---|
| viz registry（8 个独立 viz 文件强制使用） | v1.3 用 composer 自动选 viz，无需手动注册 |
| mapping data_key 字段映射 | v1.3 直接用 sheet 结构驱动 |
| Alpine.js 钻取 | YAGNI，月度报告无需下钻 |
| dark theme | 用户要求换浅色专业风 |
| ECharts / Pico.css / Jinja2 | 调研后体积/依赖过大（见 research-demos） |
| 引入 React / Vue / Tailwind | 违反轻量约束（详见 CLAUDE.md §6） |
| 做后端 / API / 用户登录 | 单文件离线部署 |
| 拆 SPA 多文件包 | 一个 HTML 解决 |

### 4.4 待办（已延后）

- ⏸ 视觉优化（CSS 间距、字体微调）
- ⏸ 真实 6 月数据测试（用真实 .docx 转的数据）
- ⏸ 钻取交互（v1.2 有 Alpine.js 设计稿）

---

## 5. 重新启动会话时（快速 checklist）

按此顺序 5 分钟内进入工作状态：

1. 读这个 README（3 分钟）
2. 读 [CLAUDE.md](CLAUDE.md) §1-3（架构 + 选型 + Anti-Patterns）
3. 看 [docs/superpowers/specs/2026-07-04-hr-dataui-v1.3-design.md](docs/superpowers/specs/2026-07-04-hr-dataui-v1.3-design.md)
4. 跑 `python build.py` 确认能跑通
5. 检查 [项目记忆](memory/)（project-overview / tech-decisions / research-status / user-style）

---

## 6. 参考资料

| 文档 | 用途 |
|---|---|
| [CLAUDE.md](CLAUDE.md) | 项目指引 + 行为准则 + Anti-Patterns |
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | v1.0 需求文档 |
| [docs/MONTHLY-WORKFLOW.md](docs/MONTHLY-WORKFLOW.md) | 月度更新操作手册 |
| [docs/superpowers/specs/2026-07-04-hr-dataui-v1.3-design.md](docs/superpowers/specs/2026-07-04-hr-dataui-v1.3-design.md) | v1.3 设计 spec |
| [docs/superpowers/plans/2026-07-04-hr-dataui-v1.3.md](docs/superpowers/plans/2026-07-04-hr-dataui-v1.3.md) | v1.3 实施计划 |
| [research-demos/README.md](research-demos/README.md) | v1.1 GitHub 调研记录 |
| [memory/project-overview.md](memory/project-overview.md) | 项目记忆：当前状态 |
| [memory/tech-decisions.md](memory/tech-decisions.md) | 项目记忆：技术决策 |
