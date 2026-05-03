#!/usr/bin/env python3
"""
练习 1 解决方案：量子比特操作

实现量子比特的创建、测量和状态显示功能
"""

import cmath
import random


def create_qubit(alpha, beta):
    """创建归一化的量子比特"""
    norm = abs(alpha)**2 + abs(beta)**2
    if abs(norm - 1.0) > 1e-10:
        # 自动归一化
        alpha = alpha / cmath.sqrt(norm)
        beta = beta / cmath.sqrt(norm)
    return (alpha, beta)


def measure_qubit(qubit):
    """测量量子比特并返回结果"""
    alpha, beta = qubit
    prob_0 = abs(alpha)**2
    return 0 if random.random() < prob_0 else 1


def get_probabilities(qubit):
    """获取量子比特的概率分布"""
    alpha, beta = qubit
    return (abs(alpha)**2, abs(beta)**2)


# 测试代码
if __name__ == "__main__":
    # 创建 |+> 态
    qubit = create_qubit(1/cmath.sqrt(2), 1/cmath.sqrt(2))
    print(f"量子比特: {qubit}")
    print(f"概率: {get_probabilities(qubit)}")
    print(f"测量结果: {measure_qubit(qubit)}")