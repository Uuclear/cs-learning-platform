#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分治算法示例2：最近点对问题（Closest Pair of Points）

在平面上给定n个点，找出距离最近的两个点。
暴力解法的时间复杂度是O(n²)，而分治算法可以将时间复杂度降低到O(n log n)。
"""

from typing import List, Tuple
import math


def closest_pair(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
    """
    找出平面上距离最近的两个点（分治算法）

    Args:
        points: 点的列表，每个点表示为(x, y)元组

    Returns:
        (点1, 点2, 距离) 的元组
    """
    # 按x坐标排序
    points_sorted_by_x = sorted(points, key=lambda p: p[0])

    # 按y坐标排序
    points_sorted_by_y = sorted(points, key=lambda p: p[1])

    return _closest_pair_rec(points_sorted_by_x, points_sorted_by_y)


def _closest_pair_rec(px: List[Tuple[float, float]], py: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
    """
    递归求解最近点对

    Args:
        px: 按x坐标排序的点列表
        py: 按y坐标排序的点列表

    Returns:
        (点1, 点2, 距离) 的元组
    """
    n = len(px)

    # 基本情况：点数较少时使用暴力解法
    if n <= 3:
        return _brute_force_closest_pair(px)

    # 分解：找到中点，将点集分成左右两半
    mid = n // 2
    midpoint = px[mid]

    # 左右两半按x排序的点
    plx = px[:mid]
    prx = px[mid:]

    # 左右两半按y排序的点
    ply = [p for p in py if p[0] <= midpoint[0]]
    pry = [p for p in py if p[0] > midpoint[0]]

    # 解决：递归求解左右两半的最近点对
    left_pair = _closest_pair_rec(plx, ply)
    right_pair = _closest_pair_rec(prx, pry)

    # 找出左右两半中距离更小的一对
    if left_pair[2] <= right_pair[2]:
        min_pair = left_pair
    else:
        min_pair = right_pair

    min_dist = min_pair[2]

    # 合并：检查跨越中线的点对
    # 找出距离中线小于min_dist的所有点
    strip = [p for p in py if abs(p[0] - midpoint[0]) < min_dist]

    # 在strip中寻找更近的点对
    strip_pair = _closest_in_strip(strip, min_dist)

    if strip_pair[2] < min_dist:
        return strip_pair
    else:
        return min_pair


def _brute_force_closest_pair(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
    """暴力求解最近点对（用于基本情况）"""
    min_dist = float('inf')
    pair = (points[0], points[1])

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = _distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                pair = (points[i], points[j])

    return (pair[0], pair[1], min_dist)


def _closest_in_strip(strip: List[Tuple[float, float]], min_dist: float) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
    """在strip中寻找最近点对"""
    min_pair = ((0, 0), (0, 0))
    best_dist = min_dist

    # 对于strip中的每个点，只需要检查其后最多7个点
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j][1] - strip[i][1]) < best_dist:
            dist = _distance(strip[i], strip[j])
            if dist < best_dist:
                best_dist = dist
                min_pair = (strip[i], strip[j])
            j += 1

    return (min_pair[0], min_pair[1], best_dist)


def _distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """计算两点间的欧几里得距离"""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


if __name__ == "__main__":
    # 测试最近点对算法
    test_points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print(f"测试点集: {test_points}")

    closest = closest_pair(test_points)
    print(f"最近点对: {closest[0]} 和 {closest[1]}")
    print(f"距离: {closest[2]:.4f}")

    # 验证结果（与暴力解法对比）
    brute_result = _brute_force_closest_pair(test_points)
    assert abs(closest[2] - brute_result[2]) < 1e-10, "分治算法结果不正确！"
    print("✅ 最近点对算法测试通过！")