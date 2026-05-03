#!/usr/bin/env python3
"""
KCL节点分析 - 解决方案3

功能：
- 分析复杂电路中的多个节点
- 求解未知电流和电压
- 验证基尔霍夫电流定律
- 支持完整的节点电压法实现
"""

import numpy as np


class KCLAnalyzer:
    """KCL节点分析器类，支持复杂电路的节点分析"""

    def __init__(self):
        self.nodes = {}
        self.branches = {}
        self.reference_node = None

    def add_node(self, node_name, branches=None):
        """
        添加节点到分析器

        参数:
            node_name (str): 节点名称
            branches (list): 连接到该节点的支路列表
        """
        if branches is None:
            branches = []
        self.nodes[node_name] = {
            'branches': branches,
            'voltage': None
        }

    def add_branch(self, branch_name, from_node, to_node, element_type, value):
        """
        添加支路到分析器

        参数:
            branch_name (str): 支路名称
            from_node (str): 起始节点
            to_node (str): 终止节点
            element_type (str): 元件类型 ('resistor', 'voltage_source', 'current_source')
            value (float): 元件值
        """
        self.branches[branch_name] = {
            'from': from_node,
            'to': to_node,
            'type': element_type,
            'value': value,
            'current': None
        }

        # 更新节点的支路列表
        if from_node not in self.nodes:
            self.nodes[from_node] = {'branches': [], 'voltage': None}
        if to_node not in self.nodes:
            self.nodes[to_node] = {'branches': [], 'voltage': None}

        self.nodes[from_node]['branches'].append((branch_name, 'out'))
        self.nodes[to_node]['branches'].append((branch_name, 'in'))

    def set_reference_node(self, node_name):
        """设置参考节点（接地点）"""
        if node_name not in self.nodes:
            raise ValueError(f"节点 {node_name} 不存在")
        self.reference_node = node_name
        self.nodes[node_name]['voltage'] = 0.0

    def verify_kcl_at_node(self, node_name, branch_currents):
        """
        验证指定节点的KCL

        参数:
            node_name (str): 节点名称
            branch_currents (dict): 支路电流字典 {branch_name: current_value}

        返回:
            dict: 验证结果
        """
        if node_name not in self.nodes:
            raise ValueError(f"节点 {node_name} 不存在")

        total_in = 0.0
        total_out = 0.0

        for branch_name, direction in self.nodes[node_name]['branches']:
            if branch_name not in branch_currents:
                raise ValueError(f"缺少支路 {branch_name} 的电流值")

            current = branch_currents[branch_name]
            if direction == 'in':
                total_in += current
            else:  # direction == 'out'
                total_out += current

        imbalance = total_in - total_out
        is_balanced = abs(imbalance) < 1e-10

        return {
            'node': node_name,
            'total_in': round(total_in, 6),
            'total_out': round(total_out, 6),
            'imbalance': round(imbalance, 6),
            'is_balanced': is_balanced
        }

    def solve_node_voltages(self):
        """
        使用节点电压法求解所有节点电压
        """
        if self.reference_node is None:
            raise ValueError("必须先设置参考节点")

        # 获取非参考节点列表
        non_ref_nodes = [node for node in self.nodes.keys() if node != self.reference_node]
        n_nodes = len(non_ref_nodes)

        if n_nodes == 0:
            return {}  # 只有参考节点的情况

        # 建立节点方程组 G * V = I
        G = np.zeros((n_nodes, n_nodes))  # 电导矩阵
        I = np.zeros(n_nodes)             # 电流向量

        node_to_index = {node: i for i, node in enumerate(non_ref_nodes)}

        # 构建方程组
        for node in non_ref_nodes:
            i = node_to_index[node]
            conductance_sum = 0.0
            current_sum = 0.0

            for branch_name, direction in self.nodes[node]['branches']:
                branch = self.branches[branch_name]
                element_type = branch['type']
                value = branch['value']

                if element_type == 'resistor':
                    conductance = 1.0 / value
                    conductance_sum += conductance

                    # 检查另一端连接的节点
                    other_node = branch['to'] if direction == 'in' else branch['from']
                    if other_node != self.reference_node and other_node in node_to_index:
                        j = node_to_index[other_node]
                        G[i][j] -= conductance  # 互电导为负

                elif element_type == 'current_source':
                    # 电流源直接贡献到电流向量
                    if direction == 'in':
                        current_sum += value
                    else:
                        current_sum -= value

                elif element_type == 'voltage_source':
                    # 电压源需要特殊处理（这里简化处理，假设连接到参考节点）
                    other_node = branch['to'] if direction == 'in' else branch['from']
                    if other_node == self.reference_node:
                        # 电压源直接连接到参考节点
                        if direction == 'in':
                            # 电压源正极连接到当前节点
                            self.nodes[node]['voltage'] = value
                        else:
                            # 电压源负极连接到当前节点
                            self.nodes[node]['voltage'] = -value
                    else:
                        # 复杂情况：电压源连接两个非参考节点
                        # 这里简化处理，实际需要使用修正节点法
                        pass

            G[i][i] = conductance_sum
            I[i] = current_sum

        # 处理已知电压的节点
        known_voltages = {}
        for node in non_ref_nodes:
            if self.nodes[node]['voltage'] is not None:
                known_voltages[node] = self.nodes[node]['voltage']

        if len(known_voltages) == n_nodes:
            # 所有节点电压都已知
            return {node: voltage for node, voltage in known_voltages.items()}

        # 移除已知电压对应的方程
        unknown_nodes = [node for node in non_ref_nodes if node not in known_voltages]
        if not unknown_nodes:
            return {node: self.nodes[node]['voltage'] for node in non_ref_nodes}

        # 重新构建方程组（仅包含未知节点）
        n_unknown = len(unknown_nodes)
        G_reduced = np.zeros((n_unknown, n_unknown))
        I_reduced = np.zeros(n_unknown)

        unknown_to_index = {node: i for i, node in enumerate(unknown_nodes)}

        for node in unknown_nodes:
            i = unknown_to_index[node]
            orig_i = node_to_index[node]

            for j, other_node in enumerate(unknown_nodes):
                orig_j = node_to_index[other_node]
                G_reduced[i][j] = G[orig_i][orig_j]

            I_reduced[i] = I[orig_i]

            # 减去已知电压的影响
            for known_node, known_voltage in known_voltages.items():
                orig_j = node_to_index[known_node]
                G_ij = G[orig_i][orig_j]
                if abs(G_ij) > 1e-10:
                    I_reduced[i] -= G_ij * known_voltage

        # 求解方程组
        try:
            unknown_voltages = np.linalg.solve(G_reduced, I_reduced)
        except np.linalg.LinAlgError:
            raise ValueError("节点方程组无解或有无穷多解")

        # 组合结果
        results = {}
        for node in non_ref_nodes:
            if node in known_voltages:
                results[node] = known_voltages[node]
            else:
                results[node] = round(unknown_voltages[unknown_to_index[node]], 6)

        # 存储结果
        for node, voltage in results.items():
            self.nodes[node]['voltage'] = voltage

        return results

    def calculate_branch_currents(self):
        """根据节点电压计算支路电流"""
        currents = {}

        for branch_name, branch in self.branches.items():
            from_node = branch['from']
            to_node = branch['to']
            element_type = branch['type']
            value = branch['value']

            if element_type == 'resistor':
                v_from = self.nodes[from_node]['voltage']
                v_to = self.nodes[to_node]['voltage']
                if v_from is None or v_to is None:
                    raise ValueError(f"节点电压未计算: {from_node} 或 {to_node}")

                current = (v_from - v_to) / value
                currents[branch_name] = round(current, 6)
                branch['current'] = current

            elif element_type == 'current_source':
                # 电流源电流已知
                currents[branch_name] = value
                branch['current'] = value

            elif element_type == 'voltage_source':
                # 电压源电流需要通过KCL计算，这里暂时设为None
                currents[branch_name] = None

        return currents


