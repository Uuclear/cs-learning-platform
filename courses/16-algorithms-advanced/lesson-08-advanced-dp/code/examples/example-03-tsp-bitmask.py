#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：状态压缩动态规划 - 旅行商问题(TSP)简化版
演示如何使用位运算压缩状态来解决TSP问题
"""

def tsp_bitmask(dist):
    """
    使用状态压缩动态规划解决TSP问题

    参数:
        dist: list[list] - 距离矩阵，dist[i][j]表示从城市i到城市j的距离

    返回:
        int - 最短回路距离
    """
    n = len(dist)
    if n <= 1:
        return 0

    # dp[mask][i] 表示访问状态为mask，当前在城市i的最短距离
    # mask是一个n位二进制数，第j位为1表示城市j已被访问
    dp = [[float('inf')] * n for _ in range(1 << n)]

    # 初始状态：从城市0开始，只访问了城市0
    dp[1][0] = 0

    # 枚举所有可能的访问状态
    for mask in range(1 << n):
        for u in range(n):
            # 如果当前状态mask中没有包含城市u，跳过
            if not (mask & (1 << u)):
                continue
            # 尝试从城市u转移到未访问的城市v
            for v in range(n):
                if mask & (1 << v):  # 如果城市v已经被访问，跳过
                    continue
                # 新的状态：在mask基础上加上城市v
                new_mask = mask | (1 << v)
                # 更新dp[new_mask][v]
                dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])

    # 找到回到起点0的最短路径
    result = float('inf')
    final_mask = (1 << n) - 1  # 所有城市都被访问的状态
    for i in range(1, n):  # 从其他城市回到城市0
        result = min(result, dp[final_mask][i] + dist[i][0])

    return result if result != float('inf') else -1

def print_tsp_solution(dist):
    """
    打印TSP问题的详细解决方案
    """
    n = len(dist)
    print(f"TSP问题 - {n}个城市")
    print("距离矩阵:")
    for i in range(n):
        print(f"  {dist[i]}")

    shortest_path = tsp_bitmask(dist)
    if shortest_path == -1:
        print("无解")
    else:
        print(f"最短回路距离: {shortest_path}")

def main():
    """主函数：演示TSP问题"""
    # 示例1：4个城市
    dist1 = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    print_tsp_solution(dist1)

    # 示例2：3个城市（更简单的例子）
    dist2 = [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]
    ]
    print()
    print_tsp_solution(dist2)

    # 解释状态压缩原理
    print("\n状态压缩原理解释:")
    print("- 使用二进制位表示访问状态")
    print("- mask = 5 (二进制101) 表示访问了城市0和城市2")
    print("- 状态总数: 2^n，每个状态对应一个子集")
    print("- 时间复杂度: O(n² × 2ⁿ)，空间复杂度: O(n × 2ⁿ)")

if __name__ == "__main__":
    main()