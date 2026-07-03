"""字段映射 - 按分组定义 dashboard 结构。

每模块的 groups 列表：分组名 + span（4/6/8/12）。
extra_sheets：额外多列 sheet（table 渲染）。
"""

MODULES = {
    "M-1 组织架构": {
        "title": "一、组织架构",
        "icon": "🏛",
        "order": 1,
        "sub": "总行 28 部 / 分行 24 家 / 网点 183 家",
        "groups": [
            {"name": "总行架构", "span": 6},
            {"name": "全行机构", "span": 6},
            {"name": "营业状态", "span": 6},
            {"name": "广州地区", "span": 6},
            {"name": "异地地区", "span": 12},
        ],
    },
    "M-2 员工情况": {
        "title": "二、员工基本情况",
        "icon": "👥",
        "order": 2,
        "sub": "正式员工 5,901 人 · 平均年龄 36 岁",
        "groups": [
            {"name": "合计总数", "span": 12},
            {"name": "员工构成", "span": 6},
            {"name": "前后台", "span": 6},
            {"name": "年龄分布", "span": 6},
            {"name": "学历分布", "span": 6},
            {"name": "性别比例", "span": 6},
            {"name": "客户经理", "span": 6},
            {"name": "客服经理", "span": 6},
        ],
    },
    "M-3 人员优化": {
        "title": "三、人员优化情况",
        "icon": "📉",
        "order": 3,
        "sub": "引进 755 人 · 退出 202 人 · 劳动仲裁 15 起",
        "groups": [
            {"name": "社招", "span": 6},
            {"name": "校招阶段", "span": 6},
            {"name": "校招岗位", "span": 6},
            {"name": "退出", "span": 6},
            {"name": "退出职级", "span": 6},
            {"name": "腾笼换鸟", "span": 12},
            {"name": "绩差退出", "span": 12},
            {"name": "劳动仲裁", "span": 12},
        ],
    },
    "M-4 干部队伍": {
        "title": "四、干部队伍建设",
        "icon": "🎖",
        "order": 4,
        "sub": "中层 211 · 已配 194 · 空缺 17",
        "groups": [
            {"name": "中层总览", "span": 12},
            {"name": "配备情况", "span": 6},
            {"name": "配备-总行", "span": 6},
            {"name": "配备-经营", "span": 6},
            {"name": "配备-正职", "span": 6},
            {"name": "配备-副职", "span": 6},
            {"name": "调整情况", "span": 12},
        ],
        "extra_sheets": [("M-4 干部职数表", 12)],
    },
    "M-5 考核薪酬": {
        "title": "五、考核薪酬",
        "icon": "💰",
        "order": 5,
        "sub": "工资总额 15 亿 · 人均 24.3 万 · 头狼 129 人",
        "groups": [
            {"name": "薪酬", "span": 6},
            {"name": "年金", "span": 6},
            {"name": "医疗", "span": 6},
            {"name": "监测", "span": 6},
            {"name": "头狼", "span": 6},
        ],
    },
    "M-6 培训赋能": {
        "title": "六、培训赋能",
        "icon": "📚",
        "order": 6,
        "sub": "能力大提升 983 场 · 重点 55 项 · 资格考 1878 人次",
        "groups": [
            {"name": "培训总量", "span": 6},
            {"name": "重点项目", "span": 6},
            {"name": "执行率", "span": 6},
            {"name": "100% 部门", "span": 6},
            {"name": "末位部门", "span": 6},
            {"name": "资格考", "span": 6},
        ],
    },
}


# 顶部 KPI 长条（从 Excel 配置 sheet 读 + 硬编码核心数字）
TOP_KPIS = [
    {"label": "正式员工", "value": 5901, "sub": "人 · 2026年5月"},
    {"label": "客户经理", "value": 1692, "sub": "人 · 占 28.7%"},
    {"label": "中层干部", "value": 211, "sub": "人 · 已配 194"},
    {"label": "工资总额", "value": "15 亿", "sub": "元 · 2025 年度"},
    {"label": "培训项目", "value": 983, "sub": "场 · 55 重点"},
    {"label": "头狼评选", "value": 129, "sub": "人 · 2026 Q1"},
]
