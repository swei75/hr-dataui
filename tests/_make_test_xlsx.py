"""生成测试 Excel。运行: python tests/_make_test_xlsx.py [out_path]

每行带 'section' 列 → 对应 mapping.py 的 data_key。Adapter 按此过滤。
"""
import sys
from pathlib import Path
import openpyxl


def make_test_xlsx(out_path: Path) -> None:
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # 配置
    ws = wb.create_sheet("配置")
    ws.append(["key", "value"])
    ws.append(["报告标题", "人力资源管理数据驾驶舱"])
    ws.append(["报告期", "2026年5月"])
    ws.append(["机构名", "XX 银行"])
    ws.append(["主色", "#1e5baa"])

    # ============= M-1 组织架构 =============
    ws = wb.create_sheet("组织架构")
    ws.append(["section", "region", "branch", "count", "status"])
    for region, branch, count in [
        ("总行本部", "一级部门", 28),
        ("总行本部", "二级部门", 13),
        ("总行直属", "一级部门", 2),
        ("广州地区", "广州分行", 37),
        ("广州地区", "海珠中心支行", 22),
        ("广州地区", "天河中心支行", 14),
        ("广州地区", "白云中心支行", 12),
        ("广州地区", "开发区中心支行", 11),
        ("广州地区", "增城中心支行", 4),
        ("广州地区", "南沙分行", 5),
        ("广州地区", "科技支行", 1),
        ("广州地区", "行总营业部", 1),
        ("异地地区", "深圳分行", 12),
        ("异地地区", "佛山分行", 12),
        ("异地地区", "南京分行", 9),
        ("异地地区", "惠州分行", 7),
        ("异地地区", "江门分行", 6),
        ("异地地区", "中山分行", 8),
        ("异地地区", "肇庆分行", 4),
        ("异地地区", "东莞分行", 8),
        ("异地地区", "横琴分行", 4),
        ("异地地区", "清远分行", 2),
    ]:
        ws.append(["region_tree", region, branch, count, "营业"])

    # ============= M-2 员工情况 =============
    ws = wb.create_sheet("员工情况")
    ws.append(["section", "label", "value", "sub"])
    ws.append(["headcount_total", "正式员工", 5901, "含劳务派遣 6589"])
    ws.append(["headcount_operating", "经营机构", 4709, "占 79.80%"])
    ws.append(["headcount_ratio", "前中后台", "1:0.73", "前 3254 : 中后台 2372"])
    for label, value in [("30岁以下", 1526), ("31-40岁", 2851), ("41-50岁", 1123), ("51岁以上", 401)]:
        ws.append(["age_distribution", label, value, ""])
    for label, value in [("硕士及以上", 1031), ("本科", 4514), ("专科", 326), ("专科以下", 30)]:
        ws.append(["edu_distribution", label, value, ""])
    for label, value in [("男", 2717), ("女", 3184)]:
        ws.append(["gender_distribution", label, value, ""])
    for label, value in [("对公客户经理", 850), ("个人客户经理", 390), ("个贷客户经理", 359), ("微贷客户经理", 93)]:
        ws.append(["customer_managers", label, value, ""])

    # ============= M-3 人员优化 =============
    ws = wb.create_sheet("人员优化")
    ws.append(["section", "label", "value", "sub"])
    ws.append(["social_hire_total", "社招入职", 34, "2026 年以来"])
    ws.append(["campus_hire_total", "校招签约", 721, "已签约/签约中"])
    ws.append(["exit_total", "累计退出", 202, "1-5 月"])
    for label, value in [("全年目标", 659), ("已签约", 721), ("管培生", 45), ("金融科技岗", 54), ("分行管培生", 112), ("英才岗", 469)]:
        ws.append(["campus_funnel", label, value, ""])
    ws.append(["teng_long_huan_yao", "腾笼换鸟", 201, "全年任务 410"])
    ws.append(["poor_perf_exit", "绩差退出", 44, "目标 50%（96人）"])

    # ============= M-4 干部队伍 =============
    ws = wb.create_sheet("干部队伍")
    ws.append(["section", "label", "value", "sub"])
    ws.append(["headcount_total", "中层总职数", 211, ""])
    ws.append(["headcount_filled", "已配备", 194, "92%"])
    ws.append(["headcount_vacancy", "空缺", 17, "8%"])
    for row in [
        ("config_table", "市管领导干部", 8, 8, 0),
        ("config_table", "高管人员", "/", 6, "/"),
        ("config_table", "派驻纪检监察组", 6, 3, 3),
        ("config_table", "中层正职", 54, 50, 4),
        ("config_table", "中层副职", 157, 144, 13),
        ("config_table", "总行部门", 100, 93, 7),
        ("config_table", "经营机构", 111, 101, 10),
    ]:
        ws.append(list(row))
    for label, value in [("提拔", 94), ("降免职", 14), ("到龄转岗", 13)]:
        ws.append(["adjustments", label, value, "人次"])

    # ============= M-5 考核薪酬 =============
    ws = wb.create_sheet("考核薪酬")
    ws.append(["section", "label", "value", "sub"])
    ws.append(["salary_total", "2025 年工资总额", "15 亿元", ""])
    ws.append(["salary_per_capita", "人均薪酬", "24.3 万元", "含预发 2026 开门红 0.3 亿"])
    ws.append(["pension_balance", "企业年金余额", "17.44 亿元", "2026.5"])
    ws.append(["tou_lang_count", "头狼评选", 129, "2026 Q1"])
    ws.append(["monitoring", "监测人数", 95, "班子成员"])
    ws.append(["monitoring", "监测人次", 113, "业绩监测"])
    ws.append(["monitoring", "黑榜人数", 15, "督导函"])
    ws.append(["monitoring", "黑榜人次", 16, "首次触发"])

    # ============= M-6 培训赋能 =============
    ws = wb.create_sheet("培训赋能")
    ws.append(["section", "label", "value", "sub"])
    ws.append(["training_total", "能力大提升项目", 983, ""])
    ws.append(["key_projects", "重点培训项目", 55, ""])
    ws.append(["exam_count", "上岗资格人次", 1878, "35 场次"])
    ws.append(["key_projects_pct", "重点项目执行率", 0.5806, "已完成 32/55"])
    for label, value in [
        ("董事会办公室", 100), ("私人银行部", 100), ("金融同业部", 100), ("金融市场部", 100),
        ("战略客户部", 100), ("消保部", 100), ("机关纪委", 100), ("安全保卫部", 100),
        ("金融科技部", 0), ("内控合规部", 0), ("运营管理部", 14.29),
    ]:
        ws.append(["dept_execution", label, value, ""])

    out_path.parent.mkdir(exist_ok=True)
    wb.save(out_path)
    print(f"Created {out_path}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/test.xlsx")
    make_test_xlsx(target)
