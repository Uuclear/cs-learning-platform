#!/usr/bin/env python3
"""
分压电路设计与计算

这个程序演示了分压器的工作原理和设计方法。
"""


def voltage_divider(v_in, r1, r2):
    """
    计算分压器的输出电压

    参数:
        v_in (float): 输入电压 (V)
        r1 (float): 上拉电阻值 (Ω)
        r2 (float): 下拉电阻值 (Ω)

    返回:
        float: 输出电压 (V)
    """
    if r1 <= 0 or r2 <= 0:
        raise ValueError("电阻值必须大于零")

    return v_in * (r2 / (r1 + r2))


def design_voltage_divider(v_in, v_out, total_resistance=None):
    """
    设计分压器电路

    参数:
        v_in (float): 输入电压 (V)
        v_out (float): 期望的输出电压 (V)
        total_resistance (float, optional): 总电阻值 (Ω)，用于控制电流消耗

    返回:
        tuple: (R1, R2) 电阻值
    """
    if v_out >= v_in or v_out <= 0:
        raise ValueError("输出电压必须在0和输入电压之间")

    # 计算电阻比例
    ratio = v_out / (v_in - v_out)  # R2/R1 = Vout/(Vin-Vout)

    if total_resistance is None:
        # 默认使用10kΩ作为R2的参考值
        r2 = 10000.0
        r1 = r2 / ratio
    else:
        # 根据总电阻分配
        r2 = total_resistance * (v_out / v_in)
        r1 = total_resistance - r2

    return r1, r2


def calculate_power_dissipation(v_in, r1, r2):
    """
    计算分压器中每个电阻的功率消耗

    参数:
        v_in (float): 输入电压 (V)
        r1 (float): 上拉电阻值 (Ω)
        r2 (float): 下拉电阻值 (Ω)

    返回:
        tuple: (P1, P2, P_total) 功率值 (W)
    """
    # 总电流
    i_total = v_in / (r1 + r2)

    # 各电阻功率
    p1 = i_total**2 * r1
    p2 = i_total**2 * r2
    p_total = p1 + p2

    return p1, p2, p_total


def main():
    """主函数 - 演示分压器的各种计算"""
    print("=== 分压电路设计与计算演示 ===\n")

    # 示例1: 基本分压计算
    print("1. 基本分压计算:")
    v_in = 9.0      # 输入电压 9V
    r1 = 6000.0     # 6kΩ
    r2 = 3000.0     # 3kΩ

    v_out = voltage_divider(v_in, r1, r2)
    print(f"   输入电压: {v_in}V")
    print(f"   电阻 R1: {r1/1000}kΩ")
    print(f"   电阻 R2: {r2/1000}kΩ")
    print(f"   输出电压: {v_out}V")
    print(f"   验证: {v_in}V × ({r2/1000}kΩ / ({r1/1000}kΩ + {r2/1000}kΩ)) = {v_out}V\n")

    # 示例2: 分压器设计
    print("2. 分压器设计:")
    target_v_in = 5.0       # 5V电源
    target_v_out = 3.3      # 需要3.3V输出

    r1_design, r2_design = design_voltage_divider(target_v_in, target_v_out)
    actual_v_out = voltage_divider(target_v_in, r1_design, r2_design)

    print(f"   设计目标: {target_v_in}V → {target_v_out}V")
    print(f"   推荐电阻: R1 = {r1_design/1000:.1f}kΩ, R2 = {r2_design/1000:.1f}kΩ")
    print(f"   实际输出: {actual_v_out:.3f}V")
    print(f"   误差: {(actual_v_out - target_v_out)/target_v_out*100:.2f}%\n")

    # 示例3: 考虑标准电阻值
    print("3. 使用标准电阻值:")
    # E12系列标准值 (1kΩ范围)
    standard_values = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
    standard_values_k = [v * 1000 for v in standard_values]  # 转换为欧姆

    best_error = float('inf')
    best_r1, best_r2 = None, None

    for r1_std in standard_values_k:
        for r2_std in standard_values_k:
            v_out_std = voltage_divider(target_v_in, r1_std, r2_std)
            error = abs(v_out_std - target_v_out)
            if error < best_error:
                best_error = error
                best_r1, best_r2 = r1_std, r2_std

    best_v_out = voltage_divider(target_v_in, best_r1, best_r2)
    print(f"   最佳标准电阻组合:")
    print(f"   R1 = {best_r1/1000}kΩ, R2 = {best_r2/1000}kΩ")
    print(f"   输出电压: {best_v_out:.3f}V")
    print(f"   误差: {(best_v_out - target_v_out)/target_v_out*100:.2f}%\n")

    # 示例4: 功率计算
    print("4. 功率消耗分析:")
    p1, p2, p_total = calculate_power_dissipation(v_in, r1, r2)
    print(f"   输入电压: {v_in}V")
    print(f"   R1 功率消耗: {p1*1000:.2f}mW")
    print(f"   R2 功率消耗: {p2*1000:.2f}mW")
    print(f"   总功率消耗: {p_total*1000:.2f}mW")
    print(f"   总电流: {v_in/(r1+r2)*1000:.2f}mA\n")

    # 示例5: 负载效应
    print("5. 负载效应考虑:")
    load_resistance = 10000.0  # 10kΩ负载
    # 当有负载时，R2实际上是与负载并联
    r2_effective = parallel_resistance([r2, load_resistance])
    v_out_loaded = voltage_divider(v_in, r1, r2_effective)
    print(f"   无负载输出电压: {v_out:.3f}V")
    print(f"   有负载输出电压: {v_out_loaded:.3f}V")
    print(f"   电压下降: {(v_out - v_out_loaded)/v_out*100:.2f}%")


def parallel_resistance(resistors):
    """辅助函数：计算并联电阻"""
    if any(r <= 0 for r in resistors):
        raise ValueError("所有电阻值必须大于零")
    return 1 / sum(1/r for r in resistors)


if __name__ == "__main__":
    main()