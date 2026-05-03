#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：FFT基础实现与多项式乘法
演示递归和迭代FFT算法以及多项式乘法应用
"""

import math
import cmath

class Complex:
    """复数类，用于FFT计算"""
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

    def __repr__(self):
        if self.imag >= 0:
            return f"{self.real:.3f}+{self.imag:.3f}i"
        else:
            return f"{self.real:.3f}{self.imag:.3f}i"

def fft_recursive(a, invert=False):
    """
    递归FFT实现

    参数:
        a: Complex对象列表，表示多项式系数
        invert: 是否计算逆FFT

    返回:
        Complex对象列表，表示DFT结果
    """
    n = len(a)
    if n == 1:
        return a

    # 分离奇偶系数
    a0 = [a[i] for i in range(0, n, 2)]
    a1 = [a[i] for i in range(1, n, 2)]

    # 递归计算
    y0 = fft_recursive(a0, invert)
    y1 = fft_recursive(a1, invert)

    # 合并结果
    y = [Complex() for _ in range(n)]
    angle = 2 * math.pi / n
    if invert:
        angle = -angle

    w = Complex(1, 0)  # 初始单位根
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
    """
    使用FFT进行多项式乘法

    参数:
        poly1, poly2: 系数列表（实数）

    返回:
        结果多项式的系数列表
    """
    # 转换为复数
    a = [Complex(coeff, 0) for coeff in poly1]
    b = [Complex(coeff, 0) for coeff in poly2]

    # 确定结果长度（至少 len1 + len2 - 1）
    result_len = len(poly1) + len(poly2) - 1
    # 扩展到2的幂
    n = 1
    while n < result_len:
        n <<= 1
    n <<= 1  # 再扩展一次确保足够

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

    # 提取实部并四舍五入
    coeffs = []
    for i in range(result_len):
        coeffs.append(round(result[i].real))

    return coeffs

def main():
    """主函数：演示FFT和多项式乘法"""
    print("FFT示例1：基础实现与多项式乘法")
    print("=" * 40)

    # 测试多项式乘法
    poly1 = [1, 2, 3]  # 1 + 2x + 3x²
    poly2 = [4, 5, 6]  # 4 + 5x + 6x²

    print(f"多项式1: {poly1}")
    print(f"多项式2: {poly2}")

    result = polynomial_multiply_fft(poly1, poly2)
    print(f"乘积结果: {result}")
    print("预期结果: [4, 13, 28, 27, 18] (因为 (1+2x+3x²)(4+5x+6x²) = 4+13x+28x²+27x³+18x⁴)")

    # 验证结果
    expected = [4, 13, 28, 27, 18]
    if result == expected:
        print("✓ 结果正确！")
    else:
        print("✗ 结果错误！")

    # 测试小规模FFT
    test_poly = [1, 1, 1, 1]  # 常数多项式
    test_complex = [Complex(coeff, 0) for coeff in test_poly]
    fft_result = fft_recursive(test_complex)
    print(f"\n测试多项式 [1,1,1,1] 的FFT结果:")
    for i, val in enumerate(fft_result):
        print(f"  F[{i}] = {val}")

if __name__ == "__main__":
    main()