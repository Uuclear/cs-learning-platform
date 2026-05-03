#!/usr/bin/env python3
"""
量子门操作模拟示例

本示例演示了基本量子门的操作：
- Hadamard 门: 创建叠加态
- Pauli-X 门: 量子比特翻转 (类似经典 NOT)
- CNOT 门: 控制非门 (双量子比特操作)
"""

import cmath
import numpy as np


def hadamard_gate():
    """Hadamard 门矩阵"""
    h = 1 / cmath.sqrt(2)
    return np.array([[h, h],
                     [h, -h]], dtype=complex)


def pauli_x_gate():
    """Pauli-X 门矩阵 (量子 NOT)"""
    return np.array([[0, 1],
                     [1, 0]], dtype=complex)


def cnot_gate():
    """CNOT 门矩阵 (控制非门)"""
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1],
                     [0, 0, 1, 0]], dtype=complex)


def apply_single_qubit_gate(qubit, gate_matrix):
    """
    应用单量子比特门

    参数:
        qubit (tuple): (alpha, beta) 量子比特状态
        gate_matrix (np.array): 2x2 门矩阵

    返回:
        tuple: 新的量子比特状态
    """
    state_vector = np.array([qubit[0], qubit[1]], dtype=complex)
    new_state = np.dot(gate_matrix, state_vector)
    return (new_state[0], new_state[1])


def apply_cnot_gate(control_qubit, target_qubit):
    """
    应用 CNOT 门到两个量子比特

    参数:
        control_qubit (tuple): 控制量子比特
        target_qubit (tuple): 目标量子比特

    返回:
        tuple: (new_control, new_target) 新的量子比特状态
    """
    # 构建双量子比特状态向量 |control,target>
    alpha_c, beta_c = control_qubit
    alpha_t, beta_t = target_qubit

    # |00> = α_c * α_t, |01> = α_c * β_t, |10> = β_c * α_t, |11> = β_c * β_t
    two_qubit_state = np.array([
        alpha_c * alpha_t,
        alpha_c * beta_t,
        beta_c * alpha_t,
        beta_c * beta_t
    ], dtype=complex)

    # 应用 CNOT 门
    new_state = np.dot(cnot_gate(), two_qubit_state)

    # 从结果中提取新的单量子比特状态（仅当结果可分离时）
    # 这里我们返回完整的双量子比特状态用于演示
    return new_state


def print_gate_operation(initial_state, final_state, gate_name):
    """打印量子门操作结果"""
    print(f"\n应用 {gate_name} 门:")
    print(f"初始状态: α={initial_state[0]:.4f}, β={initial_state[1]:.4f}")
    print(f"最终状态: α={final_state[0]:.4f}, β={final_state[1]:.4f}")


def main():
    """主函数：演示量子门操作"""
    print("=== 量子门操作模拟示例 ===\n")

    # 1. Hadamard 门操作
    print("1. Hadamard 门操作 (创建叠加态):")
    # 初始状态 |0> = (1, 0)
    initial_qubit = (1.0 + 0j, 0.0 + 0j)
    h_gate = hadamard_gate()
    final_qubit = apply_single_qubit_gate(initial_qubit, h_gate)
    print_gate_operation(initial_qubit, final_qubit, "Hadamard")

    # 2. Pauli-X 门操作
    print("\n2. Pauli-X 门操作 (量子比特翻转):")
    # 初始状态 |0> = (1, 0)
    initial_qubit_x = (1.0 + 0j, 0.0 + 0j)
    x_gate = pauli_x_gate()
    final_qubit_x = apply_single_qubit_gate(initial_qubit_x, x_gate)
    print_gate_operation(initial_qubit_x, final_qubit_x, "Pauli-X")

    # 3. CNOT 门操作
    print("\n3. CNOT 门操作 (纠缠态创建):")
    # 控制量子比特 |+> 态, 目标量子比特 |0> 态
    control_qubit = (1/cmath.sqrt(2), 1/cmath.sqrt(2))  # |+>
    target_qubit = (1.0 + 0j, 0.0 + 0j)  # |0>

    print(f"控制量子比特: α={control_qubit[0]:.4f}, β={control_qubit[1]:.4f}")
    print(f"目标量子比特: α={target_qubit[0]:.4f}, β={target_qubit[1]:.4f}")

    entangled_state = apply_cnot_gate(control_qubit, target_qubit)
    print(f"CNOT 后的纠缠态: {entangled_state}")

    # 验证贝尔态
    bell_state_expected = np.array([1/cmath.sqrt(2), 0, 0, 1/cmath.sqrt(2)])
    print(f"期望的贝尔态: {bell_state_expected}")

    # 计算差异
    diff = np.linalg.norm(entangled_state - bell_state_expected)
    print(f"与期望贝尔态的差异: {diff:.6f}")

    print("\n=== 模拟完成 ===")


if __name__ == "__main__":
    # 检查是否安装了 numpy，如果没有则使用纯 Python 实现
    try:
        import numpy as np
        main()
    except ImportError:
        print("注意: 此示例需要 numpy 库进行矩阵运算")
        print("请安装 numpy: pip install numpy")