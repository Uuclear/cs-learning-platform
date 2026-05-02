#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: O(1) vs O(n) 时间复杂度对比

这个例子展示了常数时间复杂度和线性时间复杂度的区别。
通过实际运行时间的对比，让你直观感受到不同复杂度的性能差异。
"""

import time
import random


def access_array_by_index(arr, index):
    """
    O(1) - 常数时间复杂度
    无论数组多大，通过索引访问元素的时间都是固定的
    """
    return arr[index]


def find_element_linear(arr, target):
    """
    O(n) - 线性时间复杂度
    需要遍历整个数组来查找目标元素，时间与数组长度成正比
    """
    for i, element in enumerate(arr):
        if element == target:
            return i
    return -1


def demonstrate_o1_vs_on():
    """演示O(1)和O(n)的性能差异"""
    print("=== O(1) vs O(n) 性能对比 ===")

    # 测试不同大小的数组
    sizes = [1000, 10000, 100000, 1000000]

    for size in sizes:
        # 创建随机数组
        arr = [random.randint(1, size * 10) for _ in range(size)]
        target = arr[-1]  # 确保目标存在（在最后一个位置）
        test_index = size // 2  # 测试中间位置

        # 测试O(1)操作
        start_time = time.perf_counter()
        result1 = access_array_by_index(arr, test_index)
        o1_time = time.perf_counter() - start_time

        # 测试O(n)操作（最坏情况：目标在最后）
        start_time = time.perf_counter()
        result2 = find_element_linear(arr, target)
        on_time = time.perf_counter() - start_time

        print(f"数组大小: {size:>7}")
        print(f"  O(1) 访问时间: {o1_time:.6f} 秒")
        print(f"  O(n) 查找时间: {on_time:.6f} 秒")
        print(f"  性能差距: {on_time/o1_time:.0f} 倍")
        print()


if __name__ == "__main__":
    demonstrate_o1_vs_on()