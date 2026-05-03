#!/usr/bin/env python3
"""
等效电阻计算器 - 完整解决方案

这个程序提供了计算串联、并联以及混合电路等效电阻的完整实现，
包括错误处理、输入验证和用户交互功能。
"""


def series_resistance(resistors):
    """
    计算串联电阻的总电阻

    参数:
        resistors (list): 电阻值列表 [R1, R2, R3, ...]

    返回:
        float: 总电阻值

    异常:
        ValueError: 当输入无效时
    """
    if not isinstance(resistors, (list, tuple)):
        raise ValueError("输入必须是列表或元组")

    if not resistors:
        return 0.0

    # 验证所有值都是正数
    for r in resistors:
        if not isinstance(r, (int, float)):
            raise ValueError(f"电阻值必须是数字，得到: {type(r)}")
        if r <= 0:
            raise ValueError(f"电阻值必须大于零，得到: {r}")

    return float(sum(resistors))


def parallel_resistance(resistors):
    """
    计算并联电阻的总电阻

    参数:
        resistors (list): 电阻值列表 [R1, R2, R3, ...]

    返回:
        float: 总电阻值

    异常:
        ValueError: 当输入无效时
    """
    if not isinstance(resistors, (list, tuple)):
        raise ValueError("输入必须是列表或元组")

    if not resistors:
        raise ValueError("电阻列表不能为空")

    # 验证所有值都是正数
    for r in resistors:
        if not isinstance(r, (int, float)):
            raise ValueError(f"电阻值必须是数字，得到: {type(r)}")
        if r <= 0:
            raise ValueError(f"电阻值必须大于零，得到: {r}")

    # 计算倒数和的倒数
    reciprocal_sum = sum(1.0/r for r in resistors)
    return 1.0 / reciprocal_sum


def mixed_circuit_resistance(circuit_structure):
    """
    计算混合电路的等效电阻

    参数:
        circuit_structure (dict): 电路结构描述
            格式: {'type': 'series'|'parallel', 'components': [...]}
            components 可以是数值（表示单个电阻）或其他电路结构

    返回:
        float: 等效电阻值

    异常:
        ValueError: 当输入无效时
    """
    if isinstance(circuit_structure, (int, float)):
        # 单个电阻值
        if circuit_structure <= 0:
            raise ValueError(f"电阻值必须大于零，得到: {circuit_structure}")
        return float(circuit_structure)

    if not isinstance(circuit_structure, dict):
        raise ValueError(f"不支持的组件类型: {type(circuit_structure)}")

    if 'type' not in circuit_structure or 'components' not in circuit_structure:
        raise ValueError("电路结构必须包含'type'和'components'字段")

    circuit_type = circuit_structure['type']
    components = circuit_structure['components']

    if circuit_type not in ['series', 'parallel']:
        raise ValueError(f"不支持的电路类型: {circuit_type}")

    if not isinstance(components, (list, tuple)):
        raise ValueError("components必须是列表或元组")

    if not components:
        raise ValueError("components列表不能为空")

    # 递归计算每个组件的等效电阻
    component_values = []
    for i, comp in enumerate(components):
        try:
            if isinstance(comp, (int, float)):
                if comp <= 0:
                    raise ValueError(f"组件 {i} 的电阻值必须大于零: {comp}")
                component_values.append(float(comp))
            elif isinstance(comp, dict):
                component_values.append(mixed_circuit_resistance(comp))
            else:
                raise ValueError(f"组件 {i} 的类型不支持: {type(comp)}")
        except Exception as e:
            raise ValueError(f"处理组件 {i} 时出错: {e}")

    # 根据电路类型计算总电阻
    if circuit_type == 'series':
        return series_resistance(component_values)
    else:  # parallel
        return parallel_resistance(component_values)


def format_resistance(value):
    """格式化电阻值显示"""
    if value >= 1e6:
        return f"{value/1e6:.2f}MΩ"
    elif value >= 1e3:
        return f"{value/1e3:.2f}kΩ"
    else:
        return f"{value:.2f}Ω"


def interactive_calculator():
    """交互式计算器"""
    print("=== 等效电阻计算器 ===")
    print("选择计算模式:")
    print("1. 串联电阻")
    print("2. 并联电阻")
    print("3. 混合电路")
    print("4. 退出")

    while True:
        try:
            choice = input("\n请选择 (1-4): ").strip()

            if choice == '4':
                print("再见！")
                break
            elif choice == '1':
                # 串联计算
                resistors_input = input("请输入电阻值（用空格分隔，单位Ω）: ")
                resistors = [float(x) for x in resistors_input.split()]
                result = series_resistance(resistors)
                print(f"串联总电阻: {format_resistance(result)}")

            elif choice == '2':
                # 并联计算
                resistors_input = input("请输入电阻值（用空格分隔，单位Ω）: ")
                resistors = [float(x) for x in resistors_input.split()]
                result = parallel_resistance(resistors)
                print(f"并联总电阻: {format_resistance(result)}")

            elif choice == '3':
                # 混合电路示例
                print("\n混合电路示例: [(100Ω || 200Ω) + 300Ω] || 400Ω")
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
                result = mixed_circuit_resistance(mixed_circuit)
                print(f"等效电阻: {format_resistance(result)}")

            else:
                print("无效选择，请输入1-4")

        except ValueError as e:
            print(f"输入错误: {e}")
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"发生错误: {e}")


def main():
    """主函数 - 运行演示和测试"""
    print("=== 等效电阻计算器 - 解决方案 ===\n")

    # 测试用例
    test_cases = [
        {
            'name': '简单串联',
            'func': series_resistance,
            'args': [[100, 200, 300]],
            'expected': 600.0
        },
        {
            'name': '简单并联',
            'func': parallel_resistance,
            'args': [[100, 200, 300]],
            'expected': 54.55  # 约等于
        },
        {
            'name': '混合电路',
            'func': mixed_circuit_resistance,
            'args': [{
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
            }],
            'expected': 182.61  # 约等于
        }
    ]

    for test in test_cases:
        try:
            result = test['func'](*test['args'])
            expected = test['expected']
            error = abs(result - expected)

            print(f"{test['name']}:")
            print(f"  结果: {format_resistance(result)}")
            if error < 1.0:  # 允许小误差
                print(f"  ✓ 通过测试")
            else:
                print(f"  ✗ 测试失败，期望: {format_resistance(expected)}")
            print()

        except Exception as e:
            print(f"{test['name']}: 错误 - {e}\n")

    # 询问是否运行交互式计算器
    run_interactive = input("是否运行交互式计算器? (y/n): ").strip().lower()
    if run_interactive in ['y', 'yes', '是']:
        interactive_calculator()


if __name__ == "__main__":
    main()