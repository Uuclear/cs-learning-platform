#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2: Rabin-Karp算法完整实现

这是example-02-rabin-karp.py的完整解决方案，
包含滚动哈希的标准实现。
"""

def rabin_karp_search(text, pattern, prime=101):
    """Rabin-Karp字符串搜索"""
    n, m = len(text), len(pattern)
    if m == 0 or n < m:
        return []

    d = 256
    h = 1
    for i in range(m - 1):
        h = (h * d) % prime

    pattern_hash = 0
    text_hash = 0

    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % prime
        text_hash = (d * text_hash + ord(text[i])) % prime

    matches = []

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                matches.append(i)

        if i < n - m:
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if text_hash < 0:
                text_hash += prime

    return matches

def solve_rabin_karp():
    """解决Rabin-Karp相关问题"""
    text = "ABABDABACDABABCABCABCABC"
    pattern = "ABABC"
    return rabin_karp_search(text, pattern)

if __name__ == "__main__":
    result = solve_rabin_karp()
    print(f"Rabin-Karp匹配位置: {result}")