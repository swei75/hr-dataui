"""字段映射 - 按 .docx 内容与重要性映射到 viz。

每 section 指定：
- data_key: 对应 Excel section 列
- span: 6 (half) / 12 (full) / 4 (third)
- type: 留空让 composer 自动检测
"""

MODULES = {
    "组织架构": {
        "title": "一、组织架构",
        "icon": "🏛",
        "order": 1,
        "sub": "总行 28 部 / 分行 24 家 / 网点 183 家",
        "sections": [
            {"key": "headquarters", "title": "总行架构", "type": "stats", "data_key": "headquarters", "span": 6},
            {"key": "branches", "title": "全行机构", "type": "stats", "data_key": "branches", "span": 6},
            {"key": "branch_guangzhou", "title": "广州地区网点（107 家）", "type": "grid", "data_key": "branch_guangzhou", "span": 6},
            {"key": "branch_other", "title": "异地地区网点（76 家）", "type": "grid", "data_key": "branch_other", "span": 6},
        ],
    },
    "员工情况": {
        "title": "二、员工基本情况",
        "icon": "👥",
        "order": 2,
        "sub": "正式员工 5,901 人 · 平均年龄 36 岁",
        "sections": [
            {"key": "headcount", "title": "员工总数与构成", "type": "stats", "data_key": "headcount", "span": 12},
            {"key": "age_dist", "title": "年龄分布", "type": "bar", "data_key": "age_dist", "span": 6},
            {"key": "edu_dist", "title": "学历分布", "type": "bar", "data_key": "edu_dist", "span": 6},
            {"key": "gender_dist", "title": "性别比例", "type": "donut", "data_key": "gender_dist", "span": 4},
            {"key": "customer_managers", "title": "客户经理分类（1692 人）", "type": "bar", "data_key": "customer_managers", "span": 4},
            {"key": "service_managers", "title": "客服经理（1165 人）", "type": "bar", "data_key": "service_managers", "span": 4},
        ],
    },
    "人员优化": {
        "title": "三、人员优化情况",
        "icon": "📉",
        "order": 3,
        "sub": "引进 755 人 · 退出 202 人 · 劳动仲裁 15 起",
        "sections": [
            {"key": "social_hire", "title": "社招入职（34 人）", "type": "stats", "data_key": "social_hire", "span": 4},
            {"key": "campus_hire", "title": "校招签约（721 人）", "type": "stats", "data_key": "campus_hire", "span": 8},
            {"key": "exit", "title": "人员退出（202 人）", "type": "stats", "data_key": "exit", "span": 12},
            {"key": "teng_long", "title": "腾笼换鸟完成情况", "type": "rank", "data_key": "teng_long", "span": 6},
            {"key": "poor_perf", "title": "绩差客户经理退出", "type": "rank", "data_key": "poor_perf", "span": 6},
            {"key": "labor", "title": "劳动仲裁（15 起）", "type": "stats", "data_key": "labor", "span": 12},
        ],
    },
    "干部队伍": {
        "title": "四、干部队伍建设",
        "icon": "🎖",
        "order": 4,
        "sub": "中层 211 · 已配 194 · 空缺 17",
        "sections": [
            {"key": "overview", "title": "中层干部总览", "type": "stats", "data_key": "overview", "span": 12},
            {"key": "position_table", "title": "干部职数与配置", "type": "table", "data_key": "position_table", "span": 12},
            {"key": "adjustments", "title": "新一届党委以来调整（121 人次）", "type": "stats", "data_key": "adjustments", "span": 12},
        ],
    },
    "考核薪酬": {
        "title": "五、考核薪酬",
        "icon": "💰",
        "order": 5,
        "sub": "工资总额 15 亿 · 人均 24.3 万 · 头狼 129 人",
        "sections": [
            {"key": "salary", "title": "薪酬情况", "type": "stats", "data_key": "salary", "span": 6},
            {"key": "pension", "title": "企业年金与补充医疗", "type": "stats", "data_key": "pension", "span": 6},
            {"key": "monitoring", "title": "履职监测与头狼评选", "type": "stats", "data_key": "monitoring", "span": 12},
        ],
    },
    "培训赋能": {
        "title": "六、培训赋能",
        "icon": "📚",
        "order": 6,
        "sub": "能力大提升 983 场 · 重点 55 项 · 资格考 1878 人次",
        "sections": [
            {"key": "training", "title": "培训总量", "type": "stats", "data_key": "training", "span": 4},
            {"key": "key_projects", "title": "重点培训项目（55 项）", "type": "stats", "data_key": "key_projects", "span": 4},
            {"key": "exam", "title": "上岗资格（35 场 · 1878 人次）", "type": "stats", "data_key": "exam", "span": 4},
            {"key": "dept_top", "title": "100% 完成部门（8 个）", "type": "grid", "data_key": "dept_top", "span": 8},
            {"key": "dept_bottom", "title": "执行率排名后三", "type": "rank", "data_key": "dept_bottom", "span": 4},
        ],
    },
}


# 顶部 KPI 长条（报告核心数字）
TOP_KPIS = [
    {"label": "正式员工", "value": 5901, "sub": "人 · 2026年5月"},
    {"label": "客户经理", "value": 1692, "sub": "人 · 占 28.7%"},
    {"label": "中层干部", "value": 211, "sub": "人 · 已配 194"},
    {"label": "工资总额", "value": "15 亿", "sub": "元 · 2025 年度"},
    {"label": "培训项目", "value": 983, "sub": "场 · 55 重点"},
    {"label": "头狼评选", "value": 129, "sub": "人 · 2026 Q1"},
]
