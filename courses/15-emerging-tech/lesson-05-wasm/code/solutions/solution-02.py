#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：性能对比实现

这是 example-02-perf-comparison.py 的优化解决方案。
包含了更真实的性能对比和更好的算法实现。
"""

import time
from typing import List

def optimized_matrix_multiply(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """
    高度优化的矩阵乘法实现，模拟 WebAssembly 的性能优势
    """
    rows_a, cols_a = len(a), len(a[0])
    cols_b = len(b[0])

    # 使用列表推导式预分配内存
    result = [[0.0 for _ in range(cols_b)] for _ in range(rows_a)]

    # 优化的循环顺序以提高缓存局部性
    for i in range(rows_a):
        a_row = a[i]
        result_row = result[i]
        for k in range(cols_a):
            a_ik = a_row[k]
            if a_ik != 0.0:  # 跳过零值优化
                b_k = b[k]
                for j in range(cols_b):
                    result_row[j] += a_ik * b_k[j]

    return result

def benchmark_matrix_multiply(size: int = 100) -> dict:
    """
    基准测试函数，返回详细的性能数据
    """
    import random
    random.seed(42)

    # 生成测试矩阵
    matrix_a = [[random.random() for _ in range(size)] for _ in range(size)]
    matrix_b = [[random.random() for _ in range(size)] for _ in range(size)]

    # 测试优化版本
    start = time.perf_counter()
    result = optimized_matrix_multiply(matrix_a, matrix_b)
    end = time.perf_counter()

    return {
        "size": size,
        "time": end - start,
        "result_shape": (len(result), len(result[0])) if result else (0, 0)
    }

def main():
    sizes = [50, 100, 150]
    results = []

    for size in sizes:
        result = benchmark_matrix_multiply(size)
        results.append(result)
        print(f"矩阵大小 {size}x{size}: {result['time']:.4f} 秒")

    print("✓ 性能测试完成！")

if __name__ == "__main__":
    main()