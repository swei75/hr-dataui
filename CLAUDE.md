# CLAUDE.md — hr-dataui 项目指引

> **需求文档**：[docs/REQUIREMENTS.md](docs/REQUIREMENTS.md)（v1.5，2026-07-04）
> **行为准则**：参考 `andrej-karpathy-skills:karpathy-guidelines`（强制）

---

## 1. 项目一句话

读 Excel → 生成单文件 HTML 仪表盘（**v1.5：每模块独立 viz 风格**）。**任何方案讨论、代码改动前，先回顾 §4 技术选型与 §6 Anti-Patterns。**

**技术栈**：Python 3.10+ (pandas + openpyxl) + f-string 模板 + CSS 静态图表 + 自研 CSS（参考 shanjinki）

---

## 2. 核心命令

```bash
pip install -r requirements.txt    # 安装依赖
python build.py                    # 构建 → output/index.html (~98KB)
```

**输出 = 单文件 `output/index.html`**，目标 ≤ 50KB（实际 98KB，可接受），0 外部依赖，完全离线，双击即用，可邮件/U 盘/内网分发。

---

## 3. 目录速查

| 路径 | 用途 |
|---|---|
| `data/*.xlsx` | Excel 数据源（1 文件 9 sheet） |
| `extractors/` | 数据读取 + 字段映射 + 钻取 |
| `extractors/reader.py` | `read_workbook()` 读 Excel → dict |
| `extractors/mapping.py` | sheet→键名 + viz 风格 + 字段映射 |
| `extractors/drills.py` | 钻取数据加载 |
| `viz/` | viz 函数（v1.5：每模块独立风格） |
| `viz/v_hero.py` | Dashboard 顶部数字塔 |
| `viz/v1.py` | M-1 组织架构 / M-5 考核薪酬 财务大卡 |
| `viz/v2.py` | M-4 干部队伍 分类树 |
| `viz/v8.py` | M-6 培训赋能 主体 |
| `viz/v11.py` | M-2 员工情况 |
| `viz/v_hr.py` | M-3 人员优化 融合（gauge + flow + dual-bar） |
| `viz/v_train.py` | M-6 培训赋能 复合 |
| `composer.py` | 按 mapping + `is_v_*_style` 分支组合 7 模块 HTML |
| `templates/` | Python f-string 模板函数 |
| `output/index.html` | 最终产物 ~98KB（git ignore） |
| `tests/` | pytest 测试 |
| `docs/REQUIREMENTS.md` | v1.5 需求 |
| `docs/ARCHITECTURE.md` | v1.5 架构 + ADR |
| `docs/MONTHLY-WORKFLOW.md` | 月度操作手册 |
| `research-demos/` | v1.4 调研 demo |

---

## 4. 技术选型（不许改，§7 例外）

**v1.5 选型（2026-07-04）**：

| 层 | 选型 | 体积 | 关键原因 |
|---|---|---|---|
| 数据 | pandas + openpyxl | - | Excel 标准 |
| 模板 | Python f-string（不引入 Jinja2） | - | 减少依赖 |
| 前端 | Vanilla JS（不引入 Alpine.js） | - | 单文件最简 |
| 图表 | CSS 静态图表（每模块独立风格） | ~7KB | 参考 shanjinki，v1.5 升级为多 viz |
| 样式 | 自研 CSS（继承 shanjinki 18 styles） | ~12KB | 不引入 Pico.css |
| 部署 | 单文件 HTML | 98KB | 极致可移植 |
| 参考项目 | fork shanjinki/excel-to-html-slides | - | MIT 协议 |

> 任何"要不要换 X 框架"的冲动，先看这一节。**默认选型经过评审，改它需要理由，不是反过来。**

> **历史选型**（v1.0 已弃用）：ECharts 5 / Pico.css 2 / Jinja2 / Alpine.js。调研后改选更轻量方案。

---

## 5. v1.5 视觉系统

| 维度 | 值 |
|---|---|
| 主色 | `#9f6b44` 米色红棕 |
| 深主色 | `#6b4423` |
| 警告 | `#a04030` |
| 成功 | `#4a7c59` |
| body font-size | **16px** |
| hero | **3.4em** |
| module-title | **2em** |
| kpi-card | **2.4em** |

