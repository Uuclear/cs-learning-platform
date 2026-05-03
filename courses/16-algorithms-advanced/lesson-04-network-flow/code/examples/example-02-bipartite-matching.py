#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: 二分图匹配应用

这个例子展示了如何使用网络流算法解决二分图最大匹配问题。
我们将工人和任务建模为二分图，寻找最大的工作分配方案。
"""

from collections import defaultdict, deque

class BipartiteMatcher:
    """二分图匹配器 - 使用网络流实现"""

    def __init__(self, workers, tasks):
        """
        初始化二分图匹配器

        Args:
            workers: 工人数量（左部顶点）
            tasks: 任务数量（右部顶点）
        """
        self.workers = workers
        self.tasks = tasks
        # 总顶点数 = 工人 + 任务 + 源点 + 汇点
        self.total_vertices = workers + tasks + 2
        self.source = 0
        self.sink = self.total_vertices - 1

        # 构建流网络
        self.graph = defaultdict(lambda: defaultdict(int))
        self.assignments = []  # 存储匹配结果

    def add_assignment(self, worker, task):
        """
        添加工人可以执行的任务

        Args:
            worker: 工人索引 (0-based)
            task: 任务索引 (0-based)
        """
        # 在流网络中添加边：工人 -> 任务
        # 工人顶点编号: 1 to workers
        # 任务顶点编号: workers+1 to workers+tasks
        worker_node = worker + 1
        task_node = self.workers + 1 + task
        self.graph[worker_node][task_node] = 1

    def _bfs(self, parent):
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

    def find_maximum_matching(self):
        """
        找到最大匹配

        Returns:
            tuple: (最大匹配数, 匹配列表)
        """
        # 连接源点到所有工人（容量为1）
        for i in range(self.workers):
            self.graph[self.source][i + 1] = 1

        # 连接所有任务到汇点（容量为1）
        for i in range(self.tasks):
            self.graph[self.workers + 1 + i][self.sink] = 1

        parent = [-1] * self.total_vertices
        max_flow = 0

        print("开始寻找最大匹配...")
        print(f"工人数量: {self.workers}, 任务数量: {self.tasks}")
        print("-" * 40)

        # Edmonds-Karp算法计算最大流
        while self._bfs(parent):
            path_flow = float('inf')
            current = self.sink

            # 找到瓶颈容量
            while current != self.source:
                prev = parent[current]
                path_flow = min(path_flow, self.graph[prev][current])
                current = prev

            # 更新残量图
            current = self.sink
            while current != self.source:
                prev = parent[current]
                self.graph[prev][current] -= path_flow
                self.graph[current][prev] += path_flow
                current = prev

            max_flow += path_flow

        # 从最终的流网络中提取匹配结果
        self.assignments = []
        for worker in range(self.workers):
            worker_node = worker + 1
            for task in range(self.tasks):
                task_node = self.workers + 1 + task
                # 如果反向边有流量，说明这条边被使用了
                if self.graph[task_node][worker_node] > 0:
                    self.assignments.append((worker, task))

        print(f"最大匹配数: {max_flow}")
        print("匹配结果:")
        for worker, task in self.assignments:
            print(f"  工人 {worker} -> 任务 {task}")

        return max_flow, self.assignments

def main():
    """主函数 - 演示二分图匹配"""
    print("=== 示例2: 二分图匹配应用 ===\n")

    # 场景：4个工人，4个任务
    # 工人0可以做任务0, 1
    # 工人1可以做任务1, 2
    # 工人2可以做任务2, 3
    # 工人3可以做任务0, 3

    matcher = BipartiteMatcher(4, 4)

    # 添加可能的分配
    assignments = [
        (0, 0), (0, 1),  # 工人0
        (1, 1), (1, 2),  # 工人1
        (2, 2), (2, 3),  # 工人2
        (3, 0), (3, 3)   # 工人3
    ]

    print("可用的工人-任务分配:")
    for worker, task in assignments:
        matcher.add_assignment(worker, task)
        print(f"  工人 {worker} 可以执行 任务 {task}")
    print()

    # 计算最大匹配
    max_matching, matching_list = matcher.find_maximum_matching()

    print("-" * 40)
    print(f"\n预期最大匹配: 4 (完美匹配)")
    print(f"实际最大匹配: {max_matching}")
    print(f"是否达到完美匹配: {max_matching == min(4, 4)}")

if __name__ == "__main__":
    main()

# 预期输出:
# === 示例2: 二分图匹配应用 ===
#
# 可用的工人-任务分配:
#   工人 0 可以执行 任务 0
#   工人 0 可以执行 任务 1
#   工人 1 可以执行 任务 1
#   工人 1 可以执行 任务 2
#   工人 2 可以执行 任务 2
#   工人 2 可以执行 任务 3
#   工人 3 可以执行 任务 0
#   工人 3 可以执行 任务 3
#
# 开始寻找最大匹配...
# 工人数量: 4, 任务数量: 4
# ----------------------------------------
# 最大匹配数: 4
# 匹配结果:
#   工人 0 -> 任务 1
#   工人 1 -> 任务 2
#   工人 2 -> 任务 3
#   工人 3 -> 任务 0
# ----------------------------------------
#
# 预期最大匹配: 4 (完美匹配)
# 实际最大匹配: 4
# 是否达到完美匹配: True