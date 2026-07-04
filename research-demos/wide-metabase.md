# Wide Table: Metabase

## 来源 URL

- 官方 showcase: https://www.metabase.com/dashboards/
- 销售团队 demo: https://www.metabase.com/dashboards/sales-teams
- e-Commerce 示例（含 Portfolio Performance Tab）: https://www.metabase.com/learn/metabase-basics/getting-started/explore-data

## 9 列观察

| 列 | 观察 |
|---|---|
| **demo 名称** | Metabase Sales Teams / e-Commerce Example Dashboard |
| **URL** | metabase.com/dashboards/sales-teams |
| **模块数** | 4 模块（KPI 头条 / Time series / Donut / Top 10 表）+ Tab 切换 Portfolio + Multiple Q&A |
| **章节深度** | 单页 ~6 viz + 一句 "metric description" tooltip；Q&A 栏让用户自然语言提问并自动生成 viz |
| **叙述占比** | 低（8-10%）——仅有 viz 标题和 1 句 metric 描述，**主打"探索式"由用户生成 insight** |
| **图表类型** | BigNumber、折线（revenue+orders over time）、柱形、地图（revenue by state 填色）、表格、Progress bar、Donut |
| **主色 hex** | Metabase 浅色主题 #509EE3 (蓝) + #88BF21 (绿)；深色主题 #2F353A 主色 |
| **信息密度** | 中低——viz 卡片之间空隙大，filter 在右上而不是顶部，强调"一眼看清一个指标" |
| **银行感 (0-5)** | 1/5——纯英文零售电商场景，无任何银行术语 |
| **整体印象** | minimal, QnA-friendly, blue-accent |

## 对本项目最有价值的观察

**"viz 之间大间距 + 弱填充" 让单模块更突出**——Metabase e-Commerce demo 的 viz 卡片间距是 Tableau 的 2 倍，每 viz 独立一个视觉单元。本项目 6 模块之间应**保持至少 24-32px 间距**，避免挤在一起失去节奏——shanjinki 当前间距较紧，可以借鉴 Metabase 加大。

**"右上角 help icon + 1 句 metric tooltip 解释" 是开源 BI 对用户的友好模式**——本项目每个 viz 可加 `<details>` HTML 元素（无 JS 即可展开），让用户 hover 看到"这个指标怎么算"，比写在 §10 排查指南更有用。

**"Drill down 列表在 viz 下方而不是新页面"**——Metabase 习惯"点 viz → 下方出现明细表"模式（如"点 Texas 州的 map → 下方表显示该州订单明细"）。本项目 M-2 钻取已有此模式（§3 钻取模块），可继续强化。

## 对本项目不适合的点

**依赖 Metabase server + PostgreSQL backend + React 客户端**——Metabase 是 SaaS 风格 BI，离线单文件场景完全不适合。和 Superset 同理，**仅借鉴 viz 模式 + 间距**，不借鉴服务端架构。

**"Q&A 自然语言查询" 对本项目是 overkill**——Metabase 招牌是输入"which state has most revenue?"自动生成 SQL + viz。本项目 HR 月度数据是预定义的，不是"探索式"，**不引入自然语言查询**（违反 §6 YAGNI）。
