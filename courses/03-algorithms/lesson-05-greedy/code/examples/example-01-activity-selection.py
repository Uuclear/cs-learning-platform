# 活动选择问题 - 贪心算法经典示例
# 问题：你有一天的时间表，上面有多个活动，每个活动有开始时间和结束时间
# 你只能参加不冲突的活动，如何选择才能参加最多的活动？

# 核心思想：每次都选结束最早的活动！
# 为什么选结束最早的？因为这样给后面的活动留出最多的时间

def activity_selection(activities):
    """
    活动选择问题 - 贪心算法
    参数: activities - 列表，每个元素为(活动名, 开始时间, 结束时间)
    返回: 选择的活动列表
    """
    # 按结束时间排序（贪心策略：优先选结束早的）
    sorted_activities = sorted(activities, key=lambda x: x[2])

    selected = []
    last_end_time = 0  # 上一个选中的活动的结束时间

    for name, start, end in sorted_activities:
        # 如果当前活动的开始时间 >= 上一个选中活动的结束时间，说明不冲突
        if start >= last_end_time:
            selected.append((name, start, end))
            last_end_time = end  # 更新最后结束时间

    return selected


if __name__ == "__main__":
    # 测试数据：(活动名, 开始时间, 结束时间)
    activities = [
        ("上课", 9, 10),
        ("打球", 9, 11),
        ("看书", 10, 12),
        ("写代码", 11, 13),
        ("看电影", 12, 14),
        ("开会", 13, 15),
        ("健身", 14, 16),
        ("约会", 15, 17),
        ("睡觉", 16, 18),
    ]

    print("所有活动（按开始时间）:")
    for name, start, end in activities:
        print(f"  {name}: {start}:00 - {end}:00")

    print("\n" + "=" * 40)

    selected = activity_selection(activities)

    print(f"\n最优选择（共 {len(selected)} 个活动）:")
    for name, start, end in selected:
        print(f"  {name}: {start}:00 - {end}:00")

# 输出:
# 所有活动（按开始时间）:
#   上课: 9:00 - 10:00
#   打球: 9:00 - 11:00
#   看书: 10:00 - 12:00
#   写代码: 11:00 - 13:00
#   看电影: 12:00 - 14:00
#   开会: 13:00 - 15:00
#   健身: 14:00 - 16:00
#   约会: 15:00 - 17:00
#   睡觉: 16:00 - 18:00
#
# ========================================
#
# 最优选择（共 5 个活动）:
#   上课: 9:00 - 10:00
#   看书: 10:00 - 12:00
#   看电影: 12:00 - 14:00
#   健身: 14:00 - 16:00
#   睡觉: 16:00 - 18:00
