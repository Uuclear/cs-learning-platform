# 0-1背包问题：贪心小贼的动态规划克星
# 问题：给你一个背包，容量有限，物品有价值有重量
# 怎么装才能让背包里总价值最大？

import json


def knapsack(weights, values, capacity):
    """
    0-1背包问题的动态规划解法

    核心思路：
    - dp[i][w] = 考虑前i个物品，背包容量为w时的最大价值
    - 对每个物品，有两种选择：
      1. 不装：dp[i][w] = dp[i-1][w]
      2. 装（如果能装下）：dp[i][w] = dp[i-1][w-weight] + value
    - 取两者中较大的那个

    状态转移方程：
    dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i-1]] + values[i-1])
    """
    n = len(values)  # 物品数量

    # 创建DP表：(n+1)行 × (capacity+1)列
    # dp[i][w]表示前i个物品，容量为w时的最大价值
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # 打印DP表的表头
    header_label = "物品\\容量"
    print(f"{header_label:<8}", end="")
    for w in range(capacity + 1):
        print(f"{w:>6}", end="")
    print()
    print("-" * (8 + 6 * (capacity + 1)))

    # 填表：一行一行地填
    for i in range(1, n + 1):
        print(f"物品{i-1}   ", end="")  # 物品编号从0开始
        weight = weights[i - 1]  # 当前物品的重量
        value = values[i - 1]    # 当前物品的价值

        for w in range(capacity + 1):
            # 选择不装当前物品：继承上一行的结果
            not_take = dp[i - 1][w]

            # 选择装（只有能装下时才考虑）
            if w >= weight:
                take = dp[i - 1][w - weight] + value
            else:
                take = -1  # 装不下，标记为-1

            # 取最优选择
            dp[i][w] = max(not_take, take)

            # 打印当前格子
            print(f"{dp[i][w]:>6}", end="")
        print()  # 换行

    print("-" * (8 + 6 * (capacity + 1)))

    # 回溯找出具体装了哪些物品
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        # 如果当前格子和上一行不一样，说明这个物品被选了
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)  # 记录物品编号
            w -= weights[i - 1]           # 减去该物品的重量

    selected_items.reverse()  # 按物品顺序排列

    return dp[n][capacity], selected_items


if __name__ == "__main__":
    print("=" * 60)
    print("0-1背包问题：动态规划解法")
    print("=" * 60)

    # 测试案例：4个物品，背包容量为10
    # 物品编号: 0    1    2    3
    weights = [2,    3,    4,    5]   # 重量
    values =  [3,    4,    5,    7]   # 价值
    capacity = 10                      # 背包容量

    print(f"\n物品信息：")
    for i in range(len(weights)):
        print(f"  物品{i}: 重量={weights[i]}, 价值={values[i]}, 性价比={values[i]/weights[i]:.2f}")
    print(f"背包容量: {capacity}")
    print(f"\n{'=' * 60}")
    print("DP填表过程：")
    print(f"{'=' * 60}\n")

    max_value, selected = knapsack(weights, values, capacity)

    print(f"\n{'=' * 60}")
    print("结果分析：")
    print(f"{'=' * 60}")
    print(f"最大价值: {max_value}")
    print(f"选择的物品: {[f'物品{i}' for i in selected]}")

    # 验证：打印选中物品的详细信息
    total_weight = sum(weights[i] for i in selected)
    total_value = sum(values[i] for i in selected)
    print(f"总重量: {total_weight} / {capacity}")
    print(f"总价值: {total_value}")
    print(f"剩余容量: {capacity - total_weight}")

# 输出:
# ============================================================
# 0-1背包问题：动态规划解法
# ============================================================
#
# 物品信息：
#   物品0: 重量=2, 价值=3, 性价比=1.50
#   物品1: 重量=3, 价值=4, 性价比=1.33
#   物品2: 重量=4, 价值=5, 性价比=1.25
#   物品3: 重量=5, 价值=7, 性价比=1.40
# 背包容量: 10
#
# ============================================================
# DP填表过程：
# ============================================================
#
# 物品\容量      0     1     2     3     4     5     6     7     8     9    10
# ------------------------------------------------
# 物品0         0     0     3     3     3     3     3     3     3     3     3
# 物品1         0     0     3     4     4     7     7     7     7     7     7
# 物品2         0     0     3     4     5     7     8     9     9    12    12
# 物品3         0     0     3     4     5     7     8    10    11    12    14
# ------------------------------------------------
#
# ============================================================
# 结果分析：
# ============================================================
# 最大价值: 14
# 选择的物品: ['物品0', '物品1', '物品3']
# 总重量: 10 / 10
# 总价值: 14
# 剩余容量: 0
