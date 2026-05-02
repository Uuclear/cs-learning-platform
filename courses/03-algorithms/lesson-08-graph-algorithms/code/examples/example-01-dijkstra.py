#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: Dijkstra最短路径算法实现
Dijkstra算法用于在带权图中找到从起点到所有其他顶点的最短路径
注意：该算法不能处理负权边！
"""

import heapq
from typing import Dict, List, Tuple, Optional


def dijkstra(graph: Dict[str, Dict[str, int]], start: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
    """
    使用Dijkstra算法计算从起点到所有顶点的最短路径

    Args:
        graph: 图的邻接表表示，格式为 {顶点: {邻居顶点: 权重}}
        start: 起始顶点

    Returns:
        tuple: (距离字典, 前驱字典)
        - 距离字典: {顶点: 从起点到该顶点的最短距离}
        - 前驱字典: {顶点: 最短路径上的前一个顶点}
    """
    # 初始化距离字典，所有顶点距离设为无穷大
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0  # 起点距离为0

    # 初始化前驱字典，用于重构路径
    previous = {vertex: None for vertex in graph}

    # 优先队列，存储(距离, 顶点)元组
    priority_queue = [(0, start)]

    # 已访问顶点集合
    visited = set()

    while priority_queue:
        # 取出当前距离最小的顶点
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # 如果已经访问过，跳过
        if current_vertex in visited:
            continue

        # 标记为已访问
        visited.add(current_vertex)

        # 遍历当前顶点的所有邻居
        for neighbor, weight in graph[current_vertex].items():
            # 计算通过当前顶点到达邻居的新距离
            distance = current_distance + weight

            # 如果新距离更短，则更新
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous


def reconstruct_path(previous: Dict[str, Optional[str]], start: str, end: str) -> List[str]:
    """
    根据前驱字典重构从起点到终点的最短路径

    Args:
        previous: 前驱字典
        start: 起点
        end: 终点

    Returns:
        从起点到终点的最短路径列表
    """
    path = []
    current = end

    # 从终点开始反向追踪到起点
    while current is not None:
        path.append(current)
        current = previous[current]

    # 如果路径的最后一个顶点不是起点，说明无法到达
    if path[-1] != start:
        return []

    # 反转路径得到从起点到终点的顺序
    return path[::-1]


def main():
    """主函数：演示Dijkstra算法"""
    # 构建示例图（城市间的距离）
    # A --4--> B --2--> C
    # |      / |      /
    # 3    1   5    1
    # |  /     |  /
    # D --2--> E
    graph = {
        'A': {'B': 4, 'D': 3},
        'B': {'A': 4, 'C': 2, 'D': 1, 'E': 5},
        'C': {'B': 2, 'E': 1},
        'D': {'A': 3, 'B': 1, 'E': 2},
        'E': {'B': 5, 'C': 1, 'D': 2}
    }

    print("=== Dijkstra最短路径算法演示 ===")
    print("图结构：")
    for vertex, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            print(f"  {vertex} --{weight}--> {neighbor}")

    # 计算从A到所有顶点的最短路径
    start_vertex = 'A'
    distances, previous = dijkstra(graph, start_vertex)

    print(f"\n从顶点 '{start_vertex}' 到各顶点的最短距离：")
    for vertex in sorted(distances.keys()):
        if distances[vertex] == float('infinity'):
            print(f"  {start_vertex} -> {vertex}: 无法到达")
        else:
            path = reconstruct_path(previous, start_vertex, vertex)
            path_str = " -> ".join(path)
            print(f"  {start_vertex} -> {vertex}: 距离={distances[vertex]}, 路径=[{path_str}]")


if __name__ == "__main__":
    main()