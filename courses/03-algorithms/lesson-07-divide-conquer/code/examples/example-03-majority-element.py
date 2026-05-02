#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分治算法示例3：众数问题（Majority Element）

众数是指在数组中出现次数超过n/2的元素（n为数组长度）。
如果存在众数，那么它一定是唯一的。
分治算法可以在O(n log n)时间内找到众数。
"""

from typing import List, Optional


def majority_element(arr: List[int]) -> Optional[int]:
    """
    使用分治算法找到数组中的众数

    Args:
        arr: 整数数组

    Returns:
        众数，如果不存在则返回None
    """
    if not arr:
        return None

    candidate = _majority_element_rec(arr, 0, len(arr) - 1)

    # 验证候选元素是否真的是众数
    count = arr.count(candidate)
    if count > len(arr) // 2:
        return candidate
    else:
        return None


def _majority_element_rec(arr: List[int], left: int, right: int) -> int:
    """
    递归求解众数

    Args:
        arr: 数组
        left: 左边界（包含）
        right: 右边界（包含）

    Returns:
        候选众数
    """
    # 基本情况：只有一个元素
    if left == right:
        return arr[left]

    # 分解：找到中点
    mid = (left + right) // 2

    # 解决：递归求解左右两半的候选众数
    left_candidate = _majority_element_rec(arr, left, mid)
    right_candidate = _majority_element_rec(arr, mid + 1, right)

    # 如果左右候选相同，直接返回
    if left_candidate == right_candidate:
        return left_candidate

    # 否则，计算两个候选在整个区间中的出现次数
    left_count = _count_in_range(arr, left_candidate, left, right)
    right_count = _count_in_range(arr, right_candidate, left, right)

    # 返回出现次数更多的候选
    return left_candidate if left_count > right_count else right_candidate


def _count_in_range(arr: List[int], target: int, left: int, right: int) -> int:
    """计算目标元素在指定范围内的出现次数"""
    count = 0
    for i in range(left, right + 1):
        if arr[i] == target:
            count += 1
    return count


if __name__ == "__main__":
    # 测试用例1：存在众数
    test_array1 = [3, 2, 3, 2, 2, 2, 5, 4, 2]
    print(f"测试数组1: {test_array1}")
    result1 = majority_element(test_array1)
    print(f"众数: {result1}")

    # 验证结果
    if result1 is not None:
        count = test_array1.count(result1)
        assert count > len(test_array1) // 2, "找到的不是真正的众数！"
        print("✅ 测试1通过！")
    else:
        print("❌ 测试1失败：应该找到众数！")

    # 测试用例2：不存在众数
    test_array2 = [1, 2, 3, 4, 5]
    print(f"\n测试数组2: {test_array2}")
    result2 = majority_element(test_array2)
    print(f"众数: {result2}")

    # 验证结果
    assert result2 is None, "不应该找到众数！"
    print("✅ 测试2通过！")

    # 测试用例3：单个元素
    test_array3 = [42]
    print(f"\n测试数组3: {test_array3}")
    result3 = majority_element(test_array3)
    print(f"众数: {result3}")

    assert result3 == 42, "单个元素应该是众数！"
    print("✅ 测试3通过！")