#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：最近点对暴力法完整实现
"""

import math
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

def closest_pair_brute_force(points):
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

def generate_random_points(n, min_val=0, max_val=100):
    """生成随机点集"""
    return [Point(random.uniform(min_val, max_val),
                  random.uniform(min_val, max_val)) for _ in range(n)]

def solve_closest_pair_brute_force(points):
    """解决最近点对问题（暴力法）"""
    return closest_pair_brute_force(points)

# 测试用例
if __name__ == "__main__":
    points = generate_random_points(10)
    min_dist, p1, p2 = solve_closest_pair_brute_force(points)
    print(f"最近距离: {min_dist:.4f}")
    print(f"最近点对: {p1} 和 {p2}")