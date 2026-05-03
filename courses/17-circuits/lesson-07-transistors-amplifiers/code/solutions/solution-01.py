#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三极管传输特性曲线绘制 - 完整解决方案
展示基极电流 Ib 与集电极电流 Ic 的关系，包括饱和区和截止区
"""

import numpy as np
import matplotlib.pyplot as plt

def bjt_complete_characteristic(Vbe, Vce, beta=100, Is=1e-15, Vce_sat=0.2):
    """
    计算三极管完整特性曲线（包括放大区、饱和区、截止区）

    参数:
    Vbe: 基极-发射极电压 (V)
    Vce: 集电极-发射极电压 (V)
    beta: 电流放大系数
    Is: 反向饱和电流 (A)
    Vce_sat: 饱和电压 (V)

    返回:
    Ib: 基极电流 (A)
    Ic: 集电极电流 (A)
    region: 工作区域 ('cutoff', 'active', 'saturation')
    """
    VT = 0.026  # 热电压

    # 截止区判断
    if Vbe <= 0.5:
        Ib = 0
        Ic = 0
        region = 'cutoff'
    # 饱和区判断
    elif Vce <= Vce_sat:
        Ib = Is * (np.exp(Vbe / VT) - 1)
        # 饱和区的 Ic 受 Vce 限制
        Ic_sat_max = (Vce / Vce_sat) * beta * Ib
        Ic = min(beta * Ib, Ic_sat_max)
        region = 'saturation'
    # 放大区
    else:
        Ib = Is * (np.exp(Vbe / VT) - 1)
        Ic = beta * Ib
        region = 'active'

    return Ib, Ic, region

def plot_output_characteristics():
    """绘制输出特性曲线 (Ic vs Vce for different Ib)"""
    Vce_range = np.linspace(0, 12, 500)
    Ib_values = [10e-6, 20e-6, 30e-6, 40e-6, 50e-6]  # 10-50 μA
    beta = 100

    plt.figure(figsize=(12, 8))

    for Ib in Ib_values:
        Ic_values = []
        regions = []

        for Vce in Vce_range:
            # 在放大区，Ic ≈ β * Ib
            if Vce > 0.2:
                Ic = beta * Ib
            else:
                # 饱和区，Ic 随 Vce 变化
                Ic = beta * Ib * (Vce / 0.2) if Vce > 0 else 0

            Ic_values.append(Ic)
            regions.append('active' if Vce > 0.2 else 'saturation')

        plt.plot(Vce_range, np.array(Ic_values)*1e3,
                label=f'Ib = {Ib*1e6:.0f} μA')

    plt.xlabel('集电极-发射极电压 Vce (V)')
    plt.ylabel('集电极电流 Ic (mA)')
    plt.title('三极管输出特性曲线')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 12)
    plt.ylim(0, 6)

def main():
    # 生成 Vbe 范围
    Vbe_range = np.linspace(0, 0.8, 200)
    Vce_test = 5.0  # 测试时的 Vce

    plt.figure(figsize=(15, 10))

    # 输入特性曲线
    plt.subplot(2, 2, 1)
    Ib_vals = []
    for Vbe in Vbe_range:
        Ib, Ic, region = bjt_complete_characteristic(Vbe, Vce_test)
        Ib_vals.append(Ib)

    plt.plot(Vbe_range, np.array(Ib_vals)*1e6)
    plt.xlabel('Vbe (V)')
    plt.ylabel('Ib (μA)')
    plt.title('输入特性曲线')
    plt.grid(True, alpha=0.3)

    # 传输特性曲线
    plt.subplot(2, 2, 2)
    Ic_vals = beta * np.array(Ib_vals)
    plt.plot(np.array(Ib_vals)*1e6, Ic_vals*1e3)
    plt.xlabel('Ib (μA)')
    plt.ylabel('Ic (mA)')
    plt.title('传输特性曲线')
    plt.grid(True, alpha=0.3)

    # 输出特性曲线
    plt.subplot(2, 1, 2)
    plot_output_characteristics()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()