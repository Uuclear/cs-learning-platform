#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答：实现Kruskal算法来找到最小生成树
"""

from typing import Dict, List, Tuple


class UnionFind:
    """并查集数据结构，用于Kruskal算法"""

    def __init__(self, vertices: List[str]):
        self.parent = {vertex: vertex for vertex in vertices}
        self.rank = {vertex: 0 for vertex in vertices}

    def find(self, vertex: str) -> str:
        """查找顶点的根节点（带路径压缩）"""
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, vertex1: str, vertex2: str) -> bool:
        """合并两个顶点所在的集合，如果已经在同一集合则返回False"""
        root1 = self.find(vertex1)
        root2 = self.find(vertex2)

        if root1 == root2:
            return False

        # 按秩合并
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1

        return True


def kruskal_mst(graph: Dict[str, Dict[str, int]]) -> List[Tuple[str, str, int]]:
    """
    使用Kruskal算法计算最小生成树

    Args:
        graph: 无向图的邻接表表示

    Returns:
        最小生成树的边列表
    """
    if not graph:
        return []

    # 获取所有顶点
    vertices = list(graph.keys())

    # 构建边列表（避免重复）
    edges = []
    added_edges = set()
    for vertex in vertices:
        for neighbor, weight in graph[vertex].items():
            edge_key = tuple(sorted([vertex, neighbor]))
            if edge_key not in added_edges:
                edges.append((weight, vertex, neighbor))
                added_edges.add(edge_key)

    # 按权重排序边
    edges.sort()

    # 初始化并查集
    uf = UnionFind(vertices)

    # Kruskal算法主循环
    mst_edges = []
    for weight, vertex1, vertex2 in edges:
        if uf.union(vertex1, vertex2):
            mst_edges.append((vertex1, vertex2, weight))
            if len(mst_edges) == len(vertices) - 1:
                break

    return mst_edges


# 测试代码
if __name__ == "__main__":
    graph = {
        'A': {'B': 4, 'C': 1, 'D': 2},
        'B': {'A': 4, 'D': 3},
        'C': {'A': 1, 'D': 5},
        'D': {'A': 2, 'B': 3, 'C': 5}
    }

    mst = kruskal_mst(graph)
    print("Kruskal算法找到的最小生成树:")
    total_weight = 0
    for v1, v2, weight in mst:
        print(f"  {v1} --{weight}-- {v2}")
        total_weight += weight
    print(f"总权重: {total_weight}")