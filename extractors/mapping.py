"""字段映射 - 按 .docx 内容分组。

每模块的 sections 数量匹配数据点组数。
所有 section 渲染为紧凑 stat rows，无大卡片。
"""

MODULES = {
    "组织架构": {
        "title": "一、组织架构",
        "icon": "🏛",
        "order": 1,
        "sections": [
            {"key": "headquarters", "title": "总行架构", "type": "stats", "data_key": "headquarters"},
            {"key": "branches", "title": "全行机构", "type": "stats", "data_key": "branches"},
            {"key": "branch_guangzhou", "title": "广州地区网点（107 家）", "type": "stats", "data_key": "branch_guangzhou"},
            {"key": "branch_other", "title": "异地地区网点（76 家）", "type": "stats", "data_key": "branch_other"},
        ],
    },
    "员工情况": {
        "title": "二、员工基本情况",
        "icon": "👥",
        "order": 2,
        "sections": [
            {"key": "headcount", "title": "员工总数与构成", "type": "stats", "data_key": "headcount"},
            {"key": "age_dist", "title": "年龄分布", "type": "stats", "data_key": "age_dist"},
            {"key": "gender_dist", "title": "性别比例", "type": "stats", "data_key": "gender_dist"},
            {"key": "edu_dist", "title": "学历分布", "type": "stats", "data_key": "edu_dist"},
            {"key": "customer_managers", "title": "客户经理（1692 人）", "type": "stats", "data_key": "customer_managers"},
            {"key": "service_managers", "title": "客服经理（1165 人）", "type": "stats", "data_key": "service_managers"},
        ],
    },
    "人员优化": {
        "title": "三、人员优化情况",
        "icon": "📉",
        "order": 3,
        "sections": [
            {"key": "social_hire", "title": "社招入职（2026 年以来 34 人）", "type": "stats", "data_key": "social_hire"},
            {"key": "campus_hire", "title": "校招（2026 届目标 659 人）", "type": "stats", "data_key": "campus_hire"},
            {"key": "exit", "title": "人员退出（累计 202 人）", "type": "stats", "data_key": "exit"},
            {"key": "teng_long", "title": "腾笼换鸟（任务 410 / 完成 201 / 50%）", "type": "stats", "data_key": "teng_long"},
            {"key": "poor_perf", "title": "绩差退出（目标 50% / 完成 46%）", "type": "stats", "data_key": "poor_perf"},
            {"key": "labor", "title": "劳动仲裁（1-5 月 15 起）", "type": "stats", "data_key": "labor"},
        ],
    },
    "干部队伍": {
        "title": "四、干部队伍建设",
        "icon": "🎖",
        "order": 4,
        "sections": [
            {"key": "overview", "title": "中层干部总览", "type": "stats", "data_key": "overview"},
            {"key": "position_table", "title": "干部职数与配置", "type": "table", "data_key": "position_table"},
            {"key": "adjustments", "title": "新一届党委以来调整情况", "type": "stats", "data_key": "adjustments"},
        ],
    },
    "考核薪酬": {
        "title": "五、考核薪酬",
        "icon": "💰",
        "order": 5,
        "sections": [
            {"key": "salary", "title": "薪酬情况", "type": "stats", "data_key": "salary"},
            {"key": "pension", "title": "企业年金与补充医疗", "type": "stats", "data_key": "pension"},
            {"key": "monitoring", "title": "履职监测与头狼评选", "type": "stats", "data_key": "monitoring"},
        ],
    },
    "培训赋能": {
        "title": "六、培训赋能",
        "icon": "📚",
        "order": 6,
        "sections": [
            {"key": "training", "title": "培训总量", "type": "stats", "data_key": "training"},
            {"key": "key_projects", "title": "重点培训项目", "type": "stats", "data_key": "key_projects"},
            {"key": "dept_top", "title": "100% 完成部门（8 个）", "type": "stats", "data_key": "dept_top"},
            {"key": "dept_bottom", "title": "执行率排名后三", "type": "stats", "data_key": "dept_bottom"},
            {"key": "exam", "title": "上岗资格考试", "type": "stats", "data_key": "exam"},
        ],
    },
}
