#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贪心算法解决方案 01: 活动选择问题
给定一系列活动的开始和结束时间，选择最多数量的互不冲突活动
"""

def activity_selection(activities):
    """
    活动选择问题 - 贪心算法

    参数:
        activities: 列表，每个元素为(活动名, 开始时间, 结束时间)

    返回:
        选择的活动列表（按时间顺序）
    """
    # 按结束时间排序（贪心策略：优先选结束早的）
    sorted_activities = sorted(activities, key=lambda x: x[2])

    selected = []
    last_end_time = 0

    for name, start, end in sorted_activities:
        # 如果当前活动的开始时间 >= 上一个选中活动的结束时间，不冲突
        if start >= last_end_time:
            selected.append((name, start, end))
            last_end_time = end  # 更新最后结束时间

    return selected


def activity_selection_with_value(activities):
    """
    带价值的活动选择问题（加权版本）
    注意：这个版本贪心不一定最优，仅作对比演示

    参数:
        activities: 列表，每个元素为(活动名, 开始时间, 结束时间, 价值)

    返回:
        选择的活动列表和总价值
    """
    # 贪心策略1：按价值排序（可能不是最优）
    sorted_by_value = sorted(activities, key=lambda x: x[3], reverse=True)

    selected = []
    total_value = 0
    last_end_time = 0

    for name, start, end, value in sorted_by_value:
        if start >= last_end_time:
            selected.append((name, start, end, value))
            total_value += value
            last_end_time = end

    return selected, total_value


def main():
    """主函数：演示活动选择问题的解决方案"""
    print("=== 活动选择问题贪心算法实现 ===\n")

    # 示例1：基本活动选择（最大化数量）
    print("1. 基本活动选择（最大化活动数量）:")
    activities = [
        ("上课", 9, 10), ("打球", 9, 11), ("看书", 10, 12),
        ("写代码", 11, 13), ("看电影", 12, 14), ("开会", 13, 15),
        ("健身", 14, 16), ("约会", 15, 17), ("睡觉", 16, 18),
    ]

    selected = activity_selection(activities)
    print(f"   可选活动总数: {len(activities)}")
    print(f"   最优选择数量: {len(selected)}")
    print("   选择的活动:")
    for name, start, end in selected:
        print(f"     {name}: {start}:00 - {end}:00")
    print()

    # 示例2：带价值的活动选择
    print("2. 带价值的活动选择（贪心策略对比）:")
    activities_with_value = [
        ("重要会议", 9, 11, 100),   # 高价值，长时间
        ("紧急任务", 10, 12, 80),   # 中等价值
        ("日常会议", 13, 14, 30),   # 低价值，短时间
        ("团队建设", 14, 16, 50),   # 中等价值
        ("客户拜访", 15, 17, 120),  # 高价值
        ("项目汇报", 16, 18, 90),   # 高价值
    ]

    # 按价值贪心选择
    selected_val, total_val = activity_selection_with_value(activities_with_value)
    print(f"   按价值贪心选择:")
    print(f"   总价值: {total_val}")
    print("   选择的活动:")
    for name, start, end, value in selected_val:
        print(f"     {name}: {start}:00-{end}:00 (价值: {value})")
    print()

    # 说明：带价值的活动选择需要用动态规划才能保证最优
    print("   注意：带价值的活动选择问题，贪心算法不能保证得到最优解！")
    print("   这类问题需要使用动态规划来求解。")


if __name__ == "__main__":
    main()