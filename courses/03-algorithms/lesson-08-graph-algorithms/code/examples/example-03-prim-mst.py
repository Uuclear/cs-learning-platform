#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: Prim最小生成树算法实现
Prim算法用于在带权无向图中找到最小生成树（MST）
最小生成树是连接所有顶点的边权和最小的子图
"""

import heapq
from typing import Dict, List, Tuple, Set


def prim_mst(graph: Dict[str, Dict[str, int]]) -> List[Tuple[str, str, int]]:
    """
    使用Prim算法计算最小生成树

    Args:
        graph: 无向图的邻接表表示，格式为 {顶点: {邻居顶点: 权重}}

    Returns:
        最小生成树的边列表，每个元素为(顶点1, 顶点2, 权重)
    """
    if not graph:
        return []

    # 选择任意起始顶点
    start_vertex = next(iter(graph))

    # 已包含在MST中的顶点集合
    mst_vertices: Set[str] = {start_vertex}

    # MST的边列表
    mst_edges: List[Tuple[str, str, int]] = []

    # 候选边的优先队列（最小堆）
    # 格式：(权重, 顶点1, 顶点2)
    candidate_edges = []

    # 将起始顶点的所有边加入候选队列
    for neighbor, weight in graph[start_vertex].items():
        heapq.heappush(candidate_edges, (weight, start_vertex, neighbor))

    # 当MST还没有包含所有顶点时继续
    while candidate_edges and len(mst_vertices) < len(graph):
        # 取出权重最小的边
        weight, vertex1, vertex2 = heapq.heappop(candidate_edges)

        # 如果两个顶点都已经在MST中，跳过（避免环）
        if vertex1 in mst_vertices and vertex2 in mst_vertices:
            continue

        # 确定哪个顶点不在MST中
        new_vertex = vertex2 if vertex1 in mst_vertices else vertex1
        existing_vertex = vertex1 if vertex1 in mst_vertices else vertex2

        # 将新顶点加入MST
        mst_vertices.add(new_vertex)
        mst_edges.append((existing_vertex, new_vertex, weight))

        # 将新顶点的所有边加入候选队列
        for neighbor, edge_weight in graph[new_vertex].items():
            if neighbor not in mst_vertices:
                heapq.heappush(candidate_edges, (edge_weight, new_vertex, neighbor))

    return mst_edges


def calculate_mst_weight(mst_edges: List[Tuple[str, str, int]]) -> int:
    """计算最小生成树的总权重"""
    return sum(weight for _, _, weight in mst_edges)


def main():
    """主函数：演示Prim最小生成树算法"""
    # 构建示例无向图（城市间铺设电缆的成本）
    #     4
    # A ----- B
    # | \   / |
    # |  2/   | 3
    # 1 / \   |
    # |/   \  |
    # C ----- D
    #     5
    graph = {
        'A': {'B': 4, 'C': 1, 'D': 2},
        'B': {'A': 4, 'D': 3},
        'C': {'A': 1, 'D': 5},
        'D': {'A': 2, 'B': 3, 'C': 5}
    }

    print("=== Prim最小生成树算法演示 ===")
    print("无向图结构（边权重表示连接成本）：")
    printed_edges = set()
    for vertex, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            edge_key = tuple(sorted([vertex, neighbor]))
            if edge_key not in printed_edges:
                printed_edges.add(edge_key)
                print(f"  {vertex} --{weight}-- {neighbor}")

    # 计算最小生成树
    mst_edges = prim_mst(graph)

    print(f"\n最小生成树的边：")
    total_weight = 0
    for vertex1, vertex2, weight in mst_edges:
        print(f"  {vertex1} --{weight}-- {vertex2}")
        total_weight += weight

    print(f"\n最小生成树总权重: {total_weight}")

    # 验证结果
    expected_edges = [('A', 'C', 1), ('A', 'D', 2), ('B', 'D', 3)]
    expected_weight = 6

    print(f"\n验证：预期总权重为 {expected_weight}，实际为 {total_weight}")
    if total_weight == expected_weight:
        print("✅ 结果正确！")
    else:
        print("❌ 结果有误！")


if __name__ == "__main__":
    main()