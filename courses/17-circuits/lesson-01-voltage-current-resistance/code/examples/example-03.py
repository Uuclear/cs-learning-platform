#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 03: 并联电路电流分配计算器

在并联电路中，各支路电压相等，但电流会按照电阻的倒数比例进行分配。
这个程序演示了如何计算并联电路中各支路的电流。

作者: CS 教授
课程: 17-01 电压、电流与电阻：电路的三剑客
"""

def parallel_circuit_current_divider(voltage, resistances):
    """
    计算并联电路中各支路的电流分配

    在并联电路中：
    - 各支路电压相等，等于电源电压
    - 各支路电流 = 电压 / 该支路电阻
    - 总电流 = 各支路电流之和
    - 总电阻的倒数 = 各支路电阻倒数之和

    参数：
    voltage (float): 电源电压（伏特）
    resistances (list): 各支路电阻值列表（欧姆）

    返回：
    dict: 包含详细计算结果的字典

    异常：
    ValueError: 当输入参数无效时抛出
    """
    if voltage <= 0:
        raise ValueError("电压必须为正数")

    if not resistances:
        raise ValueError("电阻列表不能为空")

    if any(r <= 0 for r in resistances):
        raise ValueError("所有电阻值必须为正数")

    # 计算各支路电流
    currents = [voltage / r for r in resistances]

    # 计算总电流
    total_current = sum(currents)

    # 计算等效总电阻
    total_resistance_inverse = sum(1/r for r in resistances)
    total_resistance = 1 / total_resistance_inverse

    # 计算电流百分比
    current_percentages = [i/total_current*100 for i in currents]

    return {
        'voltage': voltage,
        'resistances': resistances,
        'currents': currents,
        'total_current': total_current,
        'total_resistance': total_resistance,
        'current_percentages': current_percentages
    }

def main():
    """主函数：演示并联电路电流分配计算"""
    print("=== 并联电路电流分配计算器 ===\n")

    # 示例 1: 简单的两个电阻并联
    print("示例 1: 12V 电源，两个电阻并联 R1=6Ω, R2=12Ω")
    result1 = parallel_circuit_current_divider(12, [6, 12])
    print(f"电源电压: {result1['voltage']}V")
    print(f"R1 支路电流: {result1['currents'][0]:.2f}A ({result1['current_percentages'][0]:.1f}%)")
    print(f"R2 支路电流: {result1['currents'][1]:.2f}A ({result1['current_percentages'][1]:.1f}%)")
    print(f"总电流: {result1['total_current']:.2f}A")
    print(f"等效总电阻: {result1['total_resistance']:.2f}Ω\n")

    # 示例 2: 家庭电路模拟（多个电器并联）
    print("示例 2: 家庭电路模拟 - 220V 电源，并联多个电器")
    # 假设: 台灯(484Ω), 电视(242Ω), 电脑(110Ω)
    # 对应功率: 台灯~100W, 电视~200W, 电脑~440W
    appliances = [484, 242, 110]  # 电阻值（欧姆）
    appliance_names = ["台灯", "电视", "电脑"]

    result2 = parallel_circuit_current_divider(220, appliances)
    print(f"家庭电压: {result2['voltage']}V")
    for i, name in enumerate(appliance_names):
        power = result2['voltage'] * result2['currents'][i]  # P = V * I
        print(f"{name}: 电流 = {result2['currents'][i]:.2f}A, 功率 = {power:.0f}W")
    print(f"总电流: {result2['total_current']:.2f}A")
    print(f"等效总电阻: {result2['total_resistance']:.2f}Ω")
    print(f"总功率: {result2['voltage'] * result2['total_current']:.0f}W\n")

    # 实际应用：保险丝选择
    print("实际应用: 家庭电路保险丝选择")
    print("如果总电流超过保险丝额定值，保险丝会熔断保护电路")
    print("常见家用保险丝额定值: 10A, 15A, 20A")
    if result2['total_current'] > 15:
        print("警告: 当前负载可能需要20A保险丝！")
    else:
        print("当前负载可以使用15A保险丝")

if __name__ == "__main__":
    main()