#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分治算法示例1：归并排序（Merge Sort）

归并排序是分治算法的经典应用，它将数组分成两半，
递归地对每一半进行排序，然后将两个有序的子数组合并成一个有序数组。
"""

from typing import List


def merge_sort(arr: List[int]) -> List[int]:
    """
    归并排序主函数

    Args:
        arr: 待排序的整数列表

    Returns:
        排序后的整数列表
    """
    # 基本情况：如果数组长度小于等于1，直接返回
    if len(arr) <= 1:
        return arr

    # 分解：找到中点，将数组分成两半
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # 解决：递归地对左右两半进行排序
    sorted_left = merge_sort(left_half)
    sorted_right = merge_sort(right_half)

    # 合并：将两个有序数组合并成一个有序数组
    return merge(sorted_left, sorted_right)


def merge(left: List[int], right: List[int]) -> List[int]:
    """
    合并两个有序数组

    Args:
        left: 左侧有序数组
        right: 右侧有序数组

    Returns:
        合并后的有序数组
    """
    result = []
    i = j = 0

    # 比较两个数组的元素，将较小的元素添加到结果中
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 将剩余的元素添加到结果中
    result.extend(left[i:])
    result.extend(right[j:])

    return result


if __name__ == "__main__":
    # 测试归并排序
    test_array = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42]
    print(f"原始数组: {test_array}")

    sorted_array = merge_sort(test_array)
    print(f"排序后数组: {sorted_array}")

    # 验证排序是否正确
    assert sorted_array == sorted(test_array), "排序结果不正确！"
    print("✅ 归并排序测试通过！")