#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：FFT多项式乘法完整实现
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

def fft_recursive(a, invert=False):
    n = len(a)
    if n == 1:
        return a

    a0 = [a[i] for i in range(0, n, 2)]
    a1 = [a[i] for i in range(1, n, 2)]

    y0 = fft_recursive(a0, invert)
    y1 = fft_recursive(a1, invert)

    y = [Complex() for _ in range(n)]
    angle = 2 * math.pi / n
    if invert:
        angle = -angle

    w = Complex(1, 0)
    wn = Complex(math.cos(angle), math.sin(angle))

    for i in range(n // 2):
        y[i] = y0[i] + w * y1[i]
        y[i + n // 2] = y0[i] - w * y1[i]
        if invert:
            y[i].real /= 2
            y[i].imag /= 2
            y[i + n // 2].real /= 2
            y[i + n // 2].imag /= 2
        w = w * wn

    return y

def polynomial_multiply_fft(poly1, poly2):
    """使用FFT进行多项式乘法"""
    # 转换为复数
    a = [Complex(coeff, 0) for coeff in poly1]
    b = [Complex(coeff, 0) for coeff in poly2]

    # 确定结果长度
    result_len = len(poly1) + len(poly2) - 1
    n = 1
    while n < result_len:
        n <<= 1
    n <<= 1

    # 补零
    while len(a) < n:
        a.append(Complex(0, 0))
    while len(b) < n:
        b.append(Complex(0, 0))

    # FFT变换
    fa = fft_recursive(a)
    fb = fft_recursive(b)

    # 点值相乘
    for i in range(n):
        fa[i] = fa[i] * fb[i]

    # 逆FFT
    result = fft_recursive(fa, invert=True)

    # 提取实部
    coeffs = []
    for i in range(result_len):
        coeffs.append(round(result[i].real))

    return coeffs

def solve_fft_polynomial_multiplication(poly1, poly2):
    """解决FFT多项式乘法问题"""
    return polynomial_multiply_fft(poly1, poly2)

# 测试用例
if __name__ == "__main__":
    poly1 = [1, 2, 3]
    poly2 = [4, 5, 6]
    result = solve_fft_polynomial_multiplication(poly1, poly2)
    print(f"结果: {result}")