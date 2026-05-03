#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态规划解决方案 02: 0-1背包问题
给定物品的重量和价值，以及背包容量，求最大价值
"""

def knapsack_01(weights, values, capacity):
    """
    0-1背包问题的动态规划解法（二维DP表）

    参数:
        weights: 物品重量列表
        values: 物品价值列表
        capacity: 背包容量

    返回:
        最大价值和选择的物品索引列表
    """
    n = len(weights)

    # 创建DP表，dp[i][w] 表示前i个物品在容量w下的最大价值
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # 填充DP表
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # 不选第i个物品（索引i-1）
            dp[i][w] = dp[i - 1][w]

            # 如果能装下第i个物品，考虑选它的情况
            if weights[i - 1] <= w:
                # 选第i个物品的价值 = 前i-1个物品在容量(w-weight)下的最大价值 + 当前物品价值
                value_with_item = dp[i - 1][w - weights[i - 1]] + values[i - 1]
                # 取较大值
                dp[i][w] = max(dp[i][w], value_with_item)

    # 回溯找出选择的物品
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        # 如果当前价值不等于上一行的价值，说明选择了第i个物品
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)  # 转换为0-based索引
            w -= weights[i - 1]

    selected_items.reverse()  # 按原始顺序排列
    return dp[n][capacity], selected_items


def knapsack_01_optimized(weights, values, capacity):
    """
    0-1背包问题的空间优化解法（一维DP数组）

    参数:
        weights: 物品重量列表
        values: 物品价值列表
        capacity: 背包容量

    返回:
        最大价值（无法直接回溯物品，但空间复杂度更优）
    """
    # 只用一维数组，从后往前更新避免覆盖
    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        # 从后往前遍历，避免重复使用同一个物品
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]


def main():
    """主函数：演示背包问题的解决方案"""
    print("=== 0-1背包问题动态规划实现 ===\n")

    # 示例数据：4个物品
    weights = [2, 3, 4, 5]      # 物品重量
    values = [3, 4, 5, 6]       # 物品价值
    capacity = 8                # 背包容量

    print("物品信息:")
    for i in range(len(weights)):
        print(f"  物品 {i}: 重量={weights[i]}, 价值={values[i]}")
    print(f"背包容量: {capacity}\n")

    # 使用完整DP表方法（可以回溯物品）
    max_value, selected = knapsack_01(weights, values, capacity)
    print("1. 完整DP表方法:")
    print(f"   最大价值: {max_value}")
    print(f"   选择的物品: {[f'物品{i}' for i in selected]}")
    total_weight = sum(weights[i] for i in selected)
    print(f"   总重量: {total_weight}/{capacity}\n")

    # 使用空间优化方法
    max_value_opt = knapsack_01_optimized(weights, values, capacity)
    print("2. 空间优化方法:")
    print(f"   最大价值: {max_value_opt}")
    print(f"   结果一致: {max_value == max_value_opt}\n")

    # 更大的测试用例
    print("3. 更大测试用例:")
    large_weights = [10, 20, 30, 40, 50]
    large_values = [60, 100, 120, 140, 160]
    large_capacity = 100

    max_val, selected_items = knapsack_01(large_weights, large_values, large_capacity)
    print(f"   最大价值: {max_val}")
    print(f"   选择的物品: {[f'物品{i}' for i in selected_items]}")


if __name__ == "__main__":
    main()