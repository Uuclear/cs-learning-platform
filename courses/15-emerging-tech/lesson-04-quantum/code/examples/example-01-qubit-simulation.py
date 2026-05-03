#!/usr/bin/env python3
"""
量子比特模拟示例

本示例演示了量子比特的基本概念：
- 量子比特可以用复数表示状态
- 测量会导致量子态坍缩到经典状态
- 概率由振幅的模平方决定
"""

import cmath
import random


def create_qubit(alpha, beta):
    """
    创建一个量子比特

    参数:
        alpha (complex): |0> 状态的振幅
        beta (complex): |1> 状态的振幅

    返回:
        tuple: (alpha, beta) 表示量子比特状态
    """
    # 验证归一化条件: |alpha|^2 + |beta|^2 = 1
    norm = abs(alpha)**2 + abs(beta)**2
    if abs(norm - 1.0) > 1e-10:
        raise ValueError(f"量子比特未归一化: |α|² + |β|² = {norm}")

    return (alpha, beta)


def measure_qubit(qubit):
    """
    测量量子比特

    参数:
        qubit (tuple): (alpha, beta) 量子比特状态

    返回:
        int: 测量结果 (0 或 1)
    """
    alpha, beta = qubit
    prob_0 = abs(alpha)**2  # |0> 状态的概率
    prob_1 = abs(beta)**2   # |1> 状态的概率

    # 根据概率进行随机测量
    if random.random() < prob_0:
        return 0
    else:
        return 1


def print_qubit_state(qubit):
    """打印量子比特状态"""
    alpha, beta = qubit
    print(f"量子比特状态: α|0⟩ + β|1⟩")
    print(f"α = {alpha:.4f}, β = {beta:.4f}")
    print(f"P(|0⟩) = {abs(alpha)**2:.4f}, P(|1⟩) = {abs(beta)**2:.4f}")


def main():
    """主函数：演示量子比特操作"""
    print("=== 量子比特模拟示例 ===\n")

    # 创建 |+> 态: (|0> + |1>)/√2
    print("1. 创建 |+> 态 (等概率叠加态):")
    alpha_plus = 1 / cmath.sqrt(2)
    beta_plus = 1 / cmath.sqrt(2)
    qubit_plus = create_qubit(alpha_plus, beta_plus)
    print_qubit_state(qubit_plus)

    # 测量多次观察统计结果
    print("\n2. 进行10次测量:")
    measurements = []
    for i in range(10):
        result = measure_qubit(qubit_plus)
        measurements.append(result)
        print(f"   测量 {i+1}: {result}")

    count_0 = measurements.count(0)
    count_1 = measurements.count(1)
    print(f"\n   统计结果: |0⟩ 出现 {count_0} 次, |1⟩ 出现 {count_1} 次")

    # 创建一般叠加态
    print("\n3. 创建一般叠加态 (α=0.6, β=0.8):")
    alpha_gen = 0.6
    beta_gen = 0.8j  # 使用虚数
    qubit_gen = create_qubit(alpha_gen, beta_gen)
    print_qubit_state(qubit_gen)

    print("\n=== 模拟完成 ===")


if __name__ == "__main__":
    main()