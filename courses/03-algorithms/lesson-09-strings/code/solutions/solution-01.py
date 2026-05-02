#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答：实现一个函数，找出字符串中所有回文子串
使用中心扩展法，时间复杂度 O(n²)
"""

def find_all_palindromes(s: str) -> list[str]:
    """
    找出字符串中所有的回文子串

    Args:
        s: 输入字符串

    Returns:
        所有回文子串的列表（去重）
    """
    if not s:
        return []

    palindromes = set()
    n = len(s)

    def expand_around_center(left: int, right: int):
        """从中心向两边扩展找回文"""
        while left >= 0 and right < n and s[left] == s[right]:
            palindromes.add(s[left:right + 1])
            left -= 1
            right += 1

    for i in range(n):
        # 奇数长度回文（以i为中心）
        expand_around_center(i, i)
        # 偶数长度回文（以i和i+1为中心）
        expand_around_center(i, i + 1)

    return sorted(list(palindromes))


def main():
    test_string = "ababa"
    result = find_all_palindromes(test_string)
    print(f"字符串 '{test_string}' 中的所有回文子串:")
    for palindrome in result:
        print(f"  '{palindrome}'")


if __name__ == "__main__":
    main()