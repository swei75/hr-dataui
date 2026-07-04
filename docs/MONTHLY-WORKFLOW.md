# 月度更新工作流

> 这是**操作手册**——HR 月报制作人每月跑一次需要的所有步骤。
> 项目介绍见 [README.md](../README.md)，扩展指南见 [README §扩展指南](../README.md#扩展指南)。

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

**8 个 sheet**：
- `配置`：报告标题、报告期、机构名、主色
- `M-1 组织架构` / `M-2 员工情况` / `M-3 人员优化` / `M-4 干部队伍` / `M-5 考核薪酬` / `M-6 培训赋能`
- `M-4 干部职数表`（多列表，4 列结构）

**7 列结构**（每个数据 sheet）：
| 分组 | 名称 | 数值 | 单位 | 备注 | 排序 | is_total |

- 只改**数值列**，其他 6 列**不动**
- 不要改 sheet 名
- 详见 [README §数据契约](../README.md#数据契约)

**修改示例**（M-2 员工情况）：

| 分组 | 名称 | 数值 | 单位 | 备注 | 排序 | is_total |
|---|---|---|---|---|---|---|
| 合计总数 | 正式员工 | **6100** ← 改这个 | 人 | | 2 | TRUE |
| 客户经理 | 对公客户经理 | **870** ← 改这个 | 人 | | 2 |  |

### Step 2: 运行 build

```bash
python build.py
```

**输出**：
```
Built output/index.html (XX.X KB)
```

### Step 3: 双击验证

```bash
open output/index.html   # macOS
```

**检查清单**：
- [ ] 6 个模块标题正确
- [ ] donut / bar / KPI 都正常显示
- [ ] M-4 干部职数表能展开看到
- [ ] 报告期 / 机构名正确（来自 配置 sheet）
- [ ] 文件 ≤ 100KB

### Step 4: 分发

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
4. `python build.py`

dashboard 会自动在"校招岗位"分组里多显示一个 bar。

---

## 故障排查

| 现象 | 排查 |
|---|---|
| `FileNotFoundError: data/ 目录下无 .xlsx 文件` | 把 Excel 放到 `data/` 目录 |
| `KeyError: 'M-X 模块名'` | Excel 的 sheet 名和 `mapping.py` 的 `MODULES` key 不一致 |
| 文件 > 100KB | 检查 viz 渲染是否漏 `<div class="empty">` 而渲染了大量空数据 |
| M-4 干部职数表不显示 | 检查 `mapping.py` 的 `extra_sheets` 列表 |
| 中文字符乱码 | 确认 Excel 是 .xlsx 格式（不是 .xls），保存时不要转 CSV |
| 浏览器空白 | Console 看 inline JS/CSS 是否正确（无 CDN 加载问题） |
| 数据不显示 | Console 看 `window.HR_DATA` 内容 |
| 移动端布局错 | 检查 CSS 媒体查询断点（980px/640px） |
| 图表不渲染 | 检查 CSS 类名是否匹配样式定义 |
