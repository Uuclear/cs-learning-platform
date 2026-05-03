#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词向量 (Word Embedding) 概念演示

本示例通过共现矩阵和奇异值分解 (SVD) 展示词向量的基本思想，
帮助理解如何将词汇映射到连续的向量空间中。
"""

import math
from typing import List, Dict, Tuple
import numpy as np


def build_cooccurrence_matrix(documents: List[str], window_size: int = 2) -> Tuple[np.ndarray, List[str]]:
    """
    构建词汇共现矩阵

    共现矩阵记录了词汇在指定窗口内共同出现的频率。

    Args:
        documents: 文档列表
        window_size: 上下文窗口大小

    Returns:
        (cooc_matrix, vocab) - 共现矩阵和词汇表
    """
    # 构建词汇表
    all_words = set()
    tokenized_docs = []

    for doc in documents:
        tokens = doc.lower().split()
        tokenized_docs.append(tokens)
        all_words.update(tokens)

    vocab = sorted(list(all_words))
    word_to_idx = {word: idx for idx, word in enumerate(vocab)}
    vocab_size = len(vocab)

    # 初始化共现矩阵
    cooc_matrix = np.zeros((vocab_size, vocab_size))

    # 填充共现矩阵
    for tokens in tokenized_docs:
        for i, word in enumerate(tokens):
            word_idx = word_to_idx[word]
            # 在窗口范围内查找上下文词
            start = max(0, i - window_size)
            end = min(len(tokens), i + window_size + 1)

            for j in range(start, end):
                if i != j:  # 不计算自己与自己的共现
                    context_word = tokens[j]
                    context_idx = word_to_idx[context_word]
                    cooc_matrix[word_idx][context_idx] += 1

    return cooc_matrix, vocab


def apply_svd(matrix: np.ndarray, dim: int = 2) -> np.ndarray:
    """
    应用奇异值分解 (SVD) 降低矩阵维度

    SVD可以将高维的共现矩阵压缩到低维空间，同时保留主要的语义信息。

    Args:
        matrix: 输入矩阵
        dim: 目标维度

    Returns:
        降维后的矩阵
    """
    # 对矩阵进行SVD分解
    U, S, Vt = np.linalg.svd(matrix, full_matrices=False)

    # 保留前dim个奇异值对应的向量
    reduced_matrix = U[:, :dim] * np.sqrt(S[:dim])

    return reduced_matrix


def cosine_similarity_vec(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    计算两个向量的余弦相似度

    Args:
        vec1: 第一个向量
        vec2: 第二个向量

    Returns:
        余弦相似度
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


def find_similar_words(word_vectors: np.ndarray, vocab: List[str], target_word: str, top_k: int = 3) -> List[Tuple[str, float]]:
    """
    找出与目标词最相似的词汇

    Args:
        word_vectors: 词向量矩阵
        vocab: 词汇表
        target_word: 目标词汇
        top_k: 返回最相似的k个词

    Returns:
        相似词列表 [(词, 相似度), ...]
    """
    if target_word not in vocab:
        return []

    target_idx = vocab.index(target_word)
    target_vec = word_vectors[target_idx]

    similarities = []
    for i, word in enumerate(vocab):
        if word != target_word:
            sim = cosine_similarity_vec(target_vec, word_vectors[i])
            similarities.append((word, sim))

    # 按相似度排序并返回前k个
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]


if __name__ == "__main__":
    # 示例文本（模拟一个小语料库）
    documents = [
        "猫 喜欢 吃 鱼",
        "狗 喜欢 玩 球",
        "鱼 生活 在 水里",
        "猫 和 狗 都是 宠物",
        "宠物 需要 照顾",
        "水里 有 很多 鱼"
    ]

    print("=== 词向量概念演示 ===")
    print("语料库:")
    for doc in documents:
        print(f"  {doc}")

    # 构建共现矩阵
    cooc_matrix, vocab = build_cooccurrence_matrix(documents, window_size=2)
    print(f"\n词汇表: {vocab}")
    print("\n共现矩阵:")
    print("     ", end="")
    for word in vocab:
        print(f"{word:>6}", end="")
    print()

    for i, word in enumerate(vocab):
        print(f"{word:>4}:", end="")
        for j in range(len(vocab)):
            print(f"{int(cooc_matrix[i][j]):>6}", end="")
        print()

    # 应用SVD降维
    print("\n=== 应用SVD降维到2维 ===")
    word_vectors = apply_svd(cooc_matrix, dim=2)

    print("词向量 (2维):")
    for i, word in enumerate(vocab):
        vec = word_vectors[i]
        print(f"  {word}: [{vec[0]:.3f}, {vec[1]:.3f}]")

    # 查找相似词
    print("\n=== 相似词查找 ===")
    test_words = ["猫", "狗", "鱼"]
    for word in test_words:
        similar_words = find_similar_words(word_vectors, vocab, word, top_k=2)
        print(f"'{word}' 的相似词: {similar_words}")

    # 演示向量运算（简化版）
    print("\n=== 向量运算演示 ===")
    # 注意：由于我们的语料库很小，这里的结果可能不理想
    # 但在大型语料库上，"国王 - 男人 + 女人 ≈ 女王" 这样的关系会显现出来

    if "猫" in vocab and "狗" in vocab:
        cat_idx = vocab.index("猫")
        dog_idx = vocab.index("狗")
        cat_vec = word_vectors[cat_idx]
        dog_vec = word_vectors[dog_idx]

        # 计算平均向量作为"宠物"的表示
        pet_vec = (cat_vec + dog_vec) / 2
        print(f"'猫' 和 '狗' 的平均向量: [{pet_vec[0]:.3f}, {pet_vec[1]:.3f}]")

        # 找出最接近这个平均向量的词
        similarities = []
        for i, word in enumerate(vocab):
            if word not in ["猫", "狗"]:
                sim = cosine_similarity_vec(pet_vec, word_vectors[i])
                similarities.append((word, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        print(f"最接近'宠物'概念的词: {similarities[0] if similarities else '无'}")