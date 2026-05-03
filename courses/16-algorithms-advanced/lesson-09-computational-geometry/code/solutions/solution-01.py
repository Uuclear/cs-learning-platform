#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：计算几何基础算法完整实现
"""

import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

def cross_product(o, a, b):
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

def graham_scan(points):
    if len(points) <= 2:
        return points[:]

    start = min(points, key=lambda p: (p.y, p.x))

    def polar_angle(p):
        return math.atan2(p.y - start.y, p.x - start.x)

    sorted_points = sorted(points, key=lambda p: (polar_angle(p),
                                                 (p.x - start.x)**2 + (p.y - start.y)**2))

    # 移除重复点
    unique_points = []
    for p in sorted_points:
        if not unique_points or p != unique_points[-1]:
            unique_points.append(p)

    if len(unique_points) <= 2:
        return unique_points

    hull = [unique_points[0], unique_points[1]]
    for i in range(2, len(unique_points)):
        while len(hull) >= 2 and cross_product(hull[-2], hull[-1], unique_points[i]) <= 0:
            hull.pop()
        hull.append(unique_points[i])

    return hull

def point_in_polygon(point, polygon):
    x, y = point.x, point.y
    n = len(polygon)
    if n < 3:
        return False

    inside = False
    p1x, p1y = polygon[0].x, polygon[0].y

    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n].x, polygon[i % n].y

        if min(p1y, p2y) < y <= max(p1y, p2y):
            if p1y != p2y:
                xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if x < xinters:
                    inside = not inside

        p1x, p1y = p2x, p2y

    return inside

def solve_computational_geometry_basic(points, test_point, polygon):
    """解决基础计算几何问题"""
    hull = graham_scan(points)
    inside = point_in_polygon(test_point, polygon)
    return hull, inside

# 测试用例
if __name__ == "__main__":
    points = [Point(0,0), Point(1,1), Point(2,0), Point(1,2)]
    test_point = Point(1,1)
    polygon = [Point(0,0), Point(2,0), Point(2,2), Point(0,2)]

    hull, inside = solve_computational_geometry_basic(points, test_point, polygon)
    print(f"凸包: {[str(p) for p in hull]}")
    print(f"点在多边形内: {inside}")