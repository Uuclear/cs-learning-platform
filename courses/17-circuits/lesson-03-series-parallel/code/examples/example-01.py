#!/usr/bin/env python3
"""
等效电阻计算器 - 支持串并联混合电路

这个程序演示了如何计算串联、并联以及混合电路的等效电阻。
"""


def series_resistance(resistors):
    """
    计算串联电阻的总电阻

    参数:
        resistors (list): 电阻值列表 [R1, R2, R3, ...]

    返回:
        float: 总电阻值
    """
    if not resistors:
        return 0
    return sum(resistors)


def parallel_resistance(resistors):
    """
    计算并联电阻的总电阻

    参数:
        resistors (list): 电阻值列表 [R1, R2, R3, ...]

    返回:
        float: 总电阻值

    异常:
        ValueError: 当电阻列表为空或包含零/负值时
    """
    if not resistors:
        raise ValueError("电阻列表不能为空")

    if any(r <= 0 for r in resistors):
        raise ValueError("所有电阻值必须大于零")

    # 计算倒数和的倒数
    reciprocal_sum = sum(1/r for r in resistors)
    return 1 / reciprocal_sum


def mixed_circuit_resistance(circuit_structure):
    """
    计算混合电路的等效电阻

    参数:
        circuit_structure (dict): 电路结构描述
            格式: {'type': 'series'|'parallel', 'components': [...]}
            components 可以是数值（表示单个电阻）或其他电路结构

    返回:
        float: 等效电阻值
    """
    if isinstance(circuit_structure, (int, float)):
        # 单个电阻值
        return float(circuit_structure)

    circuit_type = circuit_structure['type']
    components = circuit_structure['components']

    # 递归计算每个组件的等效电阻
    component_values = []
    for comp in components:
        if isinstance(comp, (int, float)):
            component_values.append(float(comp))
        elif isinstance(comp, dict):
            component_values.append(mixed_circuit_resistance(comp))
        else:
            raise ValueError(f"不支持的组件类型: {type(comp)}")

    # 根据电路类型计算总电阻
    if circuit_type == 'series':
        return series_resistance(component_values)
    elif circuit_type == 'parallel':
        return parallel_resistance(component_values)
    else:
        raise ValueError(f"不支持的电路类型: {circuit_type}")


def main():
    """主函数 - 演示各种电路计算"""
    print("=== 等效电阻计算器演示 ===\n")

    # 示例1: 简单串联
    print("1. 简单串联电路:")
    resistors_series = [100, 200, 300]  # 单位: 欧姆
    total_series = series_resistance(resistors_series)
    print(f"   电阻值: {resistors_series}")
    print(f"   总电阻: {total_series}Ω\n")

    # 示例2: 简单并联
    print("2. 简单并联电路:")
    resistors_parallel = [100, 200, 300]
    total_parallel = parallel_resistance(resistors_parallel)
    print(f"   电阻值: {resistors_parallel}")
    print(f"   总电阻: {total_parallel:.2f}Ω\n")

    # 示例3: 混合电路
    print("3. 混合电路示例:")
    # 结构: [(100Ω || 200Ω) + 300Ω] || 400Ω
    # 其中 || 表示并联，+ 表示串联
    mixed_circuit = {
        'type': 'parallel',
        'components': [
            {
                'type': 'series',
                'components': [
                    {
                        'type': 'parallel',
                        'components': [100, 200]
                    },
                    300
                ]
            },
            400
        ]
    }

    total_mixed = mixed_circuit_resistance(mixed_circuit)
    print("   电路结构: [(100Ω || 200Ω) + 300Ω] || 400Ω")
    print(f"   等效电阻: {total_mixed:.2f}Ω\n")

    # 示例4: 实际应用 - LED限流电阻
    print("4. 实际应用示例:")
    supply_voltage = 5.0      # 电源电压 (V)
    led_voltage = 2.0         # LED正向电压 (V)
    led_current = 0.02        # LED工作电流 (A)

    resistor_value = (supply_voltage - led_voltage) / led_current
    print(f"   LED限流电阻计算:")
    print(f"   电源电压: {supply_voltage}V")
    print(f"   LED电压: {led_voltage}V")
    print(f"   LED电流: {led_current*1000}mA")
    print(f"   所需电阻: {resistor_value}Ω")


if __name__ == "__main__":
    main()