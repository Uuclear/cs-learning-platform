#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本预处理示例：展示NLP中的基本文本清洗和标准化步骤

本示例演示了从原始文本到可用于机器学习的标准化文本的完整流程，
包括分词、停用词移除、词干提取和词形还原。
"""

import re
import string
from typing import List


def tokenize(text: str) -> List[str]:
    """
    简单的英文分词函数

    Args:
        text: 输入文本

    Returns:
        分词后的词汇列表
    """
    # 转换为小写并移除标点符号
    text = text.lower()
    text = re.sub(r'[' + string.punctuation + ']', ' ', text)
    # 按空格分割并过滤空字符串
    tokens = [token for token in text.split() if token]
    return tokens


def remove_stopwords(tokens: List[str], stopwords: set) -> List[str]:
    """
    移除停用词

    Args:
        tokens: 分词后的词汇列表
        stopwords: 停用词集合

    Returns:
        移除停用词后的词汇列表
    """
    return [token for token in tokens if token not in stopwords]


def stem_word(word: str) -> str:
    """
    简单的词干提取（仅处理常见后缀）

    Args:
        word: 输入单词

    Returns:
        词干形式
    """
    # 处理常见的复数形式
    if word.endswith('ies') and len(word) > 4:
        return word[:-3] + 'y'
    elif word.endswith('es') and len(word) > 3:
        return word[:-2]
    elif word.endswith('s') and len(word) > 2 and not word.endswith('ss'):
        return word[:-1]

    # 处理常见的动词过去式/过去分词
    if word.endswith('ed') and len(word) > 3:
        return word[:-2]
    elif word.endswith('ing') and len(word) > 4:
        return word[:-3]

    return word


def lemmatize_word(word: str) -> str:
    """
    简单的词形还原（基于规则）

    Args:
        word: 输入单词

    Returns:
        词元形式
    """
    # 这里使用一个简化的词形还原字典
    lemma_dict = {
        'am': 'be', 'is': 'be', 'are': 'be', 'was': 'be', 'were': 'be',
        'have': 'have', 'has': 'have', 'had': 'have',
        'go': 'go', 'goes': 'go', 'went': 'go', 'gone': 'go',
        'do': 'do', 'does': 'do', 'did': 'do', 'done': 'do'
    }

    return lemma_dict.get(word, word)


def preprocess_text(text: str, use_stemming: bool = True) -> List[str]:
    """
    完整的文本预处理流程

    Args:
        text: 原始文本
        use_stemming: 是否使用词干提取（否则使用词形还原）

    Returns:
        预处理后的词汇列表
    """
    # 英文停用词集合（简化版）
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
    }

    # 步骤1: 分词
    tokens = tokenize(text)
    print(f"分词结果: {tokens}")

    # 步骤2: 移除停用词
    tokens = remove_stopwords(tokens, stopwords)
    print(f"移除停用词后: {tokens}")

    # 步骤3: 词干提取或词形还原
    if use_stemming:
        tokens = [stem_word(token) for token in tokens]
        print(f"词干提取后: {tokens}")
    else:
        tokens = [lemmatize_word(token) for token in tokens]
        print(f"词形还原后: {tokens}")

    return tokens


if __name__ == "__main__":
    # 测试文本
    sample_text = "The cats are running quickly through the beautiful gardens. They have been playing all day!"

    print("=== 文本预处理演示 ===")
    print(f"原始文本: {sample_text}")
    print("\n--- 使用词干提取 ---")
    result1 = preprocess_text(sample_text, use_stemming=True)

    print("\n--- 使用词形还原 ---")
    result2 = preprocess_text(sample_text, use_stemming=False)

    print(f"\n最终结果 (词干提取): {' '.join(result1)}")
    print(f"最终结果 (词形还原): {' '.join(result2)}")