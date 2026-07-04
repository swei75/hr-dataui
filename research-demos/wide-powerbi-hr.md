# Wide Table: Power BI Showcase - HR

## 来源 URL

- 主 demo: https://learn.microsoft.com/en-us/power-bi/create-reports/sample-human-resources（HR 内置 sample）
- 替代 demo: https://learn.microsoft.com/en-us/power-bi/create-reports/sample-employee-hiring-history（招聘历史）
- AppSource 模板: https://appsource.microsoft.com/en-us/power-bi/agile_analytics.hr-analytics?tab=overview（Agile HR Analytics）

## 9 列观察

| 列 | 观察 |
|---|---|
| **demo 名称** | Power BI HR built-in sample (Microsoft Learn) + Agile HR & People Analytics |
| **URL** | learn.microsoft.com/en-us/power-bi/create-reports/sample-human-resources |
| **模块数** | 4 个核心页（New Hires / Active Employees / Separation / Performance）+ 顶部 KPI tile 仪表盘 + 6+ 可下钻子页 |
| **章节深度** | 单页 ~6 个 viz，每 viz 有独立 title + data label；"Q&A" 自然语言查询是 Power BI 招牌独占功能 |
| **叙述占比** | 极低（<5%）—— 大量依赖 Q&A 模式让用户自己问；零 paragraph 文字 |
| **图表类型** | 树状图（按部门分组）+ 累计漏斗（招聘漏斗）+ KPI 多 tile + 卡片筛选 + 智能叙事（Smart Narrative 自动生成 1 句话） |
| **主色 hex** | Power BI 主题色 #118DFF (蓝) + #12239E (深蓝) + #E74694 (粉) + #6B007B (紫) accent；背景 #FFFFFF |
| **信息密度** | 中——单页 4-6 viz 不挤，但每个 viz 内部标签极全（data label + axis + tooltip） |
| **银行感 (0-5)** | 2/5——demo 是 obviEnce（虚构公司）的英文 sample，无银行语境但有 SPLY（Same Period Last Year）企业感 |
| **整体印象** | tile-cards, drilldown, blue-pink |

## 对本项目最有价值的观察

**"顶部 KPI tile 横排 + 每 tile 可点击下钻" 是企业级仪表盘标准模式**——Power BI 把每个 KPI 数字做成可点击的"tile"（不只是数字，也是一个独立 viz，可点击展开子仪表盘）。本项目 M-1 (5 个 KPI 卡) 可借鉴：KPI 卡既是数字、又是钻取入口（点击切到对应明细表）。卡片用 box-shadow + 2px border 突出可点击。

**"Smart Narrative" 自动生成 1 句洞察文字**——Power BI 自动产生 "Revenue increased by 12% in Q2 driven by West region" 类一句话。本项目若有空间，6 个模块每个模块顶部加 1 句 12-16 字的 insight 横幅（手动写在 Excel sheet metadata 里），比纯数字 KPI 更"汇报感"。

## 对本项目不适合的点

**Power BI 必须登录 + 在线 + .pbix 文件 50MB+**——本项目是单文件 HTML 完全离线分发（§2），Power BI demo 既不可独立打开，也不能打包成 50KB HTML。**仅借鉴 viz 模式，不借鉴文件分发方式**。另外 Power BI 习惯 "SPLY"（同比）字段假设，本项目 Excel 数据未必提供。
