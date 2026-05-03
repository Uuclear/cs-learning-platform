#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3: Boyer-Moore算法完整实现

这是example-03-boyer-moore.py的完整解决方案，
包含坏字符规则的标准实现。
"""

def build_bad_char_table(pattern):
    """构建坏字符表"""
    bad_char = {}
    m = len(pattern)
    for i in range(m):
        bad_char[pattern[i]] = i
    return bad_char

def boyer_moore_search(text, pattern):
    """Boyer-Moore字符串搜索（坏字符规则）"""
    n, m = len(text), len(pattern)
    if m == 0:
        return []

    bad_char = build_bad_char_table(pattern)
    matches = []
    shift = 0

    while shift <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            matches.append(shift)
            if shift + m < n:
                shift += m - bad_char.get(text[shift + m], -1)
            else:
                shift += 1
        else:
            shift += max(1, j - bad_char.get(text[shift + j], -1))

    return matches

def solve_boyer_moore():
    """解决Boyer-Moore相关问题"""
    text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG" * 10
    pattern = "LAZY DOG"
    return boyer_moore_search(text, pattern)

if __name__ == "__main__":
    result = solve_boyer_moore()
    print(f"Boyer-Moore匹配位置: {result}")