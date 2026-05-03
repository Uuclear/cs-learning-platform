#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：点在多边形内测试与最近点对
演示射线法点定位和分治法求最近点对
"""

import random
import math

class Point:
    """二维点类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

    def distance_to(self, other):
        """计算到另一个点的距离"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

def point_in_polygon(point, polygon):
    """
    射线法判断点是否在多边形内

    参数:
        point: Point对象，待测试的点
        polygon: Point对象列表，多边形顶点（按顺序）

    返回:
        bool - True表示在内部，False表示在外部
    """
    x, y = point.x, point.y
    n = len(polygon)
    if n < 3:
        return False

    inside = False
    p1x, p1y = polygon[0].x, polygon[0].y

    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n].x, polygon[i % n].y

        # 检查点是否在边的y范围内
        if min(p1y, p2y) < y <= max(p1y, p2y):
            # 计算交点的x坐标
            if p1y != p2y:
                xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if x < xinters:
                    inside = not inside

        p1x, p1y = p2x, p2y

    return inside

def closest_pair_brute_force(points):
    """
    暴力法求最近点对

    返回:
        (min_distance, point1, point2)
    """
    if len(points) < 2:
        return float('inf'), None, None

    min_dist = float('inf')
    best_pair = (None, None)

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = points[i].distance_to(points[j])
            if dist < min_dist:
                min_dist = dist
                best_pair = (points[i], points[j])

    return min_dist, best_pair[0], best_pair[1]

def closest_pair_divide_conquer(points_sorted_by_x):
    """
    分治法求最近点对（简化版，仅返回距离）

    注意：这是简化实现，完整实现需要处理跨越中线的情况
    """
    n = len(points_sorted_by_x)
    if n <= 3:
        min_dist, _, _ = closest_pair_brute_force(points_sorted_by_x)
        return min_dist

    mid = n // 2
    mid_point = points_sorted_by_x[mid]

    left_points = points_sorted_by_x[:mid]
    right_points = points_sorted_by_x[mid:]

    # 递归求解左右两半
    d_left = closest_pair_divide_conquer(left_points)
    d_right = closest_pair_divide_conquer(right_points)
    d = min(d_left, d_right)

    # 简化：这里应该检查跨越中线的点对
    # 完整实现需要按y坐标排序并检查带状区域内的点
    return d

def main():
    """主函数：演示点定位和最近点对"""
    print("计算几何示例2：点定位与最近点对")
    print("=" * 40)

    # 测试点在多边形内
    square = [
        Point(0, 0), Point(2, 0),
        Point(2, 2), Point(0, 2)
    ]

    test_points = [
        Point(1, 1),    # 内部
        Point(3, 3),    # 外部
        Point(0, 0),    # 顶点
        Point(1, 0),    # 边上
        Point(-1, -1)   # 外部
    ]

    print("正方形多边形:", [str(p) for p in square])
    for p in test_points:
        result = point_in_polygon(p, square)
        print(f"点 {p} 在多边形内: {result}")

    # 测试最近点对
    print("\n最近点对测试:")
    random_points = [Point(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(10)]
    print("随机点集:", [str(p) for p in random_points[:5]], "...")  # 只显示前5个

    min_dist, p1, p2 = closest_pair_brute_force(random_points)
    print(f"暴力法最近距离: {min_dist:.4f}")
    print(f"最近点对: {p1} 和 {p2}")

    # 分治法（简化版）
    sorted_points = sorted(random_points, key=lambda p: p.x)
    div_dist = closest_pair_divide_conquer(sorted_points)
    print(f"分治法最近距离: {div_dist:.4f}")

if __name__ == "__main__":
    main()