"""HR-UI build entry point. Usage: python build.py"""
import json
from pathlib import Path

from extractors.reader import read_config, read_workbook
from extractors.mapping import MODULES
from extractors.drills import load_drill_data
from composer import render_module
from templates.base import render_page, render_module_placeholders


def find_data_file() -> Path:
    """查找 data/ 目录下唯一 .xlsx 文件。"""
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

    # 加载所有钻取数据
    drill_data = {}
    for module_cfg in MODULES.values():
        for section in module_cfg.get("sections", []):
            if section.get("drillable"):
                dk = section["data_key"]
                drill_data[dk] = load_drill_data(dk, raw_data)

    # 拼装 6 模块
    modules_html = []
    for module_key, module_cfg in sorted(
        MODULES.items(), key=lambda x: x[1].get("order", 99)
    ):
        module_data = raw_data.get(module_key, {})
        modules_html.append(render_module(module_key, module_cfg, module_data))

    # 加载 Alpine.js (inline)
    alpine_path = Path("vendor/alpine.min.js")
    alpine_inline = alpine_path.read_text(encoding="utf-8") if alpine_path.exists() else ""

    title = config.get("报告标题", "人力资源管理数据驾驶舱")
    body = "\n".join(modules_html)
    html = render_page(
        body,
        title=title,
        alpine=alpine_inline,
        drill_data=json.dumps(drill_data, ensure_ascii=False),
    )

    output.write_text(html, encoding="utf-8")
    size_kb = output.stat().st_size / 1024
    print(f"Built {output} ({size_kb:.1f} KB)")

    if size_kb > 50:
        print(f"WARNING: exceeds 50KB budget", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
