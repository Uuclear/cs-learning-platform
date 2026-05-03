#!/usr/bin/env python3
"""
运算放大器示例 1: 反相放大器增益计算与仿真

本示例演示了反相放大器的基本原理和增益计算。
反相放大器的增益公式为: Vout = - (Rf / Rin) * Vin
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

def simulate_inverting_amplifier(Rf, Rin, Vin_min=-1, Vin_max=1, num_points=100):
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

def plot_inverting_amplifier(Rf, Rin):
    """
    绘制反相放大器的输入输出特性曲线
    """
    Vin, Vout = simulate_inverting_amplifier(Rf, Rin)
    gain = inverting_amplifier_gain(Rf, Rin)

    plt.figure(figsize=(10, 6))
    plt.plot(Vin, Vout, 'b-', linewidth=2, label=f'增益 = {gain:.1f}')
    plt.xlabel('输入电压 Vin (V)')
    plt.ylabel('输出电压 Vout (V)')
    plt.title(f'反相放大器特性 (Rf={Rf}Ω, Rin={Rin}Ω)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)
    plt.show()

if __name__ == "__main__":
    # 示例参数
    R_feedback = 10000  # 10kΩ 反馈电阻
    R_input = 2000      # 2kΩ 输入电阻

    # 计算增益
    gain = inverting_amplifier_gain(R_feedback, R_input)
    print(f"反相放大器增益: {gain:.1f}")
    print(f"这意味着输入信号会被放大 {abs(gain):.1f} 倍并反相")

    # 仿真并绘图
    plot_inverting_amplifier(R_feedback, R_input)