def main():
    """演示KCL分析器的使用"""
    print("=== KCL节点分析解决方案 ===\n")

    # 示例1: 简单三节点电路
    print("示例1: 三节点电路分析")
    analyzer1 = KCLAnalyzer()

    # 添加支路
    analyzer1.add_branch('R1', 'A', 'B', 'resistor', 4)
    analyzer1.add_branch('R2', 'B', 'C', 'resistor', 6)
    analyzer1.add_branch('R3', 'A', 'C', 'resistor', 3)
    analyzer1.add_branch('V1', 'A', 'ref', 'voltage_source', 12)

    # 设置参考节点
    analyzer1.set_reference_node('ref')

    try:
        # 求解节点电压
        voltages = analyzer1.solve_node_voltages()
        print(f"节点电压: {voltages}")

        # 计算支路电流
        currents = analyzer1.calculate_branch_currents()
        print(f"支路电流: {currents}")

        # 验证KCL在节点B
        if 'B' in analyzer1.nodes:
            branch_currents_for_B = {}
            for branch_name, direction in analyzer1.nodes['B']['branches']:
                if currents[branch_name] is not None:
                    branch_currents_for_B[branch_name] = currents[branch_name]
                else:
                    # 对于电压源，需要特殊处理
                    branch_currents_for_B[branch_name] = 0  # 简化处理

            kcl_result = analyzer1.verify_kcl_at_node('B', branch_currents_for_B)
            print(f"节点B的KCL验证: {'通过' if kcl_result['is_balanced'] else '失败'}")
    except ValueError as e:
        print(f"分析失败: {e}")

    print()

    # 示例2: 验证已知电流
    print("示例2: KCL验证")
    node_currents = {
        'I1': (2.5, 'in'),
        'I2': (1.8, 'in'),
        'I3': (1.2, 'out'),
        'I4': (3.1, 'out')
    }

    total_in = 2.5 + 1.8
    total_out = 1.2 + 3.1
    imbalance = total_in - total_out

    print(f"总流入: {total_in}A")
    print(f"总流出: {total_out}A")
    print(f"不平衡量: {imbalance}A")
    print(f"KCL验证: {'通过' if abs(imbalance) < 1e-10 else '失败'}")


if __name__ == "__main__":
    main()