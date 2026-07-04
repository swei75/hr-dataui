# hr-dataui 决策映射初稿（S1-F）

> **目的**：基于 3 深研 + 8 广扫描 + shadcn/Linear 调研，对现有 10 个 ADR 给出 KEEP / REVISE / DEPRECATE 判定。
>
> **状态**：⏳ 初稿，待用户逐条审阅
>
> **日期**：2026-07-04
>
> **作者**：Claude 综合 3 个 sub-agent 调研结果

---

## 0. 调研数据来源

| 类型 | 数量 | 文件位置 |
|---|---|---|
| 深研 demo | 3 | `research-demos/deep{1,2,3}-*.html` |
| 深研 README | 3 份 / 948 行 | `research-demos/README-deep{1,2,3}.md` |
| 广扫描 demo | 8 | `research-demos/wide-{tableau,powerbi,finebi,smartbi,superset,metabase}-*.md` |
| 广扫描矩阵 | 1 份 / 154 行 | `research-demos/README-wide-matrix.md` |
| 设计系统笔记 | 2 份 / 930 行 | `research-demos/README-{shadcn,linear}.md` |

**证据等级**（按 spec §3.2）：
- 🟢🟢🟢 深研 #1（中文 HR 月报） — 最强，直接对标 .docx
- 🟢🟢 深研 #2（银行/金融 dashboard） — 强，行业基准
- 🟢🟢 深研 #3（管理驾驶舱） — 强，领导视角
- 🟡 广扫描（8 BI 工具） — 中，横向参考
- 🟡 shadcn / Linear — 中，设计哲学参考

---

## 1. 决策映射总览

| ADR | 判定 | 修订方向 | 触发证据 |
|---|---|---|---|
| ADR-001 单 Excel | **KEEP（不可动）** | — | — |
| ADR-002 7 列契约 | **REVISE** ⚠️ | 加 `delta` + `sub_text` + `metric_note` 字段 | 深 #1 + 深 #2 + 深 #3 + 广（4/8 国内 BI） |
| ADR-003 CSS 静态图表 | **KEEP** | （heatmap 留为差异化亮点，扩展而非取代） | 深 #2 触发 Chart.js 但 C-2 限制 |
| ADR-004 自研 CSS | **KEEP** | — | — |
| ADR-005 Python f-string | **KEEP（不可动）** | — | — |
| ADR-006 composer 自动选 viz | **KEEP（可扩展）** | 扩展：加 heatmap 选项（M-2 员工 × 司龄） | 深 #3 |
| ADR-007 浅色 + 4 tone | **REVISE** ⚠️ | 加 3 色风险等级（success/warning/danger）+ `bank-dark` 可选 style | 深 #3 + 广（FineBI 银行 5/5 银行感） |
| ADR-008 12-col grid + 3 断点 | **KEEP** | — | — |
| ADR-009 钻取交互 YAGNI | **KEEP** | — | — |
| ADR-010 单文件部署 | **KEEP（不可动）** | — | — |

**统计**：2 REVISE + 8 KEEP + 0 DEPRECATE

---

## 2. KEEP（不可动）— 3 个

### ADR-001 单 Excel 数据源 — KEEP（不可动）

- **状态**：KEEP（不可动）
- **理由**：spec §3.4 已明确列入不可动清单。HR 月报场景已固化，1 个 Excel 8 sheets 是用户已认可的工作流。
- **证据**：3 个深研 demo 全部支持"单一数据源"模式（无 demo 反驳）。

### ADR-005 Python f-string 模板 — KEEP（不可动）

- **状态**：KEEP（不可动）
- **理由**：spec §3.4 已明确列入不可动清单。零依赖，符合 C-2。
- **证据**：3 深研 + 8 广扫描中无 demo 反驳 f-string 方案本身（部分 demo 用 Jinja2 但仅为语法偏好）。

### ADR-010 单文件部署 — KEEP（不可动）

- **状态**：KEEP（不可动）
- **理由**：spec §3.4 已明确。C-1 重申，邮件 / U 盘 / 内网分发的核心场景。
- **证据**：8/8 广扫描 demo **全部依赖外部 server**（Tableau Online / PowerBI Online / FineBI 服务端 / Superset server / Metabase server 等）—— 100% 违反 C-2 / C-3，证明单文件离线是少数派但也是本项目的差异化优势。

