#!/usr/bin/env python3
"""
Grover 搜索算法概念模拟示例

本示例演示了 Grover 算法的核心思想：
- 量子并行性：同时检查所有可能解
- 振幅放大：增加正确解的概率
- 平方根加速：相比经典搜索的 O(N) vs O(√N)
"""

import cmath
import random
import math


def create_uniform_superposition(n_items):
    """
    创建均匀叠加态

    参数:
        n_items (int): 项目数量

    返回:
        list: 复数列表表示每个状态的振幅
    """
    amplitude = 1 / cmath.sqrt(n_items)
    return [amplitude for _ in range(n_items)]


def oracle_mark_solution(amplitudes, solution_index):
    """
    Oracle 函数：标记正确解（翻转其相位）

    参数:
        amplitudes (list): 当前振幅列表
        solution_index (int): 正确解的索引

    返回:
        list: 标记后的振幅列表
    """
    new_amplitudes = amplitudes.copy()
    new_amplitudes[solution_index] = -new_amplitudes[solution_index]
    return new_amplitudes


def diffusion_operator(amplitudes):
    """
    扩散算子：关于平均值的反射

    参数:
        amplitudes (list): 当前振幅列表

    返回:
        list: 应用扩散算子后的振幅列表
    """
    n = len(amplitudes)
    mean_amplitude = sum(amplitudes) / n

    new_amplitudes = []
    for amp in amplitudes:
        # 关于平均值的反射: 2*mean - amp
        new_amp = 2 * mean_amplitude - amp
        new_amplitudes.append(new_amp)

    return new_amplitudes


def measure_state(amplitudes):
    """
    测量量子态

    参数:
        amplitudes (list): 振幅列表

    返回:
        int: 测量结果（索引）
    """
    probabilities = [abs(amp)**2 for amp in amplitudes]

    # 验证概率归一化
    total_prob = sum(probabilities)
    if abs(total_prob - 1.0) > 1e-10:
        # 归一化概率
        probabilities = [p / total_prob for p in probabilities]

    # 根据概率分布进行随机选择
    rand_val = random.random()
    cumulative_prob = 0
    for i, prob in enumerate(probabilities):
        cumulative_prob += prob
        if rand_val <= cumulative_prob:
            return i

    # 安全返回（理论上不会到达这里）
    return len(amplitudes) - 1


def grover_search(n_items, solution_index, iterations=None):
    """
    Grover 搜索算法模拟

    参数:
        n_items (int): 搜索空间大小
        solution_index (int): 正确解的索引
        iterations (int): 迭代次数，如果为 None 则使用最优迭代次数

    返回:
        tuple: (最终振幅, 测量结果, 成功概率)
    """
    if iterations is None:
        # 最优迭代次数 ≈ π/4 * √N
        iterations = int(math.pi / 4 * math.sqrt(n_items))

    print(f"Grover 搜索: N={n_items}, 解={solution_index}, 迭代={iterations}")

    # 1. 初始化均匀叠加态
    amplitudes = create_uniform_superposition(n_items)
    print(f"初始均匀叠加态振幅: {amplitudes[0]:.4f}")

    # 2. 执行 Grover 迭代
    for iter_num in range(iterations):
        # Oracle 步骤：标记解
        amplitudes = oracle_mark_solution(amplitudes, solution_index)

        # 扩散步骤：振幅放大
        amplitudes = diffusion_operator(amplitudes)

        # 计算当前成功概率
        success_prob = abs(amplitudes[solution_index])**2
        print(f"  迭代 {iter_num+1}: 成功概率 = {success_prob:.4f}")

    # 3. 测量
    measurement = measure_state(amplitudes)
    final_success_prob = abs(amplitudes[solution_index])**2

    return amplitudes, measurement, final_success_prob


def main():
    """主函数：演示 Grover 搜索"""
    print("=== Grover 搜索算法概念模拟 ===\n")

    # 示例 1: 小规模搜索 (4 个项目)
    print("示例 1: 在 4 个项目中搜索")
    n_items_1 = 4
    solution_1 = 2  # 假设解在索引 2
    _, result_1, prob_1 = grover_search(n_items_1, solution_1)
    print(f"测量结果: {result_1}, 正确解: {solution_1}")
    print(f"是否找到正确解: {'是' if result_1 == solution_1 else '否'}")
    print(f"最终成功概率: {prob_1:.4f}\n")

    # 示例 2: 较大规模搜索 (16 个项目)
    print("示例 2: 在 16 个项目中搜索")
    n_items_2 = 16
    solution_2 = 7  # 假设解在索引 7
    _, result_2, prob_2 = grover_search(n_items_2, solution_2)
    print(f"测量结果: {result_2}, 正确解: {solution_2}")
    print(f"是否找到正确解: {'是' if result_2 == solution_2 else '否'}")
    print(f"最终成功概率: {prob_2:.4f}\n")

    # 对比经典搜索
    print("=== 算法复杂度对比 ===")
    print(f"经典搜索平均需要 {n_items_2//2} 次尝试")
    print(f"Grover 算法只需要 {int(math.pi/4 * math.sqrt(n_items_2))} 次迭代")
    print(f"加速比: ~{math.sqrt(n_items_2):.1f}x")

    print("\n=== 模拟完成 ===")


if __name__ == "__main__":
    main()