# Wide Table: Tableau Public - Finance Dashboard

## 来源 URL

- 主 demo: https://public.tableau.com/app/profile/mishrilal.pairhar/viz/FinancialPerformanceDashboard1_17540511537030/Dashboard1
- 替代 demo: https://github.com/Madhushree-Majumder/Financial-Reporting-and-Financial-Analysis-Using-Tableau（TurtleCo P&L）
- 替代 demo: https://github.com/Khushi-12/Financial-Analysis-Tableau（US 行业财务）

## 9 列观察

| 列 | 观察 |
|---|---|
| **demo 名称** | Financial Performance Dashboard 1 (Mishrilal) + TurtleCo P&L (Madhushree) |
| **URL** | public.tableau.com/app/profile/mishrilal.pairhar/viz/FinancialPerformanceDashboard1_17540511537030/Dashboard1 |
| **模块数** | 5 模块（顶部 KPI 4 件 / Sales Over Time / Profit Over Time / Sales by Product & Discount 热力图 / Sales & Profit by Country / Sales by Product 横向条） |
| **章节深度** | 单页 5 个 viz + 顶部 KPI band，无独立 tab；标题 + 副标题 1 行 + 1 句 "as of" 时间戳，无段落 |
| **叙述占比** | <3%——几乎是纯 viz，配合 hover tooltip 显示数据，title 仅 "Sales", "Profit Margin" 等名词 |
| **图表类型** | 大数字 KPI（带 ↑↓% 涨跌指示）、时间序列折线、热力图（product × discount）、条形图（country 横向）、100% 堆叠 |
| **主色 hex** | 深色业务风 #1A1A1A 背景（部分 demo）+ #00B050 涨 / #C00000 跌；浅色 demo 用 Tableau #4A7EBB 主蓝 |
| **信息密度** | 极高——单页 12 个 viz 卡，1920×1200 全填满；坐标轴字体 8-9px 极小字号换取密度 |
| **银行感 (0-5)** | 3/5——出现 "Sales"、"Profit Margin"、"COGS"、"Region" 等财务术语，符合 banking finance 语境，但 demo 是通用制造业销售场景 |
| **整体印象** | KPI-dense, utilitarian, dark-optional |

## 对本项目最有价值的观察

**"KPI 顶部 band + 时间序列大图" 模式最适合月度驾驶舱**——金融仪表盘的核心是"现在怎样 + 趋势怎样"，4-6 个顶部数字 KPI + 2-3 个全宽时间序列图（M-3 趋势模块直接对应）。Mishrilal demo 的 Sales/Profit Over Time 占满半屏，可视性最佳，本项目应至少留 1 个模块用 100% 宽度的趋势线。

## 对本项目不适合的点

**"百分比涨幅 + 绿/红配色" 假设本项目数据未提供同比字段**——Tableau 财务 demo 习惯用 ↑↓ 百分比箭头（同比 / 环比），但银行 HR 月度数据大多只有本期 + 上期 2 列，不是连续时间序列 + 同比。强套百分比涨跌会和 §8 数据契约冲突。**借鉴布局，不借鉴同比字段假设**。
