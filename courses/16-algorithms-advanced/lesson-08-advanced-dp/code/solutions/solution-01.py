#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：矩阵链乘法完整实现
"""

def matrix_chain_order(p):
    """计算矩阵链乘法的最优括号化方案"""
    n = len(p) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s

def print_optimal_parens(s, i, j):
    """打印最优括号化方案"""
    if i == j:
        return f"A{i}"
    else:
        left = print_optimal_parens(s, i, s[i][j])
        right = print_optimal_parens(s, s[i][j] + 1, j)
        return f"({left}{right})"

def solve_matrix_chain(p):
    """解决矩阵链乘法问题的主函数"""
    m, s = matrix_chain_order(p)
    min_cost = m[1][len(p) - 1]
    optimal_parens = print_optimal_parens(s, 1, len(p) - 1)
    return min_cost, optimal_parens

# 测试用例
if __name__ == "__main__":
    # 示例测试
    p = [30, 35, 15, 5, 10, 20, 25]
    min_cost, parens = solve_matrix_chain(p)
    print(f"最小代价: {min_cost}")
    print(f"最优括号化: {parens}")