#### 5.1 v1.5.21 局部补丁（顶部 hero 区广银化）

- 顶部 Dashboard `hero` 与 KPI 数字塔区采用 **广银通报风格**（红+金）
- 新增 6 个 **hero-only token**（不污染 `--primary` 主调色板）：
  - `--hero-red #c8102e` / `--hero-red-deep #a40e25` / `--hero-gold #f5b500` / `--hero-gold-soft #fff3cd` / `--hero-text-on-red #fff` / `--hero-bg-warm #fff8e6`
- **不影响**：`--primary` 系（`#9f6b44` 等）+ 6 模块（M-1~M-6）所有 CSS 不变
- 文档：见 `docs/REQUIREMENTS.md` §3.6；详情 memory `hero-gzbank-style-v1.5.21`
- 回滚：`cp backup/pre-gzbank-2026-07-05/base.py templates/base.py && python build.py`

---

## 6. v1.5 模块 viz 实施位置（必查）

| 模块 | 风格 | composer 风格分支 | viz 文件 |
|---|---|---|---|
| Dashboard 顶部 | v_hero 数字塔 | `is_v_hero_style` | `viz/v_hero.py` |
| M-1 组织架构 | v1（6 KPI + 段落） | `is_v1_style` | `viz/v1.py` |
| M-2 员工情况 | v11（4 KPI + 5 stacked + 8 grid） | `is_v11_style` | `viz/v11.py` |
| M-3 人员优化 | v_hr 融合 | `is_v_hr_style` | `viz/v_hr.py` |
| M-4 干部队伍 | v2 分类树（4 大类 + 中层） | `is_v2_style` | `viz/v2.py` |
| M-5 考核薪酬 | v1 财务大卡（5 卡 + sparkline） | `is_v1_style` | `viz/v1.py` |
| M-6 培训赋能 | v_train（v1 顶 + v8 主体） | `is_v_train_style` | `viz/v_train.py` |

**实施时**：
- `extractors/mapping.py` 的每个模块配置项含 `"viz_style": "v_xxx"` 或 `"is_v_xxx_style": True`
- `composer.py` 根据该字段 dispatch 到对应 viz 函数

---

## 7. Karpathy 行为准则（强制）

### 7.1 Think Before Coding
- 编码前先**列假设**；不确定就问
- 多种解释 → **列选项**让我选，不要静默选一种
- 看到更简单方案 → **主动推回**，即使我让你做

### 7.2 Simplicity First
- **禁止 speculative features**（"以后可能用到"）
- 禁止为单次使用写抽象
- 禁止为未要求的"灵活性"写配置
- 200 行能 50 行写完 → **重写**
- 自检：「一个有经验的工程师会嫌这太复杂吗？」是 → 简化

### 7.3 Surgical Changes
- 只动必要的；**不顺手重构**
- 每改一行必须能**追溯到我的请求**
- 你自己改的孤儿（imports/vars/functions）→ 清
- **历史死代码不删**（除非我明确要求）

### 7.4 Goal-Driven Execution
- 每个任务**先定义 success criteria**
- 多步任务**先列 plan + verify**
- 强 success criteria → 可独立循环
- 弱 criteria（"让它工作"）→ 反复确认

---

## 8. Anti-Patterns（黑名单）

| ❌ 不要 | 原因 |
|---|---|
| 引入 React / Vue / Tailwind | 违反轻量约束 |
| 数据放 HTML 外部（fetch JSON） | `file://` 协议 CORS 失败 |
| 做后端 / API / 用户登录 | 单文件离线部署 |
| 拆 SPA 多文件包 | 一个 HTML 解决 |
| **Tailwind Play CDN**（~3MB JIT 浏览器端编译） | 违反轻量、慢 2-3 秒 |
| 加未要求的功能（导出 PDF / 暗色模式 / 实时数据 / 多语言……） | YAGNI |
| 改技术选型（§4） | 见 §9 例外 |
| 把决策从文档里挪走（"我觉得"改"我们定的是"） | 文档是真理源 |
| 自己加 README / 文档章节 / 注释 | 除非我要求 |
| 把 7 模块强制改成统一 viz 风格 | v1.5 核心创新是**每模块独立 viz**，回退到统一风格 = 倒退 |

