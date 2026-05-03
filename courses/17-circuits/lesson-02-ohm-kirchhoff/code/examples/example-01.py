#!/usr/bin/env python3
"""
欧姆定律计算器 - 示例1

功能：
- 根据已知的两个参数计算第三个参数
- 同时计算电路功率
- 支持多种输入组合
"""

def ohms_law_calculator(voltage=None, current=None, resistance=None):
    """
    欧姆定律计算器：根据已知的两个参数计算第三个参数
    同时计算功率 P = V × I = I² × R = V² / R

    参数:
        voltage (float): 电压，单位伏特(V)
        current (float): 电流，单位安培(A)
        resistance (float): 电阻，单位欧姆(Ω)

    返回:
        dict: 包含所有四个参数的字典

    异常:
        ValueError: 当提供的参数少于两个时
    """
    # 检查至少提供了两个参数
    provided_params = sum(param is not None for param in [voltage, current, resistance])
    if provided_params < 2:
        raise ValueError("至少需要提供电压、电流、电阻中的两个参数")

    # 根据提供的参数计算缺失的参数
    if voltage is not None and current is not None:
        # 已知 V 和 I，求 R
        if current == 0:
            raise ValueError("电流不能为零（会导致电阻无穷大）")
        resistance = voltage / current
        power = voltage * current
    elif voltage is not None and resistance is not None:
        # 已知 V 和 R，求 I
        if resistance == 0:
            raise ValueError("电阻不能为零（会导致电流无穷大）")
        current = voltage / resistance
        power = voltage ** 2 / resistance
    elif current is not None and resistance is not None:
        # 已知 I 和 R，求 V
        voltage = current * resistance
        power = current ** 2 * resistance
    else:
        # 理论上不会到达这里，因为前面已经检查了参数数量
        raise ValueError("参数组合无效")

    return {
        'voltage': round(voltage, 6),
        'current': round(current, 6),
        'resistance': round(resistance, 6),
        'power': round(power, 6)
    }


def main():
    """演示欧姆定律计算器的使用"""
    print("=== 欧姆定律计算器演示 ===\n")

    # 示例1: 已知电压和电阻，求电流和功率
    print("示例1: 已知电压=12V, 电阻=4Ω")
    result1 = ohms_law_calculator(voltage=12, resistance=4)
    print(f"结果: 电流={result1['current']}A, 功率={result1['power']}W\n")

    # 示例2: 已知电流和电阻，求电压和功率
    print("示例2: 已知电流=0.5A, 电阻=10Ω")
    result2 = ohms_law_calculator(current=0.5, resistance=10)
    print(f"结果: 电压={result2['voltage']}V, 功率={result2['power']}W\n")

    # 示例3: 已知电压和电流，求电阻和功率
    print("示例3: 已知电压=9V, 电流=0.3A")
    result3 = ohms_law_calculator(voltage=9, current=0.3)
    print(f"结果: 电阻={result3['resistance']}Ω, 功率={result3['power']}W\n")


if __name__ == "__main__":
    main()