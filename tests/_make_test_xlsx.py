"""生成测试 Excel。运行: python tests/_make_test_xlsx.py [out_path]"""
import sys
from pathlib import Path
import openpyxl


def make_test_xlsx(out_path: Path) -> None:
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    # 配置
    ws = wb.create_sheet("配置")
    ws.append(["key", "value"])
    ws.append(["报告标题", "人力资源管理数据驾驶舱（测试）"])
    ws.append(["报告期", "2026年5月"])
    ws.append(["机构名", "XX 银行"])
    ws.append(["主色", "#1E5BAA"])
    # 组织架构
    ws = wb.create_sheet("组织架构")
    ws.append(["区域", "机构", "数量", "状态"])
    ws.append(["广州", "广州分行", 37, "营业"])
    ws.append(["广州", "海珠支行", 22, "营业"])
    ws.append(["广州", "天河支行", 14, "营业"])
    ws.append(["异地", "深圳分行", 12, "营业"])
    ws.append(["异地", "佛山分行", 12, "营业"])
    ws.append(["异地", "南京分行", 9, "营业"])
    # 员工情况
    ws = wb.create_sheet("员工情况")
    ws.append(["维度", "类别", "数量", "占比"])
    ws.append(["年龄", "30岁以下", 1526, 0.2586])
    ws.append(["年龄", "31-40岁", 2851, 0.4831])
    ws.append(["年龄", "41-50岁", 1123, 0.1903])
    ws.append(["年龄", "51岁以上", 401, 0.0680])
    ws.append(["学历", "硕士及以上", 1031, 0.1747])
    ws.append(["学历", "本科", 4514, 0.7650])
    ws.append(["学历", "专科", 326, 0.0552])
    ws.append(["学历", "专科以下", 30, 0.0051])
    ws.append(["性别", "男", 2717, 0.4604])
    ws.append(["性别", "女", 3184, 0.5396])
    ws.append(["客户经理", "对公", 850, 0.5024])
    ws.append(["客户经理", "个人", 390, 0.2305])
    ws.append(["客户经理", "个贷", 359, 0.2122])
    ws.append(["客户经理", "微贷", 93, 0.0550])
    # 人员优化
    ws = wb.create_sheet("人员优化")
    ws.append(["指标", "计划", "实际", "完成率"])
    ws.append(["腾笼换鸟", 410, 201, 0.50])
    ws.append(["绩差退出", 96, 44, 0.46])
    ws.append(["社招入职", 0, 34, 0])
    ws.append(["校招签约", 659, 721, 1.09])
    ws.append(["总退出", 0, 202, 0])
    ws.append(["劳动仲裁", 0, 15, 0])
    # 干部队伍
    ws = wb.create_sheet("干部队伍")
    ws.append(["分类", "总职数", "已配", "空缺"])
    ws.append(["中层正职", 54, 50, 4])
    ws.append(["中层副职", 157, 144, 13])
    ws.append(["总行部门", 100, 93, 7])
    ws.append(["经营机构", 111, 101, 10])
    ws.append(["提拔", 0, 94, 0])
    ws.append(["降免", 0, 14, 0])
    ws.append(["到龄转岗", 0, 13, 0])
    # 考核薪酬
    ws = wb.create_sheet("考核薪酬")
    ws.append(["指标", "数值", "单位"])
    ws.append(["2025年工资总额", 15, "亿元"])
    ws.append(["人均薪酬", 24.3, "万元"])
    ws.append(["2026年1-5月发放", 4.2, "亿元"])
    ws.append(["企业年金余额", 17.44, "亿元"])
    ws.append(["补充医疗节余", 1.9, "亿元"])
    ws.append(["履职监测黑榜", 15, "人次"])
    ws.append(["头狼评选", 129, "人"])
    # 培训赋能
    ws = wb.create_sheet("培训赋能")
    ws.append(["部门/项目", "计划", "完成", "百分比"])
    ws.append(["能力大提升", 983, 983, 1.0])
    ws.append(["重点培训项目", 55, 32, 0.5806])
    ws.append(["董事会办公室", 0, 100, 1.0])
    ws.append(["私人银行部", 0, 100, 1.0])
    ws.append(["金融同业部", 0, 100, 1.0])
    ws.append(["金融科技部", 100, 0, 0.0])
    ws.append(["内控合规部", 100, 0, 0.0])
    ws.append(["运营管理部", 100, 14, 0.1429])
    ws.append(["上岗资格", 35, 1878, 0])

    out_path.parent.mkdir(exist_ok=True)
    wb.save(out_path)
    print(f"Created {out_path}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/test.xlsx")
    make_test_xlsx(target)
