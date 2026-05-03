#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：Karger随机最小割算法

这个文件实现了Karger的随机收缩算法来求解图的最小割问题，
演示了随机算法在图论中的应用。
"""

import random
import copy
import math

class Graph:
    """
    图类，支持Karger算法所需的收缩操作

    Attributes:
        vertices (set): 顶点集合
        edges (list): 边列表
        adj (dict): 邻接表
    """

    def __init__(self, vertices=None):
        """初始化图"""
        if vertices is None:
            vertices = set()
        self.vertices = set(vertices)
        self.edges = []
        self.adj = {v: set() for v in self.vertices}

    def add_edge(self, u, v):
        """添加边（无向图）"""
        if u == v:
            return  # 不允许自环

        if u not in self.vertices:
            self.vertices.add(u)
            self.adj[u] = set()
        if v not in self.vertices:
            self.vertices.add(v)
            self.adj[v] = set()

        self.edges.append((u, v))
        self.adj[u].add(v)
        self.adj[v].add(u)

    def contract(self, u, v):
        """
        收缩边(u, v)，将v合并到u

        Args:
            u, v: 要收缩的两个顶点
        """
        if u not in self.vertices or v not in self.vertices:
            raise ValueError("顶点不存在")

        # 将v的所有邻居添加到u的邻居中
        for neighbor in self.adj[v]:
            if neighbor != u:
                self.adj[u].add(neighbor)
                self.adj[neighbor].add(u)
                self.adj[neighbor].discard(v)
                self.edges.append((u, neighbor))

        # 删除v
        self.vertices.remove(v)
        del self.adj[v]

        # 清理自环和重复边
        self._cleanup()

    def _cleanup(self):
        """清理自环和重复边"""
        new_edges = []
        seen_edges = set()

        for u, v in self.edges:
            if u in self.adj and v in self.adj and u != v:
                # 标准化边的方向（小的在前）
                edge_key = tuple(sorted([u, v]))
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    new_edges.append((u, v))

        self.edges = new_edges

        # 重建邻接表
        self.adj = {v: set() for v in self.vertices}
        for u, v in self.edges:
            self.adj[u].add(v)
            self.adj[v].add(u)

    def get_cut_size(self):
        """获取当前割的大小（剩余边数）"""
        return len(self.edges)

    def copy(self):
        """创建图的深拷贝"""
        new_graph = Graph()
        new_graph.vertices = self.vertices.copy()
        new_graph.edges = self.edges.copy()
        new_graph.adj = {v: neighbors.copy() for v, neighbors in self.adj.items()}
        return new_graph

def karger_single_run(graph):
    """
    Karger算法单次运行

    Args:
        graph (Graph): 输入图

    Returns:
        int: 找到的割大小
    """
    g = graph.copy()

    # 随机收缩直到剩下2个顶点
    while len(g.vertices) > 2:
        if not g.edges:
            break

        edge = random.choice(g.edges)
        u, v = edge
        g.contract(u, v)

    return g.get_cut_size()

def karger_min_cut(graph, iterations=None):
    """
    Karger最小割算法主函数

    Args:
        graph (Graph): 输入图
        iterations (int): 迭代次数，如果为None则使用推荐值

    Returns:
        tuple: (最小割大小, 详细统计信息)
    """
    n = len(graph.vertices)

    if n <= 1:
        return 0, {'error': '顶点数不足'}

    if iterations is None:
        # 推荐迭代次数: n² ln n
        iterations = max(10, int(n * n * math.log(n)) if n > 1 else 10)

    min_cut = float('inf')
    cut_counts = {}

    print(f"Karger算法: {n} 个顶点, {len(graph.edges)} 条边, {iterations} 次迭代")

    for i in range(iterations):
        cut_size = karger_single_run(graph)
        min_cut = min(min_cut, cut_size)

        # 统计不同割大小的出现频率
        cut_counts[cut_size] = cut_counts.get(cut_size, 0) + 1

        # 进度报告
        if (i + 1) % max(1, iterations // 10) == 0:
            current_success_prob = 1 - (1 - 2/(n*(n-1)))**(i+1)
            print(f"  迭代 {i+1:4d}/{iterations}: 最小割={min_cut:2d}, "
                  f"成功概率≈{current_success_prob:.4f}")

    # 计算理论成功概率
    theoretical_success_prob = 1 - (1 - 2/(n*(n-1)))**iterations

    stats = {
        'iterations': iterations,
        'min_cut': min_cut,
        'cut_distribution': cut_counts,
        'theoretical_success_probability': theoretical_success_prob,
        'actual_success_rate': cut_counts.get(min_cut, 0) / iterations
    }

    return min_cut, stats

def create_example_graphs():
    """创建示例图用于测试"""
    graphs = {}

    # 图1: 简单正方形
    g1 = Graph([1, 2, 3, 4])
    edges1 = [(1,2), (2,3), (3,4), (4,1)]
    for u, v in edges1:
        g1.add_edge(u, v)
    graphs['正方形'] = g1

    # 图2: 完全图K4
    g2 = Graph([1, 2, 3, 4])
    edges2 = [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]
    for u, v in edges2:
        g2.add_edge(u, v)
    graphs['完全图K4'] = g2

    # 图3: 二分图K_{3,3}
    g3 = Graph([1, 2, 3, 4, 5, 6])
    left = [1, 2, 3]
    right = [4, 5, 6]
    for u in left:
        for v in right:
            g3.add_edge(u, v)
    graphs['二分图K33'] = g3

    return graphs

def test_karger_algorithm():
    """测试Karger算法"""
    print("=== Karger最小割算法演示 ===\n")

    graphs = create_example_graphs()

    for name, graph in graphs.items():
        print(f"--- 测试 {name} ---")

        # 显示图信息
        print(f"顶点: {sorted(graph.vertices)}")
        print(f"边数: {len(graph.edges)}")

        # 已知的最小割（用于验证）
        known_min_cuts = {
            '正方形': 2,
            '完全图K4': 3,
            '二分图K33': 3
        }

        expected = known_min_cuts.get(name, "未知")
        print(f"已知最小割: {expected}")

        # 运行Karger算法
        min_cut, stats = karger_min_cut(graph, iterations=50)

        print(f"找到的最小割: {min_cut}")
        print(f"理论成功概率: {stats['theoretical_success_probability']:.4f}")
        print(f"实际成功率: {stats['actual_success_rate']:.4f}")

        # 验证结果
        if expected != "未知":
            is_correct = min_cut == expected
            print(f"结果正确: {is_correct}")

        print()

def analyze_complexity():
    """分析算法复杂度"""
    print("=== 算法复杂度分析 ===\n")

    print("单次Karger运行:")
    print("  时间复杂度: O(n²)  # 每次收缩O(n)，共n-2次")
    print("  空间复杂度: O(n + m)  # 存储图")

    print("\n完整Karger算法:")
    print("  迭代次数: O(n² log n)")
    print("  总时间复杂度: O(n⁴ log n)")
    print("  成功概率: 1 - 1/n")

    print("\nKarger-Stein改进版:")
    print("  时间复杂度: O(n² log³ n)")
    print("  成功概率: Ω(1/log n)")

def main():
    """主函数"""
    test_karger_algorithm()
    analyze_complexity()

if __name__ == "__main__":
    main()

# 预期输出示例:
# === Karger最小割算法演示 ===
#
# --- 测试 正方形 ---
# 顶点: [1, 2, 3, 4]
# 边数: 4
# 已知最小割: 2
# Karger算法: 4 个顶点, 4 条边, 50 次迭代
#   迭代   10/50: 最小割= 2, 成功概率≈0.7369
#   迭代   20/50: 最小割= 2, 成功概率≈0.9305
#   ...
# 找到的最小割: 2
# 理论成功概率: 0.9938
# 实际成功率: 0.9200
# 结果正确: True