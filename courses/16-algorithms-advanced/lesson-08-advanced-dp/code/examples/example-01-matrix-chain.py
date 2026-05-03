#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：矩阵链乘法最优括号化
演示如何找到矩阵链乘法的最优计算顺序
"""

def matrix_chain_order(p):
    """
    计算矩阵链乘法的最优括号化方案

    参数:
        p: list - 矩阵维度数组，p[i-1]和p[i]表示第i个矩阵的行数和列数

    返回:
        m: list[list] - m[i][j]表示计算A_i到A_j的最小标量乘法次数
        s: list[list] - s[i][j]表示最优分割点k
    """
    n = len(p) - 1  # 矩阵数量
    # 初始化代价矩阵和分割点矩阵
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # 链长从2开始（单个矩阵不需要计算）
    for chain_length in range(2, n + 1):
        for i in range(1, n - chain_length + 2):
            j = i + chain_length - 1
            m[i][j] = float('inf')
            # 尝试所有可能的分割点
            for k in range(i, j):
                # 计算在k处分割的总代价
                cost = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s

def print_optimal_parens(s, i, j):
    """
    递归打印最优括号化方案

    参数:
        s: 分割点矩阵
        i, j: 当前处理的矩阵范围
    """
    if i == j:
        print(f"A{i}", end="")
    else:
        print("(", end="")
        print_optimal_parens(s, i, s[i][j])
        print_optimal_parens(s, s[i][j] + 1, j)
        print(")", end="")

def main():
    """主函数：演示矩阵链乘法"""
    # 示例：矩阵维度 [30, 35, 15, 5, 10, 20, 25]
    # 表示6个矩阵：A1(30×35), A2(35×15), A3(15×5), A4(5×10), A5(10×20), A6(20×25)
    p = [30, 35, 15, 5, 10, 20, 25]

    print("矩阵链乘法最优括号化示例")
    print(f"矩阵维度: {p}")
    print(f"矩阵数量: {len(p) - 1}")

    m, s = matrix_chain_order(p)

    print(f"\n最小标量乘法次数: {m[1][len(p) - 1]}")
    print("最优括号化方案: ", end="")
    print_optimal_parens(s, 1, len(p) - 1)
    print()

    # 显示代价矩阵
    print("\n代价矩阵 m[i][j]:")
    for i in range(1, len(p)):
        row = []
        for j in range(1, len(p)):
            if i <= j:
                row.append(str(m[i][j]))
            else:
                row.append(" - ")
        print(f"  {row}")

if __name__ == "__main__":
    main()