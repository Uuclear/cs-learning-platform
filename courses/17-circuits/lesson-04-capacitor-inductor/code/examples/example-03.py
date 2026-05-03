#!/usr/bin/env python3
"""
RC低通滤波器频率响应分析
演示不同频率下RC滤波器的输出特性
"""

import numpy as np
import matplotlib.pyplot as plt

# 电路参数
R = 1000    # 电阻值 (欧姆)
C = 1e-6    # 电容值 (法拉)

# 计算截止频率
fc = 1 / (2 * np.pi * R * C)
tau = R * C
print(f"截止频率 fc = {fc:.2f} Hz")
print(f"时间常数 τ = {tau*1000:.3f} ms")

# 频率范围 - 从0.1*fc到10*fc
f = np.logspace(np.log10(0.1*fc), np.log10(10*fc), 1000)

# RC低通滤波器传递函数
# H(f) = 1 / (1 + j*2π*f*R*C)
omega = 2 * np.pi * f
H = 1 / (1 + 1j * omega * R * C)

# 幅度和相位
magnitude = np.abs(H)
phase = np.angle(H, deg=True)

# 创建图表
plt.figure(figsize=(12, 8))

# 幅频特性
plt.subplot(2, 1, 1)
plt.semilogx(f, 20*np.log10(magnitude), 'b-', linewidth=2)
plt.axvline(x=fc, color='r', linestyle='--', alpha=0.7, label=f'截止频率 = {fc:.1f} Hz')
plt.axhline(y=-3, color='g', linestyle=':', alpha=0.7, label='-3dB点')
plt.grid(True, which="both", alpha=0.3)
plt.xlabel('频率 (Hz)')
plt.ylabel('增益 (dB)')
plt.title('RC低通滤波器 - 幅频特性')
plt.legend()
plt.ylim(-40, 5)

# 相频特性
plt.subplot(2, 1, 2)
plt.semilogx(f, phase, 'orange', linewidth=2)
plt.axvline(x=fc, color='r', linestyle='--', alpha=0.7, label=f'截止频率 = {fc:.1f} Hz')
plt.grid(True, which="both", alpha=0.3)
plt.xlabel('频率 (Hz)')
plt.ylabel('相位 (度)')
plt.title('RC低通滤波器 - 相频特性')
plt.legend()
plt.ylim(-95, 5)

plt.tight_layout()
plt.show()

# 演示时域响应
print(f"\n演示不同频率的时域响应:")

# 创建时间轴
t = np.linspace(0, 0.01, 1000)  # 10ms

# 输入信号频率
f_input_low = fc / 10   # 低频输入
f_input_high = fc * 10  # 高频输入

# 输入信号
vin_low = np.sin(2 * np.pi * f_input_low * t)
vin_high = np.sin(2 * np.pi * f_input_high * t)

# 输出信号（通过卷积模拟，简化处理）
# 对于正弦输入，输出幅度按|H(f)|衰减，相位按phase(f)偏移
H_low = 1 / (1 + 1j * 2 * np.pi * f_input_low * R * C)
H_high = 1 / (1 + 1j * 2 * np.pi * f_input_high * R * C)

vout_low = np.abs(H_low) * np.sin(2 * np.pi * f_input_low * t + np.angle(H_low))
vout_high = np.abs(H_high) * np.sin(2 * np.pi * f_input_high * t + np.angle(H_high))

# 绘制时域响应对比
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(t*1000, vin_low, 'b--', alpha=0.7, label='输入信号')
plt.plot(t*1000, vout_low, 'r-', linewidth=2, label='输出信号')
plt.grid(True, alpha=0.3)
plt.xlabel('时间 (毫秒)')
plt.ylabel('电压 (V)')
plt.title(f'低频输入 ({f_input_low:.1f} Hz)')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(t*1000, vin_high, 'b--', alpha=0.7, label='输入信号')
plt.plot(t*1000, vout_high, 'r-', linewidth=2, label='输出信号')
plt.grid(True, alpha=0.3)
plt.xlabel('时间 (毫秒)')
plt.ylabel('电压 (V)')
plt.title(f'高频输入 ({f_input_high:.0f} Hz)')
plt.legend()

plt.tight_layout()
plt.show()

print(f"低频 ({f_input_low:.1f} Hz) 衰减: {20*np.log10(np.abs(H_low)):.2f} dB")
print(f"高频 ({f_input_high:.0f} Hz) 衰减: {20*np.log10(np.abs(H_high)):.2f} dB")