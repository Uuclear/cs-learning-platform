#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：信号处理FFT应用完整实现
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
    n = len(a)

    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

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
    samples = []
    for t in range(int(sample_rate * duration)):
        value = math.sin(2 * math.pi * freq * t / sample_rate)
        samples.append(value)
    return samples

def compute_spectrum(signal, sample_rate):
    """计算信号频谱并识别主要频率"""
    n = len(signal)
    power_of_2 = 1
    while power_of_2 < n:
        power_of_2 <<= 1

    complex_signal = [Complex(val, 0) for val in signal]
    while len(complex_signal) < power_of_2:
        complex_signal.append(Complex(0, 0))

    fft_result = fft_iterative(complex_signal)

    magnitude = []
    for i in range(power_of_2 // 2):
        mag = math.sqrt(fft_result[i].real**2 + fft_result[i].imag**2)
        magnitude.append(mag)

    # 找峰值
    peaks = []
    for i in range(1, len(magnitude)-1):
        if magnitude[i] > magnitude[i-1] and magnitude[i] > magnitude[i+1]:
            freq = i * sample_rate / power_of_2
            peaks.append((freq, magnitude[i]))

    peaks.sort(key=lambda x: x[1], reverse=True)
    return magnitude, peaks[:3]

def solve_signal_processing(signal, sample_rate):
    """解决信号处理问题"""
    return compute_spectrum(signal, sample_rate)

# 测试用例
if __name__ == "__main__":
    sample_rate = 1000
    signal = generate_sine_wave(50, sample_rate, 1.0)
    spectrum, peaks = solve_signal_processing(signal, sample_rate)
    print(f"主要频率: {[f'{freq:.1f}Hz' for freq, _ in peaks]}")