#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：性能对比模拟器

这个示例模拟了 JavaScript 与 WebAssembly 的性能差异。
我们使用纯 Python 函数来代表 "JavaScript" 实现，
使用优化后的函数（带类型提示和更高效算法）来代表 "WebAssembly" 实现。

注意：这只是一个概念演示，实际的 Wasm 性能优势来自于：
1. 静态类型和编译时优化
2. 近似原生代码的执行速度
3. 更少的垃圾回收开销
"""

import time
import math
from typing import List

def js_style_matrix_multiply(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """
    模拟 JavaScript 风格的矩阵乘法实现
    - 动态类型检查
    - 较多的运行时验证
    - 使用通用数据结构
    """
    if not a or not b:
        return []

    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])

    if cols_a != rows_b:
        raise ValueError("矩阵维度不匹配")

    # 初始化结果矩阵
    result = []
    for i in range(rows_a):
        row = []
        for j in range(cols_b):
            row.append(0.0)
        result.append(row)

    # 执行乘法
    for i in range(rows_a):
        for j in range(cols_b):
            total = 0.0
            for k in range(cols_a):
                # 模拟 JavaScript 的动态类型操作
                val_a = float(a[i][k]) if isinstance(a[i][k], (int, float)) else 0.0
                val_b = float(b[k][j]) if isinstance(b[k][j], (int, float)) else 0.0
                total += val_a * val_b
            result[i][j] = total

    return result

def wasm_style_matrix_multiply(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """
    模拟 WebAssembly 风格的矩阵乘法实现
    - 静态类型假设（输入已验证）
    - 最小化运行时开销
    - 优化的内存访问模式
    - 使用局部变量减少属性访问
    """
    # 假设输入已经过验证，直接进行计算
    rows_a = len(a)
    cols_a = len(a[0])
    cols_b = len(b[0])

    # 预分配结果矩阵（避免动态扩展）
    result = [[0.0 for _ in range(cols_b)] for _ in range(rows_a)]

    # 优化的循环顺序（更好的缓存局部性）
    for i in range(rows_a):
        row_a = a[i]  # 缓存行引用
        row_result = result[i]
        for k in range(cols_a):
            val_a = row_a[k]
            if val_a == 0.0:  # 跳过零值（稀疏矩阵优化）
                continue
            col_b = [b[k][j] for j in range(cols_b)]  # 简化的列访问
            for j in range(cols_b):
                row_result[j] += val_a * col_b[j]

    return result

def generate_test_matrices(size: int) -> tuple:
    """生成测试用的随机矩阵"""
    import random
    random.seed(42)  # 固定种子以确保可重现性

    matrix_a = [[random.random() for _ in range(size)] for _ in range(size)]
    matrix_b = [[random.random() for _ in range(size)] for _ in range(size)]

    return matrix_a, matrix_b

def benchmark_function(func, *args, iterations: int = 10) -> float:
    """基准测试函数执行时间"""
    # 预热运行
    func(*args)

    start_time = time.perf_counter()
    for _ in range(iterations):
        func(*args)
    end_time = time.perf_counter()

    return (end_time - start_time) / iterations

def main():
    """演示性能对比"""
    print("=== WebAssembly vs JavaScript 性能对比模拟 ===")
    print("注意：这是一个概念演示，实际性能差异会更大！")
    print()

    # 测试不同大小的矩阵
    test_sizes = [50, 100, 150]

    for size in test_sizes:
        print(f"测试矩阵大小: {size}x{size}")

        # 生成测试数据
        matrix_a, matrix_b = generate_test_matrices(size)

        # 测试 JavaScript 风格实现
        js_time = benchmark_function(js_style_matrix_multiply, matrix_a, matrix_b)

        # 测试 WebAssembly 风格实现
        wasm_time = benchmark_function(wasm_style_matrix_multiply, matrix_a, matrix_b)

        # 计算加速比
        speedup = js_time / wasm_time if wasm_time > 0 else float('inf')

        print(f"  JavaScript 风格: {js_time:.4f} 秒")
        print(f"  WebAssembly 风格: {wasm_time:.4f} 秒")
        print(f"  加速比: {speedup:.2f}x")
        print()

    # 验证结果正确性
    print("=== 验证结果正确性 ===")
    small_a, small_b = generate_test_matrices(10)
    js_result = js_style_matrix_multiply(small_a, small_b)
    wasm_result = wasm_style_matrix_multiply(small_a, small_b)

    # 比较结果是否近似相等
    tolerance = 1e-10
    results_match = True
    for i in range(len(js_result)):
        for j in range(len(js_result[0])):
            if abs(js_result[i][j] - wasm_result[i][j]) > tolerance:
                results_match = False
                break
        if not results_match:
            break

    if results_match:
        print("✓ 两种实现的结果一致！")
    else:
        print("✗ 结果不一致，请检查实现！")

if __name__ == "__main__":
    main()