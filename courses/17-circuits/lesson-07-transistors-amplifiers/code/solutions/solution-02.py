#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共射极放大电路静态工作点计算 - 完整解决方案
包含负载线分析和工作点稳定性分析
"""

import numpy as np
import matplotlib.pyplot as plt

def calculate_quiescent_point_detailed(Vcc, R1, R2, Rc, Re, beta, Vbe=0.7):
    """
    详细计算共射极放大电路的静态工作点，包括负载线分析
    """
    # 基极偏置网络等效
    Rb = R1 * R2 / (R1 + R2)  # 基极等效电阻
    Vbb = Vcc * R2 / (R1 + R2)  # 基极等效电压

    # 使用精确公式计算
    Ie = (Vbb - Vbe) / (Re + Rb / (beta + 1))
    Ic = beta * Ie / (beta + 1)
    Ib = Ic / beta
    Ve = Ie * Re
    Vc = Vcc - Ic * Rc
    Vce = Vc - Ve

    return {
        'Ib': Ib, 'Ic': Ic, 'Ie': Ie,
        'Vb': Vbb, 'Ve': Ve, 'Vc': Vc, 'Vce': Vce,
        'Rb': Rb, 'Vbb': Vbb
    }

def plot_load_line(Vcc, Rc, Re, q_point):
    """
    绘制直流负载线和工作点
    """
    # 负载线端点
    Ic_max = Vcc / (Rc + Re)  # Vce = 0 时的 Ic
    Vce_max = Vcc             # Ic = 0 时的 Vce

    Vce_range = np.linspace(0, Vcc, 100)
    Ic_load_line = (Vcc - Vce_range) / (Rc + Re)

    plt.figure(figsize=(10, 6))
    plt.plot(Vce_range, Ic_load_line*1e3, 'b-', linewidth=2, label='直流负载线')
    plt.plot(q_point['Vce'], q_point['Ic']*1e3, 'ro', markersize=8, label=f'Q点 ({q_point["Vce"]:.2f}V, {q_point["Ic"]*1e3:.2f}mA)')

    plt.xlabel('Vce (V)')
    plt.ylabel('Ic (mA)')
    plt.title('直流负载线与静态工作点')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, Vcc)
    plt.ylim(0, Ic_max*1e3*1.1)

def analyze_stability(beta_range, Vcc, R1, R2, Rc, Re, Vbe=0.7):
    """
    分析 β 变化对工作点稳定性的影响
    """
    Ic_values = []
    Vce_values = []

    for beta in beta_range:
        q_point = calculate_quiescent_point_detailed(Vcc, R1, R2, Rc, Re, beta, Vbe)
        Ic_values.append(q_point['Ic'])
        Vce_values.append(q_point['Vce'])

    return np.array(Ic_values), np.array(Vce_values)

def main():
    # 电路参数
    Vcc = 12.0
    R1 = 22e3
    R2 = 4.7e3
    Rc = 2.2e3
    Re = 1e3
    beta_nominal = 100

    print("=== 共射极放大电路静态工作点详细分析 ===")

    # 计算标称工作点
    q_point = calculate_quiescent_point_detailed(Vcc, R1, R2, Rc, Re, beta_nominal)
    print(f"标称 β={beta_nominal} 时的工作点:")
    print(f"Ib = {q_point['Ib']*1e6:.2f} μA")
    print(f"Ic = {q_point['Ic']*1e3:.2f} mA")
    print(f"Vce = {q_point['Vce']:.2f} V")

    # 工作区域判断
    if q_point['Vce'] < 0.2:
        region = "饱和区"
    elif q_point['Ic'] < 1e-6:
        region = "截止区"
    else:
        region = "放大区"
    print(f"工作区域: {region}")

    # 稳定性分析
    beta_range = np.linspace(50, 200, 50)
    Ic_stable, Vce_stable = analyze_stability(beta_range, Vcc, R1, R2, Rc, Re)

    print(f"\nβ 从 50 到 200 变化时:")
    print(f"Ic 变化范围: {Ic_stable.min()*1e3:.2f} - {Ic_stable.max()*1e3:.2f} mA")
    print(f"变化率: {(Ic_stable.max()-Ic_stable.min())/Ic_stable.mean()*100:.1f}%")

    # 绘制负载线
    plot_load_line(Vcc, Rc, Re, q_point)

    # 绘制稳定性分析
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(beta_range, Ic_stable*1e3)
    plt.xlabel('β')
    plt.ylabel('Ic (mA)')
    plt.title('Ic 随 β 的变化')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(beta_range, Vce_stable)
    plt.xlabel('β')
    plt.ylabel('Vce (V)')
    plt.title('Vce 随 β 的变化')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()