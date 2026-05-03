#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单拼写检查器实现：使用编辑距离和n-gram语言模型

本解决方案实现了基于编辑距离的拼写纠正和基于n-gram的
语言模型来选择最可能的纠正结果。
"""

import math
from typing import List, Dict, Set, Tuple


def edit_distance(str1: str, str2: str) -> int:
    """
    计算两个字符串之间的编辑距离（Levenshtein距离）

    编辑距离是指将一个字符串转换为另一个字符串所需的最少编辑操作次数，
    编辑操作包括：插入、删除、替换。

    Args:
        str1: 第一个字符串
        str2: 第二个字符串

    Returns:
        编辑距离
    """
    m, n = len(str1), len(str2)

    # 创建DP表
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 初始化边界条件
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # 填充DP表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # 删除
                    dp[i][j - 1],      # 插入
                    dp[i - 1][j - 1]   # 替换
                )

    return dp[m][n]


def generate_candidates(word: str, vocab: Set[str], max_distance: int = 2) -> List[str]:
    """
    生成候选纠正词

    Args:
        word: 错误的单词
        vocab: 词汇表
        max_distance: 最大允许的编辑距离

    Returns:
        候选词列表
    """
    candidates = []
    for vocab_word in vocab:
        dist = edit_distance(word, vocab_word)
        if dist <= max_distance:
            candidates.append(vocab_word)
    return candidates


def build_ngram_model(documents: List[str], n: int = 2) -> Dict[str, Dict[str, int]]:
    """
    构建n-gram语言模型

    Args:
        documents: 文档列表
        n: n-gram的阶数

    Returns:
        n-gram模型 {前缀: {后缀: 频次}}
    """
    model = {}

    for doc in documents:
        tokens = doc.lower().split()
        # 添加开始和结束标记
        tokens = ['<s>'] * (n - 1) + tokens + ['</s>']

        for i in range(len(tokens) - n + 1):
            prefix = ' '.join(tokens[i:i + n - 1])
            suffix = tokens[i + n - 1]

            if prefix not in model:
                model[prefix] = {}
            model[prefix][suffix] = model[prefix].get(suffix, 0) + 1

    return model


def calculate_sentence_probability(sentence: str, ngram_model: Dict[str, Dict[str, int]], n: int = 2) -> float:
    """
    计算句子的概率（使用n-gram模型）

    Args:
        sentence: 输入句子
        ngram_model: n-gram模型
        n: n-gram的阶数

    Returns:
        句子的对数概率
    """
    tokens = sentence.lower().split()
    tokens = ['<s>'] * (n - 1) + tokens + ['</s>']

    log_prob = 0.0
    total_count = 0

    for i in range(len(tokens) - n + 1):
        prefix = ' '.join(tokens[i:i + n - 1])
        suffix = tokens[i + n - 1]

        if prefix in ngram_model and suffix in ngram_model[prefix]:
            # 计算条件概率 P(suffix | prefix)
            suffix_count = ngram_model[prefix][suffix]
            prefix_total = sum(ngram_model[prefix].values())
            prob = suffix_count / prefix_total
            log_prob += math.log(prob)
            total_count += 1
        else:
            # 未登录n-gram，使用平滑处理（这里简单返回很小的概率）
            log_prob += math.log(1e-10)

    return log_prob if total_count > 0 else float('-inf')


def spell_check_and_correct(text: str, vocab: Set[str], ngram_model: Dict[str, Dict[str, int]]) -> str:
    """
    拼写检查和纠正

    Args:
        text: 输入文本
        vocab: 词汇表
        ngram_model: n-gram语言模型

    Returns:
        纠正后的文本
    """
    tokens = text.split()
    corrected_tokens = []

    for token in tokens:
        word = token.lower()
        punctuation = ''

        # 分离标点符号
        if word and word[-1] in '.,!?;:':
            punctuation = word[-1]
            word = word[:-1]

        if word in vocab or len(word) <= 2:
            # 单词在词汇表中或很短，直接保留
            corrected_tokens.append(token)
        else:
            # 生成候选词
            candidates = generate_candidates(word, vocab, max_distance=2)

            if not candidates:
                # 没有找到候选词，保留原词
                corrected_tokens.append(token)
            else:
                # 使用语言模型选择最佳候选
                best_candidate = None
                best_score = float('-inf')

                # 构建上下文（简单的前后词）
                context_before = corrected_tokens[-1].lower() if corrected_tokens else '<s>'
                context_after = tokens[tokens.index(token) + 1].lower() if tokens.index(token) + 1 < len(tokens) else '</s>'

                for candidate in candidates:
                    # 尝试不同的上下文组合
                    test_sentences = [
                        f"{context_before} {candidate}",
                        f"{candidate} {context_after}",
                        f"{context_before} {candidate} {context_after}"
                    ]

                    for test_sent in test_sentences:
                        score = calculate_sentence_probability(test_sent, ngram_model, n=2)
                        if score > best_score:
                            best_score = score
                            best_candidate = candidate

                if best_candidate:
                    corrected_word = best_candidate + punctuation
                    # 保持原始大小写
                    if token and token[0].isupper():
                        corrected_word = corrected_word.capitalize()
                    corrected_tokens.append(corrected_word)
                else:
                    corrected_tokens.append(token)

    return ' '.join(corrected_tokens)


def create_vocabulary_and_model() -> Tuple[Set[str], Dict[str, Dict[str, int]]]:
    """创建词汇表和语言模型（基于模拟数据）"""
    # 模拟训练语料
    training_docs = [
        "这是一个很好的例子",
        "自然语言处理很有趣",
        "机器学习是人工智能的重要分支",
        "深度学习使用神经网络",
        "文本分类是常见的NLP任务",
        "情感分析可以判断文本倾向",
        "命名实体识别很有用",
        "拼写检查帮助纠正错误"
    ]

    # 构建词汇表
    vocab = set()
    for doc in training_docs:
        vocab.update(doc.lower().split())

    # 构建二元语法模型
    ngram_model = build_ngram_model(training_docs, n=2)

    return vocab, ngram_model


if __name__ == "__main__":
    print("=== 拼写检查器演示 ===")

    # 创建词汇表和语言模型
    vocab, ngram_model = create_vocabulary_and_model()
    print(f"词汇表大小: {len(vocab)}")
    print(f"词汇表: {sorted(vocab)}")

    # 测试示例（包含一些拼写错误）
    test_texts = [
        "这是一个狠好的例子",  # "狠" 应该是 "很"
        "自然语言出来很有趣",  # "出来" 应该是 "处理"
        "机器学期是人工智能的重要分支",  # "学期" 应该是 "学习"
        "深度学期使用神经网络",  # "学期" 应该是 "学习"
        "文本分雷是常见的NLP任务"  # "分雷" 应该是 "分类"
    ]

    print("\n=== 拼写纠正结果 ===")
    for text in test_texts:
        corrected = spell_check_and_correct(text, vocab, ngram_model)
        print(f"原文: {text}")
        print(f"纠正: {corrected}")
        print("-" * 40)