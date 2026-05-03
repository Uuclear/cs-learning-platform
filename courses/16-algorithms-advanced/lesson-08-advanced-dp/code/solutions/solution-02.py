#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：区间DP - 石子合并完整实现
"""

def stone_merge(stones):
    """石子合并问题 - 最小代价"""
    n = len(stones)
    if n <= 1:
        return 0

    # 前缀和
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stones[i]

    # DP表
    dp = [[0] * n for _ in range(n)]

    # 按区间长度递增计算
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + prefix[j + 1] - prefix[i]
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]

def stone_merge_max(stones):
    """石子合并问题 - 最大代价"""
    n = len(stones)
    if n <= 1:
        return 0

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stones[i]

    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = 0
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + prefix[j + 1] - prefix[i]
                dp[i][j] = max(dp[i][j], cost)

    return dp[0][n - 1]

def solve_stone_merge(stones):
    """解决石子合并问题的主函数"""
    min_cost = stone_merge(stones)
    max_cost = stone_merge_max(stones)
    return min_cost, max_cost

# 测试用例
if __name__ == "__main__":
    stones = [4, 5, 9, 4]
    min_cost, max_cost = solve_stone_merge(stones)
    print(f"最小代价: {min_cost}")
    print(f"最大代价: {max_cost}")