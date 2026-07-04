# hr-dataui · 月度更新工作流

把 .docx 报告转成单文件 HTML 仪表盘。每月 30 分钟搞定。

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
- **改哪个 sheet / 哪行 / 哪个"数值"列**
- 其他 6 列**不动**
- 不要改 sheet 名

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
Built output/index.html (69.3 KB)
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

## 添加新 viz 类型

1. 在 `viz/` 创建新文件 `xxx.py`，函数签名：
   ```python
   def render(data: list, options: dict) -> str:
       """返回 HTML 片段"""
   ```
2. 在 `viz/__init__.py` 的 `VIZ_REGISTRY` 注册
3. 在 `composer.py` 的 `_pick_viz()` 添加选择逻辑
4. 在 `templates/base.py` 添加对应 CSS

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
       "groups": [{"name": "分组1", "span": 6}, ...],
   }
   ```
3. `python build.py`

---

## 故障排查

| 现象 | 排查 |
|---|---|
| `FileNotFoundError: data/ 目录下无 .xlsx 文件` | 把 Excel 放到 `data/` 目录 |
| `KeyError: 'M-X 模块名'` | Excel 的 sheet 名和 `mapping.py` 的 `MODULES` key 不一致 |
| 文件 > 100KB | 检查 viz 渲染是否漏 `<div class="empty">` 而渲染了大量空数据 |
| M-4 干部职数表不显示 | 检查 `mapping.py` 的 `extra_sheets` 列表 |
| 中文字符乱码 | 确认 Excel 是 .xlsx 格式（不是 .xls），保存时不要转 CSV |
