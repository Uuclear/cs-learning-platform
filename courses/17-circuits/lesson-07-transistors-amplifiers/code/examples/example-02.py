#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共射极放大电路静态工作点计算
"""

import numpy as np

def calculate_quiescent_point(Vcc, R1, R2, Rc, Re, beta, Vbe=0.7):
    """
    计算共射极放大电路的静态工作点 (Q-point)

    参数:
    Vcc: 电源电压 (V)
    R1, R2: 基极偏置电阻 (Ω)
    Rc: 集电极电阻 (Ω)
    Re: 发射极电阻 (Ω)
    beta: 三极管电流放大系数
    Vbe: 基极-发射极电压 (V), 默认 0.7V

    返回:
    dict: 包含 Ib, Ic, Ie, Vb, Ve, Vc, Vce 的字典
    """
    # 计算基极偏置电压
    Vb = Vcc * R2 / (R1 + R2)

    # 计算发射极电压
    Ve = Vb - Vbe

    # 计算发射极电流
    Ie = Ve / Re if Re > 0 else 0

    # 计算集电极电流 (近似等于发射极电流)
    Ic = Ie * beta / (beta + 1)

    # 计算基极电流
    Ib = Ic / beta

    # 计算集电极电压
    Vc = Vcc - Ic * Rc

    # 计算集电极-发射极电压
    Vce = Vc - Ve

    return {
        'Ib': Ib,
        'Ic': Ic,
        'Ie': Ie,
        'Vb': Vb,
        'Ve': Ve,
        'Vc': Vc,
        'Vce': Vce
    }

def main():
    # 典型共射极放大电路参数
    Vcc = 12.0      # 电源电压 12V
    R1 = 22e3       # R1 = 22kΩ
    R2 = 4.7e3      # R2 = 4.7kΩ
    Rc = 2.2e3      # Rc = 2.2kΩ
    Re = 1e3        # Re = 1kΩ
    beta = 100      # β = 100

    # 计算静态工作点
    q_point = calculate_quiescent_point(Vcc, R1, R2, Rc, Re, beta)

    print("=== 共射极放大电路静态工作点计算 ===")
    print(f"电源电压 Vcc: {Vcc:.1f} V")
    print(f"偏置电阻 R1: {R1/1e3:.1f} kΩ, R2: {R2/1e3:.1f} kΩ")
    print(f"集电极电阻 Rc: {Rc/1e3:.1f} kΩ")
    print(f"发射极电阻 Re: {Re/1e3:.1f} kΩ")
    print(f"三极管 β: {beta}")
    print()
    print("静态工作点结果:")
    print(f"基极电流 Ib: {q_point['Ib']*1e6:.2f} μA")
    print(f"集电极电流 Ic: {q_point['Ic']*1e3:.2f} mA")
    print(f"发射极电流 Ie: {q_point['Ie']*1e3:.2f} mA")
    print(f"基极电压 Vb: {q_point['Vb']:.2f} V")
    print(f"发射极电压 Ve: {q_point['Ve']:.2f} V")
    print(f"集电极电压 Vc: {q_point['Vc']:.2f} V")
    print(f"集电极-发射极电压 Vce: {q_point['Vce']:.2f} V")
    print()

    # 判断工作状态
    if q_point['Vce'] < 0.2:
        state = "饱和区"
    elif q_point['Vce'] > Vcc - 1:
        state = "截止区"
    else:
        state = "放大区"

    print(f"三极管工作状态: {state}")

    # 计算电压增益 (近似)
    if Re > 0:
        Av = -Rc / Re  # 有发射极电阻时的增益
    else:
        re = 26e-3 / q_point['Ie']  # 动态发射结电阻
        Av = -Rc / re   # 无发射极电阻时的增益

    print(f"电压增益 Av: {Av:.1f}")

if __name__ == "__main__":
    main()