---

## 3. KEEP（可优化）— 5 个

### ADR-003 CSS 静态图表 — KEEP

- **状态**：KEEP（保留，但有 1 个差异化扩展机会）
- **理由**：CSS 静态图表体积可控（~5KB）、完全离线。深 #2（Velarasan）触发 Chart.js 需求但 **Chart.js 依赖 CDN 违反 C-2**。
- **证据**：
  - ❌ 深 #2 Chart.js：CDN 依赖，违反 C-2
  - ❌ 深 #3 Fontshare 字体：CDN 依赖
  - ✅ 深 #1 shanjinki 用纯 CSS 图表（div + width %）
  - ✅ 8/8 广扫描 demo 都用 SVG/Canvas，但都有外部 server 依赖
- **差异化亮点**（**新增建议**，不进 ADR-003 本体）：
  - **heatmap**（深 #3 Tableau RiskVue 模式）：M-2 员工 × 司龄交叉表，可用纯 CSS Grid 实现（5×5 单元格 + 背景色 tone 渐变）
  - **SVG sparkline**（深 #3）：trend mini-chart，每个 KPI 卡可附加
  - 这两个**扩展不取代** CSS 静态图表，是 v1.4 差异化亮点

### ADR-004 自研 CSS（继承 shanjinki 18 styles） — KEEP

- **状态**：KEEP
- **理由**：shadcn / Linear 调研验证 v1.3 已对齐关键设计哲学：
  - ✅ 8px 按钮圆角（对齐 Linear）
  - ✅ 4px 间距节奏（对齐 Linear）
  - ✅ CSS variables + 语义命名（学 shadcn）
  - ✅ 极简阴影（学 shadcn `--shadow-sm`）
  - ✅ Inter 字体回退（学 Linear）
- **v2.0 候选**（不进 v1.4）：token 命名规范化（`primary-soft` 替代 `primary-light`） + OKLCH 迁移

### ADR-006 composer 自动选 viz — KEEP（可扩展）

- **状态**：KEEP（保留自动选 viz 核心，扩展支持 heatmap）
- **理由**：3 深研全部支持"数据驱动 viz" 模式，无 demo 反驳。
- **唯一扩展**：加 `heatmap` 选项（5×5 网格 M-2 员工 × 司龄交叉），由 composer 按 sheet 类型判断。
- **证据**：
  - ✅ 深 #1 shanjinki 用 composer 模式（无 viz registry）
  - ✅ 深 #3 Tableau RiskVue heatmap 是新 viz 机会
  - ❌ 深 #2 Chart.js 强制 viz 选择，但本项目无 Chart.js

### ADR-008 12-col grid + 3 断点 — KEEP

- **状态**：KEEP
- **理由**：3 深研 demo + 8 广扫描 demo 全部用 CSS Grid + CSS variables。12-col + 3 断点是行业标准（深 #3 Tableau RiskVue 用 8 进制 spacing，验证 grid 必要性）。
- **证据**：
  - ✅ 深 #1 shanjinki 3 断点（980/640）
  - ✅ 深 #3 8 进制 spacing（8/16/24/32px）
  - ✅ 8/8 广扫描 demo 全部用 CSS Grid

### ADR-009 钻取交互 YAGNI — KEEP

- **状态**：KEEP（YAGNI 仍成立）
- **理由**：3 深研 demo **全部无钻取交互**（shanjinki / Velarasan / Tableau RiskVue 都是静态 dashboard）。HR 月报场景不需要下钻（用户决策）。
- **证据**：
  - ✅ 深 #1 shanjinki 无钻取
  - ✅ 深 #2 Velarasan 无钻取
  - ✅ 深 #3 Tableau RiskVue 无钻取
  - ⚠️ 广扫描 demo 多数有 drill-down（Tableau / PowerBI / FineBI），但都依赖 server（违反 C-2）

---

## 4. REVISE — 2 个

### ADR-002 7 列数据契约 — REVISE ⚠️

