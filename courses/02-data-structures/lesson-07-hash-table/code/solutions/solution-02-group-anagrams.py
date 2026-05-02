# ============================================
# 解答2：字母异位词分组
# 使用排序后的字符串作为哈希表的Key
# ============================================

def group_anagrams(strs):
    """
    将字母异位词分组
    核心思路：字母异位词排序后是相同的字符串
    用排序后的字符串作为Key，将原词归到同一组
    """
    groups = {}
    for s in strs:
        sorted_key = "".join(sorted(s))  # 排序后作为Key
        if sorted_key not in groups:
            groups[sorted_key] = []
        groups[sorted_key].append(s)
    return list(groups.values())


# 测试
if __name__ == "__main__":
    print("=== 字母异位词分组 ===")

    test1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
    result1 = group_anagrams(test1)
    print(f"输入: {test1}")
    print(f"输出: {result1}")
    print()

    test2 = [""]
    result2 = group_anagrams(test2)
    print(f"输入: {test2}")
    print(f"输出: {result2}")
    print()

    test3 = ["a"]
    result3 = group_anagrams(test3)
    print(f"输入: {test3}")
    print(f"输出: {result3}")
    print()

    test4 = ["abc", "bca", "cab", "xyz", "zyx"]
    result4 = group_anagrams(test4)
    print(f"输入: {test4}")
    print(f"输出: {result4}")

# 输出:
# === 字母异位词分组 ===
# 输入: ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
# 输出: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
#
# 输入: ['']
# 输出: [['']]
#
# 输入: ['a']
# 输出: [['a']]
#
# 输入: ['abc', 'bca', 'cab', 'xyz', 'zyx']
# 输出: [['abc', 'bca', 'cab'], ['xyz', 'zyx']]
