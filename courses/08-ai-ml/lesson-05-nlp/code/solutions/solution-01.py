#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情感分析分类器实现：使用TF-IDF + 逻辑回归

本解决方案实现了基于TF-IDF特征和逻辑回归的情感分析分类器，
仅使用numpy和标准库，不依赖机器学习框架。
"""

import math
import random
from typing import List, Dict, Tuple
import numpy as np


class SimpleLogisticRegression:
    """简单的逻辑回归实现"""

    def __init__(self, learning_rate: float = 0.01, max_iterations: int = 1000):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.weights = None
        self.bias = 0.0

    def sigmoid(self, z: np.ndarray) -> np.ndarray:
        """Sigmoid激活函数"""
        # 防止数值溢出
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def fit(self, X: np.ndarray, y: np.ndarray):
        """训练模型"""
        n_samples, n_features = X.shape

        # 初始化参数
        self.weights = np.zeros(n_features)
        self.bias = 0.0

        # 梯度下降
        for _ in range(self.max_iterations):
            # 前向传播
            linear_output = np.dot(X, self.weights) + self.bias
            predictions = self.sigmoid(linear_output)

            # 计算梯度
            dw = (1 / n_samples) * np.dot(X.T, (predictions - y))
            db = (1 / n_samples) * np.sum(predictions - y)

            # 更新参数
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """预测概率"""
        linear_output = np.dot(X, self.weights) + self.bias
        return self.sigmoid(linear_output)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """预测类别"""
        probabilities = self.predict_proba(X)
        return (probabilities >= 0.5).astype(int)


def calculate_tf_idf_features(documents: List[str], vocab: List[str]) -> np.ndarray:
    """计算TF-IDF特征矩阵"""
    # 分词
    tokenized_docs = []
    for doc in documents:
        tokens = doc.lower().split()
        tokenized_docs.append(tokens)

    # 计算IDF
    idf_dict = {}
    total_docs = len(documents)
    all_words = set(vocab)

    for word in all_words:
        containing_docs = sum(1 for doc in tokenized_docs if word in doc)
        idf_dict[word] = math.log(total_docs / containing_docs) if containing_docs > 0 else 0

    # 构建特征矩阵
    feature_matrix = np.zeros((len(documents), len(vocab)))

    for doc_idx, tokens in enumerate(tokenized_docs):
        # 计算词频
        word_count = {}
        for token in tokens:
            if token in all_words:
                word_count[token] = word_count.get(token, 0) + 1

        total_tokens = len([t for t in tokens if t in all_words])

        # 计算TF-IDF
        for word_idx, word in enumerate(vocab):
            if total_tokens > 0 and word in word_count:
                tf = word_count[word] / total_tokens
                tfidf = tf * idf_dict[word]
                feature_matrix[doc_idx][word_idx] = tfidf

    return feature_matrix


def build_sentiment_analyzer() -> Tuple[SimpleLogisticRegression, List[str]]:
    """构建情感分析器（使用模拟训练数据）"""
    # 创建模拟的训练数据
    positive_texts = [
        "这个产品很棒 很好用",
        "服务非常出色 我很满意",
        "质量很好 价格合理",
        "体验极佳 强烈推荐",
        "功能强大 使用方便"
    ]

    negative_texts = [
        "这个产品很差 很难用",
        "服务非常糟糕 我很失望",
        "质量很差 价格太贵",
        "体验极差 不推荐",
        "功能弱小 使用困难"
    ]

    # 构建词汇表
    all_texts = positive_texts + negative_texts
    vocab_set = set()
    for text in all_texts:
        vocab_set.update(text.lower().split())
    vocab = sorted(list(vocab_set))

    # 准备训练数据
    train_documents = all_texts
    train_labels = [1] * len(positive_texts) + [0] * len(negative_texts)

    # 计算TF-IDF特征
    X_train = calculate_tf_idf_features(train_documents, vocab)
    y_train = np.array(train_labels)

    # 训练模型
    model = SimpleLogisticRegression(learning_rate=0.1, max_iterations=2000)
    model.fit(X_train, y_train)

    return model, vocab


def predict_sentiment(model: SimpleLogisticRegression, vocab: List[str], text: str) -> Tuple[str, float]:
    """预测文本情感"""
    # 计算特征
    X_test = calculate_tf_idf_features([text], vocab)
    probability = model.predict_proba(X_test)[0]
    sentiment = "正面" if probability >= 0.5 else "负面"
    confidence = probability if probability >= 0.5 else 1 - probability

    return sentiment, confidence


if __name__ == "__main__":
    print("=== 情感分析分类器演示 ===")

    # 构建分类器
    model, vocab = build_sentiment_analyzer()
    print(f"词汇表大小: {len(vocab)}")
    print(f"词汇表: {vocab}")

    # 测试示例
    test_texts = [
        "这个手机非常好用 功能强大",
        "产品质量很差 完全不值得购买",
        "一般般吧 没有什么特别的",
        "服务态度极好 解决问题很快"
    ]

    print("\n=== 情感预测结果 ===")
    for text in test_texts:
        sentiment, confidence = predict_sentiment(model, vocab, text)
        print(f"文本: '{text}'")
        print(f"情感: {sentiment} (置信度: {confidence:.3f})")
        print("-" * 40)