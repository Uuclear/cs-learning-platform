#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：状态压缩DP - TSP完整实现
"""

def tsp_bitmask(dist):
    """TSP问题的状态压缩DP解法"""
    n = len(dist)
    if n <= 1:
        return 0

    # 初始化DP表
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0  # 从城市0开始

    # 状态转移
    for mask in range(1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])

    # 找到最短回路
    result = float('inf')
    final_mask = (1 << n) - 1
    for i in range(1, n):
        result = min(result, dp[final_mask][i] + dist[i][0])

    return result if result != float('inf') else -1

def solve_tsp(dist):
    """解决TSP问题的主函数"""
    return tsp_bitmask(dist)

# 测试用例
if __name__ == "__main__":
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    shortest_path = solve_tsp(dist)
    print(f"最短回路距离: {shortest_path}")