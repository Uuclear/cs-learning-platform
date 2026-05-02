#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：Transformer基础 - 注意力机制演示

这个脚本演示了注意力机制的核心计算过程，
只使用NumPy实现，帮助理解Transformer的工作原理。
"""

import numpy as np


def softmax(x, axis=-1):
    """
    计算softmax函数

    Args:
        x: 输入数组
        axis: 计算softmax的轴，默认为最后一个维度

    Returns:
        softmax后的数组
    """
    # 为了数值稳定性，减去最大值
    x = x - np.max(x, axis=axis, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)


def scaled_dot_product_attention(query, key, value):
    """
    缩放点积注意力机制的实现

    Args:
        query: 查询矩阵 [序列长度, 特征维度]
        key: 键矩阵 [序列长度, 特征维度]
        value: 值矩阵 [序列长度, 特征维度]

    Returns:
        注意力输出 [序列长度, 特征维度]
    """
    # 获取特征维度
    d_k = query.shape[-1]

    # 计算注意力分数: Q * K^T / sqrt(d_k)
    attention_scores = np.dot(query, key.T) / np.sqrt(d_k)
    print(f"注意力分数矩阵:\n{attention_scores}\n")

    # 应用softmax得到注意力权重
    attention_weights = softmax(attention_scores, axis=-1)
    print(f"注意力权重矩阵:\n{attention_weights}\n")

    # 加权求和: 权重 * 值
    output = np.dot(attention_weights, value)
    return output


def main():
    """主函数：演示注意力机制"""
    print("🚀 示例1：Transformer基础 - 注意力机制演示\n")
    print("=" * 60)

    # 设置随机种子以确保结果可重现
    np.random.seed(42)

    # 定义序列长度和特征维度
    seq_len = 3  # 序列长度（例如：3个词）
    d_model = 4  # 特征维度

    print(f"序列长度: {seq_len}")
    print(f"特征维度: {d_model}\n")

    # 创建简单的输入数据（模拟词嵌入）
    # 在实际应用中，这些会是经过嵌入层处理的向量
    query = np.random.randn(seq_len, d_model)
    key = np.random.randn(seq_len, d_model)
    value = np.random.randn(seq_len, d_model)

    print("输入数据:")
    print(f"Query:\n{query}\n")
    print(f"Key:\n{key}\n")
    print(f"Value:\n{value}\n")

    # 执行注意力机制
    print("执行注意力机制计算...")
    output = scaled_dot_product_attention(query, key, value)

    print("最终输出:")
    print(output)
    print("\n" + "=" * 60)
    print("✅ 注意力机制演示完成！")
    print("\n关键要点:")
    print("1. 注意力机制让每个位置都能关注序列中的其他位置")
    print("2. Query-Key相似度决定了注意力权重")
    print("3. 权重用于对Value进行加权求和")
    print("4. 缩放因子sqrt(d_k)防止梯度消失")


if __name__ == "__main__":
    main()