# 调研 Demo 文件

按 GitHub 调研顺序排列，双击即可在浏览器查看（无需联网）。

---

## 📄 shanjinki-HR-demo.html（32KB）⭐ 重点参考

**来源**：`shanjinki/excel-to-html-slides`，examples/sample_hr_report.html

**视觉风格**：`Editorial Brief`（米色 + 红棕色，专业感）

**关键观察点**：
1. **完全离线** — 无任何外部 CDN，Ctrl+U 看源码全是 inline CSS+JS
2. **中文优先** — 标题"HR 人员运营分析报告"，UI 全部中文
3. **响应式** — 拖窄浏览器到 980px / 640px 看布局变化
4. **5 个 KPI 卡** — 员工数 / 记录数 / 平均绩效 / 异常 / 高工时
5. **KPI 卡顶部 3px 彩条** — 不同颜色对应不同 KPI 类别
6. **2 栏布局** — 关键洞察 + 口径假设（左右栏）
7. **部门表现柱图** — 用纯 CSS 实现（div + width %），不是 SVG/Canvas
8. **岗位结构柱图** — 同上
9. **趋势柱图** — 时间序列柱图
10. **人员异常明细表格** — 详细列表
11. **风险清单与行动建议** — 2 列卡片，每张卡片有标题 + 详情 + 行动建议
12. **canvas 背景动画** — 右上角有动态光晕效果（适合演示，不适合打印）
13. **章节编号** — 01, 02, 03, 04... 顺序编号

**限制**：
- ❌ 没有交互（下钻、视图切换）
- ❌ 图表是 CSS 静态条形（不是 SVG/Canvas，无法缩放）
- ❌ 移动端表格变成横向滚动条

---

## 📄 shanjinki-finance.html（36KB）

**来源**：shanjinki/excel-to-html-slides，examples/sample_finance_report.html

**视觉风格**：`Boardroom Light`（深蓝 + 浅灰，专业金融感）

**关键观察点**：
- 同上架构，但风格不同（演示 18 个 style 的多样性）
- 5 个 KPI、利润结构、预算对比、风险清单

---

## 📄 shanjinki-sales.html（43KB）

**来源**：shanjinki/excel-to-html-slides，examples/sample_sales_order_report.html

**视觉风格**：`Command Center`（深色主题 + 青色高亮）

**关键观察点**：
- 深色主题适合演示大屏
- 漏斗图用纯 CSS 实现（多个 div + clip-path）

---

## 📄 sven-bo-demo.html（51KB）

**来源**：`Sven-Bo/pyecharts-dashboard`，Sales & Profit Overview.html

**视觉风格**：默认 pyecharts 主题（无定制）

**关键观察点**：
1. **依赖外部 CDN** — `<script src="https://assets.pyecharts.org/assets/echarts.min.js">`，断网打不开
2. **3 个 Tab 切换** — Sales by months / subcategory / Calendar（验证了 Tab 切换可行）
3. **ECharts 完整** — 真图表库，支持 hover/tooltip
4. **写死尺寸** — `style="width:900px; height:500px;"`，移动端不友好
5. **Tab 是 vanilla JS** — 不依赖 Alpine.js
6. **单 sheet** — 只有"Orders"数据，没有多模块架构

---

## 💡 对比建议

| 看什么 | 看哪个 demo |
|---|---|
| 中文 HR 报告最像我们要做的 | `shanjinki-HR-demo.html` |
| 视觉风格多样性 | `shanjinki-finance.html` (浅) / `shanjinki-sales.html` (深) |
| ECharts 真图表（pyecharts 输出） | `sven-bo-demo.html`（但注意依赖外网） |

---

## 🚫 不推荐

| 候选 | 原因 |
|---|---|
| `StructuredLabs/preswald` | 用 Pyodide + WASM 单文件包（10-20MB runtime），违反 §4 技术栈、违反 D-1（Plotly 非 ECharts）、首屏加载 > 3s 违反 P-1 |
| `sqlinsights/st-static-export` | 把 Streamlit 导出成静态 HTML，但 Streamlit 客户端架构，违反单文件约束 |

---

## ✅ 下一步

按 CLAUDE.md §7（选型变更需用户批准）+ Karpathy §1（列选项让你选），请你看完 demo 后告诉我：

1. **视觉风格**：shanjinki 的"Editorial Brief / Boardroom / Command Center"哪个最贴近你预期？
2. **ECharts 决策**：
   - (a) 放弃 ECharts（保留 CSS 静态图表）→ 走 🅰️ 改造 shanjinki
   - (b) 必须保留 ECharts（要交互式图表）→ 走 🅱️ 改造 Sven-Bo（更费工）
   - (c) 折中：shanjinki + 局部引入 ECharts 做复杂图表（漏斗/下钻）
3. **是否还有其他候选要看**？（若有，给关键词）