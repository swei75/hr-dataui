# Wide Table: Apache Superset

## 来源 URL

- 官方 docs: https://superset.apache.org/user-docs/using-superset/creating-your-first-dashboard/
- 财务 demo: https://www.padiso.co/blog/apache-superset-financial-reporting-reference-dashboard/
- 酒店 RevPAR demo: https://www.d23.io/blog/apache-superset-hotels-revpar-adr-occupancy-dashboards

## 9 列观察

| 列 | 观察 |
|---|---|
| **demo 名称** | Apache Superset P&L Financial Dashboard（PADISO 出品 reference suite） |
| **URL** | padiso.co/blog/apache-superset-financial-reporting-reference-dashboard/ |
| **模块数** | 5 大模块（Revenue Manager Dashboard / Multi-Property Portfolio / Guest Segment / Financial Reconciliation / Operations），每个模块多页 |
| **章节深度** | 单页 6-10 viz + markdown 文本段落 + filter bar，可定义多个 Tab；tech-post 深度讲解 schema |
| **叙述占比** | 较高（25-30%）—— Superset demo 配合长篇 blog post 解释数据模型和 viz 选择 |
| **图表类型** | BigNumber + delta trend、ECharts/Plotly 折线 + BigNumber with trendline、地图（州级填色）、透视表、热力图、Sankey、Sunburst |
| **主色 hex** | Superset 默认 #1FA8C9 (青) + #FF7F0E (橙) accent + 自定义主题支持；深色版 #222F3E |
| **信息密度** | 中——单页 6-8 viz，filter bar 占 15% 高度，viz 卡片间距宽松 |
| **银行感 (0-5)** | 3/5——demo 是会计 / 酒店 / 多物业 portfolio 场景，但"Revenue Recognition"、"Payment Reconciliation" 是金融术语 |
| **整体印象** | open-source, filter-bar, ECharts-rendered |

## 对本项目最有价值的观察

**"BigNumber + Delta Trend" 是趋势可视化的最简实现**——Superset 的 KPI 组件自带"和上期对比的小箭头"，比文字叙述更直接。本项目 M-1 KPI 卡可加 ↑↓ 微型图标（用 ▲▼ + color，不需要 JS），前提是 Excel 数据提供上期对比列。

**"filter bar 在顶部 + viz 卡片在下方" 的 2 区段布局是企业级 BI 的统一模式**——本项目当前是垂直滚动单列，可考虑在数据量大时**顶部加一个"按部门 / 按时间段"的筛选条**（用 CSS `<select>` + 1 个简单 JS 切换显示），不增加 50KB 体积太多。

**"viz 卡片 padding 8-12px 而不是 0"**——Superset 卡片间距比 Tableau 宽松 30%，便于手机浏览。本项目 §5.2 响应式断点（980px / 640px）下应该验证这个间距不被压扁。

## 对本项目不适合的点

**后端依赖 Python + Flask + React (assets 8MB+) + database connection**——Superset 是 web 服务端，1 个 demo 完整部署要 4GB+ Docker。本项目单文件 HTML 完全离线（§2），**绝对不引入 Superset 架构**。仅借鉴 viz 模式。

**"filter dropdown + auto update" 假设有用户输入**——本项目"双击即用"零配置原则（§2）下，filter 是反模式——用户每次切换要点击，不如一次性把数据全部静态化（shanjinki 模式）。**借鉴 display 模式，不借鉴 filter 交互**。
