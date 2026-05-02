# 最长公共子序列（LCS）：找两个字符串的共同点
# 子序列不要求连续！"ace"是"abcde"的子序列
# 比如你和前任的聊天记录，总有些共同话题...

def lcs_length(s1, s2):
    """
    最长公共子序列 - 动态规划解法

    核心思路：
    - dp[i][j] = s1的前i个字符和s2的前j个字符的LCS长度
    - 如果字符相同：dp[i][j] = dp[i-1][j-1] + 1
    - 如果字符不同：dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    - 意思就是：相同就一起走，不同就各走各的，选长的路
    """
    m, n = len(s1), len(s2)

    # 创建DP表：(m+1)行 × (n+1)列
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 填表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # 字符相同：从对角线+1（两个字符匹配上了）
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # 字符不同：从上方或左方取最大值（舍弃一个字符）
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp


def backtrack_lcs(dp, s1, s2):
    """
    回溯找出具体的LCS字符串
    从DP表右下角开始往回走
    """
    lcs = []
    i, j = len(s1), len(s2)

    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            # 字符相同：这个字符一定在LCS中
            lcs.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            # 上方的值更大：说明s1的这个字符不在LCS中
            i -= 1
        else:
            # 左方的值更大（或相等）：说明s2的这个字符不在LCS中
            j -= 1

    lcs.reverse()  # 回溯是从后往前找的，需要反转
    return "".join(lcs)


def print_dp_table(dp, s1, s2):
    """打印DP表，让填表过程一目了然"""
    print(f"     ", end="")  # 留出左上角空间
    print("  ∅  ", end="")   # 空列标记
    for ch in s2:
        print(f"  {ch}  ", end="")
    print()

    # 打印分隔线
    print("  " + "-----" * (len(s2) + 1))

    for i in range(len(dp)):
        # 打印行标记
        if i == 0:
            print("∅ |", end="")
        else:
            print(f"{s1[i-1]} |", end="")

        # 打印当前行的DP值
        for j in range(len(dp[0])):
            print(f" {dp[i][j]:>2} ", end="")
        print()


if __name__ == "__main__":
    print("=" * 60)
    print("最长公共子序列（LCS）：动态规划解法")
    print("=" * 60)

    # 案例1：基础示例
    print(f"\n--- 案例1：找共同字符 ---")
    s1 = "ABCBDAB"
    s2 = "BDCAB"
    print(f"字符串1: {s1}")
    print(f"字符串2: {s2}")
    print(f"\nDP填表过程：")

    dp1 = lcs_length(s1, s2)
    print_dp_table(dp1, s1, s2)

    lcs1 = backtrack_lcs(dp1, s1, s2)
    print(f"\n最长公共子序列: {lcs1}")
    print(f"LCS长度: {len(lcs1)}")

    # 案例2：DNA序列比对（真实应用！）
    print(f"\n{'=' * 60}")
    print(f"--- 案例2：DNA序列比对（生物信息学实际应用）---")
    dna1 = "AGCTAGCTA"
    dna2 = "AGTACTGA"
    print(f"DNA序列1: {dna1}")
    print(f"DNA序列2: {dna2}")
    print(f"\nDP填表过程：")

    dp2 = lcs_length(dna1, dna2)
    print_dp_table(dp2, dna1, dna2)

    lcs2 = backtrack_lcs(dp2, dna1, dna2)
    print(f"\n最长公共子序列: {lcs2}")
    print(f"相似度: {len(lcs2)/max(len(dna1), len(dna2))*100:.1f}%")

    # 复杂度总结
    print(f"\n{'=' * 60}")
    print(f"复杂度分析：")
    print(f"  时间复杂度: O(m × n)，m和n分别是两个字符串的长度")
    print(f"  空间复杂度: O(m × n)，可以优化到O(min(m, n))")
    print(f"{'=' * 60}")

# 输出:
# ============================================================
# 最长公共子序列（LCS）：动态规划解法
# ============================================================
#
# --- 案例1：找共同字符 ---
# 字符串1: ABCBDAB
# 字符串2: BDCAB
#
# DP填表过程：
#           ∅    B    D    C    A    B
#   ----------------------------------------
# ∅ |  0   0   0   0   0   0
# A |  0   0   0   0   1   1
# B |  0   1   1   1   1   2
# C |  0   1   1   2   2   2
# B |  0   1   1   2   2   3
# D |  0   1   2   2   2   3
# A |  0   1   2   2   3   3
# B |  0   1   2   2   3   4
#
# 最长公共子序列: BDAB
# LCS长度: 4
#
# ============================================================
# --- 案例2：DNA序列比对（生物信息学实际应用）---
# DNA序列1: AGCTAGCTA
# DNA序列2: AGTACTGA
#
# DP填表过程：
#           ∅    A    G    T    A    C    T    G    A
#   --------------------------------------------------------
# ∅ |  0   0   0   0   0   0   0   0   0
# A |  0   1   1   1   1   1   1   1   1
# G |  0   1   2   2   2   2   2   2   2
# C |  0   1   2   2   2   3   3   3   3
# T |  0   1   2   3   3   3   4   4   4
# A |  0   1   2   3   4   4   4   4   5
# G |  0   1   2   3   4   4   4   5   5
# C |  0   1   2   3   4   5   5   5   5
# T |  0   1   2   3   4   5   6   6   6
# A |  0   1   2   3   4   5   6   6   7
#
# 最长公共子序列: AGTACTA
# 相似度: 77.8%
# ============================================================
# 复杂度分析：
#   时间复杂度: O(m × n)，m和n分别是两个字符串的长度
#   空间复杂度: O(m × n)，可以优化到O(min(m, n))
# ============================================================
