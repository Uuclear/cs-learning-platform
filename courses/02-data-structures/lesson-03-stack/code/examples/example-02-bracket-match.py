# 括号匹配算法：用栈来检查括号是否正确配对
# 核心思想：遇到左括号入栈，遇到右括号检查栈顶是否匹配，最后栈应该为空

class Stack:
    """简化版栈，只保留括号匹配需要的功能"""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0


def is_matching_pair(left, right):
    """
    判断一对括号是否匹配
    左括号和右括号必须是一家的：()、[]、{}
    """
    pairs = {'(': ')', '[': ']', '{': '}'}
    return pairs.get(left) == right


def check_brackets(expression):
    """
    检查表达式中的括号是否匹配
    返回: (是否匹配, 详细过程信息)
    """
    stack = Stack()
    bracket_count = 0  # 记录括号总数

    print(f"\n检查表达式: {expression}")
    print("-" * 50)

    for i, char in enumerate(expression):
        # 只关心括号，忽略其他字符
        if char in "([{":
            stack.push(char)
            bracket_count += 1
            print(f"  位置{i}: '{char}' → 入栈, 栈: {stack.items}")

        elif char in ")]}":
            bracket_count += 1
            if stack.is_empty():
                # 右括号多了
                print(f"  位置{i}: '{char}' → 栈为空，右括号没有对应的左括号！")
                return False, f"位置{i}的 '{char}' 没有对应的左括号"

            top = stack.pop()
            if is_matching_pair(top, char):
                print(f"  位置{i}: '{char}' ← 匹配 '{top}', 弹出")
            else:
                print(f"  位置{i}: '{char}' ← 不匹配 '{top}'！")
                return False, f"位置{i}的 '{char}' 与 '{top}' 不匹配"

    if stack.is_empty():
        if bracket_count == 0:
            print("  ✓ 没有括号（不需要检查）")
            return True, "没有括号"
        print(f"  ✓ 所有括号都匹配！共检查了 {bracket_count} 个括号")
        return True, "所有括号匹配"
    else:
        print(f"  ✗ 栈不为空，还有未匹配的左括号: {stack.items}")
        return False, f"未闭合的左括号: {stack.items}"


def demo_bracket_matching():
    """演示括号匹配算法"""
    print("=" * 50)
    print("括号匹配算法演示")
    print("=" * 50)

    test_cases = [
        # (表达式, 预期结果描述)
        ("()", "简单的一对括号"),
        ("(a + b) * [c - d]", "混合括号+普通字符"),
        ("{[()]}", "嵌套括号"),
        ("((()))", "多层嵌套"),
        ("([)]", "交错括号（不匹配）"),
        ("({[}])", "乱序括号（不匹配）"),
        (")(", "右括号在前（不匹配）"),
        ("(()", "左括号多了（不匹配）"),
        ("print('hello')", "普通代码（无括号问题）"),
        ("def func(a, b): return a + [b * (c - 1)]", "真实Python代码"),
    ]

    for expr, desc in test_cases:
        result, msg = check_brackets(expr)
        status = "✓ 匹配" if result else "✗ 不匹配"
        print(f"\n结果: {status} | 原因: {msg}")
        print(f"说明: {desc}")
        print("=" * 50)


if __name__ == "__main__":
    demo_bracket_matching()

# 预期输出:
# ==================================================
# 括号匹配算法演示
# ==================================================
#
# 检查表达式: ()
# --------------------------------------------------
#   位置0: '(' → 入栈, 栈: ['(']
#   位置1: ')' ← 匹配 '(', 弹出
#   ✓ 所有括号都匹配！共检查了 2 个括号
#
# 结果: ✓ 匹配 | 原因: 所有括号匹配
# 说明: 简单的一对括号
# ==================================================
#
# 检查表达式: (a + b) * [c - d]
# --------------------------------------------------
#   位置0: '(' → 入栈, 栈: ['(']
#   位置6: ')' ← 匹配 '(', 弹出
#   位置10: '[' → 入栈, 栈: ['[']
#   位置16: ']' ← 匹配 '[', 弹出
#   ✓ 所有括号都匹配！共检查了 4 个括号
#
# 结果: ✓ 匹配 | 原因: 所有括号匹配
# 说明: 混合括号+普通字符
# ==================================================
#
# 检查表达式: {[()]}
# --------------------------------------------------
#   位置0: '{' → 入栈, 栈: ['{']
#   位置1: '[' → 入栈, 栈: ['{', '[']
#   位置2: '(' → 入栈, 栈: ['{', '[', '(']
#   位置3: ')' ← 匹配 '(', 弹出
#   位置4: ']' ← 匹配 '[', 弹出
#   位置5: '}' ← 匹配 '{', 弹出
#   ✓ 所有括号都匹配！共检查了 6 个括号
#
# 结果: ✓ 匹配 | 原因: 所有括号匹配
# 说明: 嵌套括号
# ==================================================
#
# 检查表达式: ([)]
# --------------------------------------------------
#   位置0: '(' → 入栈, 栈: ['(']
#   位置1: '[' → 入栈, 栈: ['(', '[']
#   位置2: ')' ← 不匹配 '['！
#
# 结果: ✗ 不匹配 | 原因: 位置2的 ')' 与 '[' 不匹配
# 说明: 交错括号（不匹配）
# ==================================================
