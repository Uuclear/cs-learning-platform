#!/usr/bin/env python3
"""
练习 3 解决方案：Grover 算法实现

简化版 Grover 搜索算法实现
"""

import cmath
import random
import math


def grover_step(amplitudes, solution_index):
    """执行一次 Grover 迭代"""
    n = len(amplitudes)

    # Oracle: 标记解
    amplitudes[solution_index] = -amplitudes[solution_index]

    # 扩散算子
    mean = sum(amplitudes) / n
    for i in range(n):
        amplitudes[i] = 2 * mean - amplitudes[i]

    return amplitudes


def search_with_grover(database_size, solution_index):
    """使用 Grover 算法搜索"""
    # 初始化均匀叠加态
    amplitude = 1 / cmath.sqrt(database_size)
    amplitudes = [amplitude] * database_size

    # 计算最优迭代次数
    iterations = int(math.pi / 4 * math.sqrt(database_size))

    # 执行 Grover 迭代
    for _ in range(iterations):
        amplitudes = grover_step(amplitudes, solution_index)

    # 测量
    probabilities = [abs(a)**2 for a in amplitudes]
    total = sum(probabilities)
    probabilities = [p/total for p in probabilities]  # 归一化

    rand = random.random()
    cumulative = 0
    for i, prob in enumerate(probabilities):
        cumulative += prob
        if rand <= cumulative:
            return i

    return database_size - 1


# 测试代码
if __name__ == "__main__":
    result = search_with_grover(4, 2)
    print(f"Grover 搜索结果: {result} (期望: 2)")