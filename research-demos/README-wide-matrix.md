# Wide Matrix: 8 BI 工具 Demo 横向对比

> 调研日期：2026-07-04  
> 调研目的：为本项目（银行 HR 月度管理驾驶舱 / 单文件 HTML）识别"借鉴做法"+"避坑模式"  
> 调研样本：4 国际 BI（Tableau×2 + PowerBI + Superset）+ 1 国际开源（Metabase）+ 3 国内 BI（FineBI×2 + Smartbi）

---

## §1 完整对比矩阵

| demo 名称 | URL | 模块数 | 章节深度 | 叙述占比 | 图表类型 | 主色 hex | 信息密度 | 银行感 (0-5) | 整体印象 (3 词) |
|---|---|---|---|---|---|---|---|---|---|
| Tableau HR | public.tableau.com/.../chichi.umelo/HRAttritionDashboard | 6+侧边过滤 | 2 Tab，每页 6-8 viz | <5%（纯 viz） | 散点 + KPI + 条形 + 100% 堆叠 | #1F77B4 蓝 + #FF7F0E 橙 | 高 (8-10 viz/页) | 1 | interactive dense English |
| Tableau Finance | public.tableau.com/.../mishrilal/FinancialPerformanceDashboard | 5 + 顶部 KPI band | 单页多 viz | <3%（近乎纯 viz） | KPI + 折线 + 热力图 + 横向条 | #00B050 涨 / #C00000 跌 | 极高 (12 viz/页) | 3 | KPI-dense utilitarian dark-optional |
| PowerBI HR | learn.microsoft.com/.../sample-human-resources | 4 主页 + 下钻 | 每页 ~6 viz + Q&A | <5%（靠 Q&A） | TreeMap + 漏斗 + KPI tile + Smart Narrative | #118DFF 蓝 + #E74694 粉 | 中（4-6 viz/页） | 2 | tile-cards drilldown blue-pink |
| FineBI HR | finebi.com/blog/.../6874ebe328946ecca8e3d575 | 5-6 + AI 问答框 | 单页 8-10 viz | 15-20% | 漏斗 + 饼 + 甘特 + 9 宫格 + 自然语言 | #2875FF 蓝 + #00B8A9 青 + #FF6B6B 红 | 中高 | 1（内容）/ 4（品牌） | 中文-friendly narrative-rich AI-warm |
| FineBI 银行 | finebi.com/visualization/yjdzyh | 4 Tab × 5-6 ≈ 20+ | 4 Tab + 5-6 viz/Tab | 10-15% | 堆叠面积 + 热力图 + 玫瑰图 + GIS | #0A1F3D 深海军蓝 + #D4AF37 金色 | 极高（10px 字号） | 5 | dark-blue KPI-dense bank-true |
| Smartbi 信用卡 | wiki.smartbi.com.cn/.../83697494 | 5 + TAB 组件 | 单页 4-5 viz + 多页签 | 20-25% | 排行榜 + 地图 + 嵌套环 + 雷达 + Tab | #5DECEC 青色 + #2A3F5F 深蓝 | 中 | 5 | tab-heavy Chinese-form font-spec |
| Superset 财务 | padiso.co/blog/.../financial-reporting | 5 大模块多页 | 6-10 viz + filter bar | 25-30% | BigNumber delta + 折线 + 地图 + Sankey | #1FA8C9 青 + #FF7F0E 橙 | 中（6-8 viz/页） | 3 | open-source filter-bar ECharts-rendered |
| Metabase 销售 | metabase.com/dashboards/sales-teams | 4 + Tab + Q&A | ~6 viz 单页 | 8-10% | BigNumber + 折线 + 地图 + Donut + Top10 | #509EE3 蓝 + #88BF21 绿 | 中低 | 1 | minimal QnA-friendly blue-accent |

---

## §2 按列汇总（每个维度最强）

### 2.1 模块数最多
**FineBI 银行驾驶舱** 胜出（4 Tab × 5-6 ≈ 20+ viz），最完整的多 Tab 模板。但对本项目"6 模块"反而是**警示**——模块太多反而降低月度更新可持续性，本项目应保持 6 模块不变。

### 2.2 章节深度最深
**FineBI 银行 + Superset** 并列——前者靠 Tab 切 4 视角，后者靠 doc post 解释数据模型。本项目借鉴：Tab 切视角的"未来可扩展性"提示，doc post 不可借鉴（违反 §6 不写文档）。

