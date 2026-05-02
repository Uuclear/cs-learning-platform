#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编程挑战2解答：组合总和

给定一个无重复元素的正整数数组 candidates 和一个目标数 target，
找出 candidates 中所有可以使数字和为 target 的组合。
candidates 中的数字可以无限制重复被选取。
"""

from typing import List


def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """
    找出所有和为目标值的组合

    Args:
        candidates: 候选数字数组（无重复正整数）
        target: 目标和

    Returns:
        所有满足条件的组合列表
    """
    def backtrack(start: int, current_combination: List[int], current_sum: int) -> None:
        # 剪枝：如果当前和已经超过目标，直接返回
        if current_sum > target:
            return

        # 基础情况：找到有效组合
        if current_sum == target:
            result.append(current_combination[:])
            return

        # 从start开始尝试每个候选数字（允许重复使用）
        for i in range(start, len(candidates)):
            # 选择
            current_combination.append(candidates[i])

            # 递归：注意这里传入i而不是i+1，因为可以重复使用同一数字
            backtrack(i, current_combination, current_sum + candidates[i])

            # 回溯
            current_combination.pop()

    result: List[List[int]] = []
    backtrack(0, [], 0)
    return result


if __name__ == "__main__":
    candidates = [2, 3, 6, 7]
    target = 7
    result = combination_sum(candidates, target)
    print(f"候选数组: {candidates}")
    print(f"目标值: {target}")
    print("所有组合:")
    for i, combo in enumerate(result, 1):
        print(f"{i}: {combo} (和为 {sum(combo)})")