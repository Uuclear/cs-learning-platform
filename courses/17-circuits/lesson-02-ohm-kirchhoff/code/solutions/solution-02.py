#!/usr/bin/env python3
"""
KVL回路分析 - 解决方案2

功能：
- 分析包含多个电压源和电阻的复杂闭合回路
- 计算回路电流和各元件电压
- 验证基尔霍夫电压定律
- 处理多个回路的相互影响
"""

import numpy as np


class KVLAnalyzer:
    """KVL回路分析器类，支持复杂电路分析"""

    def __init__(self):
        self.loops = []
        self.elements = {}

    def add_loop(self, loop_name, elements):
        """
        添加一个回路到分析器

        参数:
            loop_name (str): 回路名称
            elements (list): 元件列表，每个元素为 (element_id, type, value, direction)
        """
        loop_info = {
            'name': loop_name,
            'elements': elements,
            'current': None
        }
        self.loops.append(loop_info)

        # 将元件添加到全局元件字典中
        for element in elements:
            element_id = element[0]
            if element_id not in self.elements:
                self.elements[element_id] = {
                    'type': element[1],
                    'value': element[2],
                    'loops': [loop_name]
                }
            else:
                self.elements[element_id]['loops'].append(loop_name)

    def analyze_single_loop(self, loop_elements):
        """
        分析单个回路（独立回路）
        """
        voltage_sources = []
        resistors = []

        for element in loop_elements:
            if len(element) == 3:
                element_id, element_type, value = element
                direction = 'positive' if element_type == 'voltage_source' else None
            elif len(element) == 4:
                element_id, element_type, value, direction = element
            else:
                raise ValueError("元件格式错误")

            if element_type == 'voltage_source':
                effective_voltage = value if direction == 'positive' else -value
                voltage_sources.append(effective_voltage)
            elif element_type == 'resistor':
                resistors.append(value)

        total_voltage = sum(voltage_sources)
        total_resistance = sum(resistors)

        if total_resistance == 0:
            raise ValueError("回路中没有电阻，会导致无限大电流！")

        current = total_voltage / total_resistance

        # 计算各元件电压降
        voltage_drops = []
        element_voltages = {}
        for element in loop_elements:
            if len(element) == 3:
                element_id, element_type, value = element
                direction = 'positive' if element_type == 'voltage_source' else None
            else:
                element_id, element_type, value, direction = element

            if element_type == 'voltage_source':
                effective_voltage = value if direction == 'positive' else -value
                drop = -effective_voltage
                element_voltages[element_id] = effective_voltage
            elif element_type == 'resistor':
                drop = current * value
                element_voltages[element_id] = drop

            voltage_drops.append(drop)

        kvl_sum = sum(voltage_drops)
        kvl_valid = abs(kvl_sum) < 1e-10

        return {
            'current': round(current, 6),
            'voltage_drops': [round(drop, 6) for drop in voltage_drops],
            'element_voltages': {k: round(v, 6) for k, v in element_voltages.items()},
            'kvl_sum': round(kvl_sum, 6),
            'kvl_valid': kvl_valid
        }

    def analyze_mesh_circuit(self):
        """
        分析网孔电路（多个相互连接的回路）
        使用网孔电流法建立方程组
        """
        if len(self.loops) == 1:
            # 单回路情况
            return self.analyze_single_loop(self.loops[0]['elements'])

        # 多回路情况 - 建立网孔方程组
        n_loops = len(self.loops)
        A = np.zeros((n_loops, n_loops))  # 系数矩阵
        B = np.zeros(n_loops)             # 右侧向量

        # 构建方程组
        for i, loop in enumerate(self.loops):
            # 对角线元素：回路自电阻
            self_resistance = 0
            voltage_sum = 0

            for element in loop['elements']:
                element_id = element[0]
                element_type = element[1]
                value = element[2]
                direction = element[3] if len(element) > 3 else ('positive' if element_type == 'voltage_source' else None)

                if element_type == 'resistor':
                    self_resistance += value
                    # 检查是否与其他回路共享
                    shared_loops = self.elements[element_id]['loops']
                    if len(shared_loops) > 1:
                        # 与其他回路共享的电阻
                        for j, other_loop in enumerate(self.loops):
                            if j != i and other_loop['name'] in shared_loops:
                                A[i][j] -= value  # 互电阻为负

                elif element_type == 'voltage_source':
                    effective_voltage = value if direction == 'positive' else -value
                    voltage_sum += effective_voltage

            A[i][i] = self_resistance
            B[i] = voltage_sum

        # 求解线性方程组 A * I = B
        try:
            currents = np.linalg.solve(A, B)
        except np.linalg.LinAlgError:
            raise ValueError("电路方程组无解或有无穷多解")

        # 存储结果
        results = {}
        for i, loop in enumerate(self.loops):
            loop['current'] = currents[i]
            results[f"loop_{loop['name']}"] = round(currents[i], 6)

        return results


def main():
    """演示KVL分析器的使用"""
    print("=== KVL回路分析解决方案 ===\n")

    # 示例1: 单回路分析
    print("示例1: 单回路分析")
    analyzer1 = KVLAnalyzer()
    loop_elements1 = [
        ('V1', 'voltage_source', 12, 'positive'),
        ('R1', 'resistor', 4, None),
        ('R2', 'resistor', 8, None)
    ]
    result1 = analyzer1.analyze_single_loop(loop_elements1)
    print(f"回路电流: {result1['current']}A")
    print(f"各元件电压: {result1['element_voltages']}")
    print(f"KVL验证: {'通过' if result1['kvl_valid'] else '失败'}\n")

    # 示例2: 多回路分析（网孔分析）
    print("示例2: 多回路网孔分析")
    analyzer2 = KVLAnalyzer()

    # 回路1: V1 -> R1 -> R3 -> 地
    loop1_elements = [
        ('V1', 'voltage_source', 12, 'positive'),
        ('R1', 'resistor', 4, None),
        ('R3', 'resistor', 3, None)
    ]

    # 回路2: V2 -> R2 -> R3 -> 地
    loop2_elements = [
        ('V2', 'voltage_source', 6, 'positive'),
        ('R2', 'resistor', 6, None),
        ('R3', 'resistor', 3, None)  # 与回路1共享
    ]

    analyzer2.add_loop('loop1', loop1_elements)
    analyzer2.add_loop('loop2', loop2_elements)

    try:
        result2 = analyzer2.analyze_mesh_circuit()
        print(f"网孔电流结果: {result2}")
        print("注意: R3中的实际电流是两个网孔电流的代数和\n")
    except ValueError as e:
        print(f"分析失败: {e}\n")


if __name__ == "__main__":
    main()