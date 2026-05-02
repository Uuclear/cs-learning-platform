# challenge-02.md

## 挑战2: 文本分析器 ⭐⭐⭐

### 题目描述
创建一个文本分析器，能够读取一段文本并提供详细的统计信息，包括字符数、单词数、句子数、最常见的单词等。

### 具体要求
- 创建一个函数 `analyze_text(text)` 接受文本字符串作为参数
- 返回一个包含以下信息的字典：
  - `character_count`: 总字符数（包括空格）
  - `character_count_no_spaces`: 不包括空格的字符数
  - `word_count`: 单词数量
  - `sentence_count`: 句子数量（以句号、问号、感叹号分隔）
  - `most_common_word`: 出现频率最高的单词（忽略大小写）
  - `unique_words`: 不重复单词的数量
- 处理边界情况（空文本、只有标点符号等）
- 忽略大小写进行单词统计
- 只考虑字母和数字组成的单词（忽略标点符号）

### 示例使用
```python
text = "Hello world! This is a test. Hello again."
result = analyze_text(text)
print(result)
# 输出应包含所有统计信息
```

### 提示
- 使用 `string` 模块处理标点符号
- 使用 `re` 模块进行正则表达式处理（可选）
- 使用 `collections.Counter` 统计单词频率（可选）
- 注意处理多个连续空格的情况
- 考虑使用 `split()` 和 `strip()` 方法处理文本