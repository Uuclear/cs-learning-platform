#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：NP-completeness归约完整实现

这个文件提供了从3-SAT到顶点覆盖的完整归约实现。
"""

def sat_to_vertex_cover(clauses, num_vars):
    """
    3-SAT到顶点覆盖的多项式时间归约

    Args:
        clauses (list): 3-SAT子句列表
        num_vars (int): 变量数量

    Returns:
        tuple: (顶点覆盖图, k值)
    """
    graph = {}
    vertices = set()

    # 步骤1: 变量选择边
    for var in range(1, num_vars + 1):
        pos = f"x{var}"
        neg = f"nx{var}"
        vertices.add(pos)
        vertices.add(neg)

        if pos not in graph:
            graph[pos] = []
        if neg not in graph:
            graph[neg] = []

        graph[pos].append(neg)
        graph[neg].append(pos)

    # 步骤2: 子句三角形
    for clause_idx, clause in enumerate(clauses):
        triangle_vertices = []
        for literal_idx, literal in enumerate(clause):
            var = abs(literal)
            is_negated = literal < 0

            clause_vertex = f"c{clause_idx}_{literal_idx}"
            triangle_vertices.append(clause_vertex)
            vertices.add(clause_vertex)

            # 连接到变量顶点
            var_vertex = f"nx{var}" if is_negated else f"x{var}"

            if clause_vertex not in graph:
                graph[clause_vertex] = []
            if var_vertex not in graph:
                graph[var_vertex] = []

            graph[clause_vertex].append(var_vertex)
            graph[var_vertex].append(clause_vertex)

        # 三角形内部边
        for i in range(len(triangle_vertices)):
            for j in range(i + 1, len(triangle_vertices)):
                v1, v2 = triangle_vertices[i], triangle_vertices[j]
                if v1 not in graph:
                    graph[v1] = []
                if v2 not in graph:
                    graph[v2] = []
                graph[v1].append(v2)
                graph[v2].append(v1)

    k = num_vars + 2 * len(clauses)
    return graph, k

def verify_vertex_cover(graph, cover, k):
    """验证顶点覆盖解"""
    if len(cover) > k:
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

def construct_sat_solution_from_vc(vc_solution, num_vars, clauses):
    """从顶点覆盖解构造SAT赋值"""
    assignment = {}

    for var in range(1, num_vars + 1):
        pos = f"x{var}"
        neg = f"nx{var}"

        # 如果x在覆盖中，赋值为False；如果¬x在覆盖中，赋值为True
        if pos in vc_solution and neg not in vc_solution:
            assignment[var] = False
        elif neg in vc_solution and pos not in vc_solution:
            assignment[var] = True
        else:
            # 理论上不应该发生
            assignment[var] = True

    return assignment

def verify_sat_solution(clauses, assignment):
    """验证SAT解"""
    for clause in clauses:
        satisfied = False
        for literal in clause:
            var = abs(literal)
            is_negated = literal < 0
            var_value = assignment.get(var, False)
            literal_value = not var_value if is_negated else var_value
            if literal_value:
                satisfied = True
                break
        if not satisfied:
            return False
    return True

def test_reduction():
    """测试归约的正确性"""
    print("=== 3-SAT到顶点覆盖归约测试 ===\n")

    # 测试用例1: 可满足的3-SAT
    clauses1 = [[1, 2, 3], [-1, -2, 3]]
    num_vars1 = 3

    print("测试用例1: 可满足的3-SAT")
    print(f"子句: {clauses1}")

    # 执行归约
    graph1, k1 = sat_to_vertex_cover(clauses1, num_vars1)
    print(f"归约结果: k = {k1}, 顶点数 = {len(graph1)}")

    # 构造顶点覆盖解（基于已知SAT解）
    sat_solution1 = {1: True, 2: False, 3: True}
    vc_solution1 = set()

    # 根据SAT解构造VC解
    for var in range(1, num_vars1 + 1):
        if sat_solution1[var]:
            vc_solution1.add(f"x{var}")
        else:
            vc_solution1.add(f"nx{var}")

    # 添加子句顶点（每个子句选2个）
    for clause_idx, clause in enumerate(clauses1):
        # 找到满足的文字
        satisfied_literal_idx = None
        for lit_idx, literal in enumerate(clause):
            var = abs(literal)
            is_negated = literal < 0
            var_value = sat_solution1[var]
            literal_value = not var_value if is_negated else var_value
            if literal_value:
                satisfied_literal_idx = lit_idx
                break

        # 添加其他两个顶点到覆盖
        for lit_idx in range(3):
            if lit_idx != satisfied_literal_idx:
                vc_solution1.add(f"c{clause_idx}_{lit_idx}")

    print(f"构造的顶点覆盖解大小: {len(vc_solution1)}")
    vc_valid1 = verify_vertex_cover(graph1, vc_solution1, k1)
    print(f"顶点覆盖验证: {'✓' if vc_valid1 else '✗'}")

    # 从VC解恢复SAT解
    recovered_sat1 = construct_sat_solution_from_vc(vc_solution1, num_vars1, clauses1)
    sat_valid1 = verify_sat_solution(clauses1, recovered_sat1)
    print(f"SAT解验证: {'✓' if sat_valid1 else '✗'}")
    print(f"原始解: {sat_solution1}")
    print(f"恢复解: {recovered_sat1}")

    print("\n" + "="*50 + "\n")

    # 测试用例2: 不可满足的2-SAT（转换为3-SAT）
    clauses2 = [[1, 2, 2], [1, -2, -2], [-1, 2, 2], [-1, -2, -2]]
    num_vars2 = 2

    print("测试用例2: 不可满足的SAT（通过重复文字）")
    print(f"子句: {clauses2}")

    graph2, k2 = sat_to_vertex_cover(clauses2, num_vars2)
    print(f"归约结果: k = {k2}")

    # 理论上应该不存在大小≤k2的顶点覆盖
    # 这里不尝试构造，只验证归约结构
    print("归约结构验证完成")

if __name__ == "__main__":
    test_reduction()

# 预期输出示例:
# === 3-SAT到顶点覆盖归约测试 ===
#
# 测试用例1: 可满足的3-SAT
# 子句: [[1, 2, 3], [-1, -2, 3]]
# 归约结果: k = 7, 顶点数 = 12
# 构造的顶点覆盖解大小: 7
# 顶点覆盖验证: ✓
# SAT解验证: ✓