---

## 9. 何时升级选型

**同时**满足 ① 用户已明确抱怨 + ② 量化数据证明问题，才能提议改选型。

单点不满不构成理由。"我想换个更现代的"不是理由。

---

## 10. 数据契约（v1.5：10 列）

- **文件名**：严格匹配 `build.py` 中 `MODULE_FILES` 字典
- **sheet 名** = 数据维度（如"年龄分布"、"客户经理"）
- **表头**：中文优先；字段映射集中在 `extractors/mapping.py`
- **占比**：统一 0-1 浮点（`0.2586` 表示 25.86%）
- **缺失值**：空 cell，**不写** "N/A" / "无" / "-"
- **数字千分位**：统一 `,`（`5,901`）
- **时段字段**：从 `配置` sheet 读，不写死

### v1.5 Excel 10 列结构

| # | 列 | 类型 | 说明 |
|---|---|---|---|
| 1 | 分组 | string | 数据分类 |
| 2 | 名称 | string | 显示名 |
| 3 | 数值 | number | 主要数字 |
| 4 | 单位 | string | 显示单位 |
| 5 | 备注 | string | 可选说明 |
| 6 | 排序 | int | 显示顺序 |
| 7 | is_total | bool (TRUE/FALSE) | 是否总数行 |
| 8 | delta | auto | 环比差（composer 自动算） |
| 9 | sub_text | string | 模块级叙述（关键洞察） |
| 10 | metric_note | string | KPI 卡底部说明（12-16 字看图说话） |

### v1.5 `_prev` 快照

每次 build 自动写回的快照 sheet，供下次构建计算环比 delta。仅保留 1 期（v1.5 YAGNI）。

---

## 11. 文档维护

任何以下变更 → **同步对应文档**：

| 变更类型 | 同步到 |
|---|---|
| 模块新增 / 接口变更 / 验收标准调整 | `docs/REQUIREMENTS.md` |
| 架构调整 / 选型变更 | 本文件 §4 + `docs/ARCHITECTURE.md` |
| 新发现的 anti-pattern | 本文件 §8 |
| 数据契约变更 | 本文件 §10 |
| viz 风格映射变更 | 本文件 §6 |

> **违反这条 = 修改没完成。**

---

## 12. 月度更新命令

```bash
# 1. 改 data/*.xlsx（只改"数值"列）
# 2. 构建
python build.py
# 3. 验证
open output/index.html
```

详见 [docs/MONTHLY-WORKFLOW.md](docs/MONTHLY-WORKFLOW.md)。

---

## 13. 出问题排查

| 现象 | 排查 |
|---|---|
| `output/index.html` 没生成 | 路径权限、Excel 文件名匹配 `MODULE_FILES` |
| 浏览器空白 | Console 看 inline JS/CSS 是否正确（无 CDN 加载问题） |
| 数据不显示 | Console 看 `window.HR_DATA` 内容 |
| 移动端布局错 | 检查 CSS 媒体查询断点（980px/640px） |
| 图表不渲染 | 检查 CSS 类名是否匹配样式定义 |
| 某模块 viz 风格不对 | 查 `extractors/mapping.py` 的 `viz_style` 字段 |
| 文件 > 100KB | 检查 viz 渲染是否漏 `<div class="empty">` 而渲染了大量空数据 |

参考 [REQUIREMENTS §10 验收标准](docs/REQUIREMENTS.md)。

---

## 14. 何时问我 vs 何时直接做

**直接做**（无需确认）：
- 修复明确 bug（按 trace 信息改）
- 跑 `python build.py` 等命令验证
- 在 `extractors/mapping.py` 加新字段映射（按数据契约 §10）
- 重构自己刚写的代码

**必须先问**（不要假设）：
- 需求含义不明确
- 多种合理实现方式
- 涉及 §4 选型变更
- 涉及 §6 黑名单中任一条
- 涉及需求文档没覆盖的范围

**判断原则**：如果做错需要重做 → 先问。如果错了容易回滚 → 直接做。