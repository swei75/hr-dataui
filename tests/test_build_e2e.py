"""E2E 测试：build.py 用 test.xlsx 生成 output/index.html，验证结构。"""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_build_runs():
    """build.py 能跑通并生成 output/index.html。"""
    # 确保 test.xlsx 存在
    if not (PROJECT_ROOT / "data" / "test.xlsx").exists():
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "tests" / "_make_test_xlsx.py"), "data/test.xlsx"],
            check=True, cwd=PROJECT_ROOT,
        )

    result = subprocess.run(
        [sys.executable, "build.py"],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0, f"build failed: {result.stderr}"
    assert "Built" in result.stdout

    output = PROJECT_ROOT / "output" / "index.html"
    assert output.exists()
    return output


def test_output_has_6_modules():
    """输出含 6 个模块。"""
    output = PROJECT_ROOT / "output" / "index.html"
    if not output.exists():
        test_build_runs()
    html = output.read_text(encoding="utf-8")
    for title in ["一、组织架构", "二、员工基本情况", "三、人员优化情况", "四、干部队伍建设", "五、考核薪酬", "六、培训赋能"]:
        assert title in html, f"missing module: {title}"


def test_output_has_no_external_deps():
    """输出无 CDN / 外部 fetch。"""
    html = (PROJECT_ROOT / "output" / "index.html").read_text(encoding="utf-8")
    for bad in ["cdn.jsdelivr.net", "googleapis.com", "unpkg.com"]:
        assert bad not in html, f"found external dep: {bad}"


def test_output_size_under_100kb():
    """文件 ≤ 100KB。"""
    size = (PROJECT_ROOT / "output" / "index.html").stat().st_size
    assert size <= 100 * 1024, f"output is {size} bytes, exceeds 100KB budget"


def test_m4_table_renders():
    """M-4 干部职数表 多列表正确渲染。"""
    html = (PROJECT_ROOT / "output" / "index.html").read_text(encoding="utf-8")
    assert "干部职数表" in html
    assert "市管领导干部" in html
    assert "<table" in html


def test_data_composition_uses_donut():
    """组成关系用 donut 表达。"""
    html = (PROJECT_ROOT / "output" / "index.html").read_text(encoding="utf-8")
    assert html.count("donut-svg") >= 5
