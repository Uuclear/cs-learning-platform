#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：迭代FFT完整实现
"""

import math

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

def solve_iterative_fft(signal):
    """解决迭代FFT问题"""
    # 转换为复数
    complex_signal = [Complex(val, 0) for val in signal]

    # 扩展到2的幂
    n = len(complex_signal)
    power_of_2 = 1
    while power_of_2 < n:
        power_of_2 <<= 1

    while len(complex_signal) < power_of_2:
        complex_signal.append(Complex(0, 0))

    # FFT
    result = fft_iterative(complex_signal)

    # 返回幅度谱
    magnitude = []
    for i in range(power_of_2 // 2):
        mag = math.sqrt(result[i].real**2 + result[i].imag**2)
        magnitude.append(mag)

    return magnitude

# 测试用例
if __name__ == "__main__":
    signal = [1, 1, 1, 1]
    spectrum = solve_iterative_fft(signal)
    print(f"频谱: {spectrum}")