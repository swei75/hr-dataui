# hr-dataui

> **银行 HR 月度管理驾驶舱** · 单文件 HTML 仪表盘 · 0 外部依赖 · 完全离线
> **当前版本：v1.5**（2026-07-04）— 每模块独立 viz 风格 · 米色红棕主色 · 100% 覆盖范例 .docx

---

## 一句话总结

维护 1 个 Excel（9 sheets）→ 跑 `python build.py` → 生成 **98KB** 的单文件 HTML。
接收方**双击即用**，可邮件、U 盘、内网分发，无任何依赖。

---

## 1. 设计背景

### 1.1 业务场景

银行 HR 每月生成一份管理驾驶舱报告，分发给领导、HR 业务部门，并作为历史档案留存。

| 环节 | 角色 | 操作 |
|---|---|---|
| 数据录入 | HR 月报制作人 | 从 .docx 转 Excel，维护 9 个 sheet |
| 构建 | 同上 | `python build.py` 生成 HTML |
| 分发 | 同上 | 邮件 / U 盘 / 内网 |
| 阅读 | 报告接收方 | 双击 HTML 浏览 6 大模块 + Dashboard 顶部数字塔 |

### 1.2 6 大业务模块 + 独立 viz 风格（v1.5 革新）

| # | 模块 | 关键数据点 | v1.5 风格 |
|---|---|---|---|
| M-1 | 组织架构 | 28/2/24/183 网点分布 | **v1**：6 KPI 卡 + 段落叙述 |
| M-2 | 员工情况 | 5901 员工多维构成 | **v11**：4 KPI + 5 stacked + 8 grid |
| M-3 | 人员优化 | 引进 / 退出 / 腾笼换鸟 | **v_hr 融合**：gauge + flow + dual-bar + 3 排名 |
| M-4 | 干部队伍 | 211 总职 / 194 配 / 17 空 | **v2 分类树**：4 大类 + 中层分支 |
| M-5 | 考核薪酬 | 工资总额 / 年金 | **v1**：5 财务大卡 + sparkline |
| M-6 | 培训赋能 | 培训场次 / 完成率 | **v_train**：v1 顶 + v8 主体 |
| Dashboard 顶 | 顶部数字塔 | 6 项关键指标 | **v_hero**：横向 icon + 6 色左侧 border |

### 1.3 设计哲学

- **Excel = Source of Truth** — 每月只改 Excel "数值"列，其他 9 列不动
- **每模块独立 viz 风格**（v1.5 革新）— 不同模块用不同 viz 函数，表达力最大化
- **Simplicity First** — 禁止 speculative features；禁止未要求的灵活性配置
- **不要从零搭** — 基于 GitHub fork（shanjinki/excel-to-html-slides）改造

### 1.4 决策历程（v1.0 → v1.5）

| 版本 | 日期 | 关键变更 | 评价 |
|---|---|---|---|
| v1.0 | 弃用 | ECharts + Pico.css + Jinja2 + Alpine.js 重型方案 | 体积大、依赖多 |
| v1.1 | 2026-07-03 | GitHub 调研 → fork shanjinki；CSS 静态图表；自研 CSS | 选型定型 |
| v1.2 | 2026-07-03 | mapping 配置 + 8 viz + Alpine.js 钻取（43KB） | 用户："不专业" |
| v1.3 | 2026-07-04 | Excel SOT + 分组驱动 + 自动 viz + 浅色专业风 | 改进 |
| v1.4 | 2026-07-04 | 9 列契约 + 3 色风险等级 + 5 项规格 + 调研完成 | 调研 + 数据增强 |
| **v1.5** | **2026-07-04** | **每模块独立 viz 风格 + 米色红棕主色 + Dashboard v_hero 顶 + 补 M-3 任务完成量 Top 3** | **当前** |

调研记录见 [research-demos/README.md](research-demos/README.md)。

---

## 2. 基本要求

### 2.1 功能要求

| # | 要求 | 说明 |
|---|---|---|
| F-1 | 读 1 个 .xlsx | 9 sheets（1 配置 + 6 模块 + 1 多列表 + 1 _prev 快照） |
| F-2 | 每模块独立 viz | M-1~M-6 + Dashboard 顶部各自专属风格（详见 §1.2） |
| F-3 | 6 模块全显示 | 按 mapping 配置组装 |
| F-4 | 单文件输出 | 0 外部依赖，`file://` 协议双击即开 |
| F-5 | 中文优先 | 表头、UI、报告期、机构名均中文 |
| F-6 | 100% 覆盖 .docx 范例 | 77/77 关键数据点 |

