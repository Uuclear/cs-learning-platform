#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3: 最大流最小割定理验证

这是example-03-max-flow-min-cut.py的完整解决方案，
同时计算最大流和找到对应的最小割。
"""

from collections import defaultdict, deque

class MaxFlowMinCutSolver:
    """最大流最小割求解器"""

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(lambda: defaultdict(int))
        self.original_graph = defaultdict(lambda: defaultdict(int))
        self.source = 0
        self.sink = vertices - 1

    def add_edge(self, u, v, capacity):
        """添加边及其容量"""
        self.graph[u][v] = capacity
        self.original_graph[u][v] = capacity

    def bfs(self, parent):
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
        """计算最大流"""
        parent = [-1] * self.V
        max_flow = 0

        while self.bfs(parent):
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
        """找到最小割"""
        # 在残量图中从源点BFS
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

        S = [i for i in range(self.V) if visited[i]]
        T = [i for i in range(self.V) if not visited[i]]

        # 计算割容量
        cut_capacity = 0
        for u in S:
            for v in T:
                cut_capacity += self.original_graph[u][v]

        return S, T, cut_capacity

def solve_max_flow_min_cut():
    """解决最大流最小割问题"""
    solver = MaxFlowMinCutSolver(6)

    edges = [(0,1,3), (0,2,2), (1,2,1), (1,3,3),
             (2,4,2), (3,4,1), (3,5,2), (4,5,3)]

    for u, v, cap in edges:
        solver.add_edge(u, v, cap)

    max_flow = solver.compute_max_flow()
    S, T, min_cut = solver.find_min_cut()

    return max_flow, min_cut

if __name__ == "__main__":
    max_flow, min_cut = solve_max_flow_min_cut()
    print(f"最大流: {max_flow}")
    print(f"最小割容量: {min_cut}")
    print(f"定理成立: {max_flow == min_cut}")