#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 03: 并联电路分析器完整实现

这是练习题的参考答案，包含了完整的并联电路分析功能。

作者: CS 教授
课程: 17-01 电压、电流与电阻：电路的三剑客
"""

def parallel_circuit_analyzer(total_voltage, resistances):
    """
    分析并联电路

    参数：
    total_voltage (float): 总电压（各支路相同）
    resistances (list): 各支路电阻值列表

    返回：
    dict: 包含各支路电流、总电流、等效电阻的字典
    """
    if total_voltage <= 0:
        raise ValueError("总电压必须为正数")

    if not resistances:
        raise ValueError("电阻列表不能为空")

    if any(r <= 0 for r in resistances):
        raise ValueError("所有电阻值必须为正数")

    # 计算各支路电流
    currents = [total_voltage / r for r in resistances]

    # 计算总电流
    total_current = sum(currents)

    # 计算等效总电阻
    if len(resistances) == 1:
        total_resistance = resistances[0]
    else:
        total_resistance_inverse = sum(1/r for r in resistances)
        total_resistance = 1 / total_resistance_inverse

    # 计算各支路功率
    powers = [total_voltage * i for i in currents]

    return {
        'currents': currents,
        'total_current': total_current,
        'total_resistance': total_resistance,
        'powers': powers
    }

def main():
    """主函数：演示并联电路分析器"""
    print("=== 并联电路分析器 ===\n")

    # 测试用例1：基础示例
    print("测试用例1: 12V电源，三个电阻并联 [6, 12, 4] Ω")
    try:
        result1 = parallel_circuit_analyzer(12, [6, 12, 4])
        print(f"电源电压: {12}V")
        for i, (r, i_val, p) in enumerate(zip([6,12,4], result1['currents'], result1['powers'])):
            print(f"支路{i+1} ({r}Ω): 电流 = {i_val:.3f}A, 功率 = {p:.2f}W")
        print(f"总电流: {result1['total_current']:.3f}A")
        print(f"等效电阻: {result1['total_resistance']:.3f}Ω\n")
    except Exception as e:
        print(f"错误: {e}\n")

    # 测试用例2：家庭电路负载分析
    print("测试用例2: 家庭电路负载分析 (220V)")
    # 常见家用电器的等效电阻（基于典型功率计算）
    # P = V²/R => R = V²/P
    appliances = {
        "LED灯泡(10W)": 220**2 / 10,      # ~4840Ω
        "笔记本电脑(65W)": 220**2 / 65,   # ~745Ω
        "微波炉(1000W)": 220**2 / 1000,   # ~48.4Ω
        "电热水壶(1500W)": 220**2 / 1500  # ~32.3Ω
    }

    resistances = list(appliances.values())
    appliance_names = list(appliances.keys())

    try:
        result2 = parallel_circuit_analyzer(220, resistances)
        print("各电器工作状态:")
        total_power = 0
        for name, current, power in zip(appliance_names, result2['currents'], result2['powers']):
            print(f"  {name}: 电流 = {current:.3f}A, 功率 = {power:.0f}W")
            total_power += power

        print(f"\n总电流: {result2['total_current']:.3f}A")
        print(f"总功率: {total_power:.0f}W")
        print(f"等效电阻: {result2['total_resistance']:.2f}Ω")

        # 安全检查
        circuit_rating = 16  # 家用电路通常为16A
        if result2['total_current'] > circuit_rating * 0.8:  # 80%安全系数
            print(f"\n⚠️  警告: 总电流({result2['total_current']:.2f}A) "
                  f"接近电路额定值({circuit_rating}A)的80%!")
            print("建议不要同时使用所有高功率电器。")
        else:
            print(f"\n✅ 电路负载正常，总电流在安全范围内。")

    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()