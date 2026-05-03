#!/usr/bin/env python3
"""
RC电路充电过程模拟 - 解决方案
演示电容充电时电压和电流随时间的变化
"""

import numpy as np
import matplotlib.pyplot as plt

def rc_charging_simulation(R=1000, C=10e-6, V0=5):
    """
    模拟RC电路充电过程

    参数:
    R: 电阻值 (欧姆)
    C: 电容值 (法拉)
    V0: 电源电压 (伏特)
    """
    # 计算时间常数
    tau = R * C
    print(f"时间常数 τ = {tau:.6f} 秒 = {tau*1000:.3f} 毫秒")

    # 时间轴 - 从0到5τ
    t = np.linspace(0, 5*tau, 1000)

    # RC充电公式
    Vc = V0 * (1 - np.exp(-t/tau))  # 电容电压
    I = (V0/R) * np.exp(-t/tau)     # 充电电流

    # 创建图表
    plt.figure(figsize=(12, 8))

    # 电压子图
    plt.subplot(2, 1, 1)
    plt.plot(t*1000, Vc, 'b-', linewidth=2, label='电容电压 Vc(t)')
    plt.axhline(y=V0, color='r', linestyle='--', alpha=0.7, label='电源电压')
    plt.axvline(x=tau*1000, color='g', linestyle=':', alpha=0.7, label=f'τ = {tau*1000:.1f} ms')
    plt.grid(True, alpha=0.3)
    plt.xlabel('时间 (毫秒)')
    plt.ylabel('电压 (伏特)')
    plt.title('RC电路充电过程 - 电容电压')
    plt.legend()
    plt.ylim(0, V0*1.1)

    # 电流子图
    plt.subplot(2, 1, 2)
    plt.plot(t*1000, I*1000, 'orange', linewidth=2, label='充电电流 I(t)')
    plt.axvline(x=tau*1000, color='g', linestyle=':', alpha=0.7, label=f'τ = {tau*1000:.1f} ms')
    plt.grid(True, alpha=0.3)
    plt.xlabel('时间 (毫秒)')
    plt.ylabel('电流 (毫安)')
    plt.title('RC电路充电过程 - 充电电流')
    plt.legend()
    plt.ylim(0, (V0/R)*1000*1.1)

    plt.tight_layout()
    plt.show()

    # 打印关键点的值
    print(f"\n关键时间点的电压值:")
    key_times = [0, 1, 2, 5]
    for n in key_times:
        if n == 0:
            vc_val = Vc[0]
        else:
            vc_val = V0 * (1 - np.exp(-n))
        percentage = vc_val / V0 * 100
        print(f"t = {n}τ:   Vc = {vc_val:.3f} V ({percentage:.1f}%)")

if __name__ == "__main__":
    # 默认参数运行
    rc_charging_simulation()

    # 可以尝试不同的参数
    print("\n" + "="*50)
    print("使用不同的参数:")
    rc_charging_simulation(R=2000, C=22e-6, V0=12)