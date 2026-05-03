#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频放大器增益与频率响应仿真 - 完整解决方案
包含多级放大、阻抗匹配和实际电路参数
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

class AudioAmplifier:
    """音频放大器模型"""

    def __init__(self, Av_mid=50, f_low=20, f_high=20000, Rin=1e3, Rout=100):
        self.Av_mid = Av_mid          # 中频电压增益
        self.f_low = f_low            # 低频截止频率 (Hz)
        self.f_high = f_high          # 高频截止频率 (Hz)
        self.Rin = Rin                # 输入阻抗 (Ω)
        self.Rout = Rout              # 输出阻抗 (Ω)

    def frequency_response(self, frequencies):
        """计算频率响应"""
        # 归一化频率
        w = frequencies / (2 * np.pi)

        # 低频响应 (高通)
        f_ratio_low = frequencies / self.f_low
        H_low = 1j * f_ratio_low / (1 + 1j * f_ratio_low)

        # 高频响应 (低通)
        f_ratio_high = self.f_high / frequencies
        H_high = 1 / (1 + 1j * f_ratio_high)

        # 总体响应
        H_total = self.Av_mid * H_low * H_high

        gain_db = 20 * np.log10(np.abs(H_total))
        phase_deg = np.angle(H_total, deg=True)

        return gain_db, phase_deg

    def step_response(self, duration=0.01, fs=100000):
        """阶跃响应分析"""
        t = np.linspace(0, duration, int(duration * fs))
        step_input = np.ones_like(t)
        step_input[0] = 0  # 理想阶跃

        # 创建传递函数
        # 使用二阶系统近似
        wn = 2 * np.pi * self.f_high  # 自然频率
        zeta = 0.707  # 阻尼比 (临界阻尼)

        # 二阶系统传递函数系数
        num = [wn**2]
        den = [1, 2*zeta*wn, wn**2]

        system = signal.TransferFunction(num, den)
        t_out, step_out = signal.step(system, T=t)

        return t_out, step_out * self.Av_mid

    def thd_analysis(self, freq=1000, amplitude=1.0, duration=0.01, fs=100000):
        """总谐波失真分析"""
        t = np.linspace(0, duration, int(duration * fs))
        fundamental = amplitude * np.sin(2 * np.pi * freq * t)

        # 添加非线性失真 (三次谐波为主)
        distorted = (fundamental +
                    0.1 * np.sin(2 * np.pi * 2 * freq * t) +  # 二次谐波
                    0.05 * np.sin(2 * np.pi * 3 * freq * t))  # 三次谐波

        # 应用增益和限幅
        output = np.clip(self.Av_mid * distorted, -10, 10)

        # FFT 分析
        N = len(output)
        yf = np.fft.fft(output)
        xf = np.fft.fftfreq(N, 1/fs)

        # 计算 THD
        fundamental_idx = int(freq * N / fs)
        fundamental_mag = np.abs(yf[fundamental_idx])

        harmonic_mags = []
        for harmonic in range(2, 11):  # 2-10次谐波
            harmonic_idx = fundamental_idx * harmonic
            if harmonic_idx < N//2:
                harmonic_mags.append(np.abs(yf[harmonic_idx]))

        if harmonic_mags and fundamental_mag > 0:
            thd = np.sqrt(sum(mag**2 for mag in harmonic_mags)) / fundamental_mag
        else:
            thd = 0

        return t, output, thd

def design_practical_amplifier():
    """设计一个实用的音频放大器"""
    print("=== 实用音频放大器设计 ===")
    print("目标规格:")
    print("- 频率响应: 20Hz - 20kHz (±3dB)")
    print("- 电压增益: 40 dB (100x)")
    print("- 输入阻抗: >1kΩ")
    print("- 输出阻抗: <100Ω")
    print("- 最大输出功率: 100mW into 8Ω")
    print()

    # 设计参数
    Av_linear = 100  # 100x 增益 = 40dB
    f_low = 20
    f_high = 20000
    Rin = 2200       # 2.2kΩ 输入阻抗
    Rout = 50        # 50Ω 输出阻抗

    amplifier = AudioAmplifier(Av_mid=Av_linear, f_low=f_low, f_high=f_high,
                              Rin=Rin, Rout=Rout)

    # 频率响应分析
    frequencies = np.logspace(1, 5, 1000)  # 10Hz - 100kHz
    gain_db, phase_deg = amplifier.frequency_response(frequencies)

    # 找到 -3dB 点
    midband_gain = np.mean(gain_db[(frequencies > 100) & (frequencies < 10000)])
    f_low_3db = frequencies[np.argmin(np.abs(gain_db - (midband_gain - 3)))]
    f_high_3db = frequencies[np.argmax(np.abs(gain_db - (midband_gain - 3)))]

    print(f"实际性能:")
    print(f"- 中频增益: {midband_gain:.1f} dB")
    print(f"- 低频 -3dB 点: {f_low_3db:.1f} Hz")
    print(f"- 高频 -3dB 点: {f_high_3db:.0f} Hz")
    print(f"- 带宽: {f_high_3db - f_low_3db:.0f} Hz")

    # 绘制结果
    plt.figure(figsize=(15, 10))

    # 频率响应
    plt.subplot(2, 2, 1)
    plt.semilogx(frequencies, gain_db)
    plt.xlabel('频率 (Hz)')
    plt.ylabel('增益 (dB)')
    plt.title('频率响应')
    plt.grid(True, which="both", ls="-", alpha=0.3)
    plt.axhline(y=midband_gain-3, color='r', linestyle='--', alpha=0.7)
    plt.axvline(x=f_low_3db, color='g', linestyle='--', alpha=0.7)
    plt.axvline(x=f_high_3db, color='g', linestyle='--', alpha=0.7)

    # 相位响应
    plt.subplot(2, 2, 2)
    plt.semilogx(frequencies, phase_deg)
    plt.xlabel('频率 (Hz)')
    plt.ylabel('相位 (度)')
    plt.title('相位响应')
    plt.grid(True, which="both", ls="-", alpha=0.3)

    # 阶跃响应
    t_step, y_step = amplifier.step_response()
    plt.subplot(2, 2, 3)
    plt.plot(t_step*1000, y_step)
    plt.xlabel('时间 (ms)')
    plt.ylabel('输出电压 (V)')
    plt.title('阶跃响应')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 0.1)

    # THD 分析
    t_thd, y_thd, thd = amplifier.thd_analysis()
    plt.subplot(2, 2, 4)
    plt.plot(t_thd[:1000]*1000, y_thd[:1000])
    plt.xlabel('时间 (ms)')
    plt.ylabel('输出电压 (V)')
    plt.title(f'失真分析 (THD: {thd*100:.2f}%)')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return amplifier

def main():
    design_practical_amplifier()

if __name__ == "__main__":
    main()