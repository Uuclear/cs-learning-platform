#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 反向传播算法演示

本示例展示了：
1. 反向传播的基本原理
2. 手动计算梯度
3. 使用numpy实现简单神经网络训练
"""

import numpy as np


def sigmoid(x):
    """Sigmoid激活函数"""
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    """Sigmoid的导数"""
    return x * (1 - x)


# 训练数据（XOR问题）
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# 设置随机种子以便复现
np.random.seed(42)

# 初始化权重
input_size = 2
hidden_size = 3
output_size = 1

weights_input_hidden = np.random.uniform(-1, 1, (input_size, hidden_size))
weights_hidden_output = np.random.uniform(-1, 1, (hidden_size, output_size))

learning_rate = 0.5

print("=== 反向传播训练XOR问题 ===\n")

# 训练10000轮
for epoch in range(10001):
    # 前向传播
    hidden_input = np.dot(X, weights_input_hidden)
    hidden_output = sigmoid(hidden_input)

    output_input = np.dot(hidden_output, weights_hidden_output)
    predicted_output = sigmoid(output_input)

    # 计算损失（均方误差）
    error = y - predicted_output
    loss = np.mean(error ** 2)

    # 反向传播
    d_output = error * sigmoid_derivative(predicted_output)
    error_hidden = d_output.dot(weights_hidden_output.T)
    d_hidden = error_hidden * sigmoid_derivative(hidden_output)

    # 更新权重
    weights_hidden_output += hidden_output.T.dot(d_output) * learning_rate
    weights_input_hidden += X.T.dot(d_hidden) * learning_rate

    if epoch % 1000 == 0:
        print(f"Epoch {epoch}: 损失 = {loss:.6f}")

print("\n训练完成！")
print("\n预测结果:")
for i in range(4):
    print(f"  输入 {X[i].tolist()} -> 预测: {predicted_output[i][0]:.4f}, 实际: {y[i][0]}")
