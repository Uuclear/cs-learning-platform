#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: 分析给定函数的时间复杂度

题目：分析以下函数的时间复杂度，并解释原因
"""

def find_max(arr):
    """找到数组中的最大值"""
    max_val = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val


def nested_loop_example(n):
    """嵌套循环示例"""
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
    return count


def binary_search(arr, target):
    """二分查找"""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# 复杂度分析：
# find_max: O(n) - 需要遍历整个数组一次
# nested_loop_example: O(n²) - 双重嵌套循环，每层都是n次
# binary_search: O(log n) - 每次迭代都将搜索空间减半


if __name__ == "__main__":
    # 测试函数
    test_arr = [3, 7, 2, 9, 1, 5]
    print(f"最大值: {find_max(test_arr)}")

    print(f"嵌套循环计数 (n=5): {nested_loop_example(5)}")

    sorted_arr = [1, 2, 3, 5, 7, 9]
    print(f"二分查找 5 的位置: {binary_search(sorted_arr, 5)}")