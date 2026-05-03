# 挑战 1: 实现自定义的 Word Count 算法

⭐⭐⭐ 难度 | 预计时间：20分钟

## 背景
在大数据处理中，词频统计 (Word Count) 是最经典的示例之一。你需要实现一个高效的词频统计算法，能够处理大规模文本数据。

## 要求
1. 创建一个名为 `custom_word_count.py` 的文件
2. 实现一个函数 `word_count(texts: List[str]) -> Dict[str, int]`，其中：
   - `texts` 是包含多个文档字符串的列表
   - 返回值是字典，键为单词，值为该单词在整个文档集合中的出现次数
3. 算法必须支持以下功能：
   - 忽略大小写（"Hello" 和 "hello" 视为同一个词）
   - 只统计字母和数字组成的单词（忽略标点符号）
   - 过滤掉长度小于2的单词
4. 使用类似 MapReduce 的思路实现，但不需要真正的分布式处理
5. 添加适当的中文注释说明每个步骤的作用

## 测试数据
```python
test_texts = [
    "Hello world! This is a test document.",
    "Another document with some words and HELLO again.",
    "Big data processing requires distributed systems."
]
```

## 验证标准
- 代码能够正确运行并输出预期结果
- 时间复杂度应为 O(n)，其中 n 是总字符数
- 内存使用合理，不会因为输入数据量大而崩溃
- 包含完整的中文注释