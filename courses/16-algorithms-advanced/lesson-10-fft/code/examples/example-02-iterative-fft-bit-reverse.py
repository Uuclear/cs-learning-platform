#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：迭代FFT实现与位逆序置换
演示高效的迭代FFT算法和位逆序置换技术
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

    def __repr__(self):
        if self.imag >= 0:
            return f"{self.real:.3f}+{self.imag:.3f}i"
        else:
            return f"{self.real:.3f}{self.imag:.3f}i"

def bit_reverse_copy(a):
    """
    位逆序置换函数

    参数:
        a: Complex对象列表

    返回:
        位逆序后的列表
    """
    n = len(a)
    result = [Complex() for _ in range(n)]

    # 计算位数
    bits = n.bit_length() - 1

    for i in range(n):
        # 计算i的位逆序
        reversed_i = 0
        temp = i
        for _ in range(bits):
            reversed_i = (reversed_i << 1) | (temp & 1)
            temp >>= 1
        result[reversed_i] = a[i]

    return result

def fft_iterative(a, invert=False):
    """
    迭代FFT实现（包含位逆序置换）
    """
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

def compare_fft_implementations():
    """比较递归和迭代FFT的性能和结果"""
    import time

    # 测试多项式
    test_poly = [1, 0, 1, 0, 1, 0, 1, 0]  # 长度为8
    a_recursive = [Complex(coeff, 0) for coeff in test_poly]
    a_iterative = [Complex(coeff, 0) for coeff in test_poly]

    print("比较递归和迭代FFT实现:")
    print(f"测试多项式: {test_poly}")

    # 递归FFT
    start_time = time.time()
    result_recursive = fft_recursive(a_recursive)
    recursive_time = time.time() - start_time

    # 迭代FFT
    start_time = time.time()
    result_iterative = fft_iterative(a_iterative)
    iterative_time = time.time() - start_time

    print(f"递归FFT时间: {recursive_time:.6f}秒")
    print(f"迭代FFT时间: {iterative_time:.6f}秒")
    print(f"加速比: {recursive_time/iterative_time:.2f}x")

    # 验证结果一致性
    consistent = True
    for i in range(len(result_recursive)):
        if abs(result_recursive[i].real - result_iterative[i].real) > 1e-10 or \
           abs(result_recursive[i].imag - result_iterative[i].imag) > 1e-10:
            consistent = False
            break

    print(f"结果一致性: {'✓ 一致' if consistent else '✗ 不一致'}")

def fft_bit_reverse_demo():
    """演示位逆序置换"""
    n = 8
    original = list(range(n))

    # 手动计算位逆序
    bits = 3  # log2(8) = 3
    reversed_indices = []
    for i in range(n):
        reversed_i = 0
        temp = i
        for _ in range(bits):
            reversed_i = (reversed_i << 1) | (temp & 1)
            temp >>= 1
        reversed_indices.append(reversed_i)

    print(f"\n位逆序置换演示 (n={n}):")
    print("原始索引: ", original)
    print("位逆序后: ", reversed_indices)
    print("二进制表示:")
    for i in range(n):
        orig_bin = format(i, f'0{bits}b')
        rev_bin = format(reversed_indices[i], f'0{bits}b')
        print(f"  {i:2d} ({orig_bin}) -> {reversed_indices[i]:2d} ({rev_bin})")

def main():
    """主函数：演示迭代FFT和位逆序置换"""
    print("FFT示例2：迭代实现与位逆序置换")
    print("=" * 40)

    compare_fft_implementations()
    fft_bit_reverse_demo()

# 复用递归FFT函数（从示例1）
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

if __name__ == "__main__":
    main()