#!/usr/bin/env python3
"""
KVL回路分析 - 示例2

功能：
- 分析包含电压源和电阻的闭合回路
- 计算回路电流
- 验证基尔霍夫电压定律
"""

import numpy as np


def kvl_analysis(loop_elements):
    """
    KVL回路分析：给定回路中的元件，求解电流并验证KVL

    参数:
        loop_elements (list): 回路元件列表，每个元素为 (type, value, direction)
            type: 'voltage_source' 或 'resistor'
            value: 电压源的电压值(V)或电阻的阻值(Ω)
            direction: 元件方向相对于回路遍历方向
                对于电压源: 'positive' 表示从负到正与遍历方向一致
                对于电阻: 方向影响不大，因为电流方向会自动确定

    返回:
        dict: 包含电流、各元件电压降、KVL验证结果的字典
    """
    # 分离电压源和电阻
    voltage_sources = []
    resistors = []

    for element in loop_elements:
        if len(element) == 2:
            # 兼容旧格式 (type, value)
            element_type, value = element
            direction = 'positive' if element_type == 'voltage_source' else None
        else:
            # 新格式 (type, value, direction)
            element_type, value, direction = element

        if element_type == 'voltage_source':
            # 电压源：如果方向与遍历方向一致，则为正；否则为负
            effective_voltage = value if direction == 'positive' else -value
            voltage_sources.append(effective_voltage)
        elif element_type == 'resistor':
            resistors.append(value)

    total_voltage = sum(voltage_sources)
    total_resistance = sum(resistors)

    if total_resistance == 0:
        raise ValueError("回路中没有电阻，会导致无限大电流！")

    # 计算回路电流（假设顺时针方向为正）
    current = total_voltage / total_resistance

    # 计算各元件的电压降
    voltage_drops = []
    for element in loop_elements:
        if len(element) == 2:
            element_type, value = element
            direction = 'positive' if element_type == 'voltage_source' else None
        else:
            element_type, value, direction = element

        if element_type == 'voltage_source':
            effective_voltage = value if direction == 'positive' else -value
            voltage_drops.append(-effective_voltage)  # 电压源提供电压，所以是负的压降
        elif element_type == 'resistor':
            # 电阻压降 = I * R，方向与电流方向一致
            resistor_drop = current * value
            voltage_drops.append(resistor_drop)

    # 验证KVL：所有电压降之和应该为0
    kvl_sum = sum(voltage_drops)
    kvl_valid = abs(kvl_sum) < 1e-10

    return {
        'current': round(current, 6),
        'voltage_drops': [round(drop, 6) for drop in voltage_drops],
        'kvl_sum': round(kvl_sum, 6),
        'kvl_valid': kvl_valid,
        'total_voltage': round(total_voltage, 6),
        'total_resistance': round(total_resistance, 6)
    }


def main():
    """演示KVL回路分析的使用"""
    print("=== KVL回路分析演示 ===\n")

    # 示例1: 简单回路 - 12V电源 + 两个电阻
    print("示例1: 12V电源, 4Ω电阻, 8Ω电阻的串联回路")
    loop1 = [
        ('voltage_source', 12, 'positive'),
        ('resistor', 4, None),
        ('resistor', 8, None)
    ]
    result1 = kvl_analysis(loop1)
    print(f"回路电流: {result1['current']}A")
    print(f"各元件电压降: {result1['voltage_drops']}")
    print(f"KVL验证: 总和={result1['kvl_sum']}, 有效={result1['kvl_valid']}\n")

    # 示例2: 复杂回路 - 两个电源反向连接
    print("示例2: 9V和5V电源反向, 6Ω电阻")
    loop2 = [
        ('voltage_source', 9, 'positive'),   # +9V
        ('voltage_source', 5, 'negative'),   # -5V (反向)
        ('resistor', 6, None)
    ]
    result2 = kvl_analysis(loop2)
    print(f"回路电流: {result2['current']}A")
    print(f"各元件电压降: {result2['voltage_drops']}")
    print(f"KVL验证: 总和={result2['kvl_sum']}, 有效={result2['kvl_valid']}\n")


if __name__ == "__main__":
    main()