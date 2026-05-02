#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KMP (Knuth-Morris-Pratt) 字符串匹配算法示例

KMP算法通过预处理模式串，构建部分匹配表（也称为next数组），
避免在匹配失败时回溯文本串，从而实现线性时间复杂度的字符串匹配。
"""

def build_next_array(pattern: str) -> list[int]:
    """
    构建KMP算法的next数组（部分匹配表）

    Args:
        pattern: 模式串

    Returns:
        next数组，next[i]表示pattern[0:i]的最长相同前后缀长度
    """
    n = len(pattern)
    next_array = [0] * n
    j = 0  # j表示当前已匹配的前缀长度

    # 从第二个字符开始构建next数组
    for i in range(1, n):
        # 如果当前字符不匹配，回溯到next[j-1]的位置
        while j > 0 and pattern[i] != pattern[j]:
            j = next_array[j - 1]

        # 如果当前字符匹配，增加匹配长度
        if pattern[i] == pattern[j]:
            j += 1

        next_array[i] = j

    return next_array


def kmp_search(text: str, pattern: str) -> list[int]:
    """
    使用KMP算法在文本中搜索模式串的所有出现位置

    Args:
        text: 文本串
        pattern: 模式串

    Returns:
        所有匹配位置的列表（0-based索引）
    """
    if not pattern:
        return []

    next_array = build_next_array(pattern)
    matches = []
    j = 0  # 模式串的匹配位置

    for i in range(len(text)):
        # 如果当前字符不匹配，根据next数组回溯
        while j > 0 and text[i] != pattern[j]:
            j = next_array[j - 1]

        # 如果当前字符匹配，移动到下一个字符
        if text[i] == pattern[j]:
            j += 1

        # 如果完全匹配，记录位置并准备下一次匹配
        if j == len(pattern):
            matches.append(i - j + 1)
            j = next_array[j - 1]  # 利用next数组继续匹配

    return matches


def main():
    """KMP算法演示"""
    text = "ABABDABACDABABCABCABCABCABC"
    pattern = "ABABCABC"

    print("=== KMP字符串匹配算法演示 ===")
    print(f"文本串: {text}")
    print(f"模式串: {pattern}")

    # 构建next数组
    next_array = build_next_array(pattern)
    print(f"next数组: {next_array}")

    # 执行搜索
    matches = kmp_search(text, pattern)
    print(f"匹配位置: {matches}")

    # 验证结果
    if matches:
        print("\n匹配结果验证:")
        for pos in matches:
            matched_text = text[pos:pos + len(pattern)]
            print(f"  位置 {pos}: '{matched_text}' ✓")
    else:
        print("未找到匹配!")


if __name__ == "__main__":
    main()