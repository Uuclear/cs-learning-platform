#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
近似算法解决方案2：设施选址的k-center 2-近似算法

这个解决方案实现了设施选址问题的k-center 2-近似算法，
并展示了其在实际应用中的效果。
"""

import math
import random

def calculate_distance(p1, p2):
    """计算两点间的欧几里得距离"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def build_distance_matrix(points):
    """构建距离矩阵"""
    n = len(points)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist[i][j] = calculate_distance(points[i], points[j])
    return dist

def k_center_2_approx(points, k):
    """
    k-center问题的2-近似算法（贪心）

    算法步骤:
    1. 随机选择第一个中心点
    2. 重复k-1次:
       a. 找到距离当前中心点集合最远的点
       b. 将该点加入中心点集合
    3. 返回中心点集合

    近似比: 2
    时间复杂度: O(kn)
    """
    if k <= 0 or k >= len(points):
        return points if k >= len(points) else []

    n = len(points)
    centers = []

    # 随机选择第一个中心
    first_center = random.randint(0, n - 1)
    centers.append(first_center)

    # 贪心选择剩余k-1个中心
    for _ in range(k - 1):
        max_dist = -1
        best_point = -1

        # 找到距离当前中心集合最远的点
        for i in range(n):
            if i in centers:
                continue

            min_dist_to_centers = float('inf')
            for center in centers:
                dist = calculate_distance(points[i], points[center])
                min_dist_to_centers = min(min_dist_to_centers, dist)

            if min_dist_to_centers > max_dist:
                max_dist = min_dist_to_centers
                best_point = i

        if best_point != -1:
            centers.append(best_point)

    return centers

def evaluate_k_center_solution(points, centers):
    """评估k-center解的质量"""
    max_radius = 0
    assignments = []

    for i, point in enumerate(points):
        min_dist = float('inf')
        closest_center = -1

        for center_idx in centers:
            dist = calculate_distance(point, points[center_idx])
            if dist < min_dist:
                min_dist = dist
                closest_center = center_idx

        assignments.append(closest_center)
        max_radius = max(max_radius, min_dist)

    return max_radius, assignments

def brute_force_k_center(points, k):
    """
    小规模k-center的最优解（暴力搜索）
    仅用于验证，时间复杂度O(C(n,k) * n)
    """
    from itertools import combinations

    n = len(points)
    if n > 15 or k > 5:  # 避免指数时间
        return None, float('inf')

    best_centers = None
    best_radius = float('inf')

    for centers in combinations(range(n), k):
        radius, _ = evaluate_k_center_solution(points, list(centers))
        if radius < best_radius:
            best_radius = radius
            best_centers = list(centers)

    return best_centers, best_radius

def generate_random_points(n, width=100, height=100):
    """生成随机点"""
    return [(random.uniform(0, width), random.uniform(0, height)) for _ in range(n)]

def visualize_solution(points, centers, assignments):
    """简单的文本可视化"""
    print("设施选址结果:")
    print(f"客户点数量: {len(points)}")
    print(f"设施数量: {len(centers)}")
    print()

    for i, center_idx in enumerate(centers):
        center = points[center_idx]
        assigned_count = assignments.count(center_idx)
        print(f"设施 {i+1}: ({center[0]:.1f}, {center[1]:.1f}) - 服务 {assigned_count} 个客户")

def test_k_center():
    """测试k-center算法"""
    random.seed(42)

    # 生成测试数据
    points = generate_random_points(20, 100, 100)
    k = 3

    print("k-center问题测试:")
    print()

    # 运行2-近似算法
    approx_centers = k_center_2_approx(points, k)
    approx_radius, approx_assignments = evaluate_k_center_solution(points, approx_centers)

    print(f"2-近似算法结果:")
    print(f"最大服务半径: {approx_radius:.2f}")
    visualize_solution(points, approx_centers, approx_assignments)
    print()

    # 计算最优解（小规模）
    optimal_centers, optimal_radius = brute_force_k_center(points[:10], min(k, 3))
    if optimal_centers is not None:
        print(f"最优解（前10个点，k={min(k, 3)}）:")
        print(f"最大服务半径: {optimal_radius:.2f}")
        actual_ratio = approx_radius / optimal_radius if optimal_radius > 0 else 1.0
        print(f"实际近似比: {actual_ratio:.2f} (理论上限: 2.0)")

if __name__ == "__main__":
    test_k_center()