- **状态**：REVISE（修订 7 → 8 列）
- **触发强度**：🟢🟢🟢 3 个深研全部触发 + 广扫描 4/8 国内 BI 触发（**最强证据**）
- **当前**：7 列 `分组 / 名称 / 数值 / 单位 / 备注 / 排序 / is_total`
- **修订为 8 列**：增加 `delta` 字段（同比 / 环比 / 绝对差，可选）
- **delta 字段设计**：
  ```python
  # Excel sheet 第 8 列：delta
  # 格式：
  #   - 数字（如 -50 表示减少 50 人）
  #   - 百分比字符串（如 "+5.2%"）
  #   - 空 = 无对比数据
  # composer 按 is_total + delta 自动渲染：
  #   - delta 非空 + is_total=True → KPI 卡右下角"vs 上月"绿色/红色文字
  #   - delta 非空 + is_total=False → bar 末端"vs 上月"徽章
  #   - delta 空 → 不显示
  ```
- **触发证据**：
  - 🟢🟢🟢 深 #1 shanjinki：5 KPI 卡都附"看图说话"叙述（30+ 字）
  - 🟢🟢 深 #2 Velarasan：5 KPI 卡 + delta（绿涨红跌）+ chart-subtitle 解释性副标题
  - 🟢🟢 深 #3 Tableau RiskVue：4 KPI + delta + sub 注释（如 "Risk Mitigation" "Risk Profile"）
  - 🟡 广扫描：4/8 国内 BI（FineBI HR + FineBI 银行 + Smartbi + Superset）有 KPI "看图说话"
- **数据契约影响**：
  - Excel：用户每月多加 1 列（可选，不强制）
  - composer：自动计算 delta 显示逻辑（无需用户配）
  - backward compat：delta 为空时渲染与 v1.3 一致
- **是否污染 Excel**：建议**不污染**——Excel 仍只放本期数据，delta 由 `上期数据 sheet` 自动算（复用现有 sheet 结构，新增 1 个 `_prev` 影子 sheet）

**待用户决策**：
- Q1: delta 字段加吗？
- Q2: 是手动填 Excel 还是 composer 自动算（基于历史 sheet）？
- Q3: `sub_text`（叙述字段）要不要同时加？（深 #1 + 深 #3 都建议）

### ADR-007 浅色专业风 + CSS variables + 4 级 tone — REVISE ⚠️

- **状态**：REVISE（保留主色 + 4 tone，增加 3 色风险等级 + 可选 bank-dark style）
- **触发强度**：🟢🟢 深 #3 + 🟡 广扫描 FineBI 银行
- **当前**：主色 `#1E5BAA` + 4 级 tone + 12px 圆角
- **修订内容**：
  1. **新增 3 色风险等级**（success / warning / danger）：
     ```css
     --success: #16A34A;   /* 绿，完成率 ≥ 100% */
     --warning: #D97706;   /* 橙，完成率 80-100% */
     --danger:  #DC2626;   /* 红，完成率 < 80% */
     --success-foreground: #FFFFFF;
     --warning-foreground: #FFFFFF;
     --danger-foreground:  #FFFFFF;
     ```
  2. **新增可选 `bank-dark` style**（**不进 v1.4**，v2.0 候选）：
     - 主色改 `#0A1F3D`（深蓝，FineBI 银行风格）
     - 强调色 `#D4AF37`（金色）
     - 触发：广扫描 FineBI 银行 5/5 银行感配色（最深印象）
  3. **保留 v1.3 主色** `#1E5BAA`（已被用户认可）
- **触发证据**：
  - 🟢🟢 深 #3 Tableau RiskVue：3 色风险等级 + 5×5 热图编码
  - 🟡 广扫描 FineBI 银行：深蓝 #0A1F3D + 金色 #D4AF37 = 5/5 银行感
- **影响范围**：
  - `templates/base.py`：新增 3 个 CSS variable（success / warning / danger）
  - composer：识别"完成率"类数据时自动用对应风险色
  - 用户：每月填 Excel 时多打 1 个"完成率"列（也可空着，由现有"数值"列 + 推算阈值自动套色）
- **决策建议**：**保留主色 + 加 3 色风险等级**（核心修订），`bank-dark` style 进 v2.0 候选

