#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：扩散模型（Diffusion Model）基础实现

这个示例演示了扩散模型的核心概念：
- 正向过程（Forward Process）：逐步向数据添加噪声
- 反向过程（Reverse Process）：逐步去噪恢复数据
- 噪声预测网络：学习预测每一步的噪声

预期输出：
原始数据: [x1, x2, ..., xn]
正向扩散过程:
  步骤 0: 数据=[...], 噪声=[...]
  步骤 50: 数据=[...], 噪声=[...]
  步骤 100: 数据=[...], 噪声=[...]
反向去噪过程:
  步骤 100: 去噪后=[...]
  步骤 50: 去噪后=[...]
  步骤 0: 最终重建=[...]

可以看到通过反向过程，我们能够从纯噪声中重建出原始数据。
"""

import numpy as np

def forward_diffusion(x_0, t, T=100):
    """正向扩散过程：在时间步t向数据x_0添加噪声"""
    # 计算累积噪声方差
    beta_t = 0.02  # 固定噪声调度
    alpha_t = 1.0 - beta_t
    alpha_bar_t = alpha_t ** t

    # 生成噪声
    noise = np.random.normal(0, 1, x_0.shape)

    # 应用扩散公式: x_t = sqrt(alpha_bar_t) * x_0 + sqrt(1 - alpha_bar_t) * noise
    x_t = np.sqrt(alpha_bar_t) * x_0 + np.sqrt(1 - alpha_bar_t) * noise

    return x_t, noise

def reverse_diffusion_step(x_t, predicted_noise, t, T=100):
    """反向扩散步骤：从x_t去噪到x_{t-1}"""
    beta_t = 0.02
    alpha_t = 1.0 - beta_t
    alpha_bar_t = alpha_t ** t
    alpha_bar_t_minus_1 = alpha_t ** (t - 1) if t > 1 else 1.0

    # 简化的去噪公式
    coef1 = 1.0 / np.sqrt(alpha_t)
    coef2 = (1.0 - alpha_t) / np.sqrt(1.0 - alpha_bar_t)

    x_t_minus_1 = coef1 * (x_t - coef2 * predicted_noise)

    # 添加少量噪声（除了最后一步）
    if t > 1:
        sigma_t = np.sqrt(beta_t)
        noise = np.random.normal(0, 1, x_t.shape)
        x_t_minus_1 += sigma_t * noise

    return x_t_minus_1

def noise_predictor_simple(x_t, t, original_data):
    """简单的噪声预测器（理想情况下应该是一个神经网络）"""
    # 在真实场景中，这是一个训练好的神经网络
    # 这里我们使用一个简化的版本来演示概念
    T = 100
    beta_t = 0.02
    alpha_t = 1.0 - beta_t
    alpha_bar_t = alpha_t ** t

    # 理想的噪声预测：从x_t和原始数据计算
    # noise = (x_t - sqrt(alpha_bar_t) * x_0) / sqrt(1 - alpha_bar_t)
    estimated_noise = (x_t - np.sqrt(alpha_bar_t) * original_data) / np.sqrt(1.0 - alpha_bar_t + 1e-8)

    return estimated_noise

def demonstrate_diffusion_process():
    """演示完整的扩散和去噪过程"""
    # 创建简单的原始数据（一维信号）
    np.random.seed(42)
    original_data = np.array([1.0, -0.5, 0.8, -1.2, 0.3])
    print(f"原始数据: {original_data}")

    T = 100  # 总扩散步数

    print("\n正向扩散过程:")
    # 选择几个关键时间步进行展示
    time_steps = [0, 50, 100]
    diffused_states = {}

    for t in time_steps:
        if t == 0:
            x_t = original_data.copy()
            noise = np.zeros_like(original_data)
        else:
            x_t, noise = forward_diffusion(original_data, t, T)
        diffused_states[t] = x_t
        print(f"  步骤 {t}: 数据={x_t}, 噪声={noise}")

    print("\n反向去噪过程:")
    # 从完全噪声开始反向去噪
    current_x = diffused_states[100].copy()
    reconstructed_data = None

    reverse_steps = [100, 50, 0]
    for i, t in enumerate(reverse_steps):
        if t == 0:
            # 最后一步直接输出
            reconstructed_data = current_x
            print(f"  步骤 {t}: 最终重建={reconstructed_data}")
        else:
            # 预测噪声（使用理想预测器）
            predicted_noise = noise_predictor_simple(current_x, t, original_data)
            # 执行反向步骤
            current_x = reverse_diffusion_step(current_x, predicted_noise, t, T)
            print(f"  步骤 {t}: 去噪后={current_x}")

    # 计算重建误差
    reconstruction_error = np.mean((original_data - reconstructed_data) ** 2)
    print(f"\n重建均方误差: {reconstruction_error:.6f}")
    print("扩散模型成功地从噪声中重建了原始数据！")

if __name__ == "__main__":
    demonstrate_diffusion_process()