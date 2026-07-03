"""字段映射 + viz 配置。

每个模块：
- title: 显示标题
- icon: emoji
- order: 显示顺序
- sections: section 列表
  - key: section id
  - title: section 标题
  - type: viz 类型（kpi/bar/pie/...）
  - alt_types: 切换选项
  - data_key: 从原始数据提取的 key
  - drillable: 是否可钻取
"""

MODULES = {
    "组织架构": {
        "title": "一、组织架构",
        "icon": "🏛",
        "order": 1,
        "sections": [
            {
                "key": "branch_by_region",
                "title": "分行网点分布",
                "type": "hierarchy",
                "alt_types": ["table"],
                "data_key": "region_tree",
                "drillable": True,
            },
            {
                "key": "branch_status",
                "title": "网点营业状态",
                "type": "ranking",
                "alt_types": [],
                "data_key": "branch_status",
                "drillable": False,
            },
        ],
    },
    "员工情况": {
        "title": "二、员工基本情况",
        "icon": "👥",
        "order": 2,
        "sections": [
            {
                "key": "headcount_total",
                "title": "员工总数",
                "type": "kpi",
                "alt_types": [],
                "data_key": "headcount_overview",
                "drillable": False,
            },
            {
                "key": "age_dist",
                "title": "年龄分布",
                "type": "bar",
                "alt_types": ["pie"],
                "data_key": "age_distribution",
                "drillable": False,
            },
            {
                "key": "edu_dist",
                "title": "学历分布",
                "type": "bar",
                "alt_types": ["pie"],
                "data_key": "edu_distribution",
                "drillable": False,
            },
            {
                "key": "gender_dist",
                "title": "性别比例",
                "type": "pie",
                "alt_types": ["bar"],
                "data_key": "gender_distribution",
                "drillable": False,
            },
            {
                "key": "customer_managers",
                "title": "客户经理分类",
                "type": "bar",
                "alt_types": ["table"],
                "data_key": "customer_managers",
                "drillable": True,
            },
        ],
    },
    "人员优化": {
        "title": "三、人员优化情况",
        "icon": "📉",
        "order": 3,
        "sections": [
            {
                "key": "social_hire",
                "title": "社招入职",
                "type": "kpi",
                "alt_types": [],
                "data_key": "social_hire",
                "drillable": False,
            },
            {
                "key": "campus_hire",
                "title": "校招签约",
                "type": "funnel",
                "alt_types": ["bar"],
                "data_key": "campus_hire",
                "drillable": False,
            },
            {
                "key": "exit_overview",
                "title": "人员退出",
                "type": "kpi",
                "alt_types": [],
                "data_key": "exit_overview",
                "drillable": False,
            },
            {
                "key": "teng_long_huan_yao",
                "title": "腾笼换鸟",
                "type": "progress",
                "alt_types": [],
                "data_key": "teng_long_huan_yao",
                "drillable": True,
            },
            {
                "key": "poor_perf_exit",
                "title": "绩差退出",
                "type": "progress",
                "alt_types": [],
                "data_key": "poor_perf_exit",
                "drillable": True,
            },
        ],
    },
    "干部队伍": {
        "title": "四、干部队伍建设",
        "icon": "🎖",
        "order": 4,
        "sections": [
            {
                "key": "headcount_total",
                "title": "干部总职数",
                "type": "kpi",
                "alt_types": [],
                "data_key": "headcount_overview",
                "drillable": False,
            },
            {
                "key": "config_table",
                "title": "职数与配置",
                "type": "table",
                "alt_types": [],
                "data_key": "config_table",
                "drillable": False,
            },
            {
                "key": "adjustments",
                "title": "调整情况",
                "type": "ranking",
                "alt_types": [],
                "data_key": "adjustments",
                "drillable": False,
            },
        ],
    },
    "考核薪酬": {
        "title": "五、考核薪酬",
        "icon": "💰",
        "order": 5,
        "sections": [
            {
                "key": "salary_total",
                "title": "工资总额",
                "type": "kpi",
                "alt_types": [],
                "data_key": "salary_overview",
                "drillable": False,
            },
            {
                "key": "pension",
                "title": "企业年金",
                "type": "kpi",
                "alt_types": [],
                "data_key": "pension",
                "drillable": False,
            },
            {
                "key": "monitoring",
                "title": "履职监测黑榜",
                "type": "ranking",
                "alt_types": [],
                "data_key": "monitoring",
                "drillable": False,
            },
            {
                "key": "tou_lang",
                "title": "头狼评选",
                "type": "kpi",
                "alt_types": [],
                "data_key": "tou_lang",
                "drillable": False,
            },
        ],
    },
    "培训赋能": {
        "title": "六、培训赋能",
        "icon": "📚",
        "order": 6,
        "sections": [
            {
                "key": "training_overview",
                "title": "培训总量",
                "type": "kpi",
                "alt_types": [],
                "data_key": "training_overview",
                "drillable": False,
            },
            {
                "key": "key_projects",
                "title": "重点培训项目",
                "type": "progress",
                "alt_types": [],
                "data_key": "key_projects",
                "drillable": False,
            },
            {
                "key": "dept_execution",
                "title": "部门执行率",
                "type": "ranking",
                "alt_types": [],
                "data_key": "dept_execution",
                "drillable": True,
            },
        ],
    },
}
