#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：NP-completeness归约演示

这个文件演示了从3-SAT到顶点覆盖的多项式时间归约过程。
"""

def sat_to_vertex_cover(clauses, num_vars):
    """
    将3-SAT实例归约到顶点覆盖实例

    Args:
        clauses (list): 3-SAT子句列表
        num_vars (int): 变量数量

    Returns:
        tuple: (顶点覆盖图, k值)
    """
    print("=== 3-SAT 到 顶点覆盖的归约 ===")
    print(f"输入: {len(clauses)} 个子句, {num_vars} 个变量")

    # 构建顶点覆盖图
    graph = {}
    all_vertices = set()

    # 步骤1: 为每个变量创建选择边 (x_i, ¬x_i)
    print("\n步骤1: 创建变量选择边")
    for var in range(1, num_vars + 1):
        pos_vertex = f"x{var}"
        neg_vertex = f"nx{var}"  # nx 表示 ¬x

        all_vertices.add(pos_vertex)
        all_vertices.add(neg_vertex)

        # 添加边
        if pos_vertex not in graph:
            graph[pos_vertex] = []
        if neg_vertex not in graph:
            graph[neg_vertex] = []

        graph[pos_vertex].append(neg_vertex)
        graph[neg_vertex].append(pos_vertex)

        print(f"  添加边: ({pos_vertex}, {neg_vertex})")

    # 步骤2: 为每个子句创建三角形
    print("\n步骤2: 为每个子句创建三角形")
    for clause_idx, clause in enumerate(clauses):
        triangle_vertices = []
        print(f"  子句 {clause_idx + 1}: {clause}")

        for literal_idx, literal in enumerate(clause):
            var = abs(literal)
            is_negated = literal < 0

            # 创建子句顶点
            clause_vertex = f"c{clause_idx}_{literal_idx}"
            triangle_vertices.append(clause_vertex)
            all_vertices.add(clause_vertex)

            # 连接到对应的变量顶点
            var_vertex = f"nx{var}" if is_negated else f"x{var}"

            if clause_vertex not in graph:
                graph[clause_vertex] = []
            if var_vertex not in graph:
                graph[var_vertex] = []

            graph[clause_vertex].append(var_vertex)
            graph[var_vertex].append(clause_vertex)

            print(f"    添加边: ({clause_vertex}, {var_vertex})")

        # 在三角形内部添加边
        for i in range(len(triangle_vertices)):
            for j in range(i + 1, len(triangle_vertices)):
                v1, v2 = triangle_vertices[i], triangle_vertices[j]
                if v1 not in graph:
                    graph[v1] = []
                if v2 not in graph:
                    graph[v2] = []
                graph[v1].append(v2)
                graph[v2].append(v1)
                print(f"    添加三角形边: ({v1}, {v2})")

    # 计算k值
    k = num_vars + 2 * len(clauses)
    print(f"\nk值计算: {num_vars} + 2×{len(clauses)} = {k}")

    return graph, k

def verify_reduction_correctness(original_clauses, num_vars, vc_graph, k):
    """
    验证归约的正确性（通过小规模测试）
    """
    print("\n=== 验证归约正确性 ===")

    # 由于完整验证需要SAT求解器，这里只检查图结构
    total_vertices = len(vc_graph)
    expected_vertices = 2 * num_vars + 3 * len(original_clauses)
    print(f"顶点数量: 实际={total_vertices}, 期望={expected_vertices}")

    # 检查每个变量都有选择边
    for var in range(1, num_vars + 1):
        pos = f"x{var}"
        neg = f"nx{var}"
        if neg not in vc_graph.get(pos, []) or pos not in vc_graph.get(neg, []):
            print(f"错误: 变量 {var} 的选择边缺失")
            return False

    print("图结构验证通过")
    return True

def demonstrate_reduction():
    """演示归约过程"""
    print("=== 归约演示 ===\n")

    # 示例3-SAT: (x1 ∨ x2 ∨ x3) ∧ (¬x1 ∨ ¬x2 ∨ x3)
    clauses = [
        [1, 2, 3],
        [-1, -2, 3]
    ]
    num_vars = 3

    print("原始3-SAT实例:")
    for i, clause in enumerate(clauses, 1):
        clause_str = []
        for lit in clause:
            var = abs(lit)
            sign = "¬" if lit < 0 else ""
            clause_str.append(f"{sign}x{var}")
        print(f"  子句 {i}: {' ∨ '.join(clause_str)}")

    # 执行归约
    vc_graph, k = sat_to_vertex_cover(clauses, num_vars)

    # 验证归约
    verify_reduction_correctness(clauses, num_vars, vc_graph, k)

    # 显示归约后的图
    print(f"\n归约后的顶点覆盖实例:")
    print(f"k = {k}")
    print("图的邻接表:")
    for vertex in sorted(vc_graph.keys()):
        neighbors = sorted(vc_graph[vertex])
        print(f"  {vertex}: {neighbors}")

    # 简单验证：检查是否存在大小为k的覆盖
    print(f"\n注意: 原始3-SAT可满足当且仅当存在大小≤{k}的顶点覆盖")

def main():
    """主函数"""
    demonstrate_reduction()

if __name__ == "__main__":
    main()

# 预期输出示例:
# === 归约演示 ===
#
# 原始3-SAT实例:
#   子句 1: x1 ∨ x2 ∨ x3
#   子句 2: ¬x1 ∨ ¬x2 ∨ x3
#
# === 3-SAT 到 顶点覆盖的归约 ===
# 输入: 2 个子句, 3 个变量
#
# 步骤1: 创建变量选择边
#   添加边: (x1, nx1)
#   添加边: (x2, nx2)
#   ...
#
# k值计算: 3 + 2×2 = 7