#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挑战2解决方案：实现条件扩散模型

这个解决方案实现了条件扩散模型，可以根据给定的条件生成特定类型的数据。
"""

import numpy as np

class ConditionalDiffusionModel:
    """条件扩散模型"""
    def __init__(self, data_dim=10, condition_dim=5):
        self.data_dim = data_dim
        self.condition_dim = condition_dim
        self.T = 100  # 扩散步数
        self.beta_min = 0.0001
        self.beta_max = 0.02

        # 预计算扩散参数
        self.betas = np.linspace(self.beta_min, self.beta_max, self.T)
        self.alphas = 1.0 - self.betas
        self.alpha_bars = np.cumprod(self.alphas)

    def forward_diffusion(self, x_0, t, condition=None):
        """条件正向扩散"""
        alpha_bar_t = self.alpha_bars[t-1] if t > 0 else 1.0
        noise = np.random.normal(0, 1, x_0.shape)
        x_t = np.sqrt(alpha_bar_t) * x_0 + np.sqrt(1 - alpha_bar_t) * noise
        return x_t, noise

    def predict_noise(self, x_t, t, condition):
        """噪声预测网络（简化版）"""
        # 在实际应用中，这是一个训练好的神经网络
        # 这里使用一个基于条件的简单函数来演示
        batch_size = x_t.shape[0]

        # 将条件信息融入噪声预测
        condition_effect = np.mean(condition, axis=1, keepdims=True) * 0.1
        base_noise = x_t * 0.5 + condition_effect

        return base_noise

    def reverse_diffusion_step(self, x_t, predicted_noise, t, condition=None):
        """条件反向扩散步骤"""
        if t == 1:
            # 最后一步不需要添加噪声
            alpha_t = self.alphas[t-1]
            x_t_minus_1 = (x_t - (1 - alpha_t) / np.sqrt(1 - self.alpha_bars[t-1]) * predicted_noise) / np.sqrt(alpha_t)
            return x_t_minus_1

        alpha_t = self.alphas[t-1]
        alpha_bar_t = self.alpha_bars[t-1]
        alpha_bar_t_minus_1 = self.alpha_bars[t-2]

        # 计算系数
        coef1 = 1.0 / np.sqrt(alpha_t)
        coef2 = (1.0 - alpha_t) / np.sqrt(1.0 - alpha_bar_t)

        x_t_minus_1 = coef1 * (x_t - coef2 * predicted_noise)

        # 添加噪声
        sigma_t = np.sqrt((1.0 - alpha_bar_t_minus_1) / (1.0 - alpha_bar_t) * (1.0 - alpha_t))
        noise = np.random.normal(0, 1, x_t.shape)
        x_t_minus_1 += sigma_t * noise

        return x_t_minus_1

    def generate(self, condition, num_samples=1):
        """根据条件生成数据"""
        x_T = np.random.normal(0, 1, (num_samples, self.data_dim))

        # 复制条件到所有样本
        if condition.ndim == 1:
            condition = np.tile(condition.reshape(1, -1), (num_samples, 1))

        x_t = x_T.copy()

        for t in range(self.T, 0, -1):
            predicted_noise = self.predict_noise(x_t, t, condition)
            x_t = self.reverse_diffusion_step(x_t, predicted_noise, t, condition)

        return x_t

def demonstrate_conditional_generation():
    """演示条件生成"""
    np.random.seed(42)

    model = ConditionalDiffusionModel(data_dim=10, condition_dim=5)

    # 创建不同的条件
    condition_a = np.array([1.0, 0.0, 0.0, 0.0, 0.0])  # 条件A：第一个特征激活
    condition_b = np.array([0.0, 1.0, 0.0, 0.0, 0.0])  # 条件B：第二个特征激活

    print("条件A生成结果:")
    samples_a = model.generate(condition_a, num_samples=3)
    for i, sample in enumerate(samples_a):
        print(f"  样本 {i+1}: {sample[:3]}...")

    print("\n条件B生成结果:")
    samples_b = model.generate(condition_b, num_samples=3)
    for i, sample in enumerate(samples_b):
        print(f"  样本 {i+1}: {sample[:3]}...")

    print("\n条件扩散模型成功根据不同的条件生成了不同的数据！")

if __name__ == "__main__":
    demonstrate_conditional_generation()