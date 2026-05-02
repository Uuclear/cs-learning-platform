#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: O(n²) vs O(n log n) 时间复杂度对比

这个例子对比了冒泡排序（O(n²)）和归并排序（O(n log n)）的性能差异。
随着数据规模增大，两种算法的性能差距会急剧扩大。
"""

import time
import random


def bubble_sort(arr):
    """
    O(n²) - 冒泡排序
    通过重复遍历数组，比较相邻元素并交换位置
    时间复杂度为 n²，对于大数据集非常慢
    """
    arr = arr.copy()  # 不修改原数组
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def merge_sort(arr):
    """
    O(n log n) - 归并排序
    采用分治策略，将数组分成两半，递归排序后再合并
    时间复杂度为 n log n，对于大数据集表现优秀
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    """合并两个已排序的数组"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def demonstrate_on2_vs_onlogn():
    """演示O(n²)和O(n log n)的性能差异"""
    print("=== O(n²) vs O(n log n) 性能对比 ===")

    # 测试不同大小的数组（注意：O(n²)算法在大数据上会很慢）
    sizes = [100, 500, 1000, 2000]

    for size in sizes:
        # 创建随机数组
        arr = [random.randint(1, size * 10) for _ in range(size)]

        # 测试O(n²)算法
        start_time = time.perf_counter()
        sorted_bubble = bubble_sort(arr)
        on2_time = time.perf_counter() - start_time

        # 测试O(n log n)算法
        start_time = time.perf_counter()
        sorted_merge = merge_sort(arr)
        onlogn_time = time.perf_counter() - start_time

        # 验证结果正确性
        assert sorted_bubble == sorted_merge, "排序结果不一致！"

        print(f"数组大小: {size:>4}")
        print(f"  O(n²) 冒泡排序: {on2_time:.6f} 秒")
        print(f"  O(n log n) 归并排序: {onlogn_time:.6f} 秒")
        print(f"  性能差距: {on2_time/onlogn_time:.1f} 倍")
        print()


if __name__ == "__main__":
    demonstrate_on2_vs_onlogn()