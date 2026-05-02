#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解答3: 两层神经网络实现手写数字识别（简化版MNIST）

使用纯numpy实现包含一个隐藏层的神经网络，使用ReLU和softmax激活函数，
交叉熵损失函数，在简化的MNIST子集上训练。
"""

import numpy as np


def relu(x):
    """ReLU激活函数"""
    return np.maximum(0, x)


def relu_deriv(x):
    """ReLU的导数"""
    return (x > 0).astype(float)


def softmax(x):
    """数值稳定的softmax"""
    shifted = x - np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(shifted)
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


def cross_entropy_loss(predicted, actual):
    """交叉熵损失"""
    m = predicted.shape[0]
    clipped = np.clip(predicted, 1e-12, 1 - 1e-12)
    return -np.sum(actual * np.log(clipped)) / m


def one_hot(y, num_classes=10):
    """将标签转换为one-hot编码"""
    return np.eye(num_classes)[y]


# 生成简化的模拟MNIST数据（8x8像素，4个类别）
np.random.seed(42)
n_samples = 200
n_features = 64  # 8x8像素
n_classes = 4

# 生成带有模式的数据
X = np.random.randn(n_samples, n_features) * 0.5
for i in range(n_classes):
    mask = slice(i * 50, (i + 1) * 50)
    X[mask, i * 16:(i + 1) * 16] += 1.5  # 每类在不同区域有特征

y_labels = np.repeat(np.arange(n_classes), 50)
y = one_hot(y_labels, n_classes)

# 训练/测试分割
split = 160
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# 初始化权重 (784 -> 128 -> 10 的缩小版: 64 -> 32 -> 4)
W1 = np.random.randn(n_features, 32) * np.sqrt(2.0 / n_features)
b1 = np.zeros((1, 32))
W2 = np.random.randn(32, n_classes) * np.sqrt(2.0 / 32)
b2 = np.zeros((1, n_classes))

learning_rate = 0.01
epochs = 500
batch_size = 32

print("=== 两层神经网络手写数字识别（简化版）===\n")

for epoch in range(epochs + 1):
    # 小批量训练
    indices = np.random.permutation(split)
    total_loss = 0
    n_batches = 0

    for start in range(0, split, batch_size):
        end = min(start + batch_size, split)
        batch_idx = indices[start:end]
        X_batch = X[batch_idx]
        y_batch = y[batch_idx]

        # 前向传播
        z1 = X_batch @ W1 + b1
        a1 = relu(z1)
        z2 = a1 @ W2 + b2
        a2 = softmax(z2)

        total_loss += cross_entropy_loss(a2, y_batch)
        n_batches += 1

        # 反向传播
        m = X_batch.shape[0]
        dz2 = (a2 - y_batch) / m
        dW2 = a1.T @ dz2
        db2 = np.sum(dz2, axis=0, keepdims=True)

        da1 = dz2 @ W2.T
        dz1 = da1 * relu_deriv(z1)
        dW1 = X_batch.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)

        # 更新权重
        W2 -= learning_rate * dW2
        b2 -= learning_rate * db2
        W1 -= learning_rate * dW1
        b1 -= learning_rate * db1

    if epoch % 100 == 0:
        avg_loss = total_loss / n_batches
        print(f"Epoch {epoch}: loss={avg_loss:.4f}")

# 测试评估
z1_test = X_test @ W1 + b1
a1_test = relu(z1_test)
z2_test = a1_test @ W2 + b2
a2_test = softmax(z2_test)

predicted_labels = np.argmax(a2_test, axis=1)
actual_labels = np.argmax(y_test, axis=1)
accuracy = np.mean(predicted_labels == actual_labels)

print(f"\n测试准确率: {accuracy:.2%}")
print("\n预测结果示例:")
for i in range(min(10, len(X_test))):
    print(f"  样本{i}: 预测={predicted_labels[i]}, 实际={actual_labels[i]}")
