#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
额外练习解决方案：VAE（变分自编码器）实现

这个解决方案实现了变分自编码器的核心组件：
- 编码器：将数据映射到潜在空间的均值和方差
- 解码器：从潜在向量重建数据
- 重参数化技巧：实现可微分的采样
"""

import numpy as np

class VAE:
    """变分自编码器"""
    def __init__(self, input_dim=784, latent_dim=20, hidden_dim=400):
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim

        # 编码器参数
        self.enc_W1 = np.random.normal(0, 0.01, (input_dim, hidden_dim))
        self.enc_b1 = np.zeros((1, hidden_dim))
        self.enc_W2_mu = np.random.normal(0, 0.01, (hidden_dim, latent_dim))
        self.enc_b2_mu = np.zeros((1, latent_dim))
        self.enc_W2_logvar = np.random.normal(0, 0.01, (hidden_dim, latent_dim))
        self.enc_b2_logvar = np.zeros((1, latent_dim))

        # 解码器参数
        self.dec_W1 = np.random.normal(0, 0.01, (latent_dim, hidden_dim))
        self.dec_b1 = np.zeros((1, hidden_dim))
        self.dec_W2 = np.random.normal(0, 0.01, (hidden_dim, input_dim))
        self.dec_b2 = np.zeros((1, input_dim))

    def encode(self, x):
        """编码器：输出潜在空间的均值和对数方差"""
        h = np.tanh(np.dot(x, self.enc_W1) + self.enc_b1)
        mu = np.dot(h, self.enc_W2_mu) + self.enc_b2_mu
        logvar = np.dot(h, self.enc_W2_logvar) + self.enc_b2_logvar
        return mu, logvar

    def reparameterize(self, mu, logvar):
        """重参数化技巧：从N(mu, var)采样"""
        std = np.exp(0.5 * logvar)
        eps = np.random.normal(0, 1, std.shape)
        return mu + eps * std

    def decode(self, z):
        """解码器：从潜在向量重建数据"""
        h = np.tanh(np.dot(z, self.dec_W1) + self.dec_b1)
        x_recon = np.sigmoid(np.dot(h, self.dec_W2) + self.dec_b2)
        return x_recon

    def forward(self, x):
        """完整前向传播"""
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decode(z)
        return x_recon, mu, logvar

    def loss_function(self, x, x_recon, mu, logvar):
        """VAE损失函数：重构损失 + KL散度"""
        # 重构损失（二元交叉熵）
        recon_loss = -np.sum(x * np.log(x_recon + 1e-8) + (1 - x) * np.log(1 - x_recon + 1e-8), axis=1)

        # KL散度
        kl_div = -0.5 * np.sum(1 + logvar - mu**2 - np.exp(logvar), axis=1)

        return np.mean(recon_loss + kl_div)

def demonstrate_vae():
    """演示VAE的工作原理"""
    np.random.seed(42)

    # 创建简单的二值数据（模拟MNIST）
    input_dim = 16  # 4x4图像
    batch_size = 5
    x = np.random.binomial(1, 0.5, (batch_size, input_dim)).astype(np.float32)

    vae = VAE(input_dim=input_dim, latent_dim=4, hidden_dim=8)

    print("原始数据:")
    for i in range(batch_size):
        print(f"  样本 {i+1}: {x[i]}")

    # 前向传播
    x_recon, mu, logvar = vae.forward(x)

    print(f"\n潜在空间均值:\n{mu}")
    print(f"\n潜在空间对数方差:\n{logvar}")

    print("\n重建数据:")
    for i in range(batch_size):
        print(f"  重建 {i+1}: {x_recon[i]}")

    # 计算损失
    loss = vae.loss_function(x, x_recon, mu, logvar)
    print(f"\nVAE损失: {loss:.4f}")

    # 潜在空间插值
    print("\n=== 潜在空间插值 ===")
    z1 = vae.reparameterize(mu[0:1], logvar[0:1])
    z2 = vae.reparameterize(mu[1:2], logvar[1:2])

    alphas = [0.0, 0.5, 1.0]
    for alpha in alphas:
        z_interp = (1 - alpha) * z1 + alpha * z2
        x_interp = vae.decode(z_interp)
        print(f"插值 {alpha}: {x_interp[0][:4]}...")

if __name__ == "__main__":
    demonstrate_vae()