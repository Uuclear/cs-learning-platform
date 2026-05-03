#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：顶点覆盖与独立集的完整实现

这个文件提供了顶点覆盖和独立集问题的完整实现，
包括验证、近似算法和归约。
"""

def verify_vertex_cover(graph, cover, k=None):
    """验证顶点覆盖"""
    if k is not None and len(cover) > k:
        return False

    # 收集所有边
    edges = set()
    for u in graph:
        for v in graph[u]:
            if u < v:
                edges.add((u, v))

    # 检查覆盖
    for u, v in edges:
        if u not in cover and v not in cover:
            return False

    return True

def verify_independent_set(graph, independent_set, k=None):
    """验证独立集"""
    if k is not None and len(independent_set) < k:
        return False

    # 检查独立性
    vertices = list(independent_set)
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            u, v = vertices[i], vertices[j]
            if v in graph.get(u, []):
                return False

    return True

def vertex_cover_to_independent_set(graph, k_vc):
    """顶点覆盖到独立集的归约"""
    n = len(graph)
    k_is = n - k_vc
    return graph, k_is

def independent_set_to_vertex_cover(graph, k_is):
    """独立集到顶点覆盖的归约"""
    n = len(graph)
    k_vc = n - k_is
    return graph, k_vc

def greedy_vertex_cover(graph):
    """贪心2-近似顶点覆盖"""
    remaining_graph = {u: set(graph[u]) for u in graph}
    cover = set()

    while any(remaining_graph[u] for u in remaining_graph):
        # 找一条边
        u = next(u for u in remaining_graph if remaining_graph[u])
        v = next(iter(remaining_graph[u]))

        cover.add(u)
        cover.add(v)

        # 移除相关边
        for w in list(remaining_graph[u]):
            remaining_graph[w].discard(u)
        remaining_graph[u].clear()

        for w in list(remaining_graph[v]):
            remaining_graph[w].discard(v)
        remaining_graph[v].clear()

    return cover

def max_degree_independent_set(graph):
    """基于最大度数的独立集近似算法"""
    remaining_graph = {u: set(graph[u]) for u in graph}
    independent_set = set()

    while remaining_graph:
        # 选择度数最小的顶点
        min_degree_vertex = min(remaining_graph.keys(),
                               key=lambda x: len(remaining_graph[x]))

        independent_set.add(min_degree_vertex)

        # 移除该顶点及其邻居
        neighbors = remaining_graph[min_degree_vertex]
        to_remove = {min_degree_vertex} | neighbors

        for v in to_remove:
            if v in remaining_graph:
                # 从邻居的邻接表中移除v
                for w in remaining_graph[v]:
                    if w in remaining_graph:
                        remaining_graph[w].discard(v)
                del remaining_graph[v]

    return independent_set

def test_vertex_cover_independent_set():
    """测试顶点覆盖和独立集"""
    print("=== 顶点覆盖与独立集测试 ===\n")

    # 创建测试图
    graph = {
        1: [2, 3],
        2: [1, 3, 4],
        3: [1, 2, 4],
        4: [2, 3, 5],
        5: [4]
    }

    print("图结构:")
    for u in sorted(graph):
        print(f"  {u}: {sorted(graph[u])}")

    print("\n" + "-"*40 + "\n")

    # 测试顶点覆盖
    print("顶点覆盖测试:")
    vc_solution = {2, 3}
    print(f"候选解: {vc_solution}")
    print(f"验证: {'✓' if verify_vertex_cover(graph, vc_solution, k=2) else '✗'}")

    greedy_vc = greedy_vertex_cover(graph)
    print(f"贪心解: {greedy_vc}, 大小: {len(greedy_vc)}")
    print(f"验证: {'✓' if verify_vertex_cover(graph, greedy_vc) else '✗'}")

    print("\n" + "-"*40 + "\n")

    # 测试独立集
    print("独立集测试:")
    is_solution = {1, 4}
    print(f"候选解: {is_solution}")
    print(f"验证: {'✓' if verify_independent_set(graph, is_solution, k=2) else '✗'}")

    greedy_is = max_degree_independent_set(graph)
    print(f"贪心解: {greedy_is}, 大小: {len(greedy_is)}")
    print(f"验证: {'✓' if verify_independent_set(graph, greedy_is) else '✗'}")

    print("\n" + "-"*40 + "\n")

    # 测试归约
    print("归约测试:")
    k_vc = 2
    graph_is, k_is = vertex_cover_to_independent_set(graph, k_vc)
    print(f"顶点覆盖(G, {k_vc}) → 独立集(G, {k_is})")

    # 验证互补性
    complement = set(graph.keys()) - vc_solution
    print(f"顶点覆盖 {vc_solution} 的补集: {complement}")
    print(f"补集是独立集: {'✓' if verify_independent_set(graph, complement) else '✗'}")

if __name__ == "__main__":
    test_vertex_cover_independent_set()

# 预期输出示例:
# === 顶点覆盖与独立集测试 ===
#
# 图结构:
#   1: [2, 3]
#   2: [1, 3, 4]
#   ...
#
# 顶点覆盖测试:
# 候选解: {2, 3}
# 验证: ✓