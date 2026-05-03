#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：SAT问题验证与求解

这个文件演示了布尔可满足性问题（SAT）的验证过程，
以及一个简单的回溯SAT求解器。
"""

def verify_sat_solution(clauses, assignment):
    """
    验证SAT问题的解是否正确

    Args:
        clauses (list): 子句列表，每个子句包含文字（整数）
                       正数表示变量，负数表示变量的否定
        assignment (dict): 变量赋值字典，键为变量编号，值为True/False

    Returns:
        bool: 如果赋值满足所有子句返回True，否则返回False
    """
    print(f"验证SAT解: {assignment}")

    for clause_idx, clause in enumerate(clauses):
        # 检查子句是否被满足
        clause_satisfied = False

        for literal in clause:
            var = abs(literal)
            is_negated = literal < 0

            # 获取变量值，如果未赋值则默认为False
            var_value = assignment.get(var, False)
            literal_value = not var_value if is_negated else var_value

            if literal_value:
                clause_satisfied = True
                break

        if not clause_satisfied:
            print(f"  子句 {clause_idx + 1} 不满足: {clause}")
            return False
        else:
            print(f"  子句 {clause_idx + 1} 满足: {clause}")

    print("  所有子句都满足！")
    return True

def simple_sat_solver(clauses, num_vars):
    """
    简单的回溯SAT求解器（仅适用于小规模问题）

    Args:
        clauses (list): SAT子句列表
        num_vars (int): 变量数量

    Returns:
        dict or None: 如果可满足返回赋值字典，否则返回None
    """
    def backtrack(assignment, var_index):
        """回溯搜索"""
        if var_index > num_vars:
            # 所有变量都已赋值，验证解
            if verify_sat_solution_partial(clauses, assignment):
                return assignment.copy()
            return None

        # 尝试赋值为True
        assignment[var_index] = True
        result = backtrack(assignment, var_index + 1)
        if result is not None:
            return result

        # 尝试赋值为False
        assignment[var_index] = False
        result = backtrack(assignment, var_index + 1)
        if result is not None:
            return result

        # 回溯
        del assignment[var_index]
        return None

    def verify_sat_solution_partial(clauses, assignment):
        """部分赋值的验证（未赋值变量视为不影响）"""
        for clause in clauses:
            clause_satisfied = False
            for literal in clause:
                var = abs(literal)
                if var in assignment:
                    is_negated = literal < 0
                    var_value = assignment[var]
                    literal_value = not var_value if is_negated else var_value
                    if literal_value:
                        clause_satisfied = True
                        break
                else:
                    # 变量未赋值，该文字可能为真
                    clause_satisfied = True
                    break

            if not clause_satisfied:
                return False

        return True

    print(f"使用回溯法求解SAT问题 ({num_vars} 个变量)")
    return backtrack({}, 1)

def main():
    """主函数：演示SAT验证和求解"""
    print("=== SAT问题演示 ===\n")

    # 示例1: 可满足的3-SAT实例
    print("示例1: 可满足的3-SAT")
    clauses1 = [
        [1, 2, 3],      # x1 ∨ x2 ∨ x3
        [-1, -2, 3],    # ¬x1 ∨ ¬x2 ∨ x3
        [1, -2, -3]     # x1 ∨ ¬x2 ∨ ¬x3
    ]

    # 测试已知解
    solution1 = {1: True, 2: False, 3: True}
    verify_sat_solution(clauses1, solution1)

    # 尝试求解
    print("\n尝试求解:")
    result1 = simple_sat_solver(clauses1, 3)
    if result1:
        print(f"找到解: {result1}")
    else:
        print("无解")

    print("\n" + "="*50 + "\n")

    # 示例2: 不可满足的2-SAT实例
    print("示例2: 不可满足的2-SAT")
    clauses2 = [
        [1, 2],         # x1 ∨ x2
        [1, -2],        # x1 ∨ ¬x2
        [-1, 2],        # ¬x1 ∨ x2
        [-1, -2]        # ¬x1 ∨ ¬x2
    ]

    # 测试所有可能赋值
    all_assignments = [
        {1: True, 2: True},
        {1: True, 2: False},
        {1: False, 2: True},
        {1: False, 2: False}
    ]

    for i, assignment in enumerate(all_assignments, 1):
        print(f"\n测试赋值 {i}: {assignment}")
        verify_sat_solution(clauses2, assignment)

    # 尝试求解
    print("\n尝试求解:")
    result2 = simple_sat_solver(clauses2, 2)
    if result2:
        print(f"找到解: {result2}")
    else:
        print("确认无解")

if __name__ == "__main__":
    main()

# 预期输出示例:
# === SAT问题演示 ===
#
# 示例1: 可满足的3-SAT
# 验证SAT解: {1: True, 2: False, 3: True}
#   子句 1 满足: [1, 2, 3]
#   子句 2 满足: [-1, -2, 3]
#   子句 3 满足: [1, -2, -3]
#   所有子句都满足！
#
# 尝试求解:
# 使用回溯法求解SAT问题 (3 个变量)
# 找到解: {1: True, 2: False, 3: True}