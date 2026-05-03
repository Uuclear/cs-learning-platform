#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：随机选择算法完整实现

这个文件提供了随机选择算法（Quickselect）的完整实现，
包括详细的性能分析和正确性验证。
"""

import random
import time

class RandomizedSelect:
    """
    随机选择算法类，支持完整的性能跟踪和分析

    Attributes:
        comparisons (int): 总比较次数
        swaps (int): 总交换次数
        max_depth (int): 最大递归深度
        operations_log (list): 操作日志
    """

    def __init__(self):
        """初始化计数器"""
        self.comparisons = 0
        self.swaps = 0
        self.max_depth = 0
        self.operations_log = []

    def _partition(self, arr, low, high):
        """
        随机分区函数

        Args:
            arr (list): 数组
            low (int): 起始索引
            high (int): 结束索引

        Returns:
            int: 主元的最终位置
        """
        # 随机选择主元并移到末尾
        random_index = random.randint(low, high)
        arr[random_index], arr[high] = arr[high], arr[random_index]
        self.swaps += 1

        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            self.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    self.swaps += 1

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        if i + 1 != high:
            self.swaps += 1

        return i + 1

    def _select_recursive(self, arr, low, high, k, depth=0):
        """
        递归选择函数

        Args:
            arr (list): 数组
            low (int): 起始索引
            high (int): 结束索引
            k (int): 目标秩（相对于low）
            depth (int): 当前递归深度

        Returns:
            int: 第k小的元素值
        """
        self.max_depth = max(self.max_depth, depth)

        # 记录操作日志
        operation_info = {
            'type': 'recursive_call',
            'low': low,
            'high': high,
            'k': k,
            'depth': depth,
            'subarray_size': high - low + 1
        }
        self.operations_log.append(operation_info)

        if low == high:
            return arr[low]

        # 分区
        pivot_index = self._partition(arr, low, high)
        pivot_rank = pivot_index - low

        operation_info['pivot_index'] = pivot_index
        operation_info['pivot_rank'] = pivot_rank

        if k == pivot_rank:
            return arr[pivot_index]
        elif k < pivot_rank:
            return self._select_recursive(arr, low, pivot_index - 1, k, depth + 1)
        else:
            return self._select_recursive(arr, pivot_index + 1, high, k - pivot_rank - 1, depth + 1)

    def select(self, arr, k):
        """
        主选择函数

        Args:
            arr (list): 输入数组
            k (int): 要找的第k小元素的索引（0-based）

        Returns:
            tuple: (结果, 统计信息字典)
        """
        if not arr:
            raise ValueError("输入数组不能为空")
        if k < 0 or k >= len(arr):
            raise ValueError(f"k必须在范围[0, {len(arr)-1}]内")

        # 重置计数器
        self.comparisons = 0
        self.swaps = 0
        self.max_depth = 0
        self.operations_log = []

        # 创建数组副本以避免修改原数组
        arr_copy = arr.copy()
        start_time = time.time()

        result = self._select_recursive(arr_copy, 0, len(arr_copy) - 1, k)

        end_time = time.time()
        execution_time = end_time - start_time

        # 验证结果正确性
        expected_result = sorted(arr)[k]
        is_correct = result == expected_result

        stats = {
            'result': result,
            'expected': expected_result,
            'is_correct': is_correct,
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'max_depth': self.max_depth,
            'execution_time': execution_time,
            'array_size': len(arr),
            'operations_count': len(self.operations_log)
        }

        return result, stats

def analyze_randomized_select():
    """分析随机选择算法的性能"""
    print("=== 随机选择算法性能分析 ===\n")

    # 测试不同类型的输入
    test_cases = [
        ("随机数组", lambda n: [random.randint(1, 1000) for _ in range(n)]),
        ("已排序数组", lambda n: list(range(n))),
        ("逆序数组", lambda n: list(range(n, 0, -1))),
        ("重复元素", lambda n: [random.randint(1, 10) for _ in range(n)])
    ]

    sizes = [100, 500, 1000, 5000]
    k_positions = [0, 'median', -1]  # 最小、中位数、最大

    for size in sizes:
        print(f"--- 数组大小: {size} ---")

        for name, generator in test_cases:
            arr = generator(size)

            for k_pos in k_positions:
                if k_pos == 'median':
                    k = size // 2
                    pos_name = "中位数"
                elif k_pos == -1:
                    k = size - 1
                    pos_name = "最大值"
                else:
                    k = k_pos
                    pos_name = "最小值"

                selector = RandomizedSelect()
                result, stats = selector.select(arr, k)

                print(f"{name:12} {pos_name:6}: "
                      f"比较={stats['comparisons']:6d}, "
                      f"交换={stats['swaps']:5d}, "
                      f"深度={stats['max_depth']:3d}, "
                      f"时间={stats['execution_time']:.4f}s, "
                      f"正确={stats['is_correct']}")

        print()

def theoretical_analysis(n):
    """理论分析期望比较次数"""
    import math

    # 随机选择的期望比较次数 ≈ 4n
    expected_comparisons = 4 * n

    print(f"\n理论分析 (n={n}):")
    print(f"期望比较次数: {expected_comparisons:.0f}")
    print(f"最坏情况比较次数: {n*(n+1)//2}")
    print(f"最好情况比较次数: {n}")

def main():
    """主函数"""
    analyze_randomized_select()

    # 理论分析
    for n in [100, 500, 1000]:
        theoretical_analysis(n)

if __name__ == "__main__":
    main()

# 预期输出示例:
# === 随机选择算法性能分析 ===
#
# --- 数组大小: 100 ---
# 随机数组     中位数: 比较=   423, 交换=   89, 深度= 12, 时间=0.0008s, 正确=True
# 已排序数组   中位数: 比较=   389, 交换=   76, 深度= 15, 时间=0.0007s, 正确=True
# 逆序数组     中位数: 比较=   401, 交换=   82, 深度= 14, 时间=0.0008s, 正确=True
# 重复元素     中位数: 比较=   267, 交换=   65, 深度= 10, 时间=0.0006s, 正确=True