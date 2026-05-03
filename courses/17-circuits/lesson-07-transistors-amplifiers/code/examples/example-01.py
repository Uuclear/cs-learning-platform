#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三极管传输特性曲线绘制
展示基极电流 Ib 与集电极电流 Ic 的关系
"""

import numpy as np
import matplotlib.pyplot as plt

def bjt_transfer_characteristic(Vbe, beta=100, Is=1e-15):
    """
    计算三极管传输特性

    参数:
    Vbe: 基极-发射极电压 (V)
    beta: 电流放大系数
    Is: 反向饱和电流 (A)

    返回:
    Ib: 基极电流 (A)
    Ic: 集电极电流 (A)
    """
    # 使用肖克利方程计算基极电流
    VT = 0.026  # 热电压 (26mV at room temperature)
    Ib = Is * (np.exp(Vbe / VT) - 1)
    Ic = beta * Ib
    return Ib, Ic

def main():
    # 生成 Vbe 范围 (-0.2V 到 0.8V)
    Vbe_range = np.linspace(-0.2, 0.8, 1000)

    # 计算不同 beta 值下的特性曲线
    betas = [50, 100, 200]

    plt.figure(figsize=(12, 8))

    # 绘制 Ib-Vbe 曲线
    plt.subplot(2, 1, 1)
    for beta in betas:
        Ib, Ic = bjt_transfer_characteristic(Vbe_range, beta=beta)
        plt.plot(Vbe_range, Ib * 1e6, label=f'β={beta}')  # 转换为 μA

    plt.xlabel('基极-发射极电压 Vbe (V)')
    plt.ylabel('基极电流 Ib (μA)')
    plt.title('三极管输入特性曲线')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(-0.2, 0.8)

    # 绘制 Ic-Ib 曲线 (传输特性)
    plt.subplot(2, 1, 2)
    Ib_test = np.linspace(0, 50e-6, 100)  # 0 到 50 μA

    for beta in betas:
        Ic_test = beta * Ib_test
        plt.plot(Ib_test * 1e6, Ic_test * 1e3, label=f'β={beta}')  # Ib: μA, Ic: mA

    plt.xlabel('基极电流 Ib (μA)')
    plt.ylabel('集电极电流 Ic (mA)')
    plt.title('三极管传输特性曲线')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()