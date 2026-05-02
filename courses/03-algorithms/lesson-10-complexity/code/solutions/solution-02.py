#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 优化具有高时间复杂度的代码

题目：给定一个函数，其时间复杂度为O(n²)，请将其优化到O(n log n)或更好
"""

def find_duplicates_slow(arr):
    """
    O(n²) - 慢速查找重复元素
    对每个元素都与其他所有元素比较
    """
    duplicates = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in duplicates:
                duplicates.append(arr[i])
    return duplicates


def find_duplicates_fast(arr):
    """
    O(n) - 快速查找重复元素
    使用哈希表（字典）来记录已见过的元素
    """
    seen = set()
    duplicates = set()

    for element in arr:
        if element in seen:
            duplicates.add(element)
        else:
            seen.add(element)

    return list(duplicates)


def find_duplicates_sorted(arr):
    """
    O(n log n) - 通过排序查找重复元素
    先排序，然后检查相邻元素
    """
    if not arr:
        return []

    sorted_arr = sorted(arr)  # O(n log n)
    duplicates = []

    for i in range(1, len(sorted_arr)):  # O(n)
        if sorted_arr[i] == sorted_arr[i-1]:
            if not duplicates or duplicates[-1] != sorted_arr[i]:
                duplicates.append(sorted_arr[i])

    return duplicates


if __name__ == "__main__":
    test_arr = [1, 3, 2, 4, 3, 5, 2, 6, 7, 8, 9, 1]

    print("原始数组:", test_arr)
    print("慢速方法结果:", find_duplicates_slow(test_arr))
    print("快速方法结果:", find_duplicates_fast(test_arr))
    print("排序方法结果:", find_duplicates_sorted(test_arr))

    # 验证结果一致性
    assert set(find_duplicates_slow(test_arr)) == set(find_duplicates_fast(test_arr))
    assert set(find_duplicates_slow(test_arr)) == set(find_duplicates_sorted(test_arr))
    print("所有方法结果一致！")