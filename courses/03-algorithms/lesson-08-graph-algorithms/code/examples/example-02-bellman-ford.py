#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: Bellman-Ford算法实现
Bellman-Ford算法可以处理包含负权边的图，并能检测负权环
"""

from typing import Dict, List, Tuple, Optional


def bellman_ford(graph: Dict[str, Dict[str, int]], start: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]], bool]:
    """
    使用Bellman-Ford算法计算从起点到所有顶点的最短路径

    Args:
        graph: 图的邻接表表示，格式为 {顶点: {邻居顶点: 权重}}
        start: 起始顶点

    Returns:
        tuple: (距离字典, 前驱字典, 是否存在负权环)
        - 距离字典: {顶点: 从起点到该顶点的最短距离}
        - 前驱字典: {顶点: 最短路径上的前一个顶点}
        - 负权环标志: True表示存在负权环，False表示不存在
    """
    # 获取所有顶点
    vertices = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors.keys())

    vertices = list(vertices)

    # 初始化距离字典
    distances = {vertex: float('infinity') for vertex in vertices}
    distances[start] = 0

    # 初始化前驱字典
    previous = {vertex: None for vertex in vertices}

    # 进行|V|-1轮松弛操作
    for _ in range(len(vertices) - 1):
        updated = False
        for vertex in vertices:
            if distances[vertex] != float('infinity'):
                for neighbor, weight in graph.get(vertex, {}).items():
                    # 松弛操作：如果通过当前顶点到达邻居的距离更短，则更新
                    new_distance = distances[vertex] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = vertex
                        updated = True

        # 如果没有更新，提前结束
        if not updated:
            break

    # 检测负权环：再进行一轮松弛操作
    has_negative_cycle = False
    for vertex in vertices:
        if distances[vertex] != float('infinity'):
            for neighbor, weight in graph.get(vertex, {}).items():
                if distances[vertex] + weight < distances[neighbor]:
                    has_negative_cycle = True
                    break
        if has_negative_cycle:
            break

    return distances, previous, has_negative_cycle


def reconstruct_path(previous: Dict[str, Optional[str]], start: str, end: str) -> List[str]:
    """重构路径（与Dijkstra相同）"""
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = previous[current]

    if path[-1] != start:
        return []

    return path[::-1]


def main():
    """主函数：演示Bellman-Ford算法"""
    # 构建包含负权边的示例图
    # A --2--> B --(-1)--> C
    # |      / |         /
    # 4    1   3       2
    # |  /     |     /
    # D --5--> E
    graph = {
        'A': {'B': 2, 'D': 4},
        'B': {'C': -1, 'D': 1, 'E': 3},
        'C': {'E': 2},
        'D': {'B': 1, 'E': 5},
        'E': {}
    }

    print("=== Bellman-Ford算法演示 ===")
    print("图结构（包含负权边）：")
    all_vertices = set(graph.keys())
    for neighbors in graph.values():
        all_vertices.update(neighbors.keys())

    for vertex in sorted(all_vertices):
        if vertex in graph:
            for neighbor, weight in graph[vertex].items():
                print(f"  {vertex} --{weight}--> {neighbor}")

    # 计算从A到所有顶点的最短路径
    start_vertex = 'A'
    distances, previous, has_negative_cycle = bellman_ford(graph, start_vertex)

    if has_negative_cycle:
        print("\n⚠️ 检测到负权环！最短路径可能不存在。")
    else:
        print(f"\n从顶点 '{start_vertex}' 到各顶点的最短距离：")
        for vertex in sorted(distances.keys()):
            if distances[vertex] == float('infinity'):
                print(f"  {start_vertex} -> {vertex}: 无法到达")
            else:
                path = reconstruct_path(previous, start_vertex, vertex)
                path_str = " -> ".join(path)
                print(f"  {start_vertex} -> {vertex}: 距离={distances[vertex]}, 路径=[{path_str}]")

    # 演示负权环的情况
    print("\n=== 负权环检测演示 ===")
    negative_cycle_graph = {
        'A': {'B': 1},
        'B': {'C': -2},
        'C': {'A': -1}  # A->B->C->A 形成负权环: 1 + (-2) + (-1) = -2
    }

    distances, previous, has_negative_cycle = bellman_ford(negative_cycle_graph, 'A')
    print(f"负权环检测结果: {'存在负权环' if has_negative_cycle else '不存在负权环'}")


if __name__ == "__main__":
    main()