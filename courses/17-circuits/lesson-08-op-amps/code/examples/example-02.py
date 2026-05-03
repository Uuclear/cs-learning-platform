#!/usr/bin/env python3
"""
运算放大器示例 2: 同相放大器与电压跟随器

本示例演示了同相放大器和电压跟随器的工作原理。
同相放大器的增益公式为: Vout = (1 + Rf / Rin) * Vin
电压跟随器是同相放大器的特例，增益为 1。
"""

import numpy as np
import matplotlib.pyplot as plt

def non_inverting_amplifier_gain(Rf, Rin):
    """
    计算同相放大器的增益

    参数:
    Rf: 反馈电阻 (欧姆)
    Rin: 输入电阻 (欧姆)

    返回:
    增益值 (正数表示同相)
    """
    return 1 + Rf / Rin

def voltage_follower():
    """
    电压跟随器的增益始终为 1
    """
    return 1.0

def simulate_non_inverting_amplifier(Rf, Rin, Vin_min=-1, Vin_max=1, num_points=100):
    """
    仿真同相放大器的输入输出特性

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
    gain = non_inverting_amplifier_gain(Rf, Rin)
    Vout_array = gain * Vin_array
    return Vin_array, Vout_array

def plot_non_inverting_vs_inverting(Rf, Rin):
    """
    比较同相放大器和反相放大器的特性
    """
    # 同相放大器
    Vin_non, Vout_non = simulate_non_inverting_amplifier(Rf, Rin)
    gain_non = non_inverting_amplifier_gain(Rf, Rin)

    # 反相放大器
    from code.examples.example_01 import simulate_inverting_amplifier, inverting_amplifier_gain
    Vin_inv, Vout_inv = simulate_inverting_amplifier(Rf, Rin)
    gain_inv = inverting_amplifier_gain(Rf, Rin)

    plt.figure(figsize=(12, 5))

    # 同相放大器子图
    plt.subplot(1, 2, 1)
    plt.plot(Vin_non, Vout_non, 'g-', linewidth=2, label=f'同相增益 = {gain_non:.1f}')
    plt.xlabel('输入电压 Vin (V)')
    plt.ylabel('输出电压 Vout (V)')
    plt.title('同相放大器')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)

    # 反相放大器子图
    plt.subplot(1, 2, 2)
    plt.plot(Vin_inv, Vout_inv, 'b-', linewidth=2, label=f'反相增益 = {gain_inv:.1f}')
    plt.xlabel('输入电压 Vin (V)')
    plt.ylabel('输出电压 Vout (V)')
    plt.title('反相放大器')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)

    plt.tight_layout()
    plt.show()

def demonstrate_voltage_follower():
    """
    演示电压跟随器的特性
    """
    Vin = np.linspace(-2, 2, 100)
    Vout = voltage_follower() * Vin

    plt.figure(figsize=(8, 6))
    plt.plot(Vin, Vout, 'r-', linewidth=2, label='电压跟随器 (增益 = 1)')
    plt.plot(Vin, Vin, 'k--', alpha=0.5, label='理想跟随线')
    plt.xlabel('输入电压 Vin (V)')
    plt.ylabel('输出电压 Vout (V)')
    plt.title('电压跟随器特性')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)
    plt.show()

if __name__ == "__main__":
    # 示例参数
    R_feedback = 8000   # 8kΩ 反馈电阻
    R_input = 2000      # 2kΩ 输入电阻

    # 计算同相放大器增益
    gain_non_inv = non_inverting_amplifier_gain(R_feedback, R_input)
    print(f"同相放大器增益: {gain_non_inv:.1f}")
    print(f"这意味着输入信号会被放大 {gain_non_inv:.1f} 倍且保持同相")

    # 电压跟随器
    gain_follower = voltage_follower()
    print(f"电压跟随器增益: {gain_follower:.1f}")

    # 演示电压跟随器
    demonstrate_voltage_follower()