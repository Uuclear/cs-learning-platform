#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：叉积计算与凸包算法
演示向量叉积的计算和Graham扫描法求凸包
"""

import math

class Point:
    """二维点类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def cross_product(o, a, b):
    """
    计算向量oa和ob的叉积

    参数:
        o, a, b: Point对象

    返回:
        float - 叉积值
        > 0: b在oa左侧（逆时针）
        < 0: b在oa右侧（顺时针）
        = 0: 三点共线
    """
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

def orientation(p, q, r):
    """
    判断三点的方向关系

    返回:
        0: 共线
        1: 逆时针（左转）
        2: 顺时针（右转）
    """
    val = cross_product(p, q, r)
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def graham_scan(points):
    """
    Graham扫描法求凸包

    参数:
        points: Point对象列表

    返回:
        Point对象列表，表示凸包顶点（按逆时针顺序）
    """
    if len(points) <= 2:
        return points[:]

    # 找到最下方的点（y最小，x最小）
    start = min(points, key=lambda p: (p.y, p.x))

    # 按极角排序
    def polar_angle(p):
        return math.atan2(p.y - start.y, p.x - start.x)

    # 排序并处理相同极角的情况
    sorted_points = sorted(points, key=lambda p: (polar_angle(p),
                                                 (p.x - start.x)**2 + (p.y - start.y)**2))

    # 移除重复点
    unique_points = [sorted_points[0]]
    for i in range(1, len(sorted_points)):
        if sorted_points[i] != sorted_points[i-1]:
            unique_points.append(sorted_points[i])

    if len(unique_points) <= 2:
        return unique_points

    # Graham扫描
    hull = [unique_points[0], unique_points[1]]
    for i in range(2, len(unique_points)):
        while len(hull) >= 2 and cross_product(hull[-2], hull[-1], unique_points[i]) <= 0:
            hull.pop()
        hull.append(unique_points[i])

    return hull

def main():
    """主函数：演示叉积和凸包算法"""
    print("计算几何示例1：叉积与凸包")
    print("=" * 40)

    # 测试叉积
    p1 = Point(0, 0)
    p2 = Point(1, 0)
    p3 = Point(0, 1)
    p4 = Point(1, 1)

    print(f"点 p1={p1}, p2={p2}, p3={p3}, p4={p4}")
    print(f"叉积(p1, p2, p3) = {cross_product(p1, p2, p3)} (应该>0，逆时针)")
    print(f"叉积(p1, p2, p4) = {cross_product(p1, p2, p4)} (应该>0，逆时针)")

    # 测试凸包
    test_points = [
        Point(0, 0), Point(1, 1), Point(2, 0),
        Point(1, 2), Point(0, 2), Point(2, 2),
        Point(0.5, 0.5), Point(1.5, 0.5)
    ]

    print(f"\n测试点集: {[str(p) for p in test_points]}")
    hull = graham_scan(test_points)
    print(f"凸包顶点: {[str(p) for p in hull]}")

    # 验证凸包大小
    print(f"原点数: {len(test_points)}, 凸包顶点数: {len(hull)}")

if __name__ == "__main__":
    main()