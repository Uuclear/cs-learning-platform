#!/usr/bin/env python3
"""
欧姆定律计算器 - 解决方案1

功能：
- 根据已知的两个参数计算第三个参数
- 同时计算电路功率
- 支持多种输入组合
- 包含完整的错误处理和边界情况
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
        ValueError: 当提供的参数少于两个或参数无效时
    """
    # 输入验证
    if voltage is not None and voltage < 0:
        raise ValueError("电压不能为负值")
    if current is not None and current < 0:
        raise ValueError("电流不能为负值")
    if resistance is not None and resistance < 0:
        raise ValueError("电阻不能为负值")

    # 检查至少提供了两个参数
    provided_params = sum(param is not None for param in [voltage, current, resistance])
    if provided_params < 2:
        raise ValueError("至少需要提供电压、电流、电阻中的两个参数")

    # 根据提供的参数计算缺失的参数
    if voltage is not None and current is not None:
        # 已知 V 和 I，求 R
        if current == 0:
            if voltage == 0:
                # 0V/0A 的情况，电阻可以是任意值，但通常设为无穷大
                resistance = float('inf')
                power = 0
            else:
                raise ValueError("电流为零但电压不为零（开路情况）")
        else:
            resistance = voltage / current
            power = voltage * current
    elif voltage is not None and resistance is not None:
        # 已知 V 和 R，求 I
        if resistance == 0:
            if voltage == 0:
                # 0V/0Ω 的情况，电流可以是任意值，但通常设为0
                current = 0
                power = 0
            else:
                raise ValueError("电阻为零但电压不为零（短路情况）")
        else:
            current = voltage / resistance
            power = voltage ** 2 / resistance
    elif current is not None and resistance is not None:
        # 已知 I 和 R，求 V
        if resistance == float('inf'):
            # 无穷大电阻（开路）
            voltage = float('inf') if current > 0 else 0
            power = float('inf') if current > 0 else 0
        else:
            voltage = current * resistance
            power = current ** 2 * resistance
    else:
        # 理论上不会到达这里
        raise ValueError("参数组合无效")

    return {
        'voltage': voltage if voltage == float('inf') else round(voltage, 6),
        'current': current if current == float('inf') else round(current, 6),
        'resistance': resistance if resistance == float('inf') else round(resistance, 6),
        'power': power if power == float('inf') else round(power, 6)
    }


def main():
    """演示欧姆定律计算器的完整使用"""
    print("=== 欧姆定律计算器解决方案 ===\n")

    # 示例1: 正常情况
    print("示例1: 正常情况 - 电压=12V, 电阻=4Ω")
    try:
        result1 = ohms_law_calculator(voltage=12, resistance=4)
        print(f"结果: 电流={result1['current']}A, 功率={result1['power']}W\n")
    except ValueError as e:
        print(f"错误: {e}\n")

    # 示例2: 边界情况 - 零电压
    print("示例2: 边界情况 - 电压=0V, 电阻=10Ω")
    try:
        result2 = ohms_law_calculator(voltage=0, resistance=10)
        print(f"结果: 电流={result2['current']}A, 功率={result2['power']}W\n")
    except ValueError as e:
        print(f"错误: {e}\n")

    # 示例3: 错误情况 - 负值
    print("示例3: 错误情况 - 负电压")
    try:
        result3 = ohms_law_calculator(voltage=-5, resistance=10)
        print(f"结果: {result3}\n")
    except ValueError as e:
        print(f"错误: {e}\n")

    # 示例4: 开路情况
    print("示例4: 开路情况 - 电压=9V, 电流=0A")
    try:
        result4 = ohms_law_calculator(voltage=9, current=0)
        print(f"结果: 电阻={result4['resistance']}, 功率={result4['power']}W\n")
    except ValueError as e:
        print(f"错误: {e}\n")


if __name__ == "__main__":
    main()