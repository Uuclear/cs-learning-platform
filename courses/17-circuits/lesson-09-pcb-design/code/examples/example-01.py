#!/usr/bin/env python3
"""
PCB Trace Width Calculator
根据IPC-2221标准计算PCB走线宽度
"""

import math


def calculate_trace_width(current: float, temp_rise: float = 10, thickness: float = 1.4) -> float:
    """
    计算PCB走线宽度

    Args:
        current: 电流（安培）
        temp_rise: 允许温升（摄氏度），默认10°C
        thickness: 铜箔厚度（密耳），默认1.4密耳（1盎司铜）

    Returns:
        走线宽度（毫米）
    """
    # IPC-2221公式：Width(mils) = (Current / (k * Temp_Rise^b))^(1/c)
    # 对于外层走线：k=0.048, b=0.44, c=0.725
    k, b, c = 0.048, 0.44, 0.725

    width_mils = (current / (k * (temp_rise ** b))) ** (1/c)
    width_mm = width_mils * 0.0254  # 转换为毫米

    return round(width_mm, 2)


def main():
    """主函数，演示走线宽度计算"""
    print("=== PCB走线宽度计算器 ===")
    print("基于IPC-2221标准")
    print()

    # 测试不同电流值
    test_currents = [0.1, 0.5, 1.0, 2.0, 5.0]

    for current in test_currents:
        width = calculate_trace_width(current)
        print(f"电流 {current:4.1f}A → 走线宽度 {width:5.2f}mm")

    print()
    print("注意：这是外层走线的计算结果")
    print("内层走线需要使用不同的参数（k=0.024）")


if __name__ == "__main__":
    main()