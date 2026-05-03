#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：区间动态规划 - 石子合并问题
演示如何使用区间DP解决石子合并问题
"""

def stone_merge(stones):
    """
    石子合并问题：相邻石子堆可以合并，代价为两堆石子数量之和
    求合并成一堆的最小总代价

    参数:
        stones: list - 每堆石子的数量

    返回:
        int - 最小总代价
    """
    n = len(stones)
    if n <= 1:
        return 0

    # 计算前缀和，用于快速计算区间和
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + stones[i]

    # dp[i][j] 表示合并第i堆到第j堆石子的最小代价
    dp = [[0] * n for _ in range(n)]

    # 枚举区间长度（从2开始，因为单堆不需要合并）
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            # 枚举分割点k，将[i,j]分成[i,k]和[k+1,j]
            for k in range(i, j):
                # 合并代价 = 左部分代价 + 右部分代价 + 合并左右的代价
                cost = dp[i][k] + dp[k + 1][j] + prefix_sum[j + 1] - prefix_sum[i]
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]

def stone_merge_max(stones):
    """
    石子合并问题的最大代价版本
    """
    n = len(stones)
    if n <= 1:
        return 0

    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + stones[i]

    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = 0  # 初始化为0，求最大值
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + prefix_sum[j + 1] - prefix_sum[i]
                dp[i][j] = max(dp[i][j], cost)

    return dp[0][n - 1]

def main():
    """主函数：演示石子合并问题"""
    # 示例1：石子堆 [4, 5, 9, 4]
    stones1 = [4, 5, 9, 4]
    print("石子合并问题示例")
    print(f"石子堆: {stones1}")
    print(f"最小合并代价: {stone_merge(stones1)}")
    print(f"最大合并代价: {stone_merge_max(stones1)}")

    # 示例2：石子堆 [1, 2, 3, 4, 5]
    stones2 = [1, 2, 3, 4, 5]
    print(f"\n石子堆: {stones2}")
    print(f"最小合并代价: {stone_merge(stones2)}")
    print(f"最大合并代价: {stone_merge_max(stones2)}")

    # 显示DP表的构建过程（简化版）
    print("\nDP表构建说明:")
    print("- dp[i][j] 表示合并第i到第j堆石子的最小代价")
    print("- 按照区间长度从小到大计算")
    print("- 对每个区间枚举所有可能的分割点")

if __name__ == "__main__":
    main()