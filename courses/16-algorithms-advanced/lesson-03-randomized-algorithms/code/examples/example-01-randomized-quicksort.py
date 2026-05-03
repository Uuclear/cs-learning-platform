#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：随机快速排序实现与分析

这个文件演示了随机快速排序的实现，包括详细的比较次数统计
和性能分析。
"""

import random
import time

class RandomizedQuickSort:
    """
    随机快速排序类，支持详细的性能跟踪

    Attributes:
        total_comparisons (int): 总比较次数
        total_swaps (int): 总交换次数
        recursion_depth (int): 最大递归深度
    """

    def __init__(self):
        """初始化计数器"""
        self.total_comparisons = 0
        self.total_swaps = 0
        self.recursion_depth = 0
        self.max_depth = 0

    def _partition(self, arr, low, high):
        """
        分区函数，使用随机主元

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
        self.total_swaps += 1

        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            self.total_comparisons += 1
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    self.total_swaps += 1

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        if i + 1 != high:
            self.total_swaps += 1

        return i + 1

    def _quicksort_recursive(self, arr, low, high, current_depth=0):
        """
        快速排序递归函数

        Args:
            arr (list): 数组
            low (int): 起始索引
            high (int): 结束索引
            current_depth (int): 当前递归深度
        """
        if low < high:
            self.recursion_depth = current_depth
            self.max_depth = max(self.max_depth, current_depth)

            pi = self._partition(arr, low, high)
            self._quicksort_recursive(arr, low, pi - 1, current_depth + 1)
            self._quicksort_recursive(arr, pi + 1, high, current_depth + 1)

    def sort(self, arr):
        """
        对数组进行随机快速排序

        Args:
            arr (list): 要排序的数组

        Returns:
            dict: 包含性能统计信息的字典
        """
        if not arr:
            return {'comparisons': 0, 'swaps': 0, 'max_depth': 0}

        original_arr = arr.copy()
        start_time = time.time()

        self.total_comparisons = 0
        self.total_swaps = 0
        self.max_depth = 0

        self._quicksort_recursive(arr, 0, len(arr) - 1)

        end_time = time.time()
        execution_time = end_time - start_time

        # 验证排序正确性
        is_sorted = arr == sorted(original_arr)

        return {
            'comparisons': self.total_comparisons,
            'swaps': self.total_swaps,
            'max_depth': self.max_depth,
            'execution_time': execution_time,
            'is_sorted': is_sorted
        }

def analyze_randomized_quicksort():
    """分析随机快速排序的性能"""
    print("=== 随机快速排序性能分析 ===\n")

    # 测试不同类型的输入
    test_cases = [
        ("已排序数组", lambda n: list(range(n))),
        ("逆序数组", lambda n: list(range(n, 0, -1))),
        ("随机数组", lambda n: [random.randint(1, 1000) for _ in range(n)]),
        ("重复元素", lambda n: [random.randint(1, 10) for _ in range(n)])
    ]

    sizes = [100, 500, 1000]

    for size in sizes:
        print(f"--- 数组大小: {size} ---")

        for name, generator in test_cases:
            arr = generator(size)
            sorter = RandomizedQuickSort()
            stats = sorter.sort(arr)

            print(f"{name:12}: 比较={stats['comparisons']:6d}, "
                  f"交换={stats['swaps']:5d}, "
                  f"深度={stats['max_depth']:3d}, "
                  f"时间={stats['execution_time']:.4f}s, "
                  f"正确={stats['is_sorted']}")

        print()

def theoretical_analysis(n):
    """理论分析期望比较次数"""
    import math

    # 随机快速排序的期望比较次数 ≈ 2n ln n
    expected_comparisons = 2 * n * math.log(n) if n > 1 else 0

    print(f"\n理论分析 (n={n}):")
    print(f"期望比较次数: {expected_comparisons:.0f}")
    print(f"最坏情况比较次数: {n*(n-1)//2}")
    print(f"最好情况比较次数: {n*math.log2(n) if n > 1 else 0:.0f}")

def main():
    """主函数"""
    analyze_randomized_quicksort()

    # 理论分析
    for n in [100, 500, 1000]:
        theoretical_analysis(n)

if __name__ == "__main__":
    main()

# 预期输出示例:
# === 随机快速排序性能分析 ===
#
# --- 数组大小: 100 ---
# 已排序数组  : 比较=   789, 交换=  102, 深度= 15, 时间=0.0012s, 正确=True
# 逆序数组    : 比较=   823, 交换=   98, 深度= 18, 时间=0.0014s, 正确=True
# 随机数组    : 比较=   801, 交换=  105, 深度= 16, 时间=0.0013s, 正确=True
# 重复元素    : 比较=   456, 交换=   89, 深度= 12, 时间=0.0009s, 正确=True