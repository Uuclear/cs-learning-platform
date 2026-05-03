#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态规划解决方案 03: 最长公共子序列（LCS）
找出两个字符串的最长公共子序列长度和具体内容
"""

def lcs_length(s1, s2):
    """
    计算两个字符串的最长公共子序列长度

    参数:
        s1: 第一个字符串
        s2: 第二个字符串

    返回:
        LCS长度和DP表
    """
    m, n = len(s1), len(s2)

    # 创建DP表，dp[i][j] 表示s1[:i]和s2[:j]的LCS长度
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 填充DP表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # 字符相同：LCS长度 = 对角线值 + 1
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # 字符不同：取上方或左方的最大值
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n], dp


def lcs_string(s1, s2, dp):
    """
    根据DP表重构最长公共子序列字符串

    参数:
        s1: 第一个字符串
        s2: 第二个字符串
        dp: 已计算的DP表

    返回:
        LCS字符串
    """
    m, n = len(s1), len(s2)
    lcs = []

    # 从右下角开始回溯
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            # 字符相同，加入LCS
            lcs.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            # 上方值更大，向上移动
            i -= 1
        else:
            # 左方值更大，向左移动
            j -= 1

    # 回溯得到的是逆序，需要反转
    return ''.join(reversed(lcs))


def main():
    """主函数：演示LCS算法的应用"""
    print("=== 最长公共子序列（LCS）动态规划实现 ===\n")

    # 示例1：基本测试
    print("1. 基本测试:")
    s1 = "ABCDGH"
    s2 = "AEDFHR"
    length, dp_table = lcs_length(s1, s2)
    lcs_str = lcs_string(s1, s2, dp_table)
    print(f"   字符串1: '{s1}'")
    print(f"   字符串2: '{s2}'")
    print(f"   LCS长度: {length}")
    print(f"   LCS内容: '{lcs_str}'\n")

    # 示例2：DNA序列比对
    print("2. DNA序列比对应用:")
    dna1 = "AGCTAGCTA"
    dna2 = "AGTACTGA"
    length, dp_table = lcs_length(dna1, dna2)
    lcs_str = lcs_string(dna1, dna2, dp_table)
    similarity = length / max(len(dna1), len(dna2)) * 100
    print(f"   DNA序列1: {dna1}")
    print(f"   DNA序列2: {dna2}")
    print(f"   LCS长度: {length}")
    print(f"   LCS内容: {lcs_str}")
    print(f"   相似度: {similarity:.1f}%\n")

    # 示例3：文本差异比较
    print("3. 文本差异比较:")
    text1 = "dynamic programming"
    text2 = "dynmic programing"
    length, dp_table = lcs_length(text1, text2)
    lcs_str = lcs_string(text1, text2, dp_table)
    print(f"   文本1: '{text1}'")
    print(f"   文本2: '{text2}'")
    print(f"   LCS长度: {length}")
    print(f"   LCS内容: '{lcs_str}'")
    print(f"   编辑距离估算: {len(text1) + len(text2) - 2 * length}\n")

    # 示例4：中文字符串
    print("4. 中文字符串测试:")
    chinese1 = "动态规划很有趣"
    chinese2 = "动态编程非常有趣"
    length, dp_table = lcs_length(chinese1, chinese2)
    lcs_str = lcs_string(chinese1, chinese2, dp_table)
    print(f"   字符串1: '{chinese1}'")
    print(f"   字符串2: '{chinese2}'")
    print(f"   LCS长度: {length}")
    print(f"   LCS内容: '{lcs_str}'")


if __name__ == "__main__":
    main()