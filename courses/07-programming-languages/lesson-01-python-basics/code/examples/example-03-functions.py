# functions.py
def greet(name, greeting="你好"):
    """向某人打招呼的函数

    参数:
        name (str): 要打招呼的人的名字
        greeting (str): 问候语，默认为"你好"

    返回:
        str: 完整的问候消息
    """
    return f"{greeting}, {name}!"

def calculate_area(length, width):
    """计算矩形面积"""
    return length * width

def is_even(number):
    """判断数字是否为偶数"""
    return number % 2 == 0

# 使用函数
message = greet("小明")
print(message)

area = calculate_area(5, 3)
print(f"面积: {area}")

print(f"4是偶数吗? {is_even(4)}")
print(f"7是偶数吗? {is_even(7)}")

# Lambda函数（匿名函数）
square = lambda x: x ** 2
print(f"5的平方: {square(5)}")