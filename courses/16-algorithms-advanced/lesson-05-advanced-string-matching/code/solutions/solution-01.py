#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1: KMP算法完整实现

这是example-01-kmp.py的完整解决方案，
包含LPS数组构建和KMP搜索的标准实现。
"""

def compute_lps(pattern):
    """计算KMP的LPS数组"""
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(text, pattern):
    """KMP字符串搜索"""
    n, m = len(text), len(pattern)
    if m == 0:
        return []

    lps = compute_lps(pattern)
    matches = []
    i = j = 0

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches

def solve_kmp():
    """解决KMP相关问题"""
    text = "ABABDABACDABABCABCABCABC"
    pattern = "ABABC"
    return kmp_search(text, pattern)

if __name__ == "__main__":
    result = solve_kmp()
    print(f"KMP匹配位置: {result}")