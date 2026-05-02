#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答：最大子数组和（分治算法）

给定一个整数数组，找到具有最大和的连续子数组。
分治解法的时间复杂度为O(n log n)。
"""

from typing import List


def max_subarray_sum(arr: List[int]) -> int:
    """分治算法求解最大子数组和"""
    if not arr:
        return 0

    return _max_subarray_sum_rec(arr, 0, len(arr) - 1)


def _max_subarray_sum_rec(arr: List[int], left: int, right: int) -> int:
    """递归求解最大子数组和"""
    # 基本情况：只有一个元素
    if left == right:
        return arr[left]

    # 分解：找到中点
    mid = (left + right) // 2

    # 解决：递归求解左右两半的最大子数组和
    left_max = _max_subarray_sum_rec(arr, left, mid)
    right_max = _max_subarray_sum_rec(arr, mid + 1, right)

    # 合并：计算跨越中点的最大子数组和
    cross_max = _max_crossing_sum(arr, left, mid, right)

    # 返回三者中的最大值
    return max(left_max, right_max, cross_max)


def _max_crossing_sum(arr: List[int], left: int, mid: int, right: int) -> int:
    """计算跨越中点的最大子数组和"""
    # 从中点向左找最大和
    left_sum = float('-inf')
    current_sum = 0
    for i in range(mid, left - 1, -1):
        current_sum += arr[i]
        left_sum = max(left_sum, current_sum)

    # 从中点向右找最大和
    right_sum = float('-inf')
    current_sum = 0
    for i in range(mid + 1, right + 1):
        current_sum += arr[i]
        right_sum = max(right_sum, current_sum)

    return left_sum + right_sum


if __name__ == "__main__":
    test_array = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"测试数组: {test_array}")
    result = max_subarray_sum(test_array)
    print(f"最大子数组和: {result}")

    # 验证结果（与Kadane算法对比）
    def kadane(arr):
        max_ending_here = max_so_far = arr[0]
        for x in arr[1:]:
            max_ending_here = max(x, max_ending_here + x)
            max_so_far = max(max_so_far, max_ending_here)
        return max_so_far

    expected = kadane(test_array)
    assert result == expected, "分治算法结果不正确！"
    print("✅ 最大子数组和测试通过！")