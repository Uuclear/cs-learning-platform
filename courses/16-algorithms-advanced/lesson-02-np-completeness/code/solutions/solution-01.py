#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：完整的SAT求解器

这个文件提供了完整的SAT问题验证和求解实现。
"""

def verify_sat_solution(clauses, assignment):
    """
    验证SAT解的正确性

    Args:
        clauses (list): 子句列表
        assignment (dict): 变量赋值

    Returns:
        bool: 解是否正确
    """
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

def dpll_solver(clauses, num_vars):
    """
    DPLL SAT求解器实现

    Args:
        clauses (list): SAT子句
        num_vars (int): 变量数量

    Returns:
        dict or None: 满足赋值或None（无解）
    """
    def unit_propagate(clauses, assignment):
        """单元子句传播"""
        changed = True
        while changed:
            changed = False
            new_clauses = []

            for clause in clauses:
                # 检查子句状态
                unassigned = []
                satisfied = False

                for lit in clause:
                    var = abs(lit)
                    if var in assignment:
                        val = assignment[var]
                        lit_val = not val if lit < 0 else val
                        if lit_val:
                            satisfied = True
                            break
                    else:
                        unassigned.append(lit)

                if satisfied:
                    continue

                if not unassigned:
                    return None, False  # 冲突

                if len(unassigned) == 1:
                    # 单元子句
                    lit = unassigned[0]
                    var = abs(lit)
                    val = lit > 0
                    assignment[var] = val
                    changed = True
                else:
                    new_clauses.append(clause)

            clauses = new_clauses

        return clauses, True

    def pure_literal_elimination(clauses, assignment):
        """纯文字消除"""
        if not clauses:
            return clauses

        literal_count = {}
        for clause in clauses:
            for lit in clause:
                var = abs(lit)
                if var not in assignment:
                    literal_count[lit] = literal_count.get(lit, 0) + 1

        # 找纯文字
        pure_literals = []
        for lit in literal_count:
            var = abs(lit)
            neg_lit = -lit
            if neg_lit not in literal_count:
                pure_literals.append(lit)

        for lit in pure_literals:
            var = abs(lit)
            val = lit > 0
            assignment[var] = val

        # 移除被满足的子句
        new_clauses = []
        for clause in clauses:
            satisfied = False
            for lit in clause:
                var = abs(lit)
                if var in assignment:
                    val = assignment[var]
                    lit_val = not val if lit < 0 else val
                    if lit_val:
                        satisfied = True
                        break
            if not satisfied:
                new_clauses.append(clause)

        return new_clauses

    def dpll_recursive(clauses, assignment):
        """递归DPLL"""
        # 应用预处理
        clauses, ok = unit_propagate(clauses, assignment)
        if not ok:
            return None

        clauses = pure_literal_elimination(clauses, assignment)

        if not clauses:
            return assignment.copy()

        # 找未赋值变量
        unassigned_vars = set()
        for clause in clauses:
            for lit in clause:
                var = abs(lit)
                if var not in assignment:
                    unassigned_vars.add(var)

        if not unassigned_vars:
            return assignment.copy()

        # 选择变量（最简单策略）
        var = min(unassigned_vars)

        # 尝试True
        assignment_true = assignment.copy()
        assignment_true[var] = True
        result = dpll_recursive(clauses, assignment_true)
        if result is not None:
            return result

        # 尝试False
        assignment_false = assignment.copy()
        assignment_false[var] = False
        result = dpll_recursive(clauses, assignment_false)
        return result

    return dpll_recursive(clauses, {})

def test_sat_solver():
    """测试SAT求解器"""
    print("=== SAT求解器测试 ===\n")

    # 测试用例1: 可满足
    clauses1 = [[1, 2], [-1, 2], [1, -2]]
    print("测试用例1: 可满足实例")
    print(f"子句: {clauses1}")
    solution1 = dpll_solver(clauses1, 2)
    if solution1:
        print(f"找到解: {solution1}")
        print(f"验证: {'✓' if verify_sat_solution(clauses1, solution1) else '✗'}")
    else:
        print("无解")

    print("\n" + "-"*40 + "\n")

    # 测试用例2: 不可满足
    clauses2 = [[1], [-1]]
    print("测试用例2: 不可满足实例")
    print(f"子句: {clauses2}")
    solution2 = dpll_solver(clauses2, 1)
    if solution2:
        print(f"找到解: {solution2}")
        print(f"验证: {'✓' if verify_sat_solution(clauses2, solution2) else '✗'}")
    else:
        print("正确判断为无解")

if __name__ == "__main__":
    test_sat_solver()

# 预期输出:
# === SAT求解器测试 ===
#
# 测试用例1: 可满足实例
# 子句: [[1, 2], [-1, 2], [1, -2]]
# 找到解: {1: True, 2: True}
# 验证: ✓
#
# 测试用例2: 不可满足实例
# 子句: [[1], [-1]]
# 正确判断为无解