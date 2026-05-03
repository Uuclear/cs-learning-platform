#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 02: 串联电路分析器完整实现

这是练习题的参考答案，包含了完整的串联电路分析功能。

作者: CS 教授
课程: 17-01 电压、电流与电阻：电路的三剑客
"""

def series_circuit_analyzer(total_voltage, resistances):
    """
    分析串联电路

    参数：
    total_voltage (float): 总电压
    resistances (list): 电阻值列表

    返回：
    dict: 包含总电阻、总电流、各电阻电压的字典
    """
    if total_voltage <= 0:
        raise ValueError("总电压必须为正数")

    if not resistances:
        raise ValueError("电阻列表不能为空")

    if any(r <= 0 for r in resistances):
        raise ValueError("所有电阻值必须为正数")

    total_resistance = sum(resistances)
    total_current = total_voltage / total_resistance
    voltages = [total_current * r for r in resistances]

    # 验证基尔霍夫电压定律
    if abs(sum(voltages) - total_voltage) > 1e-10:
        raise RuntimeError("电压计算错误：不满足基尔霍夫电压定律")

    return {
        'total_resistance': total_resistance,
        'total_current': total_current,
        'voltages': voltages,
        'power_dissipation': [total_current**2 * r for r in resistances]  # 功率耗散
    }

def main():
    """主函数：演示串联电路分析器"""
    print("=== 串联电路分析器 ===\n")

    # 测试用例1：基础示例
    print("测试用例1: 9V电池，三个电阻串联 [100, 200, 300] Ω")
    try:
        result1 = series_circuit_analyzer(9, [100, 200, 300])
        print(f"总电阻: {result1['total_resistance']} Ω")
        print(f"电路电流: {result1['total_current']*1000:.2f} mA")
        for i, (v, p) in enumerate(zip(result1['voltages'], result1['power_dissipation'])):
            print(f"R{i+1} ({[100,200,300][i]}Ω): 电压 = {v:.2f}V, 功率 = {p*1000:.2f}mW")
        print()
    except Exception as e:
        print(f"错误: {e}\n")

    # 测试用例2：实际应用 - LED电路
    print("测试用例2: LED限流电路设计")
    print("电源: 5V, LED工作电压: 2V, 目标电流: 20mA")
    led_voltage_drop = 2.0
    target_current = 0.02  # 20mA
    supply_voltage = 5.0

    # 计算所需限流电阻
    resistor_voltage = supply_voltage - led_voltage_drop
    required_resistance = resistor_voltage / target_current

    print(f"限流电阻需要承受的电压: {resistor_voltage}V")
    print(f"所需电阻值: {required_resistance:.0f}Ω")

    # 分析实际电路（假设使用标准电阻值220Ω）
    actual_resistance = 220
    circuit_result = series_circuit_analyzer(supply_voltage, [actual_resistance])
    actual_current = circuit_result['total_current']
    actual_led_voltage = supply_voltage - circuit_result['voltages'][0]

    print(f"使用220Ω电阻时:")
    print(f"  实际电流: {actual_current*1000:.1f}mA")
    print(f"  LED实际电压: {actual_led_voltage:.2f}V")

    if actual_current > 0.03:  # 30mA上限
        print("  警告: 电流过大，可能损坏LED!")
    elif actual_current < 0.01:  # 10mA下限
        print("  提示: 电流过小，LED可能不够亮")
    else:
        print("  电流合适，LED工作正常!")

if __name__ == "__main__":
    main()