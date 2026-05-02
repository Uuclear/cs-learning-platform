#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 指数时间复杂度 O(2^n)

这个例子展示了指数时间复杂度的恐怖之处。
斐波那契数列的朴素递归实现具有O(2^n)的时间复杂度，
即使对于很小的输入，也会导致计算时间急剧增长。
"""

import time


def fibonacci_naive(n):
    """
    O(2^n) - 朴素递归实现斐波那契数列
    每次调用都会产生两个子调用，形成指数级增长的调用树
    对于n>40的情况，计算时间会变得非常长
    """
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memoized(n, memo={}):
    """
    O(n) - 带记忆化的斐波那契数列
    通过缓存已经计算过的结果，避免重复计算
    将时间复杂度从O(2^n)降低到O(n)
    """
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


def demonstrate_exponential():
    """演示指数时间复杂度的问题"""
    print("=== 指数时间复杂度 O(2^n) 的恐怖 ===")
    print("计算斐波那契数列的不同实现方式对比\n")

    # 测试不同大小的输入（注意：朴素递归在n>40时会很慢）
    test_values = [10, 20, 30, 35]

    for n in test_values:
        print(f"计算第 {n} 个斐波那契数:")

        # 测试朴素递归（O(2^n)）
        start_time = time.perf_counter()
        result_naive = fibonacci_naive(n)
        naive_time = time.perf_counter() - start_time

        # 测试记忆化递归（O(n)）
        start_time = time.perf_counter()
        result_memo = fibonacci_memoized(n, {})
        memo_time = time.perf_counter() - start_time

        # 验证结果正确性
        assert result_naive == result_memo, "计算结果不一致！"

        print(f"  朴素递归 O(2^n): {naive_time:.6f} 秒")
        print(f"  记忆化递归 O(n): {memo_time:.6f} 秒")
        if naive_time > 0.000001:  # 避免除零错误
            print(f"  性能差距: {naive_time/memo_time:.0f} 倍")
        print()

    # 展示更大的n值会有多恐怖
    print("尝试更大的数值（仅使用高效算法）:")
    large_values = [40, 50, 100]
    for n in large_values:
        start_time = time.perf_counter()
        result = fibonacci_memoized(n, {})
        memo_time = time.perf_counter() - start_time
        print(f"  F({n}) = {result} (耗时: {memo_time:.6f} 秒)")

    print("\n注意：如果用朴素递归计算F(50)，可能需要几个小时！")


if __name__ == "__main__":
    demonstrate_exponential()