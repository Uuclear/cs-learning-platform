#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解答2: 两层神经网络实现XOR

使用纯numpy实现包含一个隐藏层的神经网络来学习XOR函数。
"""

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_deriv(x):
    return x * (1 - x)


# XOR训练数据
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

np.random.seed(42)
# 2 -> 4 -> 1 的网络结构
W1 = np.random.uniform(-1, 1, (2, 4))
W2 = np.random.uniform(-1, 1, (4, 1))
lr = 0.5

print("=== 两层神经网络学习XOR ===\n")

for epoch in range(10001):
    # 前向传播
    h = sigmoid(X @ W1)
    out = sigmoid(h @ W2)

    # 反向传播
    d_out = (y - out) * sigmoid_deriv(out)
    d_h = (d_out @ W2.T) * sigmoid_deriv(h)

    # 更新权重
    W2 += h.T @ d_out * lr
    W1 += X.T @ d_h * lr

    if epoch % 2000 == 0:
        loss = np.mean((y - out) ** 2)
        print(f"Epoch {epoch}: loss={loss:.6f}")

print("\n预测结果:")
for i in range(4):
    print(f"  XOR({X[i].tolist()}) = {out[i][0]:.4f} (期望: {y[i][0]})")
