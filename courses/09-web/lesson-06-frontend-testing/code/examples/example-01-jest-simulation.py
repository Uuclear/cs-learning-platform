#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jest 单元测试框架模拟器

这个文件模拟了 Jest 测试框架的核心功能：
- describe/it 测试块组织
- expect 断言系统
- mock 函数创建和验证
- 基本的测试运行器

注意：这是一个教学演示，不是完整的 Jest 实现。
"""

import functools
from typing import Any, Callable, Dict, List


class MockFunction:
    """模拟 Jest 的 mock 函数"""

    def __init__(self):
        self.calls = []  # 存储所有调用记录
        self.return_value = None  # 默认返回值

    def __call__(self, *args, **kwargs):
        """当函数被调用时记录参数"""
        call_record = {"args": args, "kwargs": kwargs}
        self.calls.append(call_record)
        return self.return_value

    def mock_return_value(self, value: Any):
        """设置 mock 函数的返回值"""
        self.return_value = value
        return self

    def mock_calls_length(self) -> int:
        """获取函数被调用的次数"""
        return len(self.calls)

    def mock_last_call(self):
        """获取最后一次调用的参数"""
        if self.calls:
            return self.calls[-1]
        return None


class Expect:
    """模拟 Jest 的 expect 断言系统"""

    def __init__(self, actual_value: Any):
        self.actual = actual_value

    def to_be(self, expected_value: Any):
        """严格相等断言 (===)"""
        assert self.actual is expected_value, f"期望 {expected_value}, 但得到 {self.actual}"

    def to_equal(self, expected_value: Any):
        """深度相等断言 (==)"""
        assert self.actual == expected_value, f"期望 {expected_value}, 但得到 {self.actual}"

    def to_be_truthy(self):
        """断言值为真"""
        assert bool(self.actual), f"期望真值, 但得到 {self.actual}"

    def to_be_falsy(self):
        """断言值为假"""
        assert not bool(self.actual), f"期望假值, 但得到 {self.actual}"


def expect(actual_value: Any) -> Expect:
    """创建 expect 断言对象"""
    return Expect(actual_value)


def describe(description: str, test_func: Callable):
    """定义测试套件 (describe block)"""
    print(f"🧪 测试套件: {description}")
    test_func()


def it(description: str, test_func: Callable):
    """定义单个测试用例 (test case)"""
    try:
        test_func()
        print(f"✅ 通过: {description}")
    except AssertionError as e:
        print(f"❌ 失败: {description} - {e}")
    except Exception as e:
        print(f"💥 错误: {description} - {e}")


def mock_fn() -> MockFunction:
    """创建 mock 函数"""
    return MockFunction()


# 示例测试用例
def test_math_functions():
    """测试数学函数"""

    def add(a: int, b: int) -> int:
        return a + b

    def test_add_positive_numbers():
        result = add(2, 3)
        expect(result).to_equal(5)

    def test_add_negative_numbers():
        result = add(-1, -1)
        expect(result).to_equal(-2)

    it("应该正确计算正数相加", test_add_positive_numbers)
    it("应该正确计算负数相加", test_add_negative_numbers)


def test_mock_functions():
    """测试 mock 函数功能"""

    def test_mock_basic_usage():
        mock_func = mock_fn()
        mock_func.mock_return_value("hello")

        result = mock_func("world")
        expect(result).to_equal("hello")
        expect(mock_func.mock_calls_length()).to_equal(1)

    def test_mock_call_tracking():
        mock_func = mock_fn()
        mock_func(1, 2, name="test")

        last_call = mock_func.mock_last_call()
        expect(last_call["args"]).to_equal((1, 2))
        expect(last_call["kwargs"]["name"]).to_equal("test")

    it("应该正确返回 mock 值并跟踪调用", test_mock_basic_usage)
    it("应该正确记录调用参数", test_mock_call_tracking)


if __name__ == "__main__":
    print("🚀 开始运行 Jest 模拟测试...")

    describe("数学函数测试", test_math_functions)
    describe("Mock 函数测试", test_mock_functions)

    print("🏁 测试运行完成!")