# ============================================
# 示例3：哈希表的实际应用——词频统计
# 这就是哈希表最常见的用途之一：计数和统计
# ============================================

def word_frequency(text):
    """
    统计文本中每个单词出现的频率
    哈希表天然适合这种"键→计数"的场景
    """
    # 清理文本：转小写，按空格拆分
    words = text.lower().split()

    # 用哈希表（字典）统计词频
    freq = {}
    for word in words:
        # 去掉标点符号
        word = word.strip(".,!?;:\"'()[]{}")
        if word:
            freq[word] = freq.get(word, 0) + 1

    return freq


def print_top_words(freq, top_n=5):
    """
    打印出现频率最高的N个单词
    """
    # 按频率排序
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    print(f"词频统计 TOP {top_n}:")
    print("-" * 30)
    for i, (word, count) in enumerate(sorted_words[:top_n], 1):
        bar = "█" * count
        print(f"  {i:2d}. {word:15s} ({count:3d}次) {bar}")


# 测试
sample_text = """
The quick brown fox jumps over the lazy dog
The dog barks at the fox
The fox is quick and the dog is lazy
A quick brown dog runs in the park
The park is beautiful and the fox likes the park
"""

print("=== 词频统计示例 ===\n")
print("输入文本:")
for line in sample_text.strip().split("\n"):
    print(f"  {line.strip()}")
print()

freq = word_frequency(sample_text)
print(f"共统计到 {len(freq)} 个不同的单词\n")
print_top_words(freq, top_n=5)

# 看看完整统计
print("\n完整词频:")
for word in sorted(freq.keys()):
    print(f"  '{word}': {freq[word]}")
