#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：GAN（生成对抗网络）基础实现

这个示例演示了GAN的核心概念：
- 生成器（Generator）：尝试生成逼真的数据
- 判别器（Discriminator）：尝试区分真实数据和生成数据
- 对抗训练：两个网络相互竞争，共同进步

预期输出：
原始真实数据分布: [均值, 标准差]
训练轮次 0: 生成器损失=..., 判别器损失=...
训练轮次 100: 生成器损失=..., 判别器损失=...
...
最终生成数据分布: [均值, 标准差]

可以看到生成数据的分布逐渐接近真实数据分布。
"""

import numpy as np
import random

def generate_real_data(n_samples=100):
    """生成真实数据 - 正态分布"""
    return np.random.normal(loc=0.0, scale=1.0, size=(n_samples, 1))

def generator(noise):
    """简单的生成器网络 - 将噪声映射到数据空间"""
    # 使用简单的线性变换 + 非线性激活
    weights = np.array([[1.5]])  # 生成器权重
    bias = np.array([0.2])       # 生成器偏置
    return np.tanh(np.dot(noise, weights) + bias)

def discriminator(data):
    """简单的判别器网络 - 输出数据为真实的概率"""
    # 使用简单的线性分类器
    weights = np.array([[2.0]])  # 判别器权重
    bias = np.array([-0.1])      # 判别器偏置
    logits = np.dot(data, weights) + bias
    return 1.0 / (1.0 + np.exp(-logits))  # sigmoid激活

def train_gan(epochs=200, learning_rate=0.01):
    """训练GAN的基本循环"""
    print("原始真实数据分布:", end=" ")
    real_data = generate_real_data(1000)
    print(f"[均值={np.mean(real_data):.3f}, 标准差={np.std(real_data):.3f}]")

    # 初始化生成器和判别器参数
    gen_weights = np.array([[1.0]])
    gen_bias = np.array([0.0])
    disc_weights = np.array([[1.0]])
    disc_bias = np.array([0.0])

    for epoch in range(epochs):
        # 生成噪声输入
        noise = np.random.normal(0, 1, (100, 1))

        # 生成器生成假数据
        fake_data = np.tanh(np.dot(noise, gen_weights) + gen_bias)

        # 获取真实数据
        real_data_batch = generate_real_data(100)

        # 判别器训练 - 区分真假数据
        real_pred = 1.0 / (1.0 + np.exp(-(np.dot(real_data_batch, disc_weights) + disc_bias)))
        fake_pred = 1.0 / (1.0 + np.exp(-(np.dot(fake_data, disc_weights) + disc_bias)))

        # 判别器损失（希望真实数据预测为1，假数据预测为0）
        disc_loss_real = -np.log(real_pred + 1e-8)
        disc_loss_fake = -np.log(1.0 - fake_pred + 1e-8)
        disc_loss = np.mean(disc_loss_real + disc_loss_fake)

        # 更新判别器参数
        disc_grad_real = -(1.0 - real_pred) * real_data_batch
        disc_grad_fake = fake_pred * fake_data
        disc_weights -= learning_rate * np.mean(disc_grad_real - disc_grad_fake, axis=0, keepdims=True)
        disc_bias -= learning_rate * np.mean(-(1.0 - real_pred) + fake_pred)

        # 重新生成假数据用于生成器训练
        noise_gen = np.random.normal(0, 1, (100, 1))
        fake_data_gen = np.tanh(np.dot(noise_gen, gen_weights) + gen_bias)
        fake_pred_gen = 1.0 / (1.0 + np.exp(-(np.dot(fake_data_gen, disc_weights) + disc_bias)))

        # 生成器损失（希望假数据被预测为1）
        gen_loss = -np.log(fake_pred_gen + 1e-8)
        gen_loss_mean = np.mean(gen_loss)

        # 更新生成器参数（通过判别器梯度反传）
        # 简化版：直接基于fake_pred_gen计算梯度
        gen_grad = -fake_pred_gen * (1.0 - fake_pred_gen) * disc_weights.T
        gen_weights -= learning_rate * np.mean(gen_grad * (1.0 - fake_data_gen**2) * noise_gen, axis=0, keepdims=True)
        gen_bias -= learning_rate * np.mean(gen_grad * (1.0 - fake_data_gen**2))

        # 每100轮打印一次进度
        if epoch % 100 == 0:
            print(f"训练轮次 {epoch}: 生成器损失={gen_loss_mean:.4f}, 判别器损失={disc_loss:.4f}")

    # 生成最终结果
    final_noise = np.random.normal(0, 1, (1000, 1))
    final_generated = np.tanh(np.dot(final_noise, gen_weights) + gen_bias)
    print(f"最终生成数据分布: [均值={np.mean(final_generated):.3f}, 标准差={np.std(final_generated):.3f}]")

    return final_generated

if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)
    generated_data = train_gan()
    print("\nGAN训练完成！生成器学会了模拟真实数据分布。")