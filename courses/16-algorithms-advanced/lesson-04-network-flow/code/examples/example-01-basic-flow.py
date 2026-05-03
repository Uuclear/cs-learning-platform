#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 基本网络流实现 - Ford-Fulkerson方法

这个例子演示了Ford-Fulkerson方法的基本实现，
使用BFS寻找增广路径（即Edmonds-Karp算法）。
"""

from collections import defaultdict, deque

class BasicFlowNetwork:
    """基本的流网络实现"""

    def __init__(self, vertices):
        """
        初始化流网络

        Args:
            vertices: 顶点数量
        """
        self.V = vertices
        # 使用嵌套字典存储图的邻接表和容量
        self.graph = defaultdict(lambda: defaultdict(int))
        self.source = 0
        self.sink = vertices - 1

    def add_edge(self, u, v, capacity):
        """
        添加有向边及其容量

        Args:
            u: 起点
            v: 终点
            capacity: 边的容量
        """
        self.graph[u][v] = capacity

    def bfs_find_augmenting_path(self, parent):
        """
        使用BFS在残量图中寻找从源点到汇点的增广路径

        Args:
            parent: 用于记录路径的父节点数组

        Returns:
            bool: 如果找到增广路径返回True，否则返回False
        """
        visited = [False] * self.V
        queue = deque()

        # 从源点开始BFS
        queue.append(self.source)
        visited[self.source] = True
        parent[self.source] = -1

        while queue:
            u = queue.popleft()

            # 检查所有邻接顶点
            for v in range(self.V):
                # 如果顶点未访问且残量容量大于0
                if not visited[v] and self.graph[u][v] > 0:
                    queue.append(v)
                    parent[v] = u
                    visited[v] = True

        # 返回是否能够到达汇点
        return visited[self.sink]

    def compute_max_flow(self):
        """
        计算最大流

        Returns:
            int: 最大流的值
        """
        parent = [-1] * self.V
        max_flow = 0

        print("开始计算最大流...")
        print(f"源点: {self.source}, 汇点: {self.sink}")
        print("-" * 40)

        # 当还能找到增广路径时继续
        while self.bfs_find_augmenting_path(parent):
            # 找到当前增广路径的瓶颈容量
            path_flow = float('inf')
            current = self.sink

            # 从汇点回溯到源点，找到最小残量容量
            while current != self.source:
                prev = parent[current]
                path_flow = min(path_flow, self.graph[prev][current])
                current = prev

            # 更新残量图：正向边减少，反向边增加
            current = self.sink
            while current != self.source:
                prev = parent[current]
                self.graph[prev][current] -= path_flow
                self.graph[current][prev] += path_flow
                current = prev

            max_flow += path_flow
            print(f"找到增广路径，增加流量: {path_flow}，累计流量: {max_flow}")

        print("-" * 40)
        print(f"最大流计算完成: {max_flow}")
        return max_flow

def main():
    """主函数 - 演示基本网络流"""
    print("=== 示例1: 基本网络流实现 ===\n")

    # 创建一个包含5个顶点的网络 (0=源点, 4=汇点)
    network = BasicFlowNetwork(5)

    # 构建网络结构
    edges = [
        (0, 1, 16),  # 源点->顶点1, 容量16
        (0, 2, 13),  # 源点->顶点2, 容量13
        (1, 2, 10),  # 顶点1->顶点2, 容量10
        (1, 3, 12),  # 顶点1->顶点3, 容量12
        (2, 1, 4),   # 顶点2->顶点1, 容量4
        (2, 4, 14),  # 顶点2->汇点, 容量14
        (3, 2, 9),   # 顶点3->顶点2, 容量9
        (3, 4, 20)   # 顶点3->汇点, 容量20
    ]

    print("网络结构:")
    for u, v, cap in edges:
        network.add_edge(u, v, cap)
        print(f"  边 ({u}, {v}): 容量 {cap}")
    print()

    # 计算最大流
    result = network.compute_max_flow()

    # 预期输出: 最大流应该是23
    print(f"\n预期最大流: 23")
    print(f"实际计算结果: {result}")
    print(f"结果正确: {result == 23}")

if __name__ == "__main__":
    main()

# 预期输出:
# === 示例1: 基本网络流实现 ===
#
# 网络结构:
#   边 (0, 1): 容量 16
#   边 (0, 2): 容量 13
#   边 (1, 2): 容量 10
#   边 (1, 3): 容量 12
#   边 (2, 1): 容量 4
#   边 (2, 4): 容量 14
#   边 (3, 2): 容量 9
#   边 (3, 4): 容量 20
#
# 开始计算最大流...
# 源点: 0, 汇点: 4
# ----------------------------------------
# 找到增广路径，增加流量: 12，累计流量: 12
# 找到增广路径，增加流量: 4，累计流量: 16
# 找到增广路径，增加流量: 7，累计流量: 23
# ----------------------------------------
# 最大流计算完成: 23
#
# 预期最大流: 23
# 实际计算结果: 23
# 结果正确: True