### 2.3 叙述占比最重（讲故事最多）
**Superset (25-30%) > Smartbi (20-25%) > FineBI HR (15-20%)**——国内 BI + 开源 BI 都比英文 BI 更强调文字解读。**本项目当前叙述占比约 5%（shanjinki 模式），可考虑在 M-1 KPI 行 + M-6 客户经理模块加 1-2 句"看图说话"短文案**（写在 Excel metadata，不增加复杂度）。

### 2.4 图表类型最多样
**FineBI 银行（堆叠面积 + 热力图 + 玫瑰图 + GIS + 仪表盘）胜出**——本项目应至少**支持堆叠面积（趋势模块 M-3）+ 玫瑰图（M-6 客户经理画像）** 两种 shanjinki 没有的图表。

### 2.5 主色 hex 最"银行"
**FineBI 银行（#0A1F3D 深海军 + #D4AF37 金）= 5/5 银行感**——本项目可选增加 `bank-dark` style，颜色直接复用 FineBI 的银行驾驶舱色值。

### 2.6 信息密度最高
**Tableau Finance + FineBI 银行** —— 都接近可视化极限。本项目应是**中等密度**（页眉 5 KPI + 主体 5-6 图表 + 页脚 1 行动作建议），密度太高反而让领导"看不过来"。

### 2.7 银行感最强
**FineBI 银行（5/5）+ Smartbi 信用卡（5/5）**——两者都用了真实银行术语（存款/贷款/逾期率/信用卡卡种）。本项目作为 HR 月报**不需要 5/5 银行感**（HR 不严格等于银行术语），但 M-6 客户经理模块**应使用"客户经理数 / 经理人均业绩 / Top 10 客户经理"等准银行术语**。

---

## §3 跨 demo 模式（出现 ≥3 次）

### 模式 1：顶部 4-6 个 KPI 横排
出现 demo：**Tableau HR + Tableau Finance + PowerBI HR + FineBI HR + FineBI 银行 + Smartbi + Superset + Metabase（8/8 全部出现）**
→ **确认本项目 M-1（5 KPI 顶部横排）是绝对标准**。可大胆实现，无需优化。

### 模式 2：时间序列全宽大图（趋势模块）
出现 demo：**Tableau Finance + FineBI HR + FineBI 银行 + Superset（4/8）**
→ 本项目 M-3 趋势模块**必须分配至少 100% 宽度**，不能用 50% 宽度挤在边角。

### 模式 3：业务解读段落（图表下方 1-2 句）
出现 demo：**FineBI HR + FineBI 银行 + Smartbi + Superset（4/8，全是国内 BI + 开源）**
→ **强烈建议本项目加**：每个 viz 卡片下方放 12-16 字"看图说话"。Excel 数据 schema 加 `metadata_text` 字段即可零成本实现。

### 模式 4：过滤切片器（侧边或顶部）
出现 demo：**Tableau HR + Tableau Finance + PowerBI HR + Superset + Metabase（5/8）**
→ **本项目应避免**——违反"双击即用"原则。但**未来可以增加一个"按部门筛选"的简单 `<select>`**，作为可选 v2.0 增强。

### 模式 5：BigNumber + 同比涨幅 (↑↓%)
出现 demo：**Tableau Finance + PowerBI HR + Superset（3/8，但假设有同比数据）**
→ **本项目暂不引入**——Excel 数据契约 (§8) 没有定义同比字段，M-1 KPI 卡保持本期绝对值即可。

### 模式 6：Tab 多页签切换
出现 demo：**PowerBI HR + Smartbi + Superset + Metabase（4/8）**
→ **可借鉴但谨慎**：本项目当前是单页 6 模块连续滚动，加 Tab 反而破坏"一屏看完"的汇报感。若加，**单顶层 Tab 即可**（"本月 / 上月"对比），不做多 Tab。

---

## §4 国内 vs 国际 BI 差异

样本分布：
- **国内 BI（3）**：FineBI HR + FineBI 银行 + Smartbi
- **国际 BI（5）**：Tableau HR + Tableau Finance + PowerBI HR + Superset + Metabase

| 维度 | 国内 BI 倾向 | 国际 BI 倾向 |
|---|---|---|
| 文字解读 | **必有**（15-25% 占比，业务叙事层） | 极弱（<5%，靠 viz 自解释） |
| 中文标题 | **默认** | 全英文 |
| 配色 | 偏**深蓝/青色/金色**（银行/政府色系） | 偏**Tableau 默认蓝 + 橙** |
| Tab 切换 | **常用**（业务/风险/用户/服务 4 Tab 是标配） | 较少（单页多 viz 为主） |
| 配置文档 | **详尽**（字段级字号 / 颜色 / 字体） | 极简（标注 viz 类型即可） |
| 多层级权限 | **强调**（总行/分行/支行 + 用户权限表） | 弱（单一用户视角） |
| 字段配色 | **统一 token 字典**（"字号 16、微软雅黑、加粗、#FFFFFF"） | CSS reset |
| 数据来源假设 | Excel/CSV/数据库混合 | 数据库连接优先 |
| AI 自然语言查询 | **标配**（FineBI/Smartbi 都有 Q&A 框） | Power BI 有，Superset 实验性，Metabase 早期 |
| 中国地图 GIS | **标配**（Smartbi 信用卡 demo） | 默认 Tableau mapbox |

