#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：FFT在信号处理中的应用
演示FFT在音频信号频谱分析中的应用
"""

import math
import random

class Complex:
    def __init__(self, real=0.0, imag=0.0):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        return Complex(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real
        )

def fft_iterative(a, invert=False):
    """迭代FFT实现"""
    n = len(a)

    # 位逆序置换
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    # 蝴蝶操作
    length = 2
    while length <= n:
        angle = 2 * math.pi / length
        if invert:
            angle = -angle
        wlen = Complex(math.cos(angle), math.sin(angle))

        for i in range(0, n, length):
            w = Complex(1, 0)
            for j in range(length // 2):
                u = a[i + j]
                v = a[i + j + length // 2] * w
                a[i + j] = u + v
                a[i + j + length // 2] = u - v
                w = w * wlen

        length <<= 1

    if invert:
        for i in range(n):
            a[i].real /= n
            a[i].imag /= n

    return a

def generate_sine_wave(freq, sample_rate, duration):
    """
    生成正弦波信号

    参数:
        freq: 频率(Hz)
        sample_rate: 采样率(Hz)
        duration: 持续时间(秒)

    返回:
        实数列表，表示采样点
    """
    samples = []
    for t in range(int(sample_rate * duration)):
        value = math.sin(2 * math.pi * freq * t / sample_rate)
        samples.append(value)
    return samples

def add_noise(signal, noise_level=0.1):
    """添加高斯噪声"""
    noisy_signal = []
    for value in signal:
        noise = random.gauss(0, noise_level)
        noisy_signal.append(value + noise)
    return noisy_signal

def compute_spectrum(signal):
    """
    计算信号的频谱

    返回:
        幅度谱列表
    """
    n = len(signal)
    # 扩展到2的幂
    power_of_2 = 1
    while power_of_2 < n:
        power_of_2 <<= 1

    # 补零
    complex_signal = [Complex(val, 0) for val in signal]
    while len(complex_signal) < power_of_2:
        complex_signal.append(Complex(0, 0))

    # FFT
    fft_result = fft_iterative(complex_signal)

    # 计算幅度谱
    magnitude = []
    for i in range(power_of_2 // 2):  # 只取前半部分（正频率）
        mag = math.sqrt(fft_result[i].real**2 + fft_result[i].imag**2)
        magnitude.append(mag)

    return magnitude

def find_peak_frequencies(spectrum, sample_rate, num_peaks=3):
    """
    找到频谱中的峰值频率
    """
    n = len(spectrum)
    peaks = []

    # 简单的峰值检测（找局部最大值）
    for i in range(1, n-1):
        if spectrum[i] > spectrum[i-1] and spectrum[i] > spectrum[i+1]:
            freq = i * sample_rate / (2 * n)  # 频率 = 索引 * 采样率 / FFT长度
            peaks.append((freq, spectrum[i]))

    # 按幅度排序，取前几个
    peaks.sort(key=lambda x: x[1], reverse=True)
    return peaks[:num_peaks]

def main():
    """主函数：演示FFT在信号处理中的应用"""
    print("FFT示例3：信号处理应用")
    print("=" * 40)

    # 参数设置
    sample_rate = 1000  # 1kHz采样率
    duration = 1.0      # 1秒
    freq1 = 50          # 50Hz正弦波
    freq2 = 120         # 120Hz正弦波

    print(f"生成复合信号: {freq1}Hz + {freq2}Hz")
    print(f"采样率: {sample_rate}Hz, 持续时间: {duration}秒")

    # 生成信号
    signal1 = generate_sine_wave(freq1, sample_rate, duration)
    signal2 = generate_sine_wave(freq2, sample_rate, duration)
    composite_signal = [s1 + s2 for s1, s2 in zip(signal1, signal2)]

    # 添加噪声
    noisy_signal = add_noise(composite_signal, noise_level=0.05)

    # 计算频谱
    spectrum = compute_spectrum(noisy_signal[:512])  # 取前512个样本

    # 找到峰值频率
    peaks = find_peak_frequencies(spectrum, sample_rate)

    print(f"\n检测到的峰值频率:")
    for i, (freq, magnitude) in enumerate(peaks):
        print(f"  峰值{i+1}: {freq:.1f}Hz (幅度: {magnitude:.2f})")

    # 验证结果
    detected_freqs = [freq for freq, _ in peaks]
    expected_freqs = [freq1, freq2]

    correct_detections = 0
    for expected in expected_freqs:
        for detected in detected_freqs:
            if abs(detected - expected) < 5:  # 允许5Hz误差
                correct_detections += 1
                break

    print(f"\n频率检测准确率: {correct_detections}/{len(expected_freqs)}")

    # 显示频谱信息
    max_magnitude = max(spectrum)
    dominant_freq_index = spectrum.index(max_magnitude)
    dominant_freq = dominant_freq_index * sample_rate / (2 * len(spectrum))
    print(f"主导频率: {dominant_freq:.1f}Hz")

if __name__ == "__main__":
    main()