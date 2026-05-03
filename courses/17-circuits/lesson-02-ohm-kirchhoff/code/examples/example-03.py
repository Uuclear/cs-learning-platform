#!/usr/bin/env python3
"""
KCL节点分析 - 示例3

功能：
- 分析电路节点的电流分布
- 验证基尔霍夫电流定律
- 支持多个流入流出支路
"""

def kcl_analysis(node_currents):
    """
    KCL节点分析：验证节点电流是否满足KCL

    参数:
        node_currents (dict): 节点电流信息
            键: 支路名称（字符串）
            值: (current, direction) 元组
                current: 电流值（安培）
                direction: 'in' 表示流入节点，'out' 表示流出节点

    返回:
        dict: 包含总流入、总流出、平衡差值、是否平衡的字典
    """
    total_in = 0.0
    total_out = 0.0
    branches_info = []

    for branch_name, (current, direction) in node_currents.items():
        if direction == 'in':
            total_in += current
            branches_info.append(f"{branch_name}: +{current}A (流入)")
        elif direction == 'out':
            total_out += current
            branches_info.append(f"{branch_name}: -{current}A (流出)")
        else:
            raise ValueError(f"支路 {branch_name} 的方向必须是 'in' 或 'out'")

    # 计算不平衡量（流入 - 流出 应该等于0）
    imbalance = total_in - total_out
    is_balanced = abs(imbalance) < 1e-10  # 考虑浮点数精度

    return {
        'total_in': round(total_in, 6),
        'total_out': round(total_out, 6),
        'imbalance': round(imbalance, 6),
        'is_balanced': is_balanced,
        'branches_info': branches_info
    }


def solve_node_currents(known_currents, unknown_branch):
    """
    求解节点中的未知电流（基于KCL）

    参数:
        known_currents (dict): 已知电流信息，格式同kcl_analysis
        unknown_branch (str): 未知电流的支路名称

    返回:
        float: 未知支路的电流值（正值表示流入，负值表示流出）
    """
    # 计算已知电流的代数和
    known_sum = 0.0
    for current, direction in known_currents.values():
        if direction == 'in':
            known_sum += current
        else:  # direction == 'out'
            known_sum -= current

    # 根据KCL，总和应该为0，所以未知电流 = -known_sum
    # 如果结果为正，表示实际方向是流入；如果为负，表示实际方向是流出
    unknown_current = -known_sum
    return round(unknown_current, 6)


def main():
    """演示KCL节点分析的使用"""
    print("=== KCL节点分析演示 ===\n")

    # 示例1: 验证已知电流是否满足KCL
    print("示例1: 验证节点电流平衡")
    node1 = {
        'branch_A': (2.0, 'in'),
        'branch_B': (1.5, 'in'),
        'branch_C': (0.5, 'in'),
        'branch_D': (2.5, 'out'),
        'branch_E': (1.5, 'out')
    }
    result1 = kcl_analysis(node1)
    print("支路信息:")
    for info in result1['branches_info']:
        print(f"  {info}")
    print(f"总流入: {result1['total_in']}A")
    print(f"总流出: {result1['total_out']}A")
    print(f"不平衡量: {result1['imbalance']}A")
    print(f"KCL验证: {'通过' if result1['is_balanced'] else '失败'}\n")

    # 示例2: 求解未知电流
    print("示例2: 求解未知支路电流")
    known_currents = {
        'branch_X': (3.0, 'in'),
        'branch_Y': (1.2, 'out'),
        'branch_Z': (0.8, 'out')
    }
    unknown_branch = 'branch_W'
    unknown_current = solve_node_currents(known_currents, unknown_branch)

    print("已知支路:")
    for branch, (current, direction) in known_currents.items():
        print(f"  {branch}: {current}A ({'流入' if direction == 'in' else '流出'})")
    print(f"未知支路 {unknown_branch} 的电流: {abs(unknown_current)}A "
          f"({'流入' if unknown_current > 0 else '流出'})\n")

    # 验证求解结果
    all_currents = known_currents.copy()
    all_currents[unknown_branch] = (abs(unknown_current), 'in' if unknown_current > 0 else 'out')
    verification = kcl_analysis(all_currents)
    print(f"验证结果: 不平衡量={verification['imbalance']}A, "
          f"KCL验证={'通过' if verification['is_balanced'] else '失败'}")


if __name__ == "__main__":
    main()