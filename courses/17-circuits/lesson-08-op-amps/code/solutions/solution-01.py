#!/usr/bin/env python3
"""
运算放大器解决方案 1: 反相放大器增益计算与仿真

完整实现反相放大器的仿真，包括输入输出特性分析。
"""

import numpy as np
import matplotlib.pyplot as plt

def inverting_amplifier_gain(Rf, Rin):
    """
    计算反相放大器的增益

    参数:
    Rf: 反馈电阻 (欧姆)
    Rin: 输入电阻 (欧姆)

    返回:
    增益值 (负数表示反相)
    """
    return -Rf / Rin

def simulate_inverting_amplifier(Rf, Rin, Vin_min=-2, Vin_max=2, num_points=200):
    """
    仿真反相放大器的输入输出特性

    参数:
    Rf: 反馈电阻 (欧姆)
    Rin: 输入电阻 (欧姆)
    Vin_min: 输入电压最小值 (伏特)
    Vin_max: 输入电压最大值 (伏特)
    num_points: 采样点数

    返回:
    Vin_array: 输入电压数组
    Vout_array: 输出电压数组
    """
    Vin_array = np.linspace(Vin_min, Vin_max, num_points)
    gain = inverting_amplifier_gain(Rf, Rin)
    Vout_array = gain * Vin_array
    return Vin_array, Vout_array

def analyze_inverting_amplifier(Rf_values, Rin_values):
    """
    分析不同电阻组合下的反相放大器性能
    """
    plt.figure(figsize=(15, 10))

    for i, (Rf, Rin) in enumerate(zip(Rf_values, Rin_values)):
        Vin, Vout = simulate_inverting_amplifier(Rf, Rin)
        gain = inverting_amplifier_gain(Rf, Rin)

        plt.subplot(2, 3, i+1)
        plt.plot(Vin, Vout, 'b-', linewidth=2)
        plt.xlabel('输入电压 Vin (V)')
        plt.ylabel('输出电压 Vout (V)')
        plt.title(f'Rf={Rf/1000:.0f}kΩ, Rin={Rin/1000:.0f}kΩ\n增益={gain:.1f}')
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='k', linewidth=0.5)
        plt.axvline(x=0, color='k', linewidth=0.5)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 基本示例
    R_feedback = 15000  # 15kΩ
    R_input = 3000      # 3kΩ

    gain = inverting_amplifier_gain(R_feedback, R_input)
    print(f"反相放大器配置:")
    print(f"  反馈电阻 Rf = {R_feedback/1000:.0f}kΩ")
    print(f"  输入电阻 Rin = {R_input/1000:.0f}kΩ")
    print(f"  增益 = {gain:.1f}")
    print(f"  输入 1V 信号将产生 {gain:.1f}V 输出")

    # 多种配置分析
    Rf_list = [10000, 20000, 50000, 10000, 10000]
    Rin_list = [10000, 10000, 10000, 5000, 20000]

    print("\n分析多种电阻组合...")
    analyze_inverting_amplifier(Rf_list, Rin_list)