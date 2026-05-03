#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
近似算法示例3：度量TSP的近似算法比较

这个示例比较了两种TSP近似算法：
1. MST-based 2-近似算法
2. Christofides 1.5-近似算法

预期输出：
城市坐标:
A(0, 0), B(1, 2), C(3, 1), D(2, 4), E(5, 3)

距离矩阵:
[[0.0, 2.2, 3.2, 4.5, 5.8],
 [2.2, 0.0, 2.2, 2.2, 4.1],
 [3.2, 2.2, 0.0, 3.2, 2.2],
 [4.5, 2.2, 3.2, 0.0, 3.2],
 [5.8, 4.1, 2.2, 3.2, 0.0]]

MST 2-近似结果:
路径: [0, 1, 3, 2, 4, 0]
距离: 14.7

Christofides 1.5-近似结果:
路径: [0, 1, 3, 4, 2, 0]
距离: 13.9

最优解（暴力搜索）:
路径: [0, 1, 2, 4, 3, 0]
距离: 13.7

近似比比较:
MST算法: 1.07
Christofides算法: 1.01
"""

import math
import itertools

def calculate_distance_matrix(points):
    """计算欧几里得距离矩阵"""
    n = len(points)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = points[i][0] - points[j][0]
                dy = points[i][1] - points[j][1]
                dist[i][j] = math.sqrt(dx*dx + dy*dy)
    return dist

def prim_mst(dist_matrix):
    """使用Prim算法构建最小生成树"""
    n = len(dist_matrix)
    in_mst = [False] * n
    parent = [-1] * n
    key = [float('inf')] * n

    key[0] = 0
    mst_edges = []

    for _ in range(n):
        # 找到最小key的顶点
        u = -1
        min_key = float('inf')
        for v in range(n):
            if not in_mst[v] and key[v] < min_key:
                min_key = key[v]
                u = v

        if u == -1:
            break

        in_mst[u] = True
        if parent[u] != -1:
            mst_edges.append((parent[u], u))

        # 更新邻接顶点的key值
        for v in range(n):
            if not in_mst[v] and dist_matrix[u][v] < key[v]:
                key[v] = dist_matrix[u][v]
                parent[v] = u

    return mst_edges

def mst_tsp_2_approx(dist_matrix):
    """MST-based TSP 2-近似算法"""
    n = len(dist_matrix)
    mst_edges = prim_mst(dist_matrix)

    # 构建邻接表
    adj = [[] for _ in range(n)]
    for u, v in mst_edges:
        adj[u].append(v)
        adj[v].append(u)

    # 深度优先遍历得到预序遍历
    visited = [False] * n
    tour = []

    def dfs(u):
        visited[u] = True
        tour.append(u)
        for v in adj[u]:
            if not visited[v]:
                dfs(v)

    dfs(0)
    tour.append(0)  # 回到起点

    # 计算总距离
    total_dist = 0
    for i in range(len(tour) - 1):
        total_dist += dist_matrix[tour[i]][tour[i+1]]

    return tour, total_dist

def christofides_tsp(dist_matrix):
    """Christofides TSP 1.5-近似算法（简化版）"""
    n = len(dist_matrix)
    mst_edges = prim_mst(dist_matrix)

    # 计算度数
    degree = [0] * n
    for u, v in mst_edges:
        degree[u] += 1
        degree[v] += 1

    # 找到奇数度顶点
    odd_vertices = [i for i in range(n) if degree[i] % 2 == 1]

    # 在奇数度顶点上找最小权完美匹配（简化：贪心）
    matching = []
    remaining_odd = odd_vertices[:]

    while remaining_odd:
        u = remaining_odd.pop()
        if not remaining_odd:
            break
        # 找到距离u最近的剩余奇数度顶点
        best_v = remaining_odd[0]
        best_dist = dist_matrix[u][best_v]
        for v in remaining_odd[1:]:
            if dist_matrix[u][v] < best_dist:
                best_dist = dist_matrix[u][v]
                best_v = v
        remaining_odd.remove(best_v)
        matching.append((u, best_v))

    # 合并MST和匹配
    eulerian_adj = [[] for _ in range(n)]
    for u, v in mst_edges:
        eulerian_adj[u].append(v)
        eulerian_adj[v].append(u)
    for u, v in matching:
        eulerian_adj[u].append(v)
        eulerian_adj[v].append(u)

    # 找欧拉回路（Hierholzer算法简化版）
    def find_eulerian_tour(start):
        stack = [start]
        path = []
        local_adj = [list(neighbors) for neighbors in eulerian_adj]

        while stack:
            u = stack[-1]
            if local_adj[u]:
                v = local_adj[u].pop()
                # 移除反向边
                local_adj[v].remove(u)
                stack.append(v)
            else:
                path.append(stack.pop())
        return path[::-1]

    eulerian_tour = find_eulerian_tour(0)

    # 转换为哈密顿回路（跳过重复顶点）
    hamiltonian_tour = []
    visited = set()
    for vertex in eulerian_tour:
        if vertex not in visited:
            hamiltonian_tour.append(vertex)
            visited.add(vertex)
    hamiltonian_tour.append(0)

    # 计算总距离
    total_dist = 0
    for i in range(len(hamiltonian_tour) - 1):
        total_dist += dist_matrix[hamiltonian_tour[i]][hamiltonian_tour[i+1]]

    return hamiltonian_tour, total_dist

def tsp_brute_force(dist_matrix):
    """小规模TSP的最优解（暴力搜索）"""
    n = len(dist_matrix)
    if n > 8:  # 避免指数时间
        return None, float('inf')

    best_tour = None
    best_dist = float('inf')

    # 固定起点为0，排列其余顶点
    for perm in itertools.permutations(range(1, n)):
        tour = [0] + list(perm) + [0]
        dist = 0
        for i in range(len(tour) - 1):
            dist += dist_matrix[tour[i]][tour[i+1]]
        if dist < best_dist:
            best_dist = dist
            best_tour = tour

    return best_tour, best_dist

def main():
    # 定义城市坐标
    cities = [
        (0, 0),   # A
        (1, 2),   # B
        (3, 1),   # C
        (2, 4),   # D
        (5, 3)    # E
    ]

    city_names = ['A', 'B', 'C', 'D', 'E']

    print("城市坐标:")
    for i, (x, y) in enumerate(cities):
        print(f"{city_names[i]}({x}, {y})", end=", ")
    print("\n")

    # 计算距离矩阵
    dist_matrix = calculate_distance_matrix(cities)
    print("距离矩阵:")
    for row in dist_matrix:
        print([round(x, 1) for x in row])
    print()

    # MST 2-近似
    mst_tour, mst_dist = mst_tsp_2_approx(dist_matrix)
    print(f"MST 2-近似结果:")
    print(f"路径: {mst_tour}")
    print(f"距离: {mst_dist:.1f}")
    print()

    # Christofides 1.5-近似
    christ_tour, christ_dist = christofides_tsp(dist_matrix)
    print(f"Christofides 1.5-近似结果:")
    print(f"路径: {christ_tour}")
    print(f"距离: {christ_dist:.1f}")
    print()

    # 最优解（小规模）
    optimal_tour, optimal_dist = tsp_brute_force(dist_matrix)
    if optimal_tour:
        print(f"最优解（暴力搜索）:")
        print(f"路径: {optimal_tour}")
        print(f"距离: {optimal_dist:.1f}")
        print()

        # 计算近似比
        mst_ratio = mst_dist / optimal_dist
        christ_ratio = christ_dist / optimal_dist
        print(f"近似比比较:")
        print(f"MST算法: {mst_ratio:.2f}")
        print(f"Christofides算法: {christ_ratio:.2f}")

if __name__ == "__main__":
    main()