#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答：实现快速排序（分治算法）

快速排序也是分治算法的经典应用，通过选择一个基准元素，
将数组分成小于基准和大于基准的两部分，然后递归排序。
"""

from typing import List


def quick_sort(arr: List[int]) -> List[int]:
    """快速排序实现"""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]  # 选择中间元素作为基准
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


if __name__ == "__main__":
    test_array = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42]
    print(f"原始数组: {test_array}")
    sorted_array = quick_sort(test_array)
    print(f"快速排序结果: {sorted_array}")
    assert sorted_array == sorted(test_array), "快速排序结果不正确！"
    print("✅ 快速排序测试通过！")