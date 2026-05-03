#!/usr/bin/env python3
"""
RC低通滤波器频率响应分析 - 解决方案
演示不同频率下RC滤波器的输出特性
"""

import numpy as np
import matplotlib.pyplot as plt

def rc_lowpass_analysis(R=1000, C=1e-6):
    """
    分析RC低通滤波器的频率响应

    参数:
    R: 电阻值 (欧姆)
    C: 电容值 (法拉)
    """
    # 计算截止频率和时间常数
    fc = 1 / (2 * np.pi * R * C)
    tau = R * C
    print(f"截止频率 fc = {fc:.2f} Hz")
    print(f"时间常数 τ = {tau*1000:.3f} ms")

    # 频率范围 - 从0.1*fc到10*fc
    f = np.logspace(np.log10(0.1*fc), np.log10(10*fc), 1000)

    # RC低通滤波器传递函数
    omega = 2 * np.pi * f
    H = 1 / (1 + 1j * omega * R * C)

    # 幅度和相位
    magnitude = np.abs(H)
    phase = np.angle(H, deg=True)

    # 创建频域响应图表
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

    # 演示时域响应对比
    print(f"\n演示不同频率的时域响应:")

    # 创建时间轴
    t = np.linspace(0, 0.01, 1000)  # 10ms

    # 输入信号频率
    f_input_low = fc / 10   # 低频输入
    f_input_high = fc * 10  # 高频输入

    # 输入信号
    vin_low = np.sin(2 * np.pi * f_input_low * t)
    vin_high = np.sin(2 * np.pi * f_input_high * t)

    # 输出信号
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
    plt.title(f'低频输入 ({f_input_low:.1f} Hz) - 信号基本通过')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(t*1000, vin_high, 'b--', alpha=0.7, label='输入信号')
    plt.plot(t*1000, vout_high, 'r-', linewidth=2, label='输出信号')
    plt.grid(True, alpha=0.3)
    plt.xlabel('时间 (毫秒)')
    plt.ylabel('电压 (V)')
    plt.title(f'高频输入 ({f_input_high:.0f} Hz) - 信号被衰减')
    plt.legend()

    plt.tight_layout()
    plt.show()

    # 打印衰减信息
    print(f"低频 ({f_input_low:.1f} Hz) 衰减: {20*np.log10(np.abs(H_low)):.2f} dB")
    print(f"高频 ({f_input_high:.0f} Hz) 衰减: {20*np.log10(np.abs(H_high)):.2f} dB")

    # 设计指导
    print(f"\n设计指导:")
    print(f"要设计截止频率为 f_c 的低通滤波器，可以选择:")
    print(f"- 固定 R，计算 C = 1/(2π × f_c × R)")
    print(f"- 固定 C，计算 R = 1/(2π × f_c × C)")
    print(f"实际选择时需考虑元件的标准值和实际应用需求")

if __name__ == "__main__":
    # 默认参数运行
    rc_lowpass_analysis()

    # 设计特定截止频率的滤波器
    print("\n" + "="*50)
    print("设计截止频率为 1kHz 的低通滤波器:")
    target_fc = 1000  # 1kHz
    C_design = 1e-6   # 1μF
    R_design = 1 / (2 * np.pi * target_fc * C_design)
    print(f"选择 C = {C_design*1e6:.0f} μF，则 R = {R_design:.0f} Ω")
    rc_lowpass_analysis(R=R_design, C=C_design)