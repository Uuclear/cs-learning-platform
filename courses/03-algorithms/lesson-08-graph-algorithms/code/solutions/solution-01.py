#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答：实现一个函数，使用Dijkstra算法找到两点间的最短路径
"""

import heapq
from typing import Dict, List, Tuple, Optional


def dijkstra_shortest_path(graph: Dict[str, Dict[str, int]], start: str, end: str) -> Tuple[int, List[str]]:
    """
    使用Dijkstra算法找到从起点到终点的最短路径

    Args:
        graph: 图的邻接表表示
        start: 起点
        end: 终点

    Returns:
        tuple: (最短距离, 最短路径列表)
    """
    if start == end:
        return 0, [start]

    # 初始化距离字典
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0

    # 初始化前驱字典
    previous = {vertex: None for vertex in graph}

    # 优先队列
    priority_queue = [(0, start)]
    visited = set()

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        # 如果到达终点，可以提前结束
        if current_vertex == end:
            break

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    # 重构路径
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]

    if path[-1] != start:
        return -1, []  # 无法到达

    path = path[::-1]
    return distances[end], path


# 测试代码
if __name__ == "__main__":
    graph = {
        'A': {'B': 4, 'C': 2},
        'B': {'C': 1, 'D': 5},
        'C': {'D': 8, 'E': 10},
        'D': {'E': 2},
        'E': {}
    }

    distance, path = dijkstra_shortest_path(graph, 'A', 'E')
    print(f"最短距离: {distance}")
    print(f"最短路径: {' -> '.join(path)}")