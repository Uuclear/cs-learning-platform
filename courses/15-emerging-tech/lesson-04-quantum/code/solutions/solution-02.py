#!/usr/bin/env python3
"""
练习 2 解决方案：量子门实现

实现基本量子门操作，不使用外部库
"""

import cmath


def matrix_multiply_2x2(matrix_a, matrix_b):
    """2x2 矩阵乘法"""
    return [
        [matrix_a[0][0]*matrix_b[0][0] + matrix_a[0][1]*matrix_b[1][0],
         matrix_a[0][0]*matrix_b[0][1] + matrix_a[0][1]*matrix_b[1][1]],
        [matrix_a[1][0]*matrix_b[0][0] + matrix_a[1][1]*matrix_b[1][0],
         matrix_a[1][0]*matrix_b[0][1] + matrix_a[1][1]*matrix_b[1][1]]
    ]


def apply_gate_to_qubit(qubit, gate_matrix):
    """将量子门应用到量子比特"""
    alpha, beta = qubit
    new_alpha = gate_matrix[0][0] * alpha + gate_matrix[0][1] * beta
    new_beta = gate_matrix[1][0] * alpha + gate_matrix[1][1] * beta
    return (new_alpha, new_beta)


def hadamard_gate():
    """Hadamard 门"""
    h = 1 / cmath.sqrt(2)
    return [[h, h], [h, -h]]


def pauli_x_gate():
    """Pauli-X 门"""
    return [[0, 1], [1, 0]]


def create_bell_state():
    """创建贝尔纠缠态 |Φ+> = (|00> + |11>)/√2"""
    # 这需要双量子比特操作，这里返回概念性表示
    return "贝尔态: (|00⟩ + |11⟩)/√2"


# 测试代码
if __name__ == "__main__":
    # 测试 Hadamard 门
    qubit_0 = (1.0, 0.0)  # |0>
    h_gate = hadamard_gate()
    qubit_plus = apply_gate_to_qubit(qubit_0, h_gate)
    print(f"|0> 经过 H 门后: {qubit_plus}")

    # 测试 Pauli-X 门
    x_gate = pauli_x_gate()
    qubit_1 = apply_gate_to_qubit(qubit_0, x_gate)
    print(f"|0> 经过 X 门后: {qubit_1}")

    print(f"贝尔态: {create_bell_state()}")