"""字段映射 + viz 配置。

按 .docx 内容比重设计排版（size 字段）：
- "compact" → 进 KPI 行（多列小卡）
- "half" → 两列并排
- "full" → 占满整行（重要表/排名）

每个模块的 sections 顺序和 size 基于 .docx 数据重要性。
"""

MODULES = {
    "组织架构": {
        "title": "一、组织架构",
        "icon": "🏛",
        "order": 1,
        "sections": [
            # .docx 重点：分行 + 网点分布，1 个 hierarchy 全宽
            {
                "key": "branch_hierarchy",
                "title": "网点分布",
                "type": "hierarchy",
                "data_key": "region_tree",
                "size": "full",
                "drillable": True,
            },
        ],
    },
    "员工情况": {
        "title": "二、员工基本情况",
        "icon": "👥",
        "order": 2,
        "sections": [
            # 3 个核心 KPI 数字（.docx 顶部强调数据）
            {
                "key": "kpi_total",
                "title": "正式员工",
                "type": "kpi",
                "data_key": "headcount_total",
                "size": "compact",
            },
            {
                "key": "kpi_operating",
                "title": "经营机构",
                "type": "kpi",
                "data_key": "headcount_operating",
                "size": "compact",
            },
            {
                "key": "kpi_ratio",
                "title": "前中后台比例",
                "type": "kpi",
                "data_key": "headcount_ratio",
                "size": "compact",
            },
            # 4 个分布
            {
                "key": "age_dist",
                "title": "年龄分布",
                "type": "bar",
                "alt_types": ["pie"],
                "data_key": "age_distribution",
                "size": "half",
            },
            {
                "key": "edu_dist",
                "title": "学历分布",
                "type": "bar",
                "alt_types": ["pie"],
                "data_key": "edu_distribution",
                "size": "half",
            },
            {
                "key": "gender_dist",
                "title": "性别比例",
                "type": "pie",
                "alt_types": ["bar"],
                "data_key": "gender_distribution",
                "size": "half",
            },
            {
                "key": "customer_managers",
                "title": "客户经理分类",
                "type": "bar",
                "alt_types": ["table"],
                "data_key": "customer_managers",
                "size": "half",
                "drillable": True,
            },
        ],
    },
    "人员优化": {
        "title": "三、人员优化情况",
        "icon": "📉",
        "order": 3,
        "sections": [
            # 3 个核心 KPI
            {
                "key": "kpi_social",
                "title": "社招入职",
                "type": "kpi",
                "data_key": "social_hire_total",
                "size": "compact",
            },
            {
                "key": "kpi_campus",
                "title": "校招签约",
                "type": "kpi",
                "data_key": "campus_hire_total",
                "size": "compact",
            },
            {
                "key": "kpi_exit",
                "title": "累计退出",
                "type": "kpi",
                "data_key": "exit_total",
                "size": "compact",
            },
            # 校招 funnel
            {
                "key": "campus_funnel",
                "title": "校招各阶段",
                "type": "funnel",
                "data_key": "campus_funnel",
                "size": "half",
            },
            # 2 个 progress
            {
                "key": "teng_long",
                "title": "腾笼换鸟",
                "type": "progress",
                "data_key": "teng_long_huan_yao",
                "size": "half",
                "drillable": True,
            },
            {
                "key": "poor_perf",
                "title": "绩差退出",
                "type": "progress",
                "data_key": "poor_perf_exit",
                "size": "full",
                "drillable": True,
            },
        ],
    },
    "干部队伍": {
        "title": "四、干部队伍建设",
        "icon": "🎖",
        "order": 4,
        "sections": [
            # 3 个 KPI
            {
                "key": "kpi_total",
                "title": "中层总职数",
                "type": "kpi",
                "data_key": "headcount_total",
                "size": "compact",
            },
            {
                "key": "kpi_filled",
                "title": "已配备",
                "type": "kpi",
                "data_key": "headcount_filled",
                "size": "compact",
            },
            {
                "key": "kpi_vacancy",
                "title": "尚空缺",
                "type": "kpi",
                "data_key": "headcount_vacancy",
                "size": "compact",
            },
            # 1 个核心表（全宽）+ 1 个 ranking
            {
                "key": "config_table",
                "title": "职数与配置情况",
                "type": "table",
                "data_key": "config_table",
                "size": "full",
            },
            {
                "key": "adjustments",
                "title": "新一届党委以来调整",
                "type": "ranking",
                "data_key": "adjustments",
                "size": "full",
            },
        ],
    },
    "考核薪酬": {
        "title": "五、考核薪酬",
        "icon": "💰",
        "order": 5,
        "sections": [
            # 4 个 KPI（compact row）
            {
                "key": "kpi_salary",
                "title": "2025 年工资总额",
                "type": "kpi",
                "data_key": "salary_total",
                "size": "compact",
            },
            {
                "key": "kpi_per_capita",
                "title": "人均薪酬",
                "type": "kpi",
                "data_key": "salary_per_capita",
                "size": "compact",
            },
            {
                "key": "kpi_pension",
                "title": "企业年金余额",
                "type": "kpi",
                "data_key": "pension_balance",
                "size": "compact",
            },
            {
                "key": "kpi_tou_lang",
                "title": "头狼评选",
                "type": "kpi",
                "data_key": "tou_lang_count",
                "size": "compact",
            },
            # 1 个 ranking
            {
                "key": "monitoring",
                "title": "履职监测黑榜",
                "type": "ranking",
                "data_key": "monitoring",
                "size": "full",
            },
        ],
    },
    "培训赋能": {
        "title": "六、培训赋能",
        "icon": "📚",
        "order": 6,
        "sections": [
            # 3 个 KPI
            {
                "key": "kpi_total",
                "title": "能力大提升项目",
                "type": "kpi",
                "data_key": "training_total",
                "size": "compact",
            },
            {
                "key": "kpi_key",
                "title": "重点培训项目",
                "type": "kpi",
                "data_key": "key_projects",
                "size": "compact",
            },
            {
                "key": "kpi_exam",
                "title": "上岗资格人次",
                "type": "kpi",
                "data_key": "exam_count",
                "size": "compact",
            },
            # 1 个 progress + 1 个 ranking
            {
                "key": "key_projects_progress",
                "title": "重点项目执行率",
                "type": "progress",
                "data_key": "key_projects_pct",
                "size": "full",
            },
            {
                "key": "dept_execution",
                "title": "部门培训执行率",
                "type": "ranking",
                "data_key": "dept_execution",
                "size": "full",
                "drillable": True,
            },
        ],
    },
}
