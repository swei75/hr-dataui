# CLAUDE.md — hr-dataui 项目指引

> **需求文档**：[docs/REQUIREMENTS.md](docs/REQUIREMENTS.md)（v1.1，2026-07-03 调研更新）
> **行为准则**：参考 `andrej-karpathy-skills:karpathy-guidelines`（强制）

---

## 1. 项目一句话

读 Excel → 生成单文件 HTML 仪表盘。**任何方案讨论、代码改动前，先回顾 §4 技术选型与 §6 Anti-Patterns。**

**技术栈**：Python 3.10+ (pandas + openpyxl) + f-string 模板 + CSS 静态图表 + 自研 CSS（参考 shanjinki）

---

## 2. 核心命令

```bash
pip install -r requirements.txt    # 安装依赖
python build.py                    # 构建 → output/index.html
```

**输出 = 单文件 `output/index.html`**，目标 ≤ 50KB，0 外部依赖，完全离线，双击即用，可邮件/U 盘/内网分发。

---

## 3. 目录速查

| 路径 | 用途 |
|---|---|
| `data/*.xlsx` | Excel 数据源（1 个文件 6 sheet + 1 配置 sheet） |
| `extractors/` | 数据读取 + 字段映射 + 钻取 |
| `extractors/reader.py` | `read_workbook()` 读 Excel → dict |
| `extractors/mapping.py` | sheet→键名 + viz 类型 + 可钻取 配置 |
| `extractors/drills.py` | 钻取数据加载 |
| `viz/` | viz 注册表（8 个 viz 文件） |
| `viz/__init__.py` | `VIZ_REGISTRY` 字典 |
| `composer.py` | 按 mapping 组合 6 模块 HTML |
| `templates/` | Python f-string 模板函数（.py 文件，不是 .j2） |
| `vendor/` | Alpine.js + shanjinki CSS 等 vendored 资源 |
| `output/index.html` | 最终产物（git ignore） |
| `tests/` | pytest 测试（reader/mapping/viz/build_e2e） |
| `docs/REQUIREMENTS.md` | v1.1 需求 |
| `docs/superpowers/specs/` | 设计 spec |
| `docs/superpowers/plans/` | 实施计划 |
| `research-demos/` | v1.1 调研 demo |

---

## 4. 技术选型（不许改，§7 例外）

**v1.1 选型（2026-07-03 调研更新）**：

| 层 | 选型 | 体积 | 关键原因 |
|---|---|---|---|
| 数据 | pandas + openpyxl | - | Excel 标准 |
| 模板 | Python f-string（不引入 Jinja2） | - | 减少依赖 |
| 前端 | Vanilla JS（不引入 Alpine.js） | - | 单文件最简 |
| 图表 | CSS 静态图表 | ~5KB | 参考项目 shanjinki 实现，体积最小 |
| 样式 | 自研 CSS（继承 shanjinki 18 styles） | ~10KB | 不引入 Pico.css |
| 部署 | 单文件 HTML | 目标 50KB | 极致可移植 |
| 参考项目 | fork shanjinki/excel-to-html-slides | - | MIT 协议，HR demo 现成 |

> 任何"要不要换 X 框架"的冲动，先看这一节。**默认选型经过评审，改它需要理由，不是反过来。**

> **历史选型**（v1.0 已弃用）：ECharts 5 / Pico.css 2 / Jinja2 / Alpine.js。调研后改选更轻量方案。

---

## 5. Karpathy 行为准则（强制）

### 5.1 Think Before Coding
- 编码前先**列假设**；不确定就问
- 多种解释 → **列选项**让我选，不要静默选一种
- 看到更简单方案 → **主动推回**，即使我让你做

### 5.2 Simplicity First
- **禁止 speculative features**（"以后可能用到"）
- 禁止为单次使用写抽象
- 禁止为未要求的"灵活性"写配置
- 200 行能 50 行写完 → **重写**
- 自检：「一个有经验的工程师会嫌这太复杂吗？」是 → 简化

