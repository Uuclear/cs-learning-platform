#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：WebAssembly 栈机模拟器

这个示例模拟了 WebAssembly 的栈机执行模型。
WebAssembly 使用基于栈的虚拟机，指令从栈中弹出操作数，
执行操作后将结果压回栈中。

支持的基本操作：
- push: 将值压入栈
- add: 弹出两个值，相加后压回结果
- mul: 弹出两个值，相乘后压回结果
- sub: 弹出两个值，相减后压回结果
- div: 弹出两个值，相除后压回结果
"""

class WasmStackMachine:
    """WebAssembly 栈机模拟器"""

    def __init__(self):
        """初始化空栈"""
        self.stack = []

    def push(self, value):
        """将值压入栈"""
        self.stack.append(value)
        print(f"	push {value} -> 栈: {self.stack}")

    def pop(self):
        """从栈中弹出值"""
        if not self.stack:
            raise RuntimeError("栈为空，无法弹出")
        value = self.stack.pop()
        print(f"	pop -> {value}, 栈: {self.stack}")
        return value

    def add(self):
        """执行加法操作：弹出两个值，相加后压回结果"""
        b = self.pop()
        a = self.pop()
        result = a + b
        self.push(result)
        print(f"	add: {a} + {b} = {result}")

    def sub(self):
        """执行减法操作：弹出两个值，相减后压回结果"""
        b = self.pop()
        a = self.pop()
        result = a - b
        self.push(result)
        print(f"	sub: {a} - {b} = {result}")

    def mul(self):
        """执行乘法操作：弹出两个值，相乘后压回结果"""
        b = self.pop()
        a = self.pop()
        result = a * b
        self.push(result)
        print(f"	mul: {a} * {b} = {result}")

    def div(self):
        """执行除法操作：弹出两个值，相除后压回结果"""
        b = self.pop()
        a = self.pop()
        if b == 0:
            raise RuntimeError("除零错误")
        result = a / b
        self.push(result)
        print(f"	div: {a} / {b} = {result}")

    def get_result(self):
        """获取最终结果（栈顶值）"""
        if len(self.stack) != 1:
            raise RuntimeError(f"期望栈中只有一个值，但实际有 {len(self.stack)} 个")
        return self.stack[0]

def main():
    """演示 WebAssembly 栈机执行过程"""
    print("=== WebAssembly 栈机模拟器演示 ===")
    print("计算表达式: (10 + 5) * 2 - 4")
    print("对应的 Wasm 指令序列: push 10, push 5, add, push 2, mul, push 4, sub")
    print()

    machine = WasmStackMachine()

    # 执行指令序列: (10 + 5) * 2 - 4 = 26
    machine.push(10)
    machine.push(5)
    machine.add()      # 10 + 5 = 15
    machine.push(2)
    machine.mul()      # 15 * 2 = 30
    machine.push(4)
    machine.sub()      # 30 - 4 = 26

    result = machine.get_result()
    print(f"\n最终结果: {result}")

    # 演示另一个例子: (8 * 3) / 4 + 2 = 8
    print("\n=== 第二个例子 ===")
    print("计算表达式: (8 * 3) / 4 + 2")
    print("对应的 Wasm 指令序列: push 8, push 3, mul, push 4, div, push 2, add")
    print()

    machine2 = WasmStackMachine()
    machine2.push(8)
    machine2.push(3)
    machine2.mul()     # 8 * 3 = 24
    machine2.push(4)
    machine2.div()     # 24 / 4 = 6
    machine2.push(2)
    machine2.add()     # 6 + 2 = 8

    result2 = machine2.get_result()
    print(f"\n最终结果: {result2}")

if __name__ == "__main__":
    main()