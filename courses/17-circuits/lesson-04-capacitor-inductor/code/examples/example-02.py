#!/usr/bin/env python3
"""
RL电路放电过程模拟
演示电感放电时电流和电压随时间的变化
"""

import numpy as np
import matplotlib.pyplot as plt

# 电路参数
R = 100     # 电阻值 (欧姆)
L = 0.1     # 电感值 (亨利)
I0 = 0.05   # 初始电流 (安培)

# 计算时间常数
tau = L / R
print(f"时间常数 τ = {tau:.6f} 秒 = {tau*1000:.3f} 毫秒")

# 时间轴 - 从0到5τ
t = np.linspace(0, 5*tau, 1000)

# RL放电公式
I = I0 * np.exp(-t/tau)         # 电感电流
V = -I0 * R * np.exp(-t/tau)    # 电感电压（负号表示反向电动势）

# 创建图表
plt.figure(figsize=(12, 8))

# 电流子图
plt.subplot(2, 1, 1)
plt.plot(t*1000, I*1000, 'b-', linewidth=2, label='电感电流 I(t)')
plt.axvline(x=tau*1000, color='g', linestyle=':', alpha=0.7, label=f'τ = {tau*1000:.1f} ms')
plt.grid(True, alpha=0.3)
plt.xlabel('时间 (毫秒)')
plt.ylabel('电流 (毫安)')
plt.title('RL电路放电过程 - 电感电流')
plt.legend()
plt.ylim(0, I0*1000*1.1)

# 电压子图
plt.subplot(2, 1, 2)
plt.plot(t*1000, V, 'red', linewidth=2, label='电感电压 V(t)')
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=tau*1000, color='g', linestyle=':', alpha=0.7, label=f'τ = {tau*1000:.1f} ms')
plt.grid(True, alpha=0.3)
plt.xlabel('时间 (毫秒)')
plt.ylabel('电压 (伏特)')
plt.title('RL电路放电过程 - 电感电压（反向电动势）')
plt.legend()
plt.ylim(V[0]*1.1, 0)

plt.tight_layout()
plt.show()

# 打印一些关键点的值
print(f"\n关键时间点的电流值:")
print(f"t = 0:     I = {I[0]:.3f} A ({I[0]/I0*100:.1f}%)")
print(f"t = τ:     I = {I0*np.exp(-1):.3f} A ({np.exp(-1)*100:.1f}%)")
print(f"t = 2τ:    I = {I0*np.exp(-2):.3f} A ({np.exp(-2)*100:.1f}%)")
print(f"t = 5τ:    I = {I0*np.exp(-5):.3f} A ({np.exp(-5)*100:.1f}%)")

print(f"\n初始反向电动势: {abs(V[0]):.2f} V")