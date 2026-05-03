#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 01: 欧姆定律计算器

这个程序演示了如何使用欧姆定律 (V = I * R) 来计算电路中的未知参数。
用户可以输入任意两个已知参数，程序会自动计算第三个参数。

作者: CS 教授
课程: 17-01 电压、电流与电阻：电路的三剑客
"""

def ohms_law_calculator(voltage=None, current=None, resistance=None):
    """
    欧姆定律计算器：根据已知的两个参数计算第三个参数

    参数：
    voltage (float): 电压（伏特），可选
    current (float): 电流（安培），可选
    resistance (float): 电阻（欧姆），可选

    返回：
    dict: 包含所有三个参数的字典

    异常：
    ValueError: 当提供的参数不足或参数冲突时抛出
    """
    # 验证输入参数
    provided_params = sum(param is not None for param in [voltage, current, resistance])

    if provided_params < 2:
        raise ValueError("至少需要提供两个参数才能进行计算")

    if provided_params == 3:
        # 验证三个参数是否符合欧姆定律
        if abs(voltage - current * resistance) > 1e-10:
            raise ValueError("提供的三个参数不符合欧姆定律 V = I * R")
        return {
            'voltage': voltage,
            'current': current,
            'resistance': resistance
        }

    # 计算缺失的参数
    if voltage is None:
        voltage = current * resistance
        if resistance <= 0:
            raise ValueError("电阻必须为正数")
    elif current is None:
        if resistance <= 0:
            raise ValueError("电阻必须为正数")
        current = voltage / resistance
    elif resistance is None:
        if current == 0:
            raise ValueError("电流不能为零")
        resistance = voltage / current
        if resistance <= 0:
            raise ValueError("计算得到的电阻必须为正数")

    return {
        'voltage': voltage,
        'current': current,
        'resistance': resistance
    }

def main():
    """主函数：演示欧姆定律计算器的使用"""
    print("=== 欧姆定律计算器演示 ===\n")

    # 示例 1: 已知电压和电阻，求电流
    print("示例 1: 已知电压 = 12V, 电阻 = 4Ω, 求电流")
    result1 = ohms_law_calculator(voltage=12, resistance=4)
    print(f"结果: 电压 = {result1['voltage']}V, "
          f"电流 = {result1['current']}A, "
          f"电阻 = {result1['resistance']}Ω\n")

    # 示例 2: 已知电流和电阻，求电压
    print("示例 2: 已知电流 = 0.5A, 电阻 = 10Ω, 求电压")
    result2 = ohms_law_calculator(current=0.5, resistance=10)
    print(f"结果: 电压 = {result2['voltage']}V, "
          f"电流 = {result2['current']}A, "
          f"电阻 = {result2['resistance']}Ω\n")

    # 示例 3: 已知电压和电流，求电阻
    print("示例 3: 已知电压 = 9V, 电流 = 0.3A, 求电阻")
    result3 = ohms_law_calculator(voltage=9, current=0.3)
    print(f"结果: 电压 = {result3['voltage']}V, "
          f"电流 = {result3['current']}A, "
          f"电阻 = {result3['resistance']}Ω\n")

if __name__ == "__main__":
    main()