### 2.2 非功能要求

| # | 指标 | 目标 | 当前 |
|---|---|---|---|
| N-1 | 文件大小 | ≤ 50KB 目标 / ≤ 100KB 上限 | **98KB** |
| N-2 | 外部依赖 | 0（无 CDN、无 fetch） | ✅ |
| N-3 | 加载时间 | < 1s（`file://`） | ✅ |
| N-4 | 浏览器 | Chrome 80+ / Edge / Firefox 70+ / Safari 13+ | ✅ |
| N-5 | 移动端 | iOS Safari / Android Chrome / 微信内置 | ✅ |
| N-6 | 响应式断点 | 1100 / 768 / 480 | ✅ |
| N-7 | E2E 测试 | 全绿 | ✅ 10/10 passed |

### 2.3 v1.5 视觉系统

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

---

## 3. 数据契约（v1.5：10 列）

每个数据 sheet **10 列结构**：

| # | 列 | 含义 | 示例 |
|---|---|---|---|
| 1 | 分组 | 数据分类（决定 viz） | 客户经理 / 学历 |
| 2 | 名称 | 显示名 | 对公客户经理 |
| 3 | 数值 | 主要数字 | 870 |
| 4 | 单位 | 显示单位 | 人 |
| 5 | 备注 | 可选说明 | |
| 6 | 排序 | 显示顺序 | 2 |
| 7 | is_total | 是否总数行（用于 KPI+bar 组合） | TRUE |
| 8 | delta | 环比绝对差（自动） | 20 |
| 9 | sub_text | 模块级叙述（关键洞察） | 全行共 28 个一级部门 |
| 10 | metric_note | KPI 卡底部说明 | 较上月增加 12 人 |

**约定**：
- 占比统一 0-1 浮点（`0.2586` = 25.86%）
- 缺失值 = 空 cell（**不写** "N/A" / "无" / "-"）
- 千分位统一 `,`（`5,901`）
- 时段字段从 `配置` sheet 读，不写死

---

## 4. 使用用法

### 4.1 环境准备

```bash
cd hr-dataui
pip install -r requirements.txt   # pandas + openpyxl
```

### 4.2 目录速查

```
hr-dataui/
├── build.py                       # 入口：python build.py
├── requirements.txt               # pandas + openpyxl
├── README.md                      # ← 本文档
├── CLAUDE.md                      # 项目指引 + 选型 + Anti-Patterns
│
├── data/                          # Excel 数据源（1 个 .xlsx, 9 sheets）
│   └── *.xlsx                     # 配置 + 6 模块 + 多列 + _prev
│
├── extractors/
│   ├── reader.py                  #   读 Excel → dict
│   ├── mapping.py                 #   sheet→模块 + viz 风格 + 字段映射
│   └── drills.py                  #   钻取数据加载（备用）
│
├── viz/                           # viz 函数（每模块独立风格）
│   ├── v1.py v2.py v8.py v11.py
│   ├── v_hr.py v_train.py v_hero.py
│   └── ...                        # 7+ viz 函数
│
├── composer.py                    # 按 mapping + is_v_*_style 分支组合 6 模块 HTML
├── templates/base.py              # f-string 模板 + CSS（含 v1.5 视觉系统）
│
├── tests/
│   ├── _make_test_xlsx.py         #   生成测试 Excel
│   └── test_build_e2e.py          #   10 个 E2E 用例
│
├── docs/
│   ├── REQUIREMENTS.md            # v1.5 需求
│   ├── ARCHITECTURE.md            # v1.5 架构 + ADR
│   ├── MONTHLY-WORKFLOW.md        # 月度更新流程
│   └── superpowers/{specs,plans}/
│
├── research-demos/                # v1.4 调研 demo + 笔记
└── output/
    └── index.html                 #   98KB 单文件（git ignore）
```

### 4.3 快速上手

```bash
# 1. 编辑 data/*.xlsx（只改"数值"列）
# 2. 构建
python build.py
# 3. 验证
open output/index.html
```

**完整月度流程**（HR 操作手册）→ [docs/MONTHLY-WORKFLOW.md](docs/MONTHLY-WORKFLOW.md)

### 4.4 扩展指南

#### 添加新 viz 函数

