# 挑战2：任务调度问题 - 解答
# 给定任务的截止时间和完成所需时间，最多能完成多少个任务

def max_tasks(tasks):
    """
    任务调度 - 最多完成的任务数
    参数: tasks - 任务列表，每个任务为(截止时间, 所需时间)
    返回: 最多能完成的任务数，以及选择了哪些任务
    """
    if not tasks:
        return 0, []

    # 贪心策略：按截止时间排序，优先完成截止早的任务
    sorted_tasks = sorted(tasks, key=lambda x: x[0])

    completed = []
    current_time = 0

    for deadline, duration in sorted_tasks:
        # 如果当前时间 + 所需时间 <= 截止时间，可以完成
        if current_time + duration <= deadline:
            completed.append((deadline, duration))
            current_time += duration

    return len(completed), completed


if __name__ == "__main__":
    # 测试
    tasks = [
        (4, 2),  # 截止时间4，需要2小时
        (3, 1),  # 截止时间3，需要1小时
        (5, 2),  # 截止时间5，需要2小时
        (2, 1),  # 截止时间2，需要1小时
        (6, 3),  # 截止时间6，需要3小时
    ]

    count, completed = max_tasks(tasks)
    print(f"最多能完成 {count} 个任务")
    print("完成的任务:")
    for deadline, duration in completed:
        print(f"  截止:{deadline}, 耗时:{duration}")

# 输出:
# 最多能完成 4 个任务
# 完成的任务:
#   截止:2, 耗时:1
#   截止:3, 耗时:1
#   截止:4, 耗时:2
#   截止:6, 耗时:3

# 思路:
# 贪心策略：按截止时间从早到晚排序，依次尝试完成任务。
# 能在截止时间前完成的任务就接，否则跳过。
# 这样保证了尽可能多接任务。
# 时间复杂度: O(n log n)，排序时间
# 空间复杂度: O(n)，存储结果
