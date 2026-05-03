#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1: MapReduce 模拟 - 词频统计

这个脚本模拟了 Hadoop MapReduce 的工作流程，展示了如何处理大规模文本数据。
MapReduce 是 Hadoop 的核心编程模型，包含两个主要阶段：Map 和 Reduce。
"""

from collections import defaultdict
import re


def map_function(document_id, text):
    """
    Map 函数：将输入文档分解为 (单词, 1) 的键值对

    Args:
        document_id: 文档标识符
        text: 文档文本内容

    Returns:
        list: 包含 (word, 1) 元组的列表
    """
    # 使用正则表达式提取单词，转换为小写
    words = re.findall(r'\b\w+\b', text.lower())
    return [(word, 1) for word in words]


def shuffle_and_sort(mapped_data):
    """
    Shuffle 和 Sort 阶段：将相同键的值分组在一起

    Args:
        mapped_data: Map 阶段输出的键值对列表

    Returns:
        dict: 键为单词，值为计数列表的字典
    """
    shuffled = defaultdict(list)
    for word, count in mapped_data:
        shuffled[word].append(count)
    return dict(shuffled)


def reduce_function(word, counts):
    """
    Reduce 函数：对相同键的所有值进行聚合操作

    Args:
        word: 单词（键）
        counts: 计数列表（值）

    Returns:
        tuple: (word, total_count)
    """
    total_count = sum(counts)
    return (word, total_count)


def mapreduce_simulation(documents):
    """
    完整的 MapReduce 模拟流程

    Args:
        documents: 文档字典 {doc_id: text}

    Returns:
        dict: 词频统计结果 {word: count}
    """
    print("=== MapReduce 词频统计模拟 ===")

    # Step 1: Map 阶段
    print("1. 执行 Map 阶段...")
    mapped_results = []
    for doc_id, text in documents.items():
        mapped = map_function(doc_id, text)
        mapped_results.extend(mapped)
        print(f"   文档 {doc_id}: 生成 {len(mapped)} 个键值对")

    # Step 2: Shuffle 和 Sort 阶段
    print("2. 执行 Shuffle 和 Sort 阶段...")
    shuffled_data = shuffle_and_sort(mapped_results)
    print(f"   分组后得到 {len(shuffled_data)} 个唯一单词")

    # Step 3: Reduce 阶段
    print("3. 执行 Reduce 阶段...")
    final_results = {}
    for word, counts in shuffled_data.items():
        word, total = reduce_function(word, counts)
        final_results[word] = total

    return final_results


def main():
    """主函数：演示 MapReduce 词频统计"""
    # 创建示例文档数据
    sample_documents = {
        "doc1": "Hadoop 是一个分布式计算框架，用于处理大数据",
        "doc2": "Spark 比 Hadoop 更快，因为它使用内存计算",
        "doc3": "大数据处理需要分布式系统和并行计算",
        "doc4": "Hadoop 生态系统包括 HDFS、MapReduce 和 YARN"
    }

    # 执行 MapReduce 模拟
    word_counts = mapreduce_simulation(sample_documents)

    # 显示结果
    print("\n=== 最终结果 ===")
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_words[:10]:  # 显示前10个高频词
        print(f"{word}: {count}")

    print(f"\n总共统计了 {len(word_counts)} 个唯一单词")


if __name__ == "__main__":
    main()