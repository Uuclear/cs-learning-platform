#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
近似算法示例2：集合覆盖的贪心算法

这个示例演示了集合覆盖问题的贪心近似算法，
并分析其H(n)近似比。

预期输出：
全集: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

子集族:
S1: {1, 2, 3, 4, 5}
S2: {4, 5, 6, 7}
S3: {6, 7, 8, 9, 10}
S4: {1, 2, 8, 9}

贪心算法选择顺序:
第1步: 选择 S1 (覆盖5个新元素)
第2步: 选择 S3 (覆盖5个新元素)

最终覆盖: [S1, S3]
覆盖大小: 2

调和数 H(10) = 2.93
实际近似比: 1.0 (找到最优解)
"""

import math

def set_cover_greedy(universe, subsets):
    """
    集合覆盖问题的贪心近似算法

    参数:
        universe: 全集，set类型
        subsets: 子集列表，每个子集是set类型

    返回:
        list: 选择的子集索引列表
    """
    covered = set()
    selected = []
    subset_names = [f"S{i+1}" for i in range(len(subsets))]

    print("贪心算法选择顺序:")
    step = 1

    while len(covered) < len(universe):
        best_idx = -1
        best_coverage = 0

        # 找到覆盖最多未覆盖元素的子集
        for i, subset in enumerate(subsets):
            if i not in selected:  # 避免重复选择
                coverage = len(subset - covered)
                if coverage > best_coverage:
                    best_coverage = coverage
                    best_idx = i

        if best_idx == -1 or best_coverage == 0:
            break  # 无法覆盖所有元素

        selected.append(best_idx)
        covered.update(subsets[best_idx])
        print(f"第{step}步: 选择 {subset_names[best_idx]} (覆盖{best_coverage}个新元素)")
        step += 1

    return selected

def harmonic_number(n):
    """计算第n个调和数 H(n) = 1 + 1/2 + ... + 1/n"""
    return sum(1.0 / i for i in range(1, n + 1))

def find_optimal_set_cover(universe, subsets):
    """
    小规模集合覆盖的最优解（暴力搜索）
    仅用于验证，时间复杂度O(2^m)，m为子集数量
    """
    m = len(subsets)
    best_solution = None
    best_size = float('inf')

    for mask in range(1 << m):
        current_cover = set()
        selected = []

        for i in range(m):
            if mask & (1 << i):
                current_cover.update(subsets[i])
                selected.append(i)

        if current_cover >= universe and len(selected) < best_size:
            best_size = len(selected)
            best_solution = selected.copy()

    return best_solution

def main():
    # 定义全集和子集族
    universe = set(range(1, 11))  # {1, 2, ..., 10}
    subsets = [
        {1, 2, 3, 4, 5},      # S1
        {4, 5, 6, 7},         # S2
        {6, 7, 8, 9, 10},     # S3
        {1, 2, 8, 9}          # S4
    ]

    print(f"全集: {universe}")
    print()
    print("子集族:")
    for i, subset in enumerate(subsets):
        print(f"S{i+1}: {subset}")
    print()

    # 运行贪心算法
    greedy_solution = set_cover_greedy(universe, subsets)
    greedy_size = len(greedy_solution)

    print(f"\n最终覆盖: {[f'S{i+1}' for i in greedy_solution]}")
    print(f"覆盖大小: {greedy_size}")
    print()

    # 计算理论近似比上限
    n = len(universe)
    h_n = harmonic_number(n)
    print(f"调和数 H({n}) = {h_n:.2f}")

    # 计算实际最优解（小规模）
    optimal_solution = find_optimal_set_cover(universe, subsets)
    if optimal_solution:
        optimal_size = len(optimal_solution)
        actual_ratio = greedy_size / optimal_size
        print(f"实际近似比: {actual_ratio:.1f} (找到最优解)")
    else:
        print("无法找到完整覆盖")

if __name__ == "__main__":
    main()