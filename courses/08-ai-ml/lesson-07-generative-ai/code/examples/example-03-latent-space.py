#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：潜在空间（Latent Space）插值演示

这个示例演示了生成模型中潜在空间的概念：
- 潜在向量：生成模型的输入，控制生成内容的特征
- 插值：在两个潜在向量之间进行线性插值
- 生成结果：展示插值过程中生成内容的平滑过渡

预期输出：
潜在向量A: [z1, z2, ..., zn]
潜在向量B: [z1, z2, ..., zn]
插值系数 0.0: 生成结果=[...]
插值系数 0.25: 生成结果=[...]
插值系数 0.5: 生成结果=[...]
插值系数 0.75: 生成结果=[...]
插值系数 1.0: 生成结果=[...]

可以看到随着插值系数的变化，生成结果平滑地从A过渡到B。
"""

import numpy as np

def simple_generator(latent_vector):
    """简单的生成器函数 - 将潜在向量映射到数据空间"""
    # 这是一个简化的生成器，实际中会是复杂的神经网络
    # 使用正弦和余弦函数创建有趣的模式
    x = np.linspace(0, 2*np.pi, 10)
    amplitude = latent_vector[0] if len(latent_vector) > 0 else 1.0
    frequency = latent_vector[1] if len(latent_vector) > 1 else 1.0
    phase = latent_vector[2] if len(latent_vector) > 2 else 0.0

    return amplitude * np.sin(frequency * x + phase)

def interpolate_latent_vectors(z_a, z_b, alpha):
    """在两个潜在向量之间进行线性插值"""
    return (1 - alpha) * z_a + alpha * z_b

def demonstrate_latent_interpolation():
    """演示潜在空间插值"""
    np.random.seed(42)

    # 创建两个不同的潜在向量
    z_a = np.array([1.0, 1.0, 0.0])   # 幅度=1, 频率=1, 相位=0
    z_b = np.array([0.5, 2.0, np.pi/2])  # 幅度=0.5, 频率=2, 相位=π/2

    print(f"潜在向量A: {z_a}")
    print(f"潜在向量B: {z_b}")

    # 定义插值系数
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]

    print("\n插值结果:")
    for alpha in alphas:
        # 插值潜在向量
        z_interp = interpolate_latent_vectors(z_a, z_b, alpha)

        # 生成对应的数据
        generated = simple_generator(z_interp)

        print(f"插值系数 {alpha}: 生成结果={generated[:3]}...")  # 只显示前3个值

    print("\n潜在空间插值展示了生成模型的连续性和可控性！")
    print("通过在潜在空间中移动，我们可以平滑地控制生成内容的特征。")

def explore_latent_space_properties():
    """探索潜在空间的其他性质"""
    print("\n=== 潜在空间性质探索 ===")

    # 1. 随机采样
    print("1. 随机潜在向量生成:")
    for i in range(3):
        random_z = np.random.normal(0, 1, 3)
        result = simple_generator(random_z)
        print(f"   随机样本 {i+1}: {result[:3]}...")

    # 2. 潜在向量算术
    print("\n2. 潜在向量算术 (概念演示):")
    z_smile = np.array([1.2, 0.8, 0.1])   # 假设代表"微笑"
    z_serious = np.array([0.8, 1.2, -0.1])  # 假设代表"严肃"
    z_average = (z_smile + z_serious) / 2   # 平均表情

    smile_result = simple_generator(z_smile)
    serious_result = simple_generator(z_serious)
    average_result = simple_generator(z_average)

    print(f"   微笑: {smile_result[:3]}...")
    print(f"   严肃: {serious_result[:3]}...")
    print(f"   平均: {average_result[:3]}...")

if __name__ == "__main__":
    demonstrate_latent_interpolation()
    explore_latent_space_properties()