### 5.3 Surgical Changes
- 只动必要的；**不顺手重构**
- 每改一行必须能**追溯到我的请求**
- 你自己改的孤儿（imports/vars/functions）→ 清
- **历史死代码不删**（除非我明确要求）

### 5.4 Goal-Driven Execution
- 每个任务**先定义 success criteria**
- 多步任务**先列 plan + verify**
- 强 success criteria → 可独立循环
- 弱 criteria（"让它工作"）→ 反复确认

---

## 6. Anti-Patterns（黑名单）

| ❌ 不要 | 原因 |
|---|---|
| 引入 React / Vue / Tailwind | 违反轻量约束 |
| 数据放 HTML 外部（fetch JSON） | `file://` 协议 CORS 失败 |
| 做后端 / API / 用户登录 | 单文件离线部署 |
| 拆 SPA 多文件包 | 一个 HTML 解决 |
| **Tailwind Play CDN**（~3MB JIT 浏览器端编译） | 违反轻量、慢 2-3 秒 |
| 加未要求的功能（导出 PDF / 暗色模式 / 实时数据 / 多语言……） | YAGNI |
| 改技术选型（§4） | 见 §7 例外 |
| 把决策从文档里挪走（"我觉得"改"我们定的是"） | 文档是真理源 |
| 自己加 README / 文档章节 / 注释 | 除非我要求 |

---

## 7. 何时升级选型

**同时**满足 ① 用户已明确抱怨 + ② 量化数据证明问题，才能提议改选型。

单点不满不构成理由。"我想换个更现代的"不是理由。

---

## 8. 数据契约

- **文件名**：严格匹配 `build.py` 中 `MODULE_FILES` 字典
- **sheet 名** = 数据维度（如"年龄分布"、"客户经理"）
- **表头**：中文优先；字段映射集中在 `extractors/mapping.py`
- **占比**：统一 0-1 浮点（`0.2586` 表示 25.86%）
- **缺失值**：空 cell，**不写** "N/A" / "无" / "-"
- **数字千分位**：统一 `,`（`5,901`）
- **时段字段**：从 `data/` 目录下 metadata 或专门 sheet 读，不写死

---

## 9. 文档维护

任何以下变更 → **同步对应文档**：

| 变更类型 | 同步到 |
|---|---|
| 模块新增 / 接口变更 / 验收标准调整 | `docs/REQUIREMENTS.md` |
| 架构调整 / 选型变更 | 本文件 §4 |
| 新发现的 anti-pattern | 本文件 §6 |
| 数据契约变更 | 本文件 §8 |

> **违反这条 = 修改没完成。**

---

## 10. 出问题排查

| 现象 | 排查 |
|---|---|
| `output/index.html` 没生成 | 路径权限、Excel 文件名匹配 `MODULE_FILES` |
| 浏览器空白 | Console 看 inline JS/CSS 是否正确（无 CDN 加载问题） |
| 数据不显示 | Console 看 `window.HR_DATA` 内容 |
| 移动端布局错 | 检查 CSS 媒体查询断点（980px/640px） |
| 图表不渲染 | 检查 CSS 类名是否匹配样式定义 |

参考 [REQUIREMENTS §10 验收标准](docs/REQUIREMENTS.md)。

---

## 11. 何时问我 vs 何时直接做

**直接做**（无需确认）：
- 修复明确 bug（按 trace 信息改）
- 跑 `python build.py` 等命令验证
- 在 `extractors/mapping.py` 加新字段映射（按数据契约 §8）
- 重构自己刚写的代码

**必须先问**（不要假设）：
- 需求含义不明确
- 多种合理实现方式
- 涉及 §4 选型变更
- 涉及 §6 黑名单中任一条
- 涉及需求文档没覆盖的范围

**判断原则**：如果做错需要重做 → 先问。如果错了容易回滚 → 直接做。
