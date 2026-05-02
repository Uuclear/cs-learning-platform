#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编程挑战1解答：全排列

给定一个不含重复数字的数组，返回其所有可能的全排列。
"""

from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    """
    生成数组的所有全排列

    Args:
        nums: 不含重复数字的数组

    Returns:
        所有全排列的列表
    """
    def backtrack(current_permutation: List[int], used: List[bool]) -> None:
        # 基础情况：当前排列长度等于原数组长度
        if len(current_permutation) == len(nums):
            result.append(current_permutation[:])
            return

        # 尝试每个未使用的数字
        for i in range(len(nums)):
            if not used[i]:
                # 选择
                current_permutation.append(nums[i])
                used[i] = True

                # 递归
                backtrack(current_permutation, used)

                # 回溯
                current_permutation.pop()
                used[i] = False

    result: List[List[int]] = []
    backtrack([], [False] * len(nums))
    return result


if __name__ == "__main__":
    test_nums = [1, 2, 3]
    result = permute(test_nums)
    print(f"数组 {test_nums} 的全排列：")
    for i, perm in enumerate(result, 1):
        print(f"{i}: {perm}")