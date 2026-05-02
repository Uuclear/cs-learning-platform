# 练习2解答：递归判断回文串

def is_palindrome(s):
    """
    递归判断字符串是否是回文
    思路: 首尾相同 且 中间部分是回文
    基准: 长度 <= 1 的字符串是回文
    """
    # 预处理：去掉空格，统一小写
    s = s.replace(" ", "").lower()
    
    # 基准情况：空串或单字符是回文
    if len(s) <= 1:
        return True
    
    # 首尾不同，不是回文
    if s[0] != s[-1]:
        return False
    
    # 递归：检查中间部分
    return is_palindrome(s[1:-1])


if __name__ == "__main__":
    print("=== 递归判断回文串 ===\n")
    
    test_cases = [
        "racecar",
        "hello",
        "A man a plan a canal Panama",
        "Was it a car or a cat I saw",
        "no 'x' in Nixon",
        "python",
    ]
    
    for s in test_cases:
        result = is_palindrome(s)
        print(f"  输入: '{s}'")
        print(f"  回文: {result}")
        print()

# 预期输出:
# === 递归判断回文串 ===
#
#   输入: 'racecar'
#   回文: True
#
#   输入: 'hello'
#   回文: False
#
#   输入: 'A man a plan a canal Panama'
#   回文: True
#
#   输入: 'Was it a car or a cat I saw'
#   回文: True
#
#   输入: "no 'x' in Nixon"
#   回文: True
#
#   输入: 'python'
#   回文: False
