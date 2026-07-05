# 月度更新工作流

> 这是**操作手册**——HR 月报制作人每月跑一次需要的所有步骤。
> 项目介绍见 [README.md](../README.md)，扩展指南见 [CLAUDE.md §扩展](../CLAUDE.md)。

---

## 一次性环境准备

```bash
cd hr-dataui
pip install -r requirements.txt   # 装 pandas + openpyxl
```

> 整个项目只需要这两个 Python 库。

---

## 每月更新流程

### Step 1: 改 Excel（最关键）

打开 `data/` 目录下的 .xlsx 文件（如 `人力资源管理数据驾驶舱_2026年6月.xlsx`）。

**v1.5：9 个 sheet**：
- `配置`：报告标题、报告期、机构名、主色
- `M-1 组织架构` / `M-2 员工情况` / `M-3 人员优化` / `M-4 干部队伍` / `M-5 考核薪酬` / `M-6 培训赋能`
- `M-4 干部职数表`（多列结构）
- `_prev`：上期快照（composer 自动维护，**不要手改**）

### Step 2: v1.5 数据契约（10 列）

每个数据 sheet **10 列结构**：

| # | 列 | 用途 | 备注 |
|---|---|---|---|
| 1 | 分组 | 数据分类 | 影响 viz 选择 |
| 2 | 名称 | 显示名 | |
| 3 | **数值** | **主要数字** | **只改这一列** |
| 4 | 单位 | 显示单位 | |
| 5 | 备注 | 可选说明 | |
| 6 | 排序 | 显示顺序 | |
| 7 | is_total | 是否总数行 | TRUE / FALSE |
| 8 | delta | 环比差 | **不要手填**，composer 自动算 |
| 9 | sub_text | 模块级叙述 | 可选 |
| 10 | metric_note | KPI 下方说明 | 可选（12-16 字） |

**修改示例**（M-2 员工情况）：

| 分组 | 名称 | 数值 | 单位 | 备注 | 排序 | is_total | delta | sub_text | metric_note |
|---|---|---|---|---|---|---|---|---|---|
| 合计总数 | 正式员工 | **6100** ← 改这个 | 人 | | 2 | TRUE | | | 较上月增加 12 人 |
| 客户经理 | 对公客户经理 | **870** ← 改这个 | 人 | | 2 | | | | |

**关键约束**：
- 只改**数值列**，其他 9 列**不动**
- 不要改 sheet 名
- 不要手填 delta（composer 自动从 `_prev` 算）

### Step 3: 运行 build

```bash
python build.py
```

**输出**：
```
Built output/index.html (~98KB)
```

### Step 4: 双击验证

```bash
open output/index.html   # macOS
```

**检查清单（v1.5：7 模块独立 viz）**：
- [ ] Dashboard 顶部数字塔（v_hero）：6 项指标 + 6 色左侧 border
- [ ] M-1 组织架构：v1 风格（6 KPI + 段落）
- [ ] M-2 员工情况：v11 风格（4 KPI + 5 stacked + 8 grid）
- [ ] M-3 人员优化：v_hr 融合（gauge + flow + dual-bar + 3 排名，含 Top 3）
- [ ] M-4 干部队伍：v2 分类树（4 大类 + 中层分支）
- [ ] M-5 考核薪酬：v1 财务大卡（5 卡 + sparkline）
- [ ] M-6 培训赋能：v_train（v1 顶 + v8 主体）
- [ ] M-4 干部职数表能展开看到
- [ ] 报告期 / 机构名正确（来自 `配置` sheet）
- [ ] 主色为米色红棕 `#9f6b44`
- [ ] 文件 ≤ 100KB

### Step 5: 分发

`output/index.html` 是单文件，**可直接发邮件、传 U 盘、内网分享**。
接收方**双击即用**，无任何依赖。

---

## 添加新数据点

例如：新增 "M-3 校招-博士" 类别

