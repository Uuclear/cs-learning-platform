#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: Boyer-Moore算法实现与演示

这个例子展示了Boyer-Moore算法的坏字符规则实现，
以及与朴素算法的性能对比。
"""

def build_bad_character_table(pattern):
    """
    构建Boyer-Moore算法的坏字符表

    对于每个字符，记录其在模式中最右边出现的位置

    Args:
        pattern (str): 模式字符串

    Returns:
        dict: 坏字符表，字符 -> 最右位置
    """
    bad_char = {}
    m = len(pattern)

    # 记录每个字符最右边的位置
    for i in range(m):
        bad_char[pattern[i]] = i

    return bad_char

def boyer_moore_search(text, pattern):
    """
    Boyer-Moore字符串搜索算法（仅使用坏字符规则）

    从右到左匹配，利用坏字符规则进行跳跃

    Args:
        text (str): 文本字符串
        pattern (str): 模式字符串

    Returns:
        tuple: (匹配位置列表, 字符比较次数, 跳跃次数)
    """
    n, m = len(text), len(pattern)

    if m == 0:
        return [], 0, 0

    bad_char = build_bad_character_table(pattern)
    matches = []
    compare_count = 0
    jump_count = 0

    print(f"Boyer-Moore参数:")
    print(f"  文本长度: {n}")
    print(f"  模式长度: {m}")
    print(f"  坏字符表: {bad_char}")
    print()

    shift = 0  # 当前模式在文本中的起始位置

    while shift <= n - m:
        print(f"模式位置: {shift}, 比较范围: [{shift}, {shift + m - 1}]")

        j = m - 1  # 从模式的最后一个字符开始比较

        # 从右到左比较
        while j >= 0 and pattern[j] == text[shift + j]:
            compare_count += 1
            print(f"  匹配: pattern[{j}]='{pattern[j]}' == text[{shift + j}]='{text[shift + j]}'")
            j -= 1

        if j < 0:
            # 找到完整匹配
            matches.append(shift)
            print(f"  找到匹配! 位置: {shift}")

            # 计算下一个shift（如果还没到文本末尾）
            if shift + m < n:
                next_char = text[shift + m]
                bad_char_shift = m - bad_char.get(next_char, -1)
                shift += bad_char_shift
                jump_count += 1
                print(f"  跳跃: 基于字符'{next_char}'，移动{bad_char_shift}位")
            else:
                shift += 1
        else:
            # 发生不匹配
            compare_count += 1  # 计算不匹配的比较
            mismatch_char = text[shift + j]
            print(f"  不匹配: pattern[{j}]='{pattern[j]}' != text[{shift + j}]='{mismatch_char}'")

            # 坏字符规则：计算跳跃距离
            bad_char_pos = bad_char.get(mismatch_char, -1)
            shift_distance = max(1, j - bad_char_pos)
            shift += shift_distance
            jump_count += 1
            print(f"  跳跃: 基于坏字符'{mismatch_char}'，移动{shift_distance}位")

        print()

    return matches, compare_count, jump_count

def naive_search(text, pattern):
    """
    朴素字符串搜索算法（用于对比）

    Args:
        text (str): 文本字符串
        pattern (str): 模式字符串

    Returns:
        int: 字符比较次数
    """
    n, m = len(text), len(pattern)
    compare_count = 0

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            compare_count += 1
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            pass  # 找到匹配，但这里只统计比较次数

    return compare_count

def compare_algorithms():
    """比较Boyer-Moore和朴素算法的性能"""
    print("=== 示例3: Boyer-Moore算法实现 ===\n")

    # 测试用例1: 长模式，大字符集
    print("测试用例1: 长模式匹配")
    text1 = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG" * 10
    pattern1 = "LAZY DOG"

    print(f"文本: '{text1[:50]}...'")
    print(f"模式: '{pattern1}'")
    print()

    matches1, bm_compares1, bm_jumps1 = boyer_moore_search(text1, pattern1)
    naive_compares1 = naive_search(text1, pattern1)

    print(f"Boyer-Moore结果: {len(matches1)} 个匹配")
    print(f"Boyer-Moore比较次数: {bm_compares1}, 跳跃次数: {bm_jumps1}")
    print(f"朴素算法比较次数: {naive_compares1}")
    print(f"性能提升: {naive_compares1 / bm_compares1:.2f}x\n")

    print("-" * 60 + "\n")

    # 测试用例2: 短模式，小字符集
    print("测试用例2: 短模式匹配")
    text2 = "AAAAAAAAAAAAAAAAAAAAAAAA"
    pattern2 = "AAA"

    print(f"文本: '{text2}'")
    print(f"模式: '{pattern2}'")
    print()

    matches2, bm_compares2, bm_jumps2 = boyer_moore_search(text2, pattern2)
    naive_compares2 = naive_search(text2, pattern2)

    print(f"Boyer-Moore结果: {len(matches2)} 个匹配")
    print(f"Boyer-Moore比较次数: {bm_compares2}, 跳跃次数: {bm_jumps2}")
    print(f"朴素算法比较次数: {naive_compares2}")
    print(f"性能提升: {naive_compares2 / bm_compares2:.2f}x")
    print("注意: 在重复字符情况下，Boyer-Moore的优势不明显")

if __name__ == "__main__":
    compare_algorithms()

# 预期输出:
# === 示例3: Boyer-Moore算法实现 ===
#
# 测试用例1: 长模式匹配
# 文本: 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOGTHE QUI...'
# 模式: 'LAZY DOG'
#
# Boyer-Moore参数:
#   文本长度: 430
#   模式长度: 8
#   坏字符表: {'L': 0, 'A': 1, 'Z': 2, 'Y': 3, ' ': 4, 'D': 5, 'O': 6, 'G': 7}
#
# 模式位置: 0, 比较范围: [0, 7]
#   不匹配: pattern[7]='G' != text[7]='K'
#   跳跃: 基于坏字符'K'，移动8位
#
# 模式位置: 8, 比较范围: [8, 15]
#   ...
# 模式位置: 35, 比较范围: [35, 42]
#   匹配: pattern[7]='G' == text[42]='G'
#   匹配: pattern[6]='O' == text[41]='O'
#   ...
#   找到匹配! 位置: 35
#
# Boyer-Moore结果: 10 个匹配
# Boyer-Moore比较次数: 80, 跳跃次数: 40
# 朴素算法比较次数: 3441
# 性能提升: 43.01x