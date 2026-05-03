#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 02: 串联电路电压分配计算器

在串联电路中，电流处处相等，但电压会按照电阻的比例进行分配。
这个程序演示了如何计算串联电路中各电阻上的电压。

作者: CS 教授
课程: 17-01 电压、电流与电阻：电路的三剑客
"""

def series_circuit_voltage_divider(total_voltage, resistances):
    """
    计算串联电路中各电阻的电压分配

    在串联电路中：
    - 总电阻 = R1 + R2 + ... + Rn
    - 总电流 = 总电压 / 总电阻
    - 各电阻电压 = 总电流 * 该电阻值

    参数：
    total_voltage (float): 电源总电压（伏特）
    resistances (list): 电阻值列表（欧姆）

    返回：
    dict: 包含详细计算结果的字典

    异常：
    ValueError: 当输入参数无效时抛出
    """
    if total_voltage <= 0:
        raise ValueError("总电压必须为正数")

    if not resistances:
        raise ValueError("电阻列表不能为空")

    if any(r <= 0 for r in resistances):
        raise ValueError("所有电阻值必须为正数")

    # 计算总电阻
    total_resistance = sum(resistances)

    # 计算总电流（串联电路中处处相等）
    total_current = total_voltage / total_resistance

    # 计算各电阻上的电压
    voltages = [total_current * r for r in resistances]

    # 验证电压分配是否正确（基尔霍夫电压定律）
    voltage_sum = sum(voltages)
    if abs(voltage_sum - total_voltage) > 1e-10:
        raise RuntimeError("电压分配计算出现错误")

    return {
        'total_voltage': total_voltage,
        'resistances': resistances,
        'total_resistance': total_resistance,
        'total_current': total_current,
        'voltages': voltages,
        'voltage_percentages': [v/total_voltage*100 for v in voltages]
    }

def main():
    """主函数：演示串联电路电压分配计算"""
    print("=== 串联电路电压分配计算器 ===\n")

    # 示例 1: 简单的两个电阻串联
    print("示例 1: 12V 电源，两个电阻串联 R1=2Ω, R2=4Ω")
    result1 = series_circuit_voltage_divider(12, [2, 4])
    print(f"总电阻: {result1['total_resistance']}Ω")
    print(f"电路电流: {result1['total_current']:.2f}A")
    print(f"R1 上的电压: {result1['voltages'][0]:.2f}V ({result1['voltage_percentages'][0]:.1f}%)")
    print(f"R2 上的电压: {result1['voltages'][1]:.2f}V ({result1['voltage_percentages'][1]:.1f}%)\n")

    # 示例 2: 三个电阻串联（分压器应用）
    print("示例 2: 9V 电源，三个电阻串联 R1=1kΩ, R2=2kΩ, R3=6kΩ")
    result2 = series_circuit_voltage_divider(9, [1000, 2000, 6000])
    print(f"总电阻: {result2['total_resistance']/1000:.1f}kΩ")
    print(f"电路电流: {result2['total_current']*1000:.2f}mA")
    print(f"R1 上的电压: {result2['voltages'][0]:.2f}V ({result2['voltage_percentages'][0]:.1f}%)")
    print(f"R2 上的电压: {result2['voltages'][1]:.2f}V ({result2['voltage_percentages'][1]:.1f}%)")
    print(f"R3 上的电压: {result2['voltages'][2]:.2f}V ({result2['voltage_percentages'][2]:.1f}%)\n")

    # 实际应用：LED限流电阻
    print("实际应用: LED限流电阻计算")
    print("假设: 电源5V, LED工作电压2V, 工作电流20mA")
    print("需要的限流电阻电压 = 5V - 2V = 3V")
    led_resistance = 3 / 0.02  # V/I = 3V/0.02A
    print(f"限流电阻值: {led_resistance:.0f}Ω")

if __name__ == "__main__":
    main()