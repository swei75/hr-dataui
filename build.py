"""hr-dataui build entry point. Usage: python build.py"""
from pathlib import Path

from extractors.reader import read_config, read_workbook, write_prev_sheet
from extractors.mapping import MODULES, TOP_KPIS
from composer import render_module, render_kpi_strip
from templates.base import render_page


def find_data_file() -> Path:
    data_dir = Path("data")
    if not data_dir.exists():
        raise FileNotFoundError("data/ 目录不存在")
    files = list(data_dir.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError("data/ 目录下无 .xlsx 文件")
    return files[0]


def main() -> int:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output = output_dir / "index.html"

    data_file = find_data_file()
    config = read_config(data_file)
    raw_data = read_workbook(data_file)
    prev_data = raw_data.get("prev", {})

    # 拼装 6 模块（extra_sheets 传 raw_data + v1.4 prev_records）
    modules_html = []
    for module_key, module_cfg in sorted(MODULES.items(), key=lambda x: x[1].get("order", 99)):
        module_data = raw_data.get(module_key, [])
        prev_records = prev_data.get(module_key, [])
        modules_html.append(render_module(module_key, module_cfg, module_data, extra_sheets=raw_data, prev_records=prev_records))

    # 顶部 KPI 长条
    kpi_strip = render_kpi_strip(TOP_KPIS)

    title = config.get("报告标题", "人力资源管理数据驾驶舱")
    report_date = config.get("报告期", "2026年5月")
    body = kpi_strip + "\n" + "\n".join(modules_html)
    html = render_page(body, title=title, report_date=report_date)

    output.write_text(html, encoding="utf-8")
    size_kb = output.stat().st_size / 1024
    print(f"Built {output} ({size_kb:.1f} KB)")

    # v1.4: 把当前数据写入 _prev sheet（下一次构建用于 delta 计算）
    write_prev_sheet(data_file, raw_data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
