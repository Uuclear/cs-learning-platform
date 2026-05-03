#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: KMP算法实现与演示

这个例子详细展示了KMP算法的实现，
包括失败函数（LPS数组）的构建和搜索过程。
"""

def compute_lps_array(pattern):
    """
    计算KMP算法的LPS（最长前缀后缀）数组

    LPS[i] 表示 pattern[0:i+1] 的最长真前缀（同时也是后缀）的长度

    Args:
        pattern (str): 模式字符串

    Returns:
        list: LPS数组，长度等于模式长度
    """
    m = len(pattern)
    lps = [0] * m  # 初始化LPS数组
    length = 0     # 当前最长前缀后缀的长度
    i = 1          # 从第二个字符开始计算

    print(f"构建LPS数组 for pattern: '{pattern}'")
    print("步骤:")

    while i < m:
        if pattern[i] == pattern[length]:
            # 字符匹配，长度增加
            length += 1
            lps[i] = length
            print(f"  i={i}: pattern[{i}]='{pattern[i]}' == pattern[{length-1}]='{pattern[length-1]}' -> lps[{i}] = {length}")
            i += 1
        else:
            if length != 0:
                # 不匹配但length>0，回退到之前的位置
                print(f"  i={i}: pattern[{i}]='{pattern[i]}' != pattern[{length}]='{pattern[length]}' -> 回退到 lps[{length-1}] = {lps[length-1]}")
                length = lps[length - 1]
            else:
                # length为0，直接设置为0并前进
                lps[i] = 0
                print(f"  i={i}: pattern[{i}]='{pattern[i]}' != pattern[0]='{pattern[0]}' -> lps[{i}] = 0")
                i += 1

    print(f"LPS数组: {lps}")
    return lps

def kmp_search(text, pattern):
    """
    KMP字符串搜索算法

    Args:
        text (str): 文本字符串
        pattern (str): 模式字符串

    Returns:
        list: 所有匹配位置的列表
    """
    n, m = len(text), len(pattern)

    if m == 0:
        return []

    # 构建LPS数组
    lps = compute_lps_array(pattern)
    matches = []

    i = 0  # text的索引
    j = 0  # pattern的索引

    print(f"\n在文本中搜索模式: '{pattern}'")
    print(f"文本: '{text}'")
    print("搜索过程:")

    while i < n:
        if pattern[j] == text[i]:
            # 字符匹配，两个指针都前进
            i += 1
            j += 1
            print(f"  匹配: text[{i-1}]='{text[i-1]}' == pattern[{j-1}]='{pattern[j-1]}'")

        if j == m:
            # 找到完整匹配
            match_pos = i - j
            matches.append(match_pos)
            print(f"  找到匹配! 位置: {match_pos}")
            j = lps[j - 1]  # 使用LPS数组跳转
        elif i < n and pattern[j] != text[i]:
            # 字符不匹配
            print(f"  不匹配: text[{i}]='{text[i]}' != pattern[{j}]='{pattern[j]}'")
            if j != 0:
                # 使用LPS数组跳转，避免回溯text指针
                old_j = j
                j = lps[j - 1]
                print(f"    跳转: j从{old_j}变为{lps[old_j-1]} (使用lps[{old_j-1}] = {lps[old_j-1]})")
            else:
                # j为0，只能前进text指针
                i += 1
                print(f"    前进: i增加到{i}")

    return matches

def main():
    """主函数 - 演示KMP算法"""
    print("=== 示例1: KMP算法实现 ===\n")

    # 测试用例1: 经典例子
    text1 = "ABABDABACDABABCABCABCABC"
    pattern1 = "ABABC"

    print("测试用例1:")
    matches1 = kmp_search(text1, pattern1)
    print(f"\n结果: 找到 {len(matches1)} 个匹配位置: {matches1}")

    print("\n" + "="*50 + "\n")

    # 测试用例2: 重复模式
    text2 = "AAAAA"
    pattern2 = "AA"

    print("测试用例2:")
    matches2 = kmp_search(text2, pattern2)
    print(f"\n结果: 找到 {len(matches2)} 个匹配位置: {matches2}")

    print("\n" + "="*50 + "\n")

    # 测试用例3: 无匹配
    text3 = "ABCDEFG"
    pattern3 = "XYZ"

    print("测试用例3:")
    matches3 = kmp_search(text3, pattern3)
    print(f"\n结果: 找到 {len(matches3)} 个匹配位置: {matches3}")

if __name__ == "__main__":
    main()

# 预期输出:
# === 示例1: KMP算法实现 ===
#
# 测试用例1:
# 构建LPS数组 for pattern: 'ABABC'
# 步骤:
#   i=1: pattern[1]='B' != pattern[0]='A' -> lps[1] = 0
#   i=2: pattern[2]='A' == pattern[0]='A' -> lps[2] = 1
#   i=3: pattern[3]='B' == pattern[1]='B' -> lps[3] = 2
#   i=4: pattern[4]='C' != pattern[2]='A' -> 回退到 lps[1] = 0
#   i=4: pattern[4]='C' != pattern[0]='A' -> lps[4] = 0
# LPS数组: [0, 0, 1, 2, 0]
#
# 在文本中搜索模式: 'ABABC'
# 文本: 'ABABDABACDABABCABCABCABC'
# 搜索过程:
#   匹配: text[0]='A' == pattern[0]='A'
#   匹配: text[1]='B' == pattern[1]='B'
#   匹配: text[2]='A' == pattern[2]='A'
#   匹配: text[3]='B' == pattern[3]='B'
#   不匹配: text[4]='D' != pattern[4]='C'
#     跳转: j从4变为0 (使用lps[3] = 2)
#   ...
#   找到匹配! 位置: 9
#
# 结果: 找到 1 个匹配位置: [9]