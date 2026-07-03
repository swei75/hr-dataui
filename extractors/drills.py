"""钻取数据加载。函数签名: load(key, raw_data) -> dict (JSON-serializable)"""
from typing import Any

from .mapping import MODULES


def _find_section(key: str) -> dict | None:
    for module_cfg in MODULES.values():
        for section in module_cfg.get("sections", []):
            if section.get("data_key") == key:
                return section
    return None


def _find_sheet_for_key(key: str) -> str:
    """通过 data_key 找到对应 sheet 名。"""
    mapping = {
        "region_tree": "组织架构",
        "branch_status": "组织架构",
        "headcount_overview": "员工情况",
        "age_distribution": "员工情况",
        "edu_distribution": "员工情况",
        "gender_distribution": "员工情况",
        "customer_managers": "员工情况",
        "social_hire": "人员优化",
        "campus_hire": "人员优化",
        "exit_overview": "人员优化",
        "teng_long_huan_yao": "人员优化",
        "poor_perf_exit": "人员优化",
        "config_table": "干部队伍",
        "adjustments": "干部队伍",
        "salary_overview": "考核薪酬",
        "pension": "考核薪酬",
        "monitoring": "考核薪酬",
        "tou_lang": "考核薪酬",
        "training_overview": "培训赋能",
        "key_projects": "培训赋能",
        "dept_execution": "培训赋能",
    }
    return mapping.get(key, "组织架构")


def load_drill_data(key: str, raw_data: dict) -> dict:
    """按 data_key 加载钻取数据。返回 JSON 序列化友好的 dict。"""
    section = _find_section(key)
    if not section:
        return {"error": f"unknown drill key: {key}"}

    sheet_name = _find_sheet_for_key(key)
    rows = raw_data.get(sheet_name, [])
    return {"key": key, "rows": rows, "count": len(rows)}
