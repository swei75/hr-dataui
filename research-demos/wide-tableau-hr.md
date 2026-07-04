# Wide Table: Tableau Public - HR Analytics

## 来源 URL

- 主 demo: https://public.tableau.com/app/profile/chichi.umelo/viz/HRAttritionDashboardTest/HRAttritionDashboard
- 替代 demo: https://public.tableau.com/app/profile/tanmay.khedekar/viz/HRDashboard_17394575535210/HRSummary
- 替代 demo: https://public.tableau.com/app/profile/ahana.podder/viz/WorkforceAnalytics_17243637278100/Dashboard1

## 9 列观察

| 列 | 观察 |
|---|---|
| **demo 名称** | HR Attrition Analytics Dashboard (chichi.umelo) + Workforce_Analytics (ahana) |
| **URL** | public.tableau.com/app/profile/chichi.umelo/viz/HRAttritionDashboardTest/HRAttritionDashboard（公开 viz） |
| **模块数** | 6 模块（KPI 头条 / 部门分布 / 性别维度 / 工龄-收入散点 / 满意度 / 工作生活平衡）+ 过滤器侧栏 |
| **章节深度** | 2 个标签页（Dashboard 1 主图 + Dashboard 2 下钻），每页 6-8 个 viz 卡片，平均 1-2 句标题，无段落叙述 |
| **叙述占比** | 极低（<5%）—— 仅 KPI 标题 + 图注，无 "Executive Summary" 类文字段落，所有洞察靠 viz 表达 |
| **图表类型** | KPI 大数字、水平条形图（部门 attrition）、散点图（工龄 vs 收入）、折线趋势、100% 堆叠条（满意度）、饼图（教育背景）、过滤切片器 |
| **主色 hex** | Tableau 默认 #1F77B4 (蓝) + #FF7F0E (橙) accent；深色文字 #2F2F2F；背景 #FFFFFF，KPI 卡 #F2F2F2 |
| **信息密度** | 高——1920px 宽页面塞 8-10 个 viz，单 viz 平均 3-5 个数字 + 1 轴 |
| **银行感 (0-5)** | 1/5——完全英文，零售/通用企业语境，无任何银行术语 |
| **整体印象** | interactive, dense, English-first |

## 对本项目最有价值的观察

**"Headline KPI 行 + 下钻散点图" 是 HR 仪表盘的核心模式**——Tableau HR demo 几乎 100% 采用 4-6 个大数字 KPI 占顶部行，下方是散点 + 条形组合。本项目 M-1 模块应强烈借鉴：5 个 KPI 卡顶部横排 + 散点揭示"工龄-收入-流失"三维关系，是 HR 数据最有故事的视图。

## 对本项目不适合的点

**依赖外部 viz 服务器（public.tableau.com）+ 强交互**——本项目要单文件 HTML 完全离线 + 可邮件分发，Tableau 的 viz 必须在 Tableau Server 渲染，导出 PNG/PDF 又会丧失交互。和 §4 单文件 50KB 目标完全背离。**仅借鉴布局，不借鉴技术栈**。
