# solution-02.py - 简单计算器
def simple_calculator(num1, num2, operation):
    """
    简单计算器函数

    参数:
        num1: 第一个数字
        num2: 第二个数字
        operation: 运算符 ("+", "-", "*", "/")

    返回:
        计算结果

    异常:
        ValueError: 如果运算符不支持
        ZeroDivisionError: 如果除数为零
        TypeError: 如果输入不是数字
    """
    # 输入验证
    if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
        raise TypeError("输入必须是数字")

    # 执行运算
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        if num2 == 0:
            raise ZeroDivisionError("除数不能为零")
        return num1 / num2
    else:
        raise ValueError(f"不支持的运算符: {operation}")

# 测试示例
if __name__ == "__main__":
    try:
        print(f"10 + 5 = {simple_calculator(10, 5, '+')}")
        print(f"10 - 5 = {simple_calculator(10, 5, '-')}")
        print(f"10 * 5 = {simple_calculator(10, 5, '*')}")
        print(f"10 / 5 = {simple_calculator(10, 5, '/')}")

        # 测试除零错误
        print(simple_calculator(10, 0, '/'))
    except (ValueError, ZeroDivisionError, TypeError) as e:
        print(f"错误: {e}")