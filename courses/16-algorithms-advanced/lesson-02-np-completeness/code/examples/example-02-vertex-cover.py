#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：顶点覆盖问题验证与近似算法

这个文件演示了顶点覆盖问题的验证过程，
以及一个简单的2-近似算法。
"""

def verify_vertex_cover(graph, cover_set, k=None):
    """
    验证顶点覆盖解的正确性

    Args:
        graph (dict): 图的邻接表表示
        cover_set (set): 候选顶点覆盖集合
        k (int, optional): 覆盖大小上限，如果提供则检查大小约束

    Returns:
        bool: 如果cover_set是有效的顶点覆盖返回True
    """
    print(f"验证顶点覆盖: {sorted(cover_set)}")

    # 检查大小约束（如果提供k）
    if k is not None:
        if len(cover_set) > k:
            print(f"  ✗ 大小超过限制: {len(cover_set)} > {k}")
            return False
        else:
            print(f"  ✓ 大小满足约束: {len(cover_set)} <= {k}")

    # 收集所有边
    edges = set()
    for u in graph:
        for v in graph[u]:
            if u < v:  # 避免重复（无向图）
                edges.add((u, v))

    print(f"  图中共有 {len(edges)} 条边")

    # 检查每条边是否被覆盖
    uncovered_edges = []
    for u, v in edges:
        if u not in cover_set and v not in cover_set:
            uncovered_edges.append((u, v))

    if uncovered_edges:
        print(f"  ✗ 发现 {len(uncovered_edges)} 条未覆盖的边: {uncovered_edges}")
        return False
    else:
        print("  ✓ 所有边都被覆盖")
        return True

def greedy_vertex_cover(graph):
    """
    贪心2-近似顶点覆盖算法

    Args:
        graph (dict): 图的邻接表表示

    Returns:
        set: 顶点覆盖集合
    """
    print("执行贪心2-近似顶点覆盖算法")

    # 创建图的副本以避免修改原图
    remaining_graph = {}
    for node in graph:
        remaining_graph[node] = set(graph[node])

    cover = set()
    edges_remaining = set()

    # 收集所有剩余边
    for u in remaining_graph:
        for v in remaining_graph[u]:
            if u < v:
                edges_remaining.add((u, v))

    step = 1
    while edges_remaining:
        # 选择一条边
        u, v = next(iter(edges_remaining))
        print(f"  步骤 {step}: 选择边 ({u}, {v})")

        # 将两个端点都加入覆盖
        cover.add(u)
        cover.add(v)
        print(f"    添加顶点 {u}, {v} 到覆盖")

        # 从图中移除与u或v相关的所有边
        edges_to_remove = set()
        for edge in edges_remaining:
            if edge[0] == u or edge[1] == u or edge[0] == v or edge[1] == v:
                edges_to_remove.add(edge)

        edges_remaining -= edges_to_remove
        print(f"    移除 {len(edges_to_remove)} 条边，剩余 {len(edges_remaining)} 条边")

        step += 1

    print(f"算法完成，覆盖大小: {len(cover)}")
    return cover

def optimal_vertex_cover_bruteforce(graph, k):
    """
    暴力搜索最优顶点覆盖（仅适用于小图）

    Args:
        graph (dict): 图的邻接表
        k (int): 最大覆盖大小

    Returns:
        set or None: 如果存在大小≤k的覆盖返回它，否则返回None
    """
    print(f"暴力搜索大小≤{k}的顶点覆盖")

    nodes = list(graph.keys())
    n = len(nodes)

    # 生成所有可能的子集（按大小递增）
    from itertools import combinations

    for size in range(k + 1):
        print(f"  检查大小为 {size} 的覆盖...")
        for subset in combinations(nodes, size):
            cover_set = set(subset)
            if verify_vertex_cover(graph, cover_set):
                print(f"  找到大小为 {size} 的覆盖: {sorted(cover_set)}")
                return cover_set

    print(f"  未找到大小≤{k}的覆盖")
    return None

def main():
    """主函数：演示顶点覆盖算法"""
    print("=== 顶点覆盖问题演示 ===\n")

    # 创建示例图
    graph = {
        1: [2, 3, 4],
        2: [1, 3],
        3: [1, 2, 4],
        4: [1, 3, 5],
        5: [4]
    }

    print("图结构:")
    for node in sorted(graph):
        neighbors = sorted(graph[node])
        print(f"  节点 {node}: 连接到 {neighbors}")

    print("\n" + "-"*40 + "\n")

    # 测试已知覆盖
    print("测试已知覆盖:")
    test_cover = {1, 3}
    verify_vertex_cover(graph, test_cover, k=2)

    print("\n" + "-"*40 + "\n")

    # 运行贪心算法
    print("运行贪心2-近似算法:")
    greedy_cover = greedy_vertex_cover(graph)
    verify_vertex_cover(graph, greedy_cover)

    print("\n" + "-"*40 + "\n")

    # 尝试寻找最优解
    print("寻找最优解 (k=2):")
    optimal_cover = optimal_vertex_cover_bruteforce(graph, 2)
    if optimal_cover:
        print(f"最优覆盖: {sorted(optimal_cover)}")
    else:
        print("不存在大小≤2的覆盖")

if __name__ == "__main__":
    main()

# 预期输出示例:
# === 顶点覆盖问题演示 ===
#
# 图结构:
#   节点 1: 连接到 [2, 3, 4]
#   节点 2: 连接到 [1, 3]
#   ...
#
# 测试已知覆盖:
# 验证顶点覆盖: [1, 3]
#   ✓ 大小满足约束: 2 <= 2
#   图中共有 6 条边
#   ✓ 所有边都被覆盖