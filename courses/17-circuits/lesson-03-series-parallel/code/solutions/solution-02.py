#!/usr/bin/env python3
"""
分压电路设计与计算 - 完整解决方案

这个程序提供了分压器的完整设计、分析和优化功能，
包括标准电阻值选择、负载效应分析和功率计算。
"""


import math


def voltage_divider(v_in, r1, r2):
    """
    计算分压器的输出电压

    参数:
        v_in (float): 输入电压 (V)
        r1 (float): 上拉电阻值 (Ω)
        r2 (float): 下拉电阻值 (Ω)

    返回:
        float: 输出电压 (V)

    异常:
        ValueError: 当输入无效时
    """
    if not all(isinstance(x, (int, float)) for x in [v_in, r1, r2]):
        raise ValueError("所有参数必须是数字")

    if v_in <= 0:
        raise ValueError("输入电压必须大于零")

    if r1 <= 0 or r2 <= 0:
        raise ValueError("电阻值必须大于零")

    return v_in * (r2 / (r1 + r2))


def design_voltage_divider(v_in, v_out, total_resistance=None, e_series='E12'):
    """
    设计分压器电路，自动选择标准电阻值

    参数:
        v_in (float): 输入电压 (V)
        v_out (float): 期望的输出电压 (V)
        total_resistance (float, optional): 总电阻值 (Ω)
        e_series (str): 标准电阻系列 ('E6', 'E12', 'E24')

    返回:
        dict: 包含设计结果的字典
    """
    if not all(isinstance(x, (int, float)) for x in [v_in, v_out]):
        raise ValueError("电压参数必须是数字")

    if v_out >= v_in or v_out <= 0:
        raise ValueError("输出电压必须在0和输入电压之间")

    # E系列标准值（1-10范围）
    e_series_values = {
        'E6': [1.0, 1.5, 2.2, 3.3, 4.7, 6.8],
        'E12': [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2],
        'E24': [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
    }

    if e_series not in e_series_values:
        raise ValueError(f"不支持的E系列: {e_series}")

    base_values = e_series_values[e_series]

    # 生成标准电阻值（考虑常用范围：100Ω 到 1MΩ）
    standard_resistors = []
    decades = [1, 10, 100, 1000, 10000, 100000, 1000000]  # 1Ω 到 1MΩ

    for decade in decades:
        for base in base_values:
            standard_resistors.append(base * decade)

    # 计算理想的电阻比例
    ideal_ratio = v_out / (v_in - v_out)  # R2/R1

    best_error = float('inf')
    best_r1, best_r2 = None, None

    # 搜索最佳标准电阻组合
    for r1_candidate in standard_resistors:
        if total_resistance is not None:
            # 如果指定了总电阻，计算对应的R2
            r2_ideal = total_resistance - r1_candidate
            if r2_ideal <= 0:
                continue

            # 找到最接近的理想R2的标准值
            r2_candidate = min(standard_resistors,
                             key=lambda r: abs(r - r2_ideal))
        else:
            # 基于理想比例计算R2
            r2_ideal = r1_candidate * ideal_ratio
            r2_candidate = min(standard_resistors,
                             key=lambda r: abs(r - r2_ideal))

        # 计算实际输出电压和误差
        try:
            actual_v_out = voltage_divider(v_in, r1_candidate, r2_candidate)
            error = abs(actual_v_out - v_out)

            if error < best_error:
                best_error = error
                best_r1, best_r2 = r1_candidate, r2_candidate
        except:
            continue

    if best_r1 is None:
        raise ValueError("无法找到合适的电阻组合")

    actual_v_out = voltage_divider(v_in, best_r1, best_r2)
    actual_error_pct = (actual_v_out - v_out) / v_out * 100

    return {
        'r1': best_r1,
        'r2': best_r2,
        'actual_v_out': actual_v_out,
        'target_v_out': v_out,
        'error_volts': best_error,
        'error_percent': actual_error_pct,
        'e_series': e_series,
        'total_resistance': best_r1 + best_r2
    }


def calculate_power_dissipation(v_in, r1, r2):
    """
    计算分压器中每个电阻的功率消耗

    参数:
        v_in (float): 输入电压 (V)
        r1 (float): 上拉电阻值 (Ω)
        r2 (float): 下拉电阻值 (Ω)

    返回:
        dict: 功率计算结果
    """
    total_resistance = r1 + r2
    total_current = v_in / total_resistance

    p1 = total_current**2 * r1
    p2 = total_current**2 * r2
    p_total = p1 + p2

    # 推荐的安全额定功率（通常是实际消耗的2倍）
    recommended_p1 = p1 * 2
    recommended_p2 = p2 * 2

    return {
        'current': total_current,
        'power_r1': p1,
        'power_r2': p2,
        'power_total': p_total,
        'recommended_rating_r1': recommended_p1,
        'recommended_rating_r2': recommended_p2
    }


def analyze_load_effect(v_in, r1, r2, load_resistance):
    """
    分析负载对分压器输出的影响

    参数:
        v_in (float): 输入电压 (V)
        r1 (float): 上拉电阻值 (Ω)
        r2 (float): 下拉电阻值 (Ω)
        load_resistance (float): 负载电阻值 (Ω)

    返回:
        dict: 负载效应分析结果
    """
    # 无负载时的输出电压
    v_out_no_load = voltage_divider(v_in, r1, r2)

    # 有负载时，R2与负载并联
    r2_parallel = parallel_resistance([r2, load_resistance])
    v_out_with_load = voltage_divider(v_in, r1, r2_parallel)

    voltage_drop = v_out_no_load - v_out_with_load
    drop_percentage = voltage_drop / v_out_no_load * 100

    return {
        'v_out_no_load': v_out_no_load,
        'v_out_with_load': v_out_with_load,
        'voltage_drop': voltage_drop,
        'drop_percentage': drop_percentage,
        'effective_output_resistance': r1 * r2 / (r1 + r2)  # Thevenin等效电阻
    }


def parallel_resistance(resistors):
    """辅助函数：计算并联电阻"""
    if any(r <= 0 for r in resistors):
        raise ValueError("所有电阻值必须大于零")
    return 1.0 / sum(1.0/r for r in resistors)


def format_resistance(value):
    """格式化电阻值显示"""
    if value >= 1e6:
        return f"{value/1e6:.2f}MΩ"
    elif value >= 1e3:
        return f"{value/1e3:.2f}kΩ"
    else:
        return f"{value:.2f}Ω"


def main():
    """主函数 - 运行完整的分压器设计演示"""
    print("=== 分压电路设计与计算 - 完整解决方案 ===\n")

    # 示例1: 基本分压器设计
    print("1. 基本分压器设计 (5V → 3.3V):")
    try:
        design = design_voltage_divider(5.0, 3.3, e_series='E12')
        print(f"   R1 = {format_resistance(design['r1'])}")
        print(f"   R2 = {format_resistance(design['r2'])}")
        print(f"   实际输出: {design['actual_v_out']:.3f}V")
        print(f"   误差: {design['error_percent']:.2f}%")

        # 功率分析
        power = calculate_power_dissipation(5.0, design['r1'], design['r2'])
        print(f"   总电流: {power['current']*1000:.2f}mA")
        print(f"   R1功率: {power['power_r1']*1000:.2f}mW")
        print(f"   R2功率: {power['power_r2']*1000:.2f}mW")
        print(f"   推荐电阻功率等级: ≥{max(power['recommended_rating_r1'], power['recommended_rating_r2'])*1000:.1f}mW")
    except Exception as e:
        print(f"   错误: {e}")
    print()

    # 示例2: 考虑负载效应
    print("2. 负载效应分析:")
    r1_test = 1800  # 1.8kΩ
    r2_test = 3300  # 3.3kΩ
    load_r = 10000  # 10kΩ负载

    try:
        load_analysis = analyze_load_effect(5.0, r1_test, r2_test, load_r)
        print(f"   无负载输出: {load_analysis['v_out_no_load']:.3f}V")
        print(f"   有负载输出: {load_analysis['v_out_with_load']:.3f}V")
        print(f"   电压下降: {load_analysis['drop_percentage']:.2f}%")
        print(f"   等效输出电阻: {format_resistance(load_analysis['effective_output_resistance'])}")

        # 规则：负载电阻应至少是等效输出电阻的10倍
        min_recommended_load = load_analysis['effective_output_resistance'] * 10
        print(f"   推荐最小负载电阻: {format_resistance(min_recommended_load)}")
    except Exception as e:
        print(f"   错误: {e}")
    print()

    # 示例3: 不同精度要求
    print("3. 不同E系列精度比较:")
    target_v_in, target_v_out = 9.0, 5.0

    for series in ['E6', 'E12', 'E24']:
        try:
            design = design_voltage_divider(target_v_in, target_v_out, e_series=series)
            print(f"   {series}: R1={format_resistance(design['r1'])}, R2={format_resistance(design['r2'])}, "
                  f"误差={design['error_percent']:.2f}%")
        except Exception as e:
            print(f"   {series}: 错误 - {e}")
    print()

    # 示例4: 低功耗设计
    print("4. 低功耗分压器设计:")
    # 对于电池供电应用，希望总电阻较大以减少电流消耗
    try:
        low_power_design = design_voltage_divider(3.3, 1.8, total_resistance=100000)  # 100kΩ总电阻
        power_analysis = calculate_power_dissipation(3.3, low_power_design['r1'], low_power_design['r2'])
        print(f"   R1 = {format_resistance(low_power_design['r1'])}")
        print(f"   R2 = {format_resistance(low_power_design['r2'])}")
        print(f"   总电流: {power_analysis['current']*1000:.3f}mA")
        print(f"   总功耗: {power_analysis['power_total']*1000:.3f}mW")
        print(f"   误差: {low_power_design['error_percent']:.2f}%")
    except Exception as e:
        print(f"   错误: {e}")


if __name__ == "__main__":
    main()