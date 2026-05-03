#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：WebAssembly 栈机实现

这是 example-01-wasm-concept.py 的完整解决方案。
包含了所有基本的栈操作和错误处理。
"""

class WasmStackMachine:
    """WebAssembly 栈机模拟器"""

    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if not self.stack:
            raise RuntimeError("栈为空")
        return self.stack.pop()

    def add(self):
        b = self.pop()
        a = self.pop()
        self.push(a + b)

    def sub(self):
        b = self.pop()
        a = self.pop()
        self.push(a - b)

    def mul(self):
        b = self.pop()
        a = self.pop()
        self.push(a * b)

    def div(self):
        b = self.pop()
        a = self.pop()
        if b == 0:
            raise RuntimeError("除零错误")
        self.push(a / b)

    def get_result(self):
        if len(self.stack) != 1:
            raise RuntimeError(f"期望一个结果，但栈中有 {len(self.stack)} 个值")
        return self.stack[0]

def main():
    # 测试用例1: (10 + 5) * 2 - 4 = 26
    machine = WasmStackMachine()
    machine.push(10)
    machine.push(5)
    machine.add()
    machine.push(2)
    machine.mul()
    machine.push(4)
    machine.sub()
    assert machine.get_result() == 26

    # 测试用例2: (8 * 3) / 4 + 2 = 8
    machine2 = WasmStackMachine()
    machine2.push(8)
    machine2.push(3)
    machine2.mul()
    machine2.push(4)
    machine2.div()
    machine2.push(2)
    machine2.add()
    assert machine2.get_result() == 8.0

    print("✓ 所有测试通过！")

if __name__ == "__main__":
    main()