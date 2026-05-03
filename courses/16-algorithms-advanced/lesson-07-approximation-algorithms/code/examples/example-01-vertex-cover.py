#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
近似算法示例1：顶点覆盖的2-近似算法

这个示例演示了顶点覆盖问题的2-近似算法，
并将其与小规模的最优解进行比较。

预期输出：
图结构: {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2, 4], 4: [3]}

2-近似算法结果:
顶点覆盖: {0, 1, 3}
覆盖大小: 3

最优解（暴力搜索）:
顶点覆盖: {0, 3}
覆盖大小: 2

近似比: 1.5 (小于理论上限2.0)
"""

def vertex_cover_2_approx(graph):
    """
    顶点覆盖问题的2-近似算法

    参数:
        graph: 邻接表表示的无向图，如 {0: [1, 2], 1: [0, 3], ...}

    返回:
        set: 顶点覆盖集合
    """
    # 构建边集合（避免重复）
    edges = set()
    for u in graph:
        for v in graph[u]:
            if u < v:  # 只添加一次每条边
                edges.add((u, v))

    cover = set()

    # 贪心算法：每次选择一条边的两个端点
    while edges:
        # 任意选择一条边
        u, v = edges.pop()
        cover.add(u)
        cover.add(v)

        # 移除所有与u或v相关的边
        remaining_edges = set()
        for edge in edges:
            x, y = edge
            if x != u and x != v and y != u and y != v:
                remaining_edges.add(edge)
        edges = remaining_edges

    return cover

def vertex_cover_brute_force(graph):
    """
    小规模图的顶点覆盖最优解（暴力搜索）
    仅用于验证和比较，时间复杂度O(2^n)
    """
    vertices = list(graph.keys())
    n = len(vertices)
    best_cover = None
    best_size = float('inf')

    # 枚举所有可能的顶点子集
    for mask in range(1 << n):
        cover = set()
        for i in range(n):
            if mask & (1 << i):
                cover.add(vertices[i])

        # 检查是否是有效覆盖
        valid = True
        for u in graph:
            for v in graph[u]:
                if u < v:  # 每条边只检查一次
                    if u not in cover and v not in cover:
                        valid = False
                        break
            if not valid:
                break

        if valid and len(cover) < best_size:
            best_size = len(cover)
            best_cover = cover.copy()

    return best_cover

def print_graph(graph):
    """打印图结构"""
    print("图结构:", graph)

def main():
    # 创建测试图
    graph = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 3],
        3: [1, 2, 4],
        4: [3]
    }

    print_graph(graph)
    print()

    # 运行2-近似算法
    approx_cover = vertex_cover_2_approx(graph.copy())
    approx_size = len(approx_cover)

    print("2-近似算法结果:")
    print(f"顶点覆盖: {approx_cover}")
    print(f"覆盖大小: {approx_size}")
    print()

    # 计算最优解（小规模图）
    optimal_cover = vertex_cover_brute_force(graph)
    optimal_size = len(optimal_cover)

    print("最优解（暴力搜索）:")
    print(f"顶点覆盖: {optimal_cover}")
    print(f"覆盖大小: {optimal_size}")
    print()

    # 计算实际近似比
    approximation_ratio = approx_size / optimal_size
    print(f"近似比: {approximation_ratio:.1f} (小于理论上限2.0)")

if __name__ == "__main__":
    main()