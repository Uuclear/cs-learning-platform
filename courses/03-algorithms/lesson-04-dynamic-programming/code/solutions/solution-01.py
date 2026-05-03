#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态规划解决方案 01: 斐波那契数列
实现两种方法：记忆化递归（自顶向下）和迭代法（自底向上）
"""

import time


def fibonacci_memo(n, memo=None):
    """
    记忆化递归实现斐波那契数列（自顶向下）

    参数:
        n: 要计算的斐波那契数列项数
        memo: 缓存字典，存储已计算的结果

    返回:
        第n项斐波那契数
    """
    if memo is None:
        memo = {}

    # 基准情况
    if n <= 0:
        return 0
    if n == 1:
        return 1

    # 检查缓存
    if n in memo:
        return memo[n]

    # 递归计算并缓存结果
    result = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    memo[n] = result
    return result


def fibonacci_iterative(n):
    """
    迭代法实现斐波那契数列（自底向上）

    参数:
        n: 要计算的斐波那契数列项数

    返回:
        第n项斐波那契数
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1

    # 只需要保存前两个值，空间复杂度O(1)
    prev2, prev1 = 0, 1

    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current

    return prev1


def main():
    """主函数：演示两种方法的性能对比"""
    print("=== 斐波那契数列动态规划实现 ===\n")

    # 测试小数值
    print("1. 小数值测试 (n=10):")
    n = 10
    result_memo = fibonacci_memo(n)
    result_iter = fibonacci_iterative(n)
    print(f"   记忆化递归: F({n}) = {result_memo}")
    print(f"   迭代法:     F({n}) = {result_iter}")
    print(f"   结果一致: {result_memo == result_iter}\n")

    # 性能对比
    print("2. 性能对比测试 (n=35):")
    n = 35

    # 测试记忆化递归
    start_time = time.time()
    result_memo = fibonacci_memo(n)
    time_memo = time.time() - start_time

    # 测试迭代法
    start_time = time.time()
    result_iter = fibonacci_iterative(n)
    time_iter = time.time() - start_time

    print(f"   记忆化递归: F({n}) = {result_memo}, 耗时 {time_memo:.6f} 秒")
    print(f"   迭代法:     F({n}) = {result_iter}, 耗时 {time_iter:.6f} 秒")
    print(f"   性能提升: {time_memo/time_iter:.0f} 倍\n")

    # 测试大数值（只用迭代法，避免递归深度问题）
    print("3. 大数值测试 (n=100, 仅迭代法):")
    n = 100
    result = fibonacci_iterative(n)
    print(f"   F({n}) = {result}")


if __name__ == "__main__":
    main()