1. 打开 `M-3 人员优化` sheet
2. 找到 `校招岗位` 分组
3. 末尾追加一行：
   - 分组：`校招岗位`
   - 名称：`博士`
   - 数值：`5`
   - 单位：`人`
   - 备注：（可选）
   - 排序：0
   - is_total：（留空）
   - delta：（留空，composer 自动算）
   - sub_text：（留空）
   - metric_note：（留空）
4. `python build.py`

dashboard 会自动在 M-3 模块的 v_hr 融合 viz 中显示这个新类别。

---

## 添加新模块

1. 在 `data/*.xlsx` 添加新 sheet
2. 在 `extractors/mapping.py` 的 `MODULES` 加配置：
   ```python
   "M-7 新模块": {
       "title": "七、新模块",
       "icon": "🆕",
       "order": 7,
       "sub": "描述",
       "viz_style": "v_xxx",  # 或 is_v_xxx_style: True
       "groups": [{"name": "分组1", "span": 6}, ...],
   }
   ```
3. 在 `viz/` 创建对应 viz 函数（或复用现有 v1/v2/v8/v11）
4. 在 `composer.py` 的风格分支添加调用
5. 在 `templates/base.py` 添加对应 CSS
6. `python build.py`

---

## 故障排查

| 现象 | 排查 |
|---|---|
| `FileNotFoundError: data/ 目录下无 .xlsx 文件` | 把 Excel 放到 `data/` 目录 |
| `KeyError: 'M-X 模块名'` | Excel 的 sheet 名和 `mapping.py` 的 `MODULES` key 不一致 |
| 文件 > 100KB | 检查 viz 渲染是否漏 `<div class="empty">` 而渲染了大量空数据 |
| M-4 干部职数表不显示 | 检查 `mapping.py` 的 `extra_sheets` 列表 |
| delta 不显示 | 检查 `_prev` sheet 是否存在；首次构建 delta 为空是正常的 |
| 主色不是米色红棕 | 检查 `templates/base.py` 的 `--primary` CSS 变量 |
| 某模块 viz 风格不对 | 查 `extractors/mapping.py` 的 `viz_style` / `is_v_*_style` 字段 |
| 中文字符乱码 | 确认 Excel 是 .xlsx 格式（不是 .xls），保存时不要转 CSV |
| 浏览器空白 | Console 看 inline JS/CSS 是否正确（无 CDN 加载问题） |
| 数据不显示 | Console 看 `window.HR_DATA` 内容 |
| 移动端布局错 | 检查 CSS 媒体查询断点（1100/768/480） + §5.2 v1.5.21.3 响应式补丁（CLAUDE.md）|
| 图表不渲染 | 检查 CSS 类名是否匹配样式定义 |

---

## 常见问题

**Q: 每月必须改所有 sheet 吗？**
A: 不需要。只想更新某模块 → 只改对应 sheet 的"数值"列，其他 sheet 完全不动。

**Q: delta 列需要手填吗？**
A: **不要**。delta 由 composer 从 `_prev` 快照自动算。每月首次构建时 `_prev` 是空的，delta 也不显示。

**Q: 改了数值后 `_prev` 会自动更新吗？**
A: 是的。composer 在每次 build 末尾把当前 sheet 写入 `_prev`，供下次构建计算环比 delta。

**Q: 删了 `_prev` 会怎样？**
A: 删了之后 delta 全部不显示（首次构建状态）。下次 build 会自动重建 `_prev`。

**Q: 7 个 viz 风格可以混用吗？比如 M-1 用 v11？**
A: 可以，但**不建议**。每个 viz 风格是为特定模块设计的（M-1 v1、M-2 v11、M-3 v_hr...）。混用可能导致布局错乱。

**Q: 输出文件 98KB 接近 100KB 上限，会不会继续变大？**
A: 11 月增加新模块会增加体积。超 100KB 时考虑：删除未用 CSS 变量、合并相近 viz 函数。