#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2: 二分图匹配

这是example-02-bipartite-matching.py的完整解决方案，
展示了如何使用网络流解决二分图最大匹配问题。
"""

from collections import defaultdict, deque

class BipartiteMatchingSolver:
    """二分图匹配求解器"""

    def __init__(self, left_size, right_size):
        self.left_size = left_size
        self.right_size = right_size
        self.total_vertices = left_size + right_size + 2
        self.source = 0
        self.sink = self.total_vertices - 1
        self.graph = defaultdict(lambda: defaultdict(int))

    def add_edge(self, left, right):
        """添加左部到右部的可能匹配"""
        left_node = left + 1
        right_node = self.left_size + 1 + right
        self.graph[left_node][right_node] = 1

    def bfs(self, parent):
        """BFS寻找增广路径"""
        visited = [False] * self.total_vertices
        queue = deque()

        queue.append(self.source)
        visited[self.source] = True
        parent[self.source] = -1

        while queue:
            u = queue.popleft()
            for v in range(self.total_vertices):
                if not visited[v] and self.graph[u][v] > 0:
                    queue.append(v)
                    parent[v] = u
                    visited[v] = True

        return visited[self.sink]

    def solve(self):
        """求解最大匹配"""
        # 连接源点到左部
        for i in range(self.left_size):
            self.graph[self.source][i + 1] = 1

        # 连接右部到汇点
        for i in range(self.right_size):
            self.graph[self.left_size + 1 + i][self.sink] = 1

        parent = [-1] * self.total_vertices
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

def solve_bipartite_matching():
    """解决二分图匹配问题"""
    # 示例：4个工人，4个任务
    solver = BipartiteMatchingSolver(4, 4)

    # 可能的分配
    assignments = [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,0), (3,3)]

    for worker, task in assignments:
        solver.add_edge(worker, task)

    return solver.solve()

if __name__ == "__main__":
    result = solve_bipartite_matching()
    print(f"最大匹配数: {result}")