#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解答1: 感知机实现AND门

使用纯numpy实现感知机，训练它识别AND逻辑门。
"""

import numpy as np


def step_function(x):
    """阶跃激活函数"""
    return 1 if x >= 0 else 0


# AND门训练数据
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 0, 0, 1])

# 初始化权重和偏置
w = np.random.uniform(-0.5, 0.5, 2)
b = 0.0
learning_rate = 0.1

print("=== 感知机学习AND门 ===")

# 训练20轮
for epoch in range(20):
    errors = 0
    for xi, target in zip(X, y):
        output = step_function(np.dot(xi, w) + b)
        error = target - output
        if error != 0:
            errors += 1
            w += learning_rate * error * xi
            b += learning_rate * error
    if errors == 0:
        print(f"\nEpoch {epoch}: 所有样本分类正确！")
        break

# 测试
print("\n测试结果:")
for xi in X:
    pred = step_function(np.dot(xi, w) + b)
    print(f"  {xi.tolist()} -> {pred}")
