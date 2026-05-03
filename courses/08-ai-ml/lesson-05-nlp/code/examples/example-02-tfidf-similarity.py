#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TF-IDF向量化和文档相似度计算示例

本示例展示了如何使用TF-IDF将文本转换为向量表示，
并计算文档之间的余弦相似度。
"""

import math
from typing import List, Dict, Tuple


def calculate_tf(doc_tokens: List[str]) -> Dict[str, float]:
    """
    计算词频 (Term Frequency)

    TF(t) = (词t在文档中出现的次数) / (文档中的总词数)

    Args:
        doc_tokens: 文档的分词列表

    Returns:
        词频字典 {词: TF值}
    """
    tf_dict = {}
    total_tokens = len(doc_tokens)

    # 统计每个词的出现次数
    word_count = {}
    for token in doc_tokens:
        word_count[token] = word_count.get(token, 0) + 1

    # 计算TF值
    for word, count in word_count.items():
        tf_dict[word] = count / total_tokens

    return tf_dict


def calculate_idf(documents: List[List[str]]) -> Dict[str, float]:
    """
    计算逆文档频率 (Inverse Document Frequency)

    IDF(t) = log(总文档数 / 包含词t的文档数)

    Args:
        documents: 所有文档的分词列表

    Returns:
        IDF字典 {词: IDF值}
    """
    idf_dict = {}
    total_docs = len(documents)

    # 获取所有唯一词汇
    all_words = set()
    for doc in documents:
        all_words.update(doc)

    # 计算每个词的IDF
    for word in all_words:
        containing_docs = sum(1 for doc in documents if word in doc)
        idf_dict[word] = math.log(total_docs / containing_docs)

    return idf_dict


def calculate_tfidf(tf_dict: Dict[str, float], idf_dict: Dict[str, float]) -> Dict[str, float]:
    """
    计算TF-IDF值

    TF-IDF(t) = TF(t) * IDF(t)

    Args:
        tf_dict: 词频字典
        idf_dict: 逆文档频率字典

    Returns:
        TF-IDF字典 {词: TF-IDF值}
    """
    tfidf_dict = {}
    for word in tf_dict:
        tfidf_dict[word] = tf_dict[word] * idf_dict.get(word, 0)
    return tfidf_dict


def vectorize_documents(documents: List[str]) -> Tuple[List[Dict[str, float]], List[str]]:
    """
    将文档集合转换为TF-IDF向量

    Args:
        documents: 原始文档列表

    Returns:
        (tfidf_vectors, vocabulary) - TF-IDF向量列表和词汇表
    """
    # 预处理：简单分词（转换为小写并按空格分割）
    tokenized_docs = []
    for doc in documents:
        tokens = doc.lower().split()
        tokenized_docs.append(tokens)

    # 计算IDF（基于所有文档）
    idf_dict = calculate_idf(tokenized_docs)

    # 为每个文档计算TF-IDF
    tfidf_vectors = []
    for tokens in tokenized_docs:
        tf_dict = calculate_tf(tokens)
        tfidf_dict = calculate_tfidf(tf_dict, idf_dict)
        tfidf_vectors.append(tfidf_dict)

    # 构建词汇表
    vocabulary = sorted(set(word for doc in tokenized_docs for word in doc))

    return tfidf_vectors, vocabulary


def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """
    计算两个向量的余弦相似度

    cos(θ) = (A·B) / (||A|| * ||B||)

    Args:
        vec1: 第一个向量（字典形式）
        vec2: 第二个向量（字典形式）

    Returns:
        余弦相似度值 [0, 1]
    """
    # 获取所有共同的词汇
    all_words = set(vec1.keys()) | set(vec2.keys())

    # 计算点积
    dot_product = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in all_words)

    # 计算向量的模长
    norm1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    norm2 = math.sqrt(sum(val ** 2 for val in vec2.values()))

    # 避免除零错误
    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


if __name__ == "__main__":
    # 示例文档
    documents = [
        "机器学习是人工智能的重要分支",
        "深度学习使用神经网络进行模式识别",
        "自然语言处理让计算机理解人类语言",
        "机器学习算法可以从数据中学习规律"
    ]

    print("=== TF-IDF 文档相似度计算演示 ===")
    print("文档集合:")
    for i, doc in enumerate(documents):
        print(f"文档 {i+1}: {doc}")

    # 转换为TF-IDF向量
    tfidf_vectors, vocab = vectorize_documents(documents)
    print(f"\n词汇表: {vocab}")
    print("\nTF-IDF 向量:")
    for i, vec in enumerate(tfidf_vectors):
        print(f"文档 {i+1}: {vec}")

    # 计算文档间相似度
    print("\n=== 文档相似度矩阵 ===")
    for i in range(len(documents)):
        similarities = []
        for j in range(len(documents)):
            sim = cosine_similarity(tfidf_vectors[i], tfidf_vectors[j])
            similarities.append(f"{sim:.3f}")
        print(f"文档 {i+1}: [{', '.join(similarities)}]")

    # 找出最相似的文档对
    max_sim = 0
    best_pair = (0, 0)
    for i in range(len(documents)):
        for j in range(i + 1, len(documents)):
            sim = cosine_similarity(tfidf_vectors[i], tfidf_vectors[j])
            if sim > max_sim:
                max_sim = sim
                best_pair = (i, j)

    print(f"\n最相似的文档对: 文档 {best_pair[0]+1} 和 文档 {best_pair[1]+1}")
    print(f"相似度: {max_sim:.3f}")