#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rabin-Karp 字符串匹配算法示例

Rabin-Karp算法使用滚动哈希技术来高效地在文本中搜索模式串。
通过预先计算模式串的哈希值，然后在文本中滑动窗口计算哈希值，
只有当哈希值匹配时才进行实际的字符串比较，从而减少不必要的比较。
"""

def rabin_karp_search(text: str, pattern: str, prime: int = 101) -> list[int]:
    """
    使用Rabin-Karp算法在文本中搜索模式串

    Args:
        text: 文本串
        pattern: 模式串
        prime: 用于哈希计算的大质数（默认101）

    Returns:
        所有匹配位置的列表（0-based索引）
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    n = len(text)
    m = len(pattern)
    matches = []

    # 计算d^(m-1) % prime，用于滚动哈希
    h = pow(256, m - 1, prime)

    # 计算模式串和文本前m个字符的哈希值
    pattern_hash = 0
    text_hash = 0

    for i in range(m):
        pattern_hash = (pattern_hash * 256 + ord(pattern[i])) % prime
        text_hash = (text_hash * 256 + ord(text[i])) % prime

    # 在文本中滑动窗口
    for i in range(n - m + 1):
        # 如果哈希值匹配，进行实际字符串比较（防止哈希冲突）
        if pattern_hash == text_hash:
            # 验证实际字符串是否匹配
            if text[i:i + m] == pattern:
                matches.append(i)

        # 计算下一个窗口的哈希值（如果不是最后一个窗口）
        if i < n - m:
            # 移除最左边字符的影响
            text_hash = (text_hash - ord(text[i]) * h) % prime
            # 添加新字符
            text_hash = (text_hash * 256 + ord(text[i + m])) % prime
            # 处理负数情况
            if text_hash < 0:
                text_hash += prime

    return matches


def compute_hash(s: str, prime: int = 101) -> int:
    """
    计算字符串的简单哈希值

    Args:
        s: 输入字符串
        prime: 质数模数

    Returns:
        哈希值
    """
    hash_value = 0
    for char in s:
        hash_value = (hash_value * 256 + ord(char)) % prime
    return hash_value


def main():
    """Rabin-Karp算法演示"""
    text = "ABABDABACDABABCABCABCABCABC"
    pattern = "ABABCABC"

    print("=== Rabin-Karp字符串匹配算法演示 ===")
    print(f"文本串: {text}")
    print(f"模式串: {pattern}")

    # 计算哈希值
    pattern_hash = compute_hash(pattern)
    print(f"模式串哈希值: {pattern_hash}")

    # 执行搜索
    matches = rabin_karp_search(text, pattern)
    print(f"匹配位置: {matches}")

    # 验证结果
    if matches:
        print("\n匹配结果验证:")
        for pos in matches:
            matched_text = text[pos:pos + len(pattern)]
            print(f"  位置 {pos}: '{matched_text}' ✓")
    else:
        print("未找到匹配!")

    # 性能对比演示
    print("\n--- 算法特点 ---")
    print("✅ 时间复杂度: 平均 O(n+m)，最坏 O(nm)")
    print("✅ 空间复杂度: O(1)")
    print("✅ 优点: 可以同时搜索多个模式，适合多模式匹配")
    print("⚠️  注意: 存在哈希冲突的可能性，需要二次验证")


if __name__ == "__main__":
    main()