**待用户决策**：
- Q4: 加 3 色风险等级（success/warning/danger）吗？
- Q5: `bank-dark` 深蓝金色 style 进 v2.0 还是 v1.4？

---

## 5. DEPRECATE — 0 个

无 ADR 被淘汰。所有 ADR 在调研后都保留（修订或不修订），证明 v1.3 选型稳定。

---

## 6. v1.4 零风险改进候选（不进 ADR，仅记录）

> 以下是调研中发现的具体可执行改进，**风险低、收益明确**，可作为 v1.4 小迭代采纳。

| # | 改进 | 来源 | 风险 | 文件 |
|---|---|---|---|---|
| 1 | 加 `cv01, ss03` OpenType features（数字 0 切平、`a` 单层） | Linear README | 🟢 零（仅 font-feature-settings 加 2 个值） | `templates/base.py` |
| 2 | 加 `metric_note` 字段（KPI 下方 12-16 字"看图说话"） | 广扫描 4/8 国内 BI | 🟢 低（Excel 加 1 可选列） | `extractors/mapping.py` + `templates/base.py` |
| 3 | 加 KPI delta 自动计算（基于上期 sheet） | 深 #2 + 深 #3 | 🟡 中（需要历史数据存储） | `extractors/delta.py` (新) |

---

## 7. v2.0 候选（不进 v1.4）

| # | 改进 | 来源 |
|---|---|---|
| 1 | token 命名规范化（`primary-soft` 替代 `primary-light`） | shadcn |
| 2 | OKLCH 迁移（更感知均匀的色阶） | shadcn v4 |
| 3 | `bank-dark` style（深蓝 #0A1F3D + 金色 #D4AF37） | 广扫描 FineBI 银行 |
| 4 | heatmap 可视化（M-2 员工 × 司龄交叉） | 深 #3 Tableau RiskVue |
| 5 | SVG sparkline（每个 KPI 卡附加 mini trend） | 深 #3 |

---

## 8. 用户决策记录（已确认）

> 2026-07-04 用户确认全部 5 个问题答案。

| # | 问题 | 答案 | 影响 |
|---|---|---|---|
| **Q1** ✅ | ADR-002 加 `delta` 字段？ | **(a) 加** | ADR-002 修订：7 列 → 8 列 |
| **Q2** ✅ | delta 手动 vs 自动？ | **(b) composer 自动算**（基于 _prev sheet） | Excel 不污染，composer 维护历史快照 |
| **Q3** ✅ | ADR-002 加 `sub_text` 叙述字段？ | **(a) 加** | ADR-002 修订：8 列 → 9 列 |
| **Q4** ✅ | ADR-007 加 3 色风险等级？ | **(a) 加** | ADR-007 修订：主色 + 4 tone + 3 色风险 |
| **Q5** ✅ | `bank-dark` style 是 v1.4 还是 v2.0？ | **(b) v2.0** | 进 v2.0 候选，不阻塞 v1.4 |

**修订后 ADR 数量**：

| 判定 | ADR |
|---|---|
| **KEEP（不可动）** | ADR-001 / ADR-005 / ADR-010（3 个） |
| **KEEP** | ADR-003 / ADR-004 / ADR-006 / ADR-008 / ADR-009（5 个） |
| **REVISE** | ADR-002（9 列）+ ADR-007（加 3 色风险等级）（2 个） |
| **DEPRECATE** | 无 |

---

## 9. 下一步流程（按 spec §3.3）

```
当前：决策映射 v2 已用户确认 ✅
    ↓
下一步：写入 ARCHITECTURE.md §"研究驱动的修订建议"
    ↓
S2 完成
    ↓
新 spec（v1.4）：基于修订后 ADR-002 + ADR-007 的实施方案
（启动前需要用户明确确认 — 不在 S1/S2 范围）
```

**不在 S1 范围**（spec §1.4）：重写代码、实现新功能、修订 ADR 的具体实施 —— 这些是 S2 / 后续 session 的事。

---

## 变更日志

| 日期 | 变更 | 作者 |
|---|---|---|
| 2026-07-04 | 初稿（综合 3 深研 + 8 广扫描 + shadcn/Linear） | Claude |