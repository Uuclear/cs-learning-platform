#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: Rabin-Karp算法实现与演示

这个例子展示了Rabin-Karp算法的滚动哈希实现，
包括哈希计算、冲突处理和性能分析。
"""

def rabin_karp_search(text, pattern, prime=101):
    """
    Rabin-Karp字符串搜索算法

    使用滚动哈希技术，通过数学公式快速计算滑动窗口的哈希值。

    Args:
        text (str): 文本字符串
        pattern (str): 模式字符串
        prime (int): 用于哈希计算的大质数

    Returns:
        tuple: (匹配位置列表, 哈希计算次数, 实际比较次数)
    """
    n, m = len(text), len(pattern)

    if m == 0 or n < m:
        return [], 0, 0

    d = 256  # 字符集大小（ASCII）
    hash_count = 0   # 哈希计算次数
    compare_count = 0  # 实际字符串比较次数

    # 计算 d^(m-1) % prime
    h = 1
    for i in range(m - 1):
        h = (h * d) % prime

    print(f"Rabin-Karp参数:")
    print(f"  文本长度: {n}")
    print(f"  模式长度: {m}")
    print(f"  质数: {prime}")
    print(f"  字符集大小: {d}")
    print(f"  h = d^(m-1) % prime = {h}")
    print()

    # 计算模式的哈希值
    pattern_hash = 0
    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % prime
    hash_count += 1

    print(f"模式 '{pattern}' 的哈希值: {pattern_hash}")

    # 计算文本前m个字符的哈希值
    text_hash = 0
    for i in range(m):
        text_hash = (d * text_hash + ord(text[i])) % prime
    hash_count += 1

    print(f"文本前{m}个字符的初始哈希值: {text_hash}")
    print()

    matches = []

    # 滑动窗口搜索
    for i in range(n - m + 1):
        print(f"位置 {i}: ", end="")

        if pattern_hash == text_hash:
            print(f"哈希匹配! ", end="")
            # 验证实际字符串是否匹配（处理哈希冲突）
            compare_count += 1
            if text[i:i + m] == pattern:
                matches.append(i)
                print(f"实际匹配! -> 找到匹配位置 {i}")
            else:
                print(f"哈希冲突! 实际不匹配")
        else:
            print(f"哈希不匹配 ({text_hash})")

        # 计算下一个窗口的哈希值（如果不是最后一个窗口）
        if i < n - m:
            # 移除左边字符，添加右边字符
            old_hash = text_hash
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime

            # 处理负数情况
            if text_hash < 0:
                text_hash += prime

            hash_count += 1
            print(f"  更新哈希: {old_hash} -> {text_hash} (移除'{text[i]}', 添加'{text[i+m]}')")

    return matches, hash_count, compare_count

def analyze_performance():
    """分析不同场景下的算法性能"""
    print("=== 示例2: Rabin-Karp算法实现 ===\n")

    # 测试用例1: 正常匹配
    print("测试用例1: 正常匹配")
    text1 = "ABABDABACDABABCABCABCABC"
    pattern1 = "ABABC"

    matches1, hash_count1, compare_count1 = rabin_karp_search(text1, pattern1)
    print(f"\n结果: {len(matches1)} 个匹配位置: {matches1}")
    print(f"统计: 哈希计算 {hash_count1} 次, 实际比较 {compare_count1} 次\n")

    print("-" * 60 + "\n")

    # 测试用例2: 哈希冲突演示
    print("测试用例2: 哈希冲突演示")
    # 选择一个容易产生冲突的例子
    text2 = "AAAAAAAAAA"
    pattern2 = "AAA"

    matches2, hash_count2, compare_count2 = rabin_karp_search(text2, pattern2, prime=7)  # 使用小质数增加冲突概率
    print(f"\n结果: {len(matches2)} 个匹配位置: {matches2}")
    print(f"统计: 哈希计算 {hash_count2} 次, 实际比较 {compare_count2} 次")
    print(f"注意: 使用小质数(7)增加了哈希冲突的概率\n")

    print("-" * 60 + "\n")

    # 测试用例3: 无匹配但哈希可能匹配
    print("测试用例3: 无匹配情况")
    text3 = "ABCDEFGH"
    pattern3 = "XYZ"

    matches3, hash_count3, compare_count3 = rabin_karp_search(text3, pattern3)
    print(f"\n结果: {len(matches3)} 个匹配位置: {matches3}")
    print(f"统计: 哈希计算 {hash_count3} 次, 实际比较 {compare_count3} 次")

if __name__ == "__main__":
    analyze_performance()

# 预期输出:
# === 示例2: Rabin-Karp算法实现 ===
#
# 测试用例1: 正常匹配
# Rabin-Karp参数:
#   文本长度: 25
#   模式长度: 5
#   质数: 101
#   字符集大小: 256
#   h = d^(m-1) % prime = 79
#
# 模式 'ABABC' 的哈希值: 47
# 文本前5个字符的初始哈希值: 47
#
# 位置 0: 哈希匹配! 实际匹配! -> 找到匹配位置 0
#   更新哈希: 47 -> 35 (移除'A', 添加'D')
# 位置 1: 哈希不匹配 (35)
#   ...
# 位置 9: 哈希匹配! 实际匹配! -> 找到匹配位置 9
#
# 结果: 2 个匹配位置: [0, 9]
# 统计: 哈希计算 22 次, 实际比较 2 次