#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1: MapReduce 词频统计

这是 example-01-mapreduce-simulation.py 的完整解决方案，
包含了更完善的错误处理和性能优化。
"""

from collections import defaultdict
import re
import sys


def map_function(document_id, text):
    """Map 函数：将输入文档分解为 (单词, 1) 的键值对"""
    if not text or not isinstance(text, str):
        return []

    # 使用正则表达式提取单词，转换为小写，过滤空字符串
    words = [word.lower() for word in re.findall(r'\b\w+\b', text) if word.strip()]
    return [(word, 1) for word in words]


def shuffle_and_sort(mapped_data):
    """Shuffle 和 Sort 阶段：将相同键的值分组在一起"""
    if not mapped_data:
        return {}

    shuffled = defaultdict(list)
    for item in mapped_data:
        if len(item) == 2:
            word, count = item
            if isinstance(word, str) and isinstance(count, int):
                shuffled[word].append(count)

    return dict(shuffled)


def reduce_function(word, counts):
    """Reduce 函数：对相同键的所有值进行聚合操作"""
    if not counts:
        return (word, 0)
    return (word, sum(counts))


def mapreduce_simulation(documents):
    """完整的 MapReduce 模拟流程"""
    if not documents:
        return {}

    # Map 阶段
    mapped_results = []
    for doc_id, text in documents.items():
        mapped = map_function(doc_id, text)
        mapped_results.extend(mapped)

    # Shuffle 和 Sort 阶段
    shuffled_data = shuffle_and_sort(mapped_results)

    # Reduce 阶段
    final_results = {}
    for word, counts in shuffled_data.items():
        word, total = reduce_function(word, counts)
        final_results[word] = total

    return final_results


def main():
    # 测试数据
    sample_documents = {
        "doc1": "Hadoop 是一个分布式计算框架，用于处理大数据",
        "doc2": "Spark 比 Hadoop 更快，因为它使用内存计算",
        "doc3": "大数据处理需要分布式系统和并行计算",
        "doc4": "Hadoop 生态系统包括 HDFS、MapReduce 和 YARN"
    }

    word_counts = mapreduce_simulation(sample_documents)

    # 输出结果
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_words:
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()