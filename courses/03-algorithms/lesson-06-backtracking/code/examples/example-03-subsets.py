#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子集生成 - 回溯算法基础应用

给定一个不含重复元素的整数数组，返回该数组所有可能的子集（幂集）。

回溯策略：
1. 从空集开始
2. 对于每个元素，有两个选择：包含或不包含
3. 递归处理剩余元素
4. 到达叶子节点时，将当前子集加入结果
5. 回溯时自动恢复状态（通过函数参数传递）
"""

from typing import List


def subsets(nums: List[int]) -> List[List[int]]:
    """
    生成所有子集

    Args:
        nums: 输入数组

    Returns:
        所有子集的列表
    """
    def backtrack(start: int, current_subset: List[int]) -> None:
        """
        回溯函数

        Args:
            start: 当前考虑的元素起始索引
            current_subset: 当前构建的子集
        """
        # 每个节点都是一个有效解（包括空集）
        result.append(current_subset[:])  # 注意要复制列表

        # 从start开始，逐个考虑剩余元素
        for i in range(start, len(nums)):
            # 选择：包含当前元素
            current_subset.append(nums[i])

            # 递归：处理剩余元素
            backtrack(i + 1, current_subset)

            # 回溯：撤销选择
            current_subset.pop()

    result: List[List[int]] = []
    backtrack(0, [])
    return result


def subsets_iterative(nums: List[int]) -> List[List[int]]:
    """
    迭代方法生成子集（对比用）

    对于每个新元素，将其添加到所有现有子集中
    """
    result = [[]]
    for num in nums:
        new_subsets = []
        for subset in result:
            new_subsets.append(subset + [num])
        result.extend(new_subsets)
    return result


def print_subsets(subsets_list: List[List[int]]) -> None:
    """打印所有子集"""
    print(f"找到 {len(subsets_list)} 个子集：")
    for i, subset in enumerate(subsets_list):
        print(f"{i+1:2d}: {subset}")


if __name__ == "__main__":
    # 测试子集生成
    test_nums = [1, 2, 3]
    print(f"生成数组 {test_nums} 的所有子集：\n")

    # 回溯方法
    backtrack_result = subsets(test_nums)
    print("回溯方法结果：")
    print_subsets(backtrack_result)

    print("\n" + "="*40 + "\n")

    # 迭代方法（对比）
    iterative_result = subsets_iterative(test_nums)
    print("迭代方法结果：")
    print_subsets(iterative_result)

    # 验证两种方法结果一致
    print(f"\n两种方法结果一致: {sorted(backtrack_result) == sorted(iterative_result)}")