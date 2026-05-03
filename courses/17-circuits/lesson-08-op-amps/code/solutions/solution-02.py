#!/usr/bin/env python3
"""
运算放大器解决方案 2: 同相放大器与电压跟随器

完整实现同相放大器和电压跟随器的仿真与比较。
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

def voltage_follower_gain():
    """
    电压跟随器的增益
    """
    return 1.0

def simulate_non_inverting_amplifier(Rf, Rin, Vin_range=(-1.5, 1.5)):
    """
    仿真同相放大器
    """
    Vin = np.linspace(Vin_range[0], Vin_range[1], 200)
    gain = non_inverting_amplifier_gain(Rf, Rin)
    Vout = gain * Vin
    return Vin, Vout, gain

def simulate_voltage_follower(Vin_range=(-2, 2)):
    """
    仿真电压跟随器
    """
    Vin = np.linspace(Vin_range[0], Vin_range[1], 200)
    gain = voltage_follower_gain()
    Vout = gain * Vin
    return Vin, Vout, gain

def compare_amplifier_types():
    """
    全面对比反相、同相放大器和电压跟随器
    """
    # 参数设置
    Rf = 9000   # 9kΩ
    Rin = 1000  # 1kΩ

    # 反相放大器
    Vin_inv = np.linspace(-1, 1, 200)
    gain_inv = -Rf / Rin
    Vout_inv = gain_inv * Vin_inv

    # 同相放大器
    Vin_non = np.linspace(-1, 1, 200)
    gain_non = 1 + Rf / Rin
    Vout_non = gain_non * Vin_non

    # 电压跟随器
    Vin_fol = np.linspace(-2, 2, 200)
    gain_fol = 1.0
    Vout_fol = gain_fol * Vin_fol

    # 绘图
    plt.figure(figsize=(15, 5))

    # 反相放大器
    plt.subplot(1, 3, 1)
    plt.plot(Vin_inv, Vout_inv, 'b-', linewidth=2, label=f'增益 = {gain_inv:.1f}')
    plt.xlabel('Vin (V)')
    plt.ylabel('Vout (V)')
    plt.title('反相放大器')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)

    # 同相放大器
    plt.subplot(1, 3, 2)
    plt.plot(Vin_non, Vout_non, 'g-', linewidth=2, label=f'增益 = {gain_non:.1f}')
    plt.xlabel('Vin (V)')
    plt.ylabel('Vout (V)')
    plt.title('同相放大器')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)

    # 电压跟随器
    plt.subplot(1, 3, 3)
    plt.plot(Vin_fol, Vout_fol, 'r-', linewidth=2, label=f'增益 = {gain_fol:.1f}')
    plt.plot(Vin_fol, Vin_fol, 'k--', alpha=0.5)
    plt.xlabel('Vin (V)')
    plt.ylabel('Vout (V)')
    plt.title('电压跟随器')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)

    plt.tight_layout()
    plt.show()

    # 打印分析结果
    print("=== 放大器类型比较 ===")
    print(f"反相放大器: 增益 = {gain_inv:.1f}, 输入阻抗 ≈ {Rin/1000:.0f}kΩ")
    print(f"同相放大器: 增益 = {gain_non:.1f}, 输入阻抗 ≈ 非常高 (理想情况下无穷大)")
    print(f"电压跟随器: 增益 = {gain_fol:.1f}, 输入阻抗 ≈ 非常高, 输出阻抗 ≈ 0")

if __name__ == "__main__":
    print("同相放大器示例:")
    R_feedback = 8000
    R_input = 2000
    gain = non_inverting_amplifier_gain(R_feedback, R_input)
    print(f"Rf = {R_feedback/1000:.0f}kΩ, Rin = {R_input/1000:.0f}kΩ")
    print(f"同相放大器增益 = {gain:.1f}")

    print("\n电压跟随器示例:")
    gain_follower = voltage_follower_gain()
    print(f"电压跟随器增益 = {gain_follower:.1f}")

    print("\n显示三种放大器类型的比较...")
    compare_amplifier_types()