1. 在 `viz/` 创建 `xxx.py`（如 `v_new.py`），函数签名：
   ```python
   def render(data: list, options: dict) -> str:
       """返回 HTML 片段"""
   ```
2. 在 `extractors/mapping.py` 的目标模块加 `"viz": "v_new"` 或 `"is_v_new_style": True`
3. 在 `composer.py` 的风格分支添加调用
4. 在 `templates/base.py` 添加对应 CSS

#### 添加新模块

1. 在 `data/*.xlsx` 添加新 sheet
2. 在 `extractors/mapping.py` 的 `MODULES` 加配置（参考 M-1~M-6）
3. `python build.py`

---

## 5. v1.5 模块 viz 实施位置（速查）

| 模块 | viz 风格 | composer 风格分支 | viz 函数 |
|---|---|---|---|
| Dashboard 顶 | v_hero | `is_v_hero_style` | `viz/v_hero.py` |
| M-1 组织架构 | v1 | `is_v1_style` | `viz/v1.py` |
| M-2 员工情况 | v11 | `is_v11_style` | `viz/v11.py` |
| M-3 人员优化 | v_hr 融合 | `is_v_hr_style` | `viz/v_hr.py` |
| M-4 干部队伍 | v2 分类树 | `is_v2_style` | `viz/v2.py` |
| M-5 考核薪酬 | v1 财务大卡 | `is_v1_style`（同 M-1） | `viz/v1.py` |
| M-6 培训赋能 | v_train | `is_v_train_style` | `viz/v_train.py` |

---

## 6. 项目成果

### 6.1 v1.5 已交付

- ✅ 6 模块 + Dashboard 顶部数字塔（7 套独立 viz 风格）
- ✅ Excel source of truth（10 sheets：配置 + 6 模块 + 多列 + _prev）
- ✅ 100% 覆盖 .docx 范例 77/77 关键数据点（含 v1.5.20 补 M-3 任务完成量 Top 3）
- ✅ 5 项规格（spec 阶段设计改进）
- ✅ E2E 测试 10/10 passed
- ✅ 月度更新工作流文档化

### 6.2 v1.5 关键决策

详见 [docs/ARCHITECTURE.md §5 ADR](docs/ARCHITECTURE.md)。

### 6.3 已弃用方案（**不要回退**）

| ❌ 弃用 | 原因 |
|---|---|
| 单一 viz 风格（v1.3 统一默认） | v1.5 每模块独立 viz，表达力更强 |
| Alpine.js 钻取 | YAGNI，月度报告无需下钻 |
| ECharts / Pico.css / Jinja2 | 调研后体积/依赖过大（见 research-demos） |
| 引入 React / Vue / Tailwind | 违反轻量约束（详见 CLAUDE.md §6） |
| 做后端 / API / 用户登录 | 单文件离线部署 |
| 拆 SPA 多文件包 | 一个 HTML 解决 |

### 6.4 待办（v2.0 候选）

- ⏸ SVG sparkline（每个 KPI 卡 mini trend）
- ⏸ `bank-dark` 深蓝金色 style
- ⏸ OKLCH 迁移

---

## 7. 重新启动会话时（快速 checklist）

按此顺序 5 分钟内进入工作状态：

1. 读这个 README（3 分钟）
2. 读 [CLAUDE.md](CLAUDE.md) §1-3（架构 + 选型 + Anti-Patterns）
3. 跑 `python build.py` 确认能跑通
4. 检查 [项目记忆](memory/)

---

## 8. 参考资料

| 文档 | 用途 |
|---|---|
| [CLAUDE.md](CLAUDE.md) | 项目指引 + 行为准则 + Anti-Patterns |
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | v1.5 需求 |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | v1.5 架构 + ADR |
| [docs/MONTHLY-WORKFLOW.md](docs/MONTHLY-WORKFLOW.md) | 月度更新操作手册 |
| [docs/superpowers/specs/2026-07-04-hr-dataui-v1.4-design.md](docs/superpowers/specs/2026-07-04-hr-dataui-v1.4-design.md) | v1.4 设计 spec（含 v1.5 演进说明） |
| [docs/superpowers/plans/2026-07-04-hr-dataui-v1.4.md](docs/superpowers/plans/2026-07-04-hr-dataui-v1.4.md) | v1.4 实施计划 |
| [research-demos/README.md](research-demos/README.md) | 调研记录 |
| [memory/project-overview.md](memory/project-overview.md) | 项目记忆 |