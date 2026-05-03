#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1: 基本网络流实现

这是example-01-basic-flow.py的完整解决方案，
包含了Ford-Fulkerson方法（Edmonds-Karp算法）的标准实现。
"""

from collections import defaultdict, deque

class FlowNetwork:
    """标准的流网络实现"""

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(lambda: defaultdict(int))
        self.source = 0
        self.sink = vertices - 1

    def add_edge(self, u, v, capacity):
        """添加有向边及其容量"""
        self.graph[u][v] = capacity

    def bfs(self, parent):
        """使用BFS在残量图中寻找增广路径"""
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

    def ford_fulkerson(self):
        """Ford-Fulkerson方法（使用BFS即Edmonds-Karp）"""
        parent = [-1] * self.V
        max_flow = 0

        while self.bfs(parent):
            # 找到瓶颈容量
            path_flow = float('inf')
            s = self.sink
            while s != self.source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # 更新残量图
            v = self.sink
            while v != self.source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow

        return max_flow

def solve_basic_flow():
    """解决基本网络流问题"""
    # 创建网络
    g = FlowNetwork(5)

    # 添加边
    edges = [(0,1,16), (0,2,13), (1,2,10), (1,3,12),
             (2,1,4), (2,4,14), (3,2,9), (3,4,20)]

    for u, v, cap in edges:
        g.add_edge(u, v, cap)

    return g.ford_fulkerson()

if __name__ == "__main__":
    result = solve_basic_flow()
    print(f"最大流: {result}")