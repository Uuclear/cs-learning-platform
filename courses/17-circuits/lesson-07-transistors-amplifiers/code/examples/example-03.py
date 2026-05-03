#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频放大器增益与频率响应仿真
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def audio_amplifier_response(frequencies, Av_mid=50, f_low=20, f_high=20000):
    """
    模拟音频放大器的频率响应

    参数:
    frequencies: 频率数组 (Hz)
    Av_mid: 中频增益
    f_low: 低频截止频率 (Hz)
    f_high: 高频截止频率 (Hz)

    返回:
    gain_db: 增益 (dB)
    phase_deg: 相位 (度)
    """
    # 创建二阶带通滤波器来模拟放大器频率响应
    # 低频部分 (高通特性)
    b_low, a_low = signal.butter(1, f_low, btype='high', fs=100000)

    # 高频部分 (低通特性)
    b_high, a_high = signal.butter(1, f_high, btype='low', fs=100000)

    # 组合响应
    w = 2 * np.pi * frequencies
    H_low = np.polyval(b_low[::-1], np.exp(1j*w/50000)) / np.polyval(a_low[::-1], np.exp(1j*w/50000))
    H_high = np.polyval(b_high[::-1], np.exp(1j*w/50000)) / np.polyval(a_high[::-1], np.exp(1j*w/50000))

    H_total = Av_mid * H_low * H_high

    gain_db = 20 * np.log10(np.abs(H_total))
    phase_deg = np.angle(H_total, deg=True)

    return gain_db, phase_deg

def simulate_distortion(input_signal, max_output=5.0):
    """
    模拟放大器的削波失真
    """
    # 简单的硬限幅失真模型
    distorted = np.clip(input_signal, -max_output, max_output)
    return distorted

def main():
    # 频率响应分析
    frequencies = np.logspace(1, 5, 1000)  # 10Hz 到 100kHz
    gain_db, phase_deg = audio_amplifier_response(frequencies)

    plt.figure(figsize=(15, 10))

    # 增益响应
    plt.subplot(2, 2, 1)
    plt.semilogx(frequencies, gain_db)
    plt.xlabel('频率 (Hz)')
    plt.ylabel('增益 (dB)')
    plt.title('音频放大器频率响应 - 增益')
    plt.grid(True, which="both", ls="-", alpha=0.3)
    plt.axvline(x=20, color='r', linestyle='--', alpha=0.7, label='20 Hz')
    plt.axvline(x=20000, color='r', linestyle='--', alpha=0.7, label='20 kHz')
    plt.legend()

    # 相位响应
    plt.subplot(2, 2, 2)
    plt.semilogx(frequencies, phase_deg)
    plt.xlabel('频率 (Hz)')
    plt.ylabel('相位 (度)')
    plt.title('音频放大器频率响应 - 相位')
    plt.grid(True, which="both", ls="-", alpha=0.3)

    # 时域信号失真演示
    t = np.linspace(0, 0.01, 1000)  # 10ms
    input_freq = 1000  # 1kHz 测试信号
    input_signal = 8 * np.sin(2 * np.pi * input_freq * t)  # 8V 输入信号
    output_signal = simulate_distortion(input_signal, max_output=5.0)

    plt.subplot(2, 1, 2)
    plt.plot(t*1000, input_signal, 'b-', alpha=0.7, label='输入信号 (8V)')
    plt.plot(t*1000, output_signal, 'r-', alpha=0.9, label='输出信号 (限幅到 ±5V)')
    plt.xlabel('时间 (ms)')
    plt.ylabel('电压 (V)')
    plt.title('放大器削波失真演示')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 5)

    plt.tight_layout()
    plt.show()

    # 计算总谐波失真 (THD) 的简单估计
    from scipy.fft import fft, fftfreq

    N = len(output_signal)
    yf = fft(output_signal)
    xf = fftfreq(N, t[1]-t[0])

    # 找到基频分量
    fundamental_idx = np.argmax(np.abs(yf[:N//2]))
    fundamental_mag = np.abs(yf[fundamental_idx])

    # 计算谐波分量 (2次、3次等)
    harmonic_mags = []
    for harmonic in range(2, 6):
        harmonic_idx = fundamental_idx * harmonic
        if harmonic_idx < N//2:
            harmonic_mags.append(np.abs(yf[harmonic_idx]))

    if harmonic_mags:
        thd = np.sqrt(sum(mag**2 for mag in harmonic_mags)) / fundamental_mag
        print(f"估计的总谐波失真 (THD): {thd*100:.2f}%")
    else:
        print("无法计算 THD - 谐波分量超出范围")

if __name__ == "__main__":
    main()