### 关键借鉴点（针对本项目银行 HR 中文场景）：

1. **加深蓝主色（#1A3A6E 或 #0A1F3D）+ 金色高亮（#D4AF37）**——比 shanjinki 默认的"Editorial Brief 米色"更银行
2. **每个图表下方加 12-16 字"看图说话"**——国内 BI 标配，本项目零成本可加
3. **用 CSS conic-gradient 实现"客户经理玫瑰图"**——国内 BI 特有 viz，shanjinki 18 styles 没覆盖
4. **预留"按支行筛选"的 dropdown 接口**——国内 BI 强调多层级权限，本项目 v1.3 可不实现但要在 viz/ 下留 stub

### 关键避坑点：

1. **不引入 AI 自然语言 Q&A**——国内 BI 标配但本项目 §6 YAGNI 黑名单
2. **不引入中国地图 GIS**——Excel 数据契约 (§8) 无"省份"字段，强行加会让数据 schema 爆炸
3. **不引入多层级权限**——本期单用户视角
4. **不做国内 BI 的"详尽配置文档"**——本项目要"0 配置",用户用月度工作流跑 `python build.py` 即可

---

## §5 不适合本项目的模式（跨 demo 警示）

### 警示 1：依赖外部 server / 数据库（出现在 8/8 全部）
**Tableau Online、PowerBI Online、FineBI 服务端、Smartbi 服务端、Superset server、Metabase server**——全部违反 §2 单文件 HTML 完全离线原则。本项目是**反 BI 工具模式**，只借鉴 viz 模式。

### 警示 2：基于同比/月环比字段假设（出现在 5/8）
**Tableau Finance、PowerBI HR、Superset 等都默认数据含 SPLY 字段**——本项目 §8 数据契约只有本期 + 上期 2 列对比，没有完整时间序列 + 同比字段。**M-1 KPI 卡不要强加百分比涨跌箭头**——用绝对值最稳妥。

### 警示 3：filter dropdown + 实时交互（出现在 5/8）
**Tableau / PowerBI / Superset 都强依赖 filter**——本项目"双击即用"零配置原则下，filter 是反模式。仅 v2.0 才考虑。

### 警示 4：10px 极小字号（FineBI 银行）
中国 BI 厂商习惯为 LED 大屏做极致字号压缩。但本项目是桌面浏览器 + 邮件分发，**最小字号 ≥12px**。

### 警示 5：登录 / 权限 / 多用户（国内 BI 强调）
**本项目单用户场景**，不做登录页、不做权限切换。Excel 数据全部 read-only 嵌入 HTML。

### 警示 6：自然语言 AI Q&A 框（FineBI / PowerBI / 国内 BI 标配）
**违反 §6 YAGNI 黑名单**。本项目用户是 HR 月度填 Excel 的同事，不是数据分析师，自然语言查询反而增加心智负担。

---

## §6 综合建议（4 条）

1. **M-1 KPI 行加 "看图说话" 文案**（**国内 BI 模式**）
   每个 KPI 卡下方 12-16 字说明，由 Excel metadata `metric_note` 字段提供。零 HTML 改动，只改 schema。

2. **预留 `bank-dark` style 选项**（**FineBI 银行模式**）
   主色 #0A1F3D + 高亮 #D4AF37，作为可选主题供用户切换。

3. **M-3 趋势模块 100% 全宽**（**国际 + 国内一致模式**）
   不做任何 50% 宽度挤压，时间序列图必须独占整行。

4. **M-6 客户经理模块用 CSS conic-gradient 玫瑰图**（**国内 BI 特有**）
   把饼图扇区延伸半径，shanjinki 18 styles 没有，本项目差异化亮点。

---

## §7 参考资源

- 8 个 demo 详细观察：见 `wide-*.md` 8 个文件
- 已下载 demo：`shanjinki-HR-demo.html`、`shanjinki-finance.html`、`shanjinki-sales.html`、`sven-bo-demo.html`
- 项目技术约束：CLAUDE.md §4（不许改选型）+ §6（Anti-Patterns 黑名单）
