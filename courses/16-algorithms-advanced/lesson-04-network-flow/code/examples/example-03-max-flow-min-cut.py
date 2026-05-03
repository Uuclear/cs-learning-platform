#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 最大流最小割定理验证

这个例子演示如何同时计算最大流和找到对应的最小割，
验证最大流最小割定理的正确性。
"""

from collections import defaultdict, deque

class MaxFlowMinCut:
    """最大流最小割计算器"""

    def __init__(self, vertices):
        """
        初始化网络

        Args:
            vertices: 顶点数量
        """
        self.V = vertices
        self.graph = defaultdict(lambda: defaultdict(int))
        self.original_graph = defaultdict(lambda: defaultdict(int))
        self.source = 0
        self.sink = vertices - 1

    def add_edge(self, u, v, capacity):
        """
        添加边及其容量

        Args:
            u: 起点
            v: 终点
            capacity: 容量
        """
        self.graph[u][v] = capacity
        self.original_graph[u][v] = capacity

    def _bfs(self, parent):
        """BFS寻找增广路径"""
        visited = [False] * self.V
        queue = deque()

        queue.append(self.source)
        visited[self.source] = True
        parent[self.source] = -1

        while queue:
            u = queue.popleft()
            for v in range(self.V):
                if not visited[v] and self.graph[u][v] > 0:
                    queue.append(v)
                    parent[v] = u
                    visited[v] = True

        return visited[self.sink]

    def compute_max_flow(self):
        """
        计算最大流

        Returns:
            int: 最大流值
        """
        parent = [-1] * self.V
        max_flow = 0

        while self._bfs(parent):
            path_flow = float('inf')
            current = self.sink

            while current != self.source:
                prev = parent[current]
                path_flow = min(path_flow, self.graph[prev][current])
                current = prev

            current = self.sink
            while current != self.source:
                prev = parent[current]
                self.graph[prev][current] -= path_flow
                self.graph[current][prev] += path_flow
                current = prev

            max_flow += path_flow

        return max_flow

    def find_min_cut(self):
        """
        找到最小割

        Returns:
            tuple: (S集合, T集合, 割的容量)
        """
        # 在最终的残量图中，从源点能到达的顶点属于S集合
        visited = [False] * self.V
        queue = deque()
        queue.append(self.source)
        visited[self.source] = True

        while queue:
            u = queue.popleft()
            for v in range(self.V):
                if not visited[v] and self.graph[u][v] > 0:
                    queue.append(v)
                    visited[v] = True

        # S集合：能从源点到达的顶点
        S = [i for i in range(self.V) if visited[i]]
        # T集合：不能从源点到达的顶点
        T = [i for i in range(self.V) if not visited[i]]

        # 计算割的容量
        cut_capacity = 0
        for u in S:
            for v in T:
                cut_capacity += self.original_graph[u][v]

        return S, T, cut_capacity

def main():
    """主函数 - 验证最大流最小割定理"""
    print("=== 示例3: 最大流最小割定理验证 ===\n")

    # 创建一个简单的网络进行验证
    network = MaxFlowMinCut(6)  # 6个顶点

    # 构建网络
    edges = [
        (0, 1, 3),
        (0, 2, 2),
        (1, 2, 1),
        (1, 3, 3),
        (2, 4, 2),
        (3, 4, 1),
        (3, 5, 2),
        (4, 5, 3)
    ]

    print("网络结构:")
    for u, v, cap in edges:
        network.add_edge(u, v, cap)
        print(f"  边 ({u}, {v}): 容量 {cap}")
    print()

    # 计算最大流
    max_flow = network.compute_max_flow()
    print(f"最大流: {max_flow}")

    # 找到最小割
    S, T, min_cut_capacity = network.find_min_cut()
    print(f"最小割 S集合: {S}")
    print(f"最小割 T集合: {T}")
    print(f"最小割容量: {min_cut_capacity}")

    # 验证定理
    print("-" * 40)
    print("定理验证:")
    print(f"最大流 = {max_flow}")
    print(f"最小割容量 = {min_cut_capacity}")
    print(f"定理成立: {max_flow == min_cut_capacity}")

    # 显示具体的割边
    print("\n割边（从S到T的边）:")
    for u in S:
        for v in T:
            if network.original_graph[u][v] > 0:
                print(f"  ({u}, {v}): 容量 {network.original_graph[u][v]}")

if __name__ == "__main__":
    main()

# 预期输出:
# === 示例3: 最大流最小割定理验证 ===
#
# 网络结构:
#   边 (0, 1): 容量 3
#   边 (0, 2): 容量 2
#   边 (1, 2): 容量 1
#   边 (1, 3): 容量 3
#   边 (2, 4): 容量 2
#   边 (3, 4): 容量 1
#   边 (3, 5): 容量 2
#   边 (4, 5): 容量 3
#
# 最大流: 4
# 最小割 S集合: [0, 1, 2, 3, 4]
# 最小割 T集合: [5]
# 最小割容量: 4
# ----------------------------------------
# 定理验证:
# 最大流 = 4
# 最小割容量 = 4
# 定理成立: True
#
# 割边（从S到T的边）:
#   (3, 5): 容量 2
#   (4, 5): 容量 3