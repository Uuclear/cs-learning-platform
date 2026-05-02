#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答：斯特拉森矩阵乘法（Strassen's Matrix Multiplication）

传统的矩阵乘法时间复杂度为O(n³)，而斯特拉森算法使用分治思想，
将时间复杂度降低到约O(n^2.807)。
"""

from typing import List
import math


def strassen_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """
    使用斯特拉森算法进行矩阵乘法

    Args:
        A: 第一个矩阵 (n x n)
        B: 第二个矩阵 (n x n)

    Returns:
        矩阵乘积 C = A * B
    """
    n = len(A)

    # 如果矩阵大小不是2的幂，需要填充
    if not _is_power_of_two(n):
        new_n = 2 ** math.ceil(math.log2(n))
        A_padded = _pad_matrix(A, new_n)
        B_padded = _pad_matrix(B, new_n)
        C_padded = strassen_multiply(A_padded, B_padded)
        return _unpad_matrix(C_padded, n)

    # 基本情况：1x1矩阵
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    # 分解：将矩阵分成四个子矩阵
    mid = n // 2

    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    # 计算7个乘积（斯特拉森的关键）
    P1 = strassen_multiply(_matrix_add(A11, A22), _matrix_add(B11, B22))
    P2 = strassen_multiply(_matrix_add(A21, A22), B11)
    P3 = strassen_multiply(A11, _matrix_sub(B12, B22))
    P4 = strassen_multiply(A22, _matrix_sub(B21, B11))
    P5 = strassen_multiply(_matrix_add(A11, A12), B22)
    P6 = strassen_multiply(_matrix_sub(A21, A11), _matrix_add(B11, B12))
    P7 = strassen_multiply(_matrix_sub(A12, A22), _matrix_add(B21, B22))

    # 合并：计算结果矩阵的四个象限
    C11 = _matrix_add(_matrix_sub(_matrix_add(P1, P4), P5), P7)
    C12 = _matrix_add(P3, P5)
    C21 = _matrix_add(P2, P4)
    C22 = _matrix_add(_matrix_sub(_matrix_add(P1, P3), P2), P6)

    # 组合结果矩阵
    C = []
    for i in range(mid):
        C.append(C11[i] + C12[i])
    for i in range(mid):
        C.append(C21[i] + C22[i])

    return C


def _is_power_of_two(n: int) -> bool:
    """检查n是否为2的幂"""
    return n > 0 and (n & (n - 1)) == 0


def _pad_matrix(matrix: List[List[int]], new_size: int) -> List[List[int]]:
    """填充矩阵到指定大小"""
    padded = [[0] * new_size for _ in range(new_size)]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            padded[i][j] = matrix[i][j]
    return padded


def _unpad_matrix(matrix: List[List[int]], original_size: int) -> List[List[int]]:
    """去除填充，恢复原始大小"""
    return [row[:original_size] for row in matrix[:original_size]]


def _matrix_add(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """矩阵加法"""
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] + B[i][j]
    return result


def _matrix_sub(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """矩阵减法"""
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] - B[i][j]
    return result


def _standard_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """标准矩阵乘法（用于验证）"""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


if __name__ == "__main__":
    # 测试2x2矩阵
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    print("矩阵A:")
    for row in A:
        print(row)
    print("\n矩阵B:")
    for row in B:
        print(row)

    C_strassen = strassen_multiply(A, B)
    C_standard = _standard_multiply(A, B)

    print("\n斯特拉森算法结果:")
    for row in C_strassen:
        print(row)

    print("\n标准算法结果:")
    for row in C_standard:
        print(row)

    # 验证结果
    assert C_strassen == C_standard, "斯特拉森算法结果不正确！"
    print("\n✅ 斯特拉森矩阵乘法测试通过！")