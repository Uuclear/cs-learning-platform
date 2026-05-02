# 栈操作演示
# 模拟函数调用时的栈行为

class Stack:
    """简单的栈实现"""
    def __init__(self):
        self.items = []

    def push(self, item):
        """入栈"""
        self.items.append(item)
        print(f"  压栈: {item} → 栈: {self.items}")

    def pop(self):
        """出栈"""
        if not self.items:
            return None
        item = self.items.pop()
        print(f"  弹栈: {item} → 栈: {self.items}")
        return item

    def peek(self):
        """查看栈顶"""
        return self.items[-1] if self.items else None

    def __str__(self):
        return str(self.items)


def factorial(n, call_stack):
    """
    计算阶乘，展示递归调用时的栈行为
    """
    # 创建栈帧信息
    frame_info = f"factorial({n})"
    call_stack.push(frame_info)

    print(f"  计算 {n}! ...")

    if n <= 1:
        result = 1
        print(f"  基准情况: {n}! = 1")
    else:
        result = n * factorial(n - 1, call_stack)
        print(f"  回溯: {n}! = {n} × {(result // n)} = {result}")

    call_stack.pop()
    return result


def demonstrate_stack():
    """
    演示栈的工作原理
    """
    print("=== 栈操作演示 ===\n")

    # 1. 基本栈操作
    print("1. 基本栈操作（后进先出）:")
    stack = Stack()
    print(f"初始栈: {stack}")

    stack.push("函数A")
    stack.push("函数B")
    stack.push("函数C")

    print(f"\n当前栈顶: {stack.peek()}")
    print("开始弹栈:")
    stack.pop()
    stack.pop()
    stack.pop()
    print()

    # 2. 函数调用栈演示
    print("2. 递归函数调用栈演示（计算 4!）:")
    call_stack = Stack()
    result = factorial(4, call_stack)
    print(f"\n最终结果: 4! = {result}")
    print()

    # 3. 展示局部变量的生命周期
    print("3. 局部变量生命周期演示:")
    demonstrate_local_variables()


def demonstrate_local_variables():
    """演示局部变量在栈中的行为"""
    x = 10
    print(f"  外层函数: x = {x}, id = {hex(id(x))}")

    def inner_function():
        y = 20
        print(f"  内层函数: y = {y}, id = {hex(id(y))}")
        print(f"  内层函数可以访问外层变量: x = {x}")
        return y

    result = inner_function()
    # y 在这里已经不可访问了（已从栈中弹出）
    print(f"  回到外层: result = {result}")
    print(f"  注意: y 已经随着 inner_function 的返回而被释放了")


# 运行演示
if __name__ == "__main__":
    demonstrate_stack()

# 输出示例:
# === 栈操作演示 ===
#
# 1. 基本栈操作（后进先出）:
# 初始栈: []
#   压栈: 函数A → 栈: ['函数A']
#   压栈: 函数B → 栈: ['函数A', '函数B']
#   压栈: 函数C → 栈: ['函数A', '函数B', '函数C']
#
# 当前栈顶: 函数C
# 开始弹栈:
#   弹栈: 函数C → 栈: ['函数A', '函数B']
#   弹栈: 函数B → 栈: ['函数A']
#   弹栈: 函数A → 栈: []
#
# 2. 递归函数调用栈演示（计算 4!）:
#   压栈: factorial(4) → 栈: ['factorial(4)']
#   计算 4! ...
#   压栈: factorial(3) → 栈: ['factorial(4)', 'factorial(3)']
#   计算 3! ...
#   ...
