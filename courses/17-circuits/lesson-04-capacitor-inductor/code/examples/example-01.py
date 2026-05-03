#!/usr/bin/env python3
"""
RC电路充电过程模拟
演示电容充电时电压和电流随时间的变化
"""

import numpy as np
import matplotlib.pyplot as plt

# 电路参数
R = 1000    # 电阻值 (欧姆)
C = 10e-6   # 电容值 (法拉)
V0 = 5      # 电源电压 (伏特)

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

# 打印一些关键点的值
print(f"\n关键时间点的电压值:")
print(f"t = 0:     Vc = {Vc[0]:.3f} V ({Vc[0]/V0*100:.1f}%)")
print(f"t = τ:     Vc = {V0*(1-np.exp(-1)):.3f} V ({(1-np.exp(-1))*100:.1f}%)")
print(f"t = 2τ:    Vc = {V0*(1-np.exp(-2)):.3f} V ({(1-np.exp(-2))*100:.1f}%)")
print(f"t = 5τ:    Vc = {V0*(1-np.exp(-5)):.3f} V ({(1-np.exp(-5))*100:.1f}%)")