#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答: 空间复杂度分析和优化

题目：分析给定算法的空间复杂度，并尝试优化
"""

def fibonacci_recursive(n):
    """
    时间复杂度: O(2^n)
    空间复杂度: O(n) - 递归调用栈的深度
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n):
    """
    时间复杂度: O(n)
    空间复杂度: O(1) - 只使用常数个变量
    """
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b

    return b


def reverse_string_recursive(s):
    """
    时间复杂度: O(n)
    空间复杂度: O(n) - 递归调用栈 + 字符串切片创建新字符串
    """
    if len(s) <= 1:
        return s
    return s[-1] + reverse_string_recursive(s[:-1])


def reverse_string_iterative(s):
    """
    时间复杂度: O(n)
    空间复杂度: O(n) - 需要创建新字符串存储结果
    注意：在Python中字符串是不可变的，所以无论如何都需要O(n)空间
    """
    return s[::-1]


def reverse_list_inplace(arr):
    """
    时间复杂度: O(n)
    空间复杂度: O(1) - 原地反转，只使用常数额外空间
    """
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr


if __name__ == "__main__":
    # 测试斐波那契
    n = 10
    print(f"斐波那契 F({n}):")
    print(f"  递归方法: {fibonacci_recursive(n)}")
    print(f"  迭代方法: {fibonacci_iterative(n)}")

    # 测试字符串反转
    test_str = "hello world"
    print(f"\n字符串反转 '{test_str}':")
    print(f"  递归方法: {reverse_string_recursive(test_str)}")
    print(f"  迭代方法: {reverse_string_iterative(test_str)}")

    # 测试列表原地反转
    test_list = [1, 2, 3, 4, 5]
    print(f"\n列表原地反转 {test_list}:")
    print(f"  结果: {reverse_list_inplace(test_list.copy())}")

    print("\n空间复杂度总结:")
    print("- 递归通常需要O(n)栈空间")
    print("- 迭代通常可以达到O(1)空间复杂度")
    print("- 对于不可变对象（如Python字符串），操作通常需要O(n)空间")
    print("- 原地操作可以最小化空间使用")