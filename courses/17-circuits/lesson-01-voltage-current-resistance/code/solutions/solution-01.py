#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 01: 欧姆定律计算器完整实现

这是练习题的参考答案，包含了完整的错误处理和用户交互功能。

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

def get_user_input():
    """获取用户输入并返回参数字典"""
    print("请输入已知的电路参数（未知参数直接按回车）:")

    try:
        voltage_input = input("电压 (V): ").strip()
        voltage = float(voltage_input) if voltage_input else None

        current_input = input("电流 (A): ").strip()
        current = float(current_input) if current_input else None

        resistance_input = input("电阻 (Ω): ").strip()
        resistance = float(resistance_input) if resistance_input else None

        return voltage, current, resistance

    except ValueError:
        raise ValueError("请输入有效的数字")

def format_result(result):
    """格式化输出结果"""
    return (f"计算结果:\n"
            f"  电压: {result['voltage']:.3f} V\n"
            f"  电流: {result['current']:.6f} A\n"
            f"  电阻: {result['resistance']:.3f} Ω")

def main():
    """主函数：完整的交互式欧姆定律计算器"""
    print("=== 欧姆定律计算器 ===")
    print("根据欧姆定律 V = I × R\n")

    while True:
        try:
            voltage, current, resistance = get_user_input()
            result = ohms_law_calculator(voltage, current, resistance)
            print("\n" + format_result(result))

            # 询问是否继续
            continue_calc = input("\n是否继续计算？(y/n): ").strip().lower()
            if continue_calc != 'y':
                break
            print()

        except ValueError as e:
            print(f"\n错误: {e}")
            retry = input("是否重试？(y/n): ").strip().lower()
            if retry != 'y':
                break
            print()
        except KeyboardInterrupt:
            print("\n\n程序已退出")
            break

if __name__ == "__main__":
    main()