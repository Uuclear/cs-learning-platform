#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：从零实现简单的注意力机制

这个脚本实现了完整的自注意力机制，
包括多头注意力的简化版本。
"""

import numpy as np


class SimpleAttention:
    """简单的注意力机制实现"""

    def __init__(self, d_model, d_k=None, d_v=None):
        """
        初始化注意力层

        Args:
            d_model: 模型维度
            d_k: Key的维度（默认等于d_model）
            d_v: Value的维度（默认等于d_model）
        """
        self.d_model = d_model
        self.d_k = d_k if d_k is not None else d_model
        self.d_v = d_v if d_v is not None else d_model

        # 初始化权重矩阵（在实际Transformer中，这些是可学习的参数）
        self.W_q = np.random.randn(d_model, self.d_k) * 0.1
        self.W_k = np.random.randn(d_model, self.d_k) * 0.1
        self.W_v = np.random.randn(d_model, self.d_v) * 0.1

    def softmax(self, x, axis=-1):
        """数值稳定的softmax函数"""
        x = x - np.max(x, axis=axis, keepdims=True)
        exp_x = np.exp(x)
        return exp_x / np.sum(exp_x, axis=axis, keepdims=True)

    def forward(self, x):
        """
        前向传播计算注意力

        Args:
            x: 输入张量 [batch_size, seq_len, d_model]

        Returns:
            注意力输出 [batch_size, seq_len, d_v]
        """
        batch_size, seq_len, d_model = x.shape

        # 线性变换得到Q, K, V
        Q = np.dot(x, self.W_q)  # [batch_size, seq_len, d_k]
        K = np.dot(x, self.W_k)  # [batch_size, seq_len, d_k]
        V = np.dot(x, self.W_v)  # [batch_size, seq_len, d_v]

        # 计算注意力分数
        scores = np.matmul(Q, K.transpose(0, 2, 1))  # [batch_size, seq_len, seq_len]
        scores = scores / np.sqrt(self.d_k)

        # 应用softmax得到注意力权重
        attention_weights = self.softmax(scores, axis=-1)

        # 加权求和
        output = np.matmul(attention_weights, V)  # [batch_size, seq_len, d_v]

        return output, attention_weights


class MultiHeadAttention:
    """多头注意力机制的简化实现"""

    def __init__(self, d_model, num_heads):
        """
        初始化多头注意力

        Args:
            d_model: 模型维度
            num_heads: 注意力头的数量
        """
        assert d_model % num_heads == 0, "d_model必须能被num_heads整除"

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.d_v = d_model // num_heads

        # 为每个头创建独立的注意力层
        self.heads = [SimpleAttention(d_model, self.d_k, self.d_v) for _ in range(num_heads)]

        # 输出投影矩阵
        self.W_o = np.random.randn(d_model, d_model) * 0.1

    def forward(self, x):
        """
        多头注意力前向传播

        Args:
            x: 输入张量 [batch_size, seq_len, d_model]

        Returns:
            多头注意力输出 [batch_size, seq_len, d_model]
        """
        # 并行计算所有头的输出
        head_outputs = []
        all_weights = []

        for head in self.heads:
            head_output, head_weights = head.forward(x)
            head_outputs.append(head_output)
            all_weights.append(head_weights)

        # 拼接所有头的输出
        concatenated = np.concatenate(head_outputs, axis=-1)  # [batch_size, seq_len, d_model]

        # 最终线性变换
        output = np.dot(concatenated, self.W_o)

        return output, all_weights


def main():
    """主函数：演示注意力机制实现"""
    print("🎯 解决方案1：从零实现注意力机制\n")
    print("=" * 60)

    # 设置随机种子
    np.random.seed(42)

    # 创建测试数据
    batch_size = 2
    seq_len = 4
    d_model = 8

    print(f"测试参数:")
    print(f"  批次大小: {batch_size}")
    print(f"  序列长度: {seq_len}")
    print(f"  模型维度: {d_model}\n")

    # 生成随机输入
    x = np.random.randn(batch_size, seq_len, d_model)
    print(f"输入形状: {x.shape}")

    # 测试单头注意力
    print("\n--- 单头注意力测试 ---")
    single_head = SimpleAttention(d_model)
    output_single, weights_single = single_head.forward(x)
    print(f"单头输出形状: {output_single.shape}")
    print(f"注意力权重形状: {weights_single.shape}")

    # 测试多头注意力
    print("\n--- 多头注意力测试 ---")
    num_heads = 4
    multi_head = MultiHeadAttention(d_model, num_heads)
    output_multi, weights_multi = multi_head.forward(x)
    print(f"多头输出形状: {output_multi.shape}")
    print(f"头数量: {len(weights_multi)}")
    print(f"每个头的权重形状: {weights_multi[0].shape}")

    # 验证输出维度正确
    assert output_single.shape == (batch_size, seq_len, d_model)
    assert output_multi.shape == (batch_size, seq_len, d_model)

    print("\n✅ 注意力机制实现验证通过！")
    print("\n关键理解:")
    print("1. 自注意力让序列中的每个位置都能关注其他所有位置")
    print("2. 多头注意力允许模型同时关注不同子空间的信息")
    print("3. 线性变换（W_q, W_k, W_v）将输入映射到查询、键、值空间")
    print("4. 缩放因子防止梯度消失问题")


if __name__ == "__main__":
    main()