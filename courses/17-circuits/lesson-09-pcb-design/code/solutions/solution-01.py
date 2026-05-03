#!/usr/bin/env python3
"""
PCB Trace Width Calculator - Solution
根据IPC-2221标准计算PCB走线宽度（完整解决方案）
"""

import math
from typing import Dict, Tuple


class TraceWidthCalculator:
    """PCB走线宽度计算器类"""

    # IPC-2221常数
    IPC_CONSTANTS = {
        'external': {'k': 0.048, 'b': 0.44, 'c': 0.725},
        'internal': {'k': 0.024, 'b': 0.44, 'c': 0.725}
    }

    @staticmethod
    def calculate_width(current: float, temp_rise: float = 10,
                       thickness_mils: float = 1.4, layer_type: str = 'external') -> float:
        """
        计算PCB走线宽度

        Args:
            current: 电流（安培）
            temp_rise: 允许温升（摄氏度），默认10°C
            thickness_mils: 铜箔厚度（密耳），默认1.4密耳（1盎司铜）
            layer_type: 层类型，'external'（外层）或'internal'（内层）

        Returns:
            走线宽度（毫米）
        """
        if current <= 0:
            raise ValueError("电流必须大于0")
        if temp_rise <= 0:
            raise ValueError("温升必须大于0")

        constants = TraceWidthCalculator.IPC_CONSTANTS.get(layer_type)
        if not constants:
            raise ValueError("层类型必须是 'external' 或 'internal'")

        k, b, c = constants['k'], constants['b'], constants['c']

        # IPC-2221公式
        width_mils = (current / (k * (temp_rise ** b))) ** (1/c)
        width_mm = width_mils * 0.0254  # 转换为毫米

        return round(width_mm, 2)

    @staticmethod
    def get_copper_thickness_options() -> Dict[str, float]:
        """获取常用铜箔厚度选项"""
        return {
            '0.5oz': 0.7,   # 0.5盎司铜 ≈ 0.7密耳
            '1oz': 1.4,     # 1盎司铜 ≈ 1.4密耳
            '2oz': 2.8,     # 2盎司铜 ≈ 2.8密耳
            '3oz': 4.2      # 3盎司铜 ≈ 4.2密耳
        }


def main():
    """主函数，完整的走线宽度计算演示"""
    print("=== PCB走线宽度计算器（完整版）===")
    print("基于IPC-2221标准")
    print()

    calculator = TraceWidthCalculator()

    # 测试不同场景
    test_cases = [
        {'current': 0.5, 'temp_rise': 10, 'layer': 'external', 'desc': '信号线（外层）'},
        {'current': 2.0, 'temp_rise': 20, 'layer': 'external', 'desc': '电源线（外层）'},
        {'current': 3.0, 'temp_rise': 10, 'layer': 'internal', 'desc': '电源线（内层）'},
    ]

    for case in test_cases:
        try:
            width = calculator.calculate_width(
                current=case['current'],
                temp_rise=case['temp_rise'],
                layer_type=case['layer']
            )
            print(f"{case['desc']}: {case['current']}A, ΔT={case['temp_rise']}°C → {width}mm")
        except ValueError as e:
            print(f"错误: {e}")

    print()
    print("铜箔厚度参考:")
    thickness_options = calculator.get_copper_thickness_options()
    for name, mils in thickness_options.items():
        print(f"  {name}: {mils}密耳 ({mils*0.0254:.2f}mm)")


if __name__ == "__main__":
    main()