#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答：实现一个函数，检测图中是否存在负权环
"""

from typing import Dict, List


def has_negative_cycle(graph: Dict[str, Dict[str, int]]) -> bool:
    """
    使用Bellman-Ford算法检测图中是否存在负权环

    Args:
        graph: 图的邻接表表示

    Returns:
        bool: True表示存在负权环，False表示不存在
    """
    # 获取所有顶点
    vertices = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors.keys())

    vertices = list(vertices)
    if not vertices:
        return False

    # 初始化距离字典（从任意顶点开始）
    start = vertices[0]
    distances = {vertex: float('infinity') for vertex in vertices}
    distances[start] = 0

    # 进行|V|-1轮松弛操作
    for _ in range(len(vertices) - 1):
        updated = False
        for vertex in vertices:
            if distances[vertex] != float('infinity'):
                for neighbor, weight in graph.get(vertex, {}).items():
                    new_distance = distances[vertex] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        updated = True
        if not updated:
            break

    # 检测负权环
    for vertex in vertices:
        if distances[vertex] != float('infinity'):
            for neighbor, weight in graph.get(vertex, {}).items():
                if distances[vertex] + weight < distances[neighbor]:
                    return True

    return False


# 测试代码
if __name__ == "__main__":
    # 测试无负权环的图
    graph1 = {
        'A': {'B': 1, 'C': 4},
        'B': {'C': -2},
        'C': {}
    }
    print(f"图1存在负权环: {has_negative_cycle(graph1)}")  # 应该是False

    # 测试有负权环的图
    graph2 = {
        'A': {'B': 1},
        'B': {'C': -2},
        'C': {'A': -1}
    }
    print(f"图2存在负权环: {has_negative_cycle(graph2)}")  # 应该是True