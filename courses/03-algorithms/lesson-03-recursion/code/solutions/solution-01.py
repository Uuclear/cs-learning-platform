# 练习1解答：递归反转字符串

def reverse_string(s):
    """
    递归实现字符串反转
    思路: reverse(s) = reverse(s[1:]) + s[0]
    基准: 空串或单字符直接返回
    
    时间复杂度: O(n^2) —— 每次切片 O(n)，共 n 层
    空间复杂度: O(n) —— 调用栈深度
    """
    # 基准情况：空串或单字符
    if len(s) <= 1:
        return s
    
    # 递归情况：反转剩余部分 + 第一个字符放到最后
    return reverse_string(s[1:]) + s[0]


if __name__ == "__main__":
    print("=== 递归反转字符串 ===\n")
    
    test_cases = [
        "hello",
        "a",
        "",
        "abcdef",
        "racecar",
    ]
    
    for s in test_cases:
        result = reverse_string(s)
        print(f"  输入: '{s}'")
        print(f"  输出: '{result}'")
        print()

# 预期输出:
# === 递归反转字符串 ===
#
#   输入: 'hello'
#   输出: 'olleh'
#
#   输入: 'a'
#   输出: 'a'
#
#   输入: ''
#   输出: ''
#
#   输入: 'abcdef'
#   输出: 'fedcba'
#
#   输入: 'racecar'
#   输出: 'racecar'
