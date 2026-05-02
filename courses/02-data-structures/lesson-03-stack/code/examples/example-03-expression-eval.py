# 表达式求值：用栈把中缀表达式变成后缀表达式，然后计算
# 核心思想：人写的算式（中缀）计算机不好算，转成后缀（逆波兰）就好算了

import ast
import operator as op

class Stack:
    """简易栈"""
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


# 运算符优先级
PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3,  # 幂运算，优先级最高
}


def infix_to_postfix(expression):
    """
    中缀表达式 → 后缀表达式（逆波兰表达式）
    例如: "3 + 4 * 2" → "3 4 2 * +"
    使用栈来处理运算符的优先级和括号

    算法步骤：
    1. 数字直接输出
    2. 左括号入栈
    3. 右括号：把栈顶到左括号之间的运算符全部输出
    4. 运算符：把栈中优先级 >= 自己的运算符都弹出再入栈
    5. 最后把栈里剩余的运算符全部输出
    """
    output = []   # 后缀表达式结果
    op_stack = Stack()  # 运算符栈

    tokens = expression.split()  # 按空格分词

    print(f"  中缀表达式: {expression}")
    print(f"  分词结果: {tokens}")

    for token in tokens:
        if token.isdigit() or token.replace('.', '', 1).isdigit():
            # 数字：直接输出
            output.append(token)
            print(f"    数字 '{token}' → 输出")

        elif token == '(':
            # 左括号：入栈
            op_stack.push(token)
            print(f"    左括号 '(' → 入栈")

        elif token == ')':
            # 右括号：弹出到左括号
            print(f"    右括号 ')' → 弹出到左括号")
            while not op_stack.is_empty() and op_stack.peek() != '(':
                output.append(op_stack.pop())
                print(f"      弹出运算符 '{output[-1]}' → 输出")
            op_stack.pop()  # 扔掉左括号

        elif token in PRECEDENCE:
            # 运算符：处理优先级
            print(f"    运算符 '{token}' → 处理优先级")
            while (not op_stack.is_empty()
                   and op_stack.peek() != '('
                   and PRECEDENCE.get(op_stack.peek(), 0) >= PRECEDENCE.get(token, 0)):
                output.append(op_stack.pop())
                print(f"      弹出 '{output[-1]}'（优先级>= '{token}'）→ 输出")
            op_stack.push(token)
            print(f"      '{token}' → 入栈")

    # 弹出栈中剩余的运算符
    while not op_stack.is_empty():
        op_char = op_stack.pop()
        output.append(op_char)
        print(f"    弹出 '{op_char}' → 输出")

    postfix = ' '.join(output)
    print(f"  后缀表达式: {postfix}\n")
    return output


def evaluate_postfix(postfix_tokens):
    """
    计算后缀表达式
    例如: ["3", "4", "2", "*", "+"] → 3 + 4*2 = 11
    使用栈：遇到数字入栈，遇到运算符弹出两个数计算后入栈
    """
    stack = Stack()

    print(f"  计算后缀表达式: {' '.join(postfix_tokens)}")

    for token in postfix_tokens:
        if token.replace('.', '', 1).isdigit():
            # 数字：入栈
            stack.push(float(token))
            print(f"    数字 '{token}' → 入栈, 栈: {stack.items}")
        else:
            # 运算符：弹出两个数计算
            b = stack.pop()  # 注意：先弹出的是右操作数
            a = stack.pop()  # 后弹出的是左操作数

            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                result = a / b
            elif token == '^':
                result = a ** b
            else:
                raise ValueError(f"未知运算符: {token}")

            stack.push(result)
            print(f"    {a} {token} {b} = {result} → 入栈, 栈: {stack.items}")

    final = stack.pop()
    # 处理浮点显示：整数就显示为整数
    if final == int(final):
        final = int(final)
    print(f"  最终结果: {final}\n")
    return final


def safe_eval_expression(expr_str):
    """
    安全地计算只包含数字和四则运算的表达式
    手动解析AST并计算，不用eval
    """
    # 将 ^ 替换为 **
    expr_str = expr_str.replace('^', '**')
    try:
        tree = ast.parse(expr_str, mode='eval')
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                     ast.Constant, ast.Num, ast.Add, ast.Sub,
                                     ast.Mult, ast.Div, ast.Pow, ast.USub,
                                     ast.Mod)):
                raise ValueError("表达式包含不支持的操作")
        return _eval_ast(tree.body)
    except Exception:
        return None


def _eval_ast(node):
    """递归计算AST节点的值"""
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Num):  # Python 3.7兼容
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        ops = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Pow: op.pow,
        }
        op_type = type(node.op)
        if op_type in ops:
            return ops[op_type](left, right)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_ast(node.operand)
    raise ValueError("不支持的节点类型")


def evaluate_expression(expression):
    """
    完整流程：中缀 → 后缀 → 求值
    """
    print(f"\n{'=' * 50}")
    print(f"表达式求值")
    print(f"{'=' * 50}")

    postfix = infix_to_postfix(expression)
    result = evaluate_postfix(postfix)
    return result


def demo_expression_evaluation():
    """演示表达式求值"""
    test_cases = [
        "3 + 4 * 2",           # 优先级：乘法先算 → 3 + 8 = 11
        "( 3 + 4 ) * 2",       # 括号优先 → 7 * 2 = 14
        "10 - 3 * 2 + 4",      # 混合运算 → 10 - 6 + 4 = 8
        "2 ^ 3 + 4 * 5",       # 幂运算优先级最高 → 8 + 20 = 28
        "( 1 + 2 ) * ( 3 + 4 )",  # 多括号 → 3 * 7 = 21
    ]

    for expr in test_cases:
        result = evaluate_expression(expr)
        # 用ast安全验证
        expected = safe_eval_expression(expr.replace('^', '**'))
        match = '✓' if result == expected else '✗'
        print(f"  验证: {expr} = {expected} {match}\n")
        print(f"{'=' * 50}")


if __name__ == "__main__":
    demo_expression_evaluation()

# 预期输出（部分展示）:
# ==================================================
# 表达式求值
# ==================================================
#   中缀表达式: 3 + 4 * 2
#   分词结果: ['3', '+', '4', '*', '2']
#     数字 '3' → 输出
#     运算符 '+' → 处理优先级
#       '+' → 入栈
#     数字 '4' → 输出
#     运算符 '*' → 处理优先级
#       '*' → 入栈
#     数字 '2' → 输出
#     弹出 '*' → 输出
#     弹出 '+' → 输出
#   后缀表达式: 3 4 2 * +
#
#   计算后缀表达式: 3 4 2 * +
#     数字 '3' → 入栈, 栈: [3.0]
#     数字 '4' → 入栈, 栈: [3.0, 4.0]
#     数字 '2' → 入栈, 栈: [3.0, 4.0, 2.0]
#     4.0 * 2.0 = 8.0 → 入栈, 栈: [3.0, 8.0]
#     3.0 + 8.0 = 11.0 → 入栈, 栈: [11.0]
#   最终结果: 11
#
#   验证: 3 + 4 * 2 = 11 ✓
