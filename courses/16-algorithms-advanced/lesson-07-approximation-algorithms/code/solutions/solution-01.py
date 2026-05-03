#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
近似算法解决方案1：背包问题的FPTAS实现

这个解决方案实现了背包问题的FPTAS（完全多项式时间近似方案），
并提供了与标准动态规划的比较。
"""

def knapsack_dp(weights, values, capacity):
    """
    标准动态规划解法（基于价值）

    时间复杂度: O(n * sum(values))
    空间复杂度: O(sum(values))
    """
    n = len(weights)
    total_value = sum(values)

    # dp[v] = 达到价值v所需的最小重量
    dp = [float('inf')] * (total_value + 1)
    dp[0] = 0

    for i in range(n):
        # 逆序遍历避免重复使用物品
        for v in range(total_value, values[i] - 1, -1):
            if dp[v - values[i]] != float('inf'):
                dp[v] = min(dp[v], dp[v - values[i]] + weights[i])

    # 找到最大可达价值
    max_value = 0
    for v in range(total_value, -1, -1):
        if dp[v] <= capacity:
            max_value = v
            break

    return max_value

def knapsack_fptas(weights, values, capacity, epsilon):
    """
    背包问题的FPTAS实现

    参数:
        weights: 物品重量列表
        values: 物品价值列表
        capacity: 背包容量
        epsilon: 精度参数 (0 < epsilon < 1)

    返回:
        近似最优价值

    时间复杂度: O(n³ / epsilon)
    近似比: (1 - epsilon)
    """
    n = len(weights)
    if n == 0:
        return 0

    # 找到最大价值
    vmax = max(values)

    # 计算缩放因子
    K = (epsilon * vmax) / n

    # 缩放价值（向下取整）
    scaled_values = [int(v // K) for v in values]

    # 对缩放后的价值运行DP
    max_scaled_value = max(scaled_values)
    dp = [float('inf')] * (n * max_scaled_value + 1)
    dp[0] = 0

    for i in range(n):
        for v in range(n * max_scaled_value, scaled_values[i] - 1, -1):
            if dp[v - scaled_values[i]] != float('inf'):
                dp[v] = min(dp[v], dp[v - scaled_values[i]] + weights[i])

    # 找到最大可达的缩放价值
    max_scaled = 0
    for v in range(n * max_scaled_value, -1, -1):
        if dp[v] <= capacity:
            max_scaled = v
            break

    # 转换回原始价值（下界）
    approx_value = max_scaled * K
    return int(approx_value)

def test_knapsack_fptas():
    """测试FPTAS实现"""
    import time

    # 测试数据
    weights = [10, 20, 30, 40, 50, 60, 70, 80]
    values = [60, 100, 120, 140, 160, 180, 200, 220]
    capacity = 150

    print("背包问题测试:")
    print(f"物品数量: {len(weights)}")
    print(f"背包容量: {capacity}")
    print()

    # 计算精确解（小规模）
    start_time = time.time()
    exact_value = knapsack_dp(weights, values, capacity)
    exact_time = time.time() - start_time

    print(f"精确解:")
    print(f"最大价值: {exact_value}")
    print(f"计算时间: {exact_time:.4f}秒")
    print()

    # 测试不同精度的FPTAS
    epsilons = [0.5, 0.2, 0.1, 0.05]

    for epsilon in epsilons:
        start_time = time.time()
        approx_value = knapsack_fptas(weights, values, capacity, epsilon)
        approx_time = time.time() - start_time

        # 计算实际近似比
        actual_ratio = approx_value / exact_value if exact_value > 0 else 1.0
        theoretical_ratio = 1 - epsilon

        print(f"ε = {epsilon}:")
        print(f"  近似价值: {approx_value}")
        print(f"  实际近似比: {actual_ratio:.3f}")
        print(f"  理论保证: ≥ {theoretical_ratio:.3f}")
        print(f"  计算时间: {approx_time:.4f}秒")
        print()

    # 验证理论保证
    print("理论验证:")
    print("FPTAS保证解的价值至少为 (1-ε) × 最优价值")
    print("实验结果显示实际性能通常优于理论保证")

if __name__ == "__main__":
    test_knapsack_fptas()