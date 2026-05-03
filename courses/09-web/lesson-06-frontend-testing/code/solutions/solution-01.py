#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 01: Jest 测试模拟器实现

这个文件提供了完整的 Jest 测试框架模拟实现，
包括 describe/it 块、expect 断言系统和 mock 函数。
"""

import functools
from typing import Any, Callable, Dict, List


class MockFunction:
    """Jest mock 函数的完整实现"""

    def __init__(self):
        self.calls = []
        self.return_value = None
        self.implementation = None

    def __call__(self, *args, **kwargs):
        call_record = {"args": args, "kwargs": kwargs}
        self.calls.append(call_record)

        if self.implementation:
            return self.implementation(*args, **kwargs)
        return self.return_value

    def mock_return_value(self, value: Any):
        self.return_value = value
        return self

    def mock_implementation(self, func: Callable):
        self.implementation = func
        return self

    def mock_calls_length(self) -> int:
        return len(self.calls)

    def mock_last_call(self):
        return self.calls[-1] if self.calls else None

    def mock_clear(self):
        self.calls = []


class Expect:
    """Jest expect 断言系统的完整实现"""

    def __init__(self, actual_value: Any):
        self.actual = actual_value

    def to_be(self, expected_value: Any):
        assert self.actual is expected_value, f"期望 {expected_value} (严格相等), 但得到 {self.actual}"

    def to_equal(self, expected_value: Any):
        assert self.actual == expected_value, f"期望 {expected_value} (深度相等), 但得到 {self.actual}"

    def to_be_truthy(self):
        assert bool(self.actual), f"期望真值, 但得到 {self.actual}"

    def to_be_falsy(self):
        assert not bool(self.actual), f"期望假值, 但得到 {self.actual}"

    def to_be_defined(self):
        assert self.actual is not None, f"期望定义的值, 但得到 {self.actual}"

    def to_be_null(self):
        assert self.actual is None, f"期望 null, 但得到 {self.actual}"


def expect(actual_value: Any) -> Expect:
    return Expect(actual_value)


def describe(description: str, test_func: Callable):
    print(f"🧪 测试套件: {description}")
    test_func()


def it(description: str, test_func: Callable):
    try:
        test_func()
        print(f"✅ 通过: {description}")
    except AssertionError as e:
        print(f"❌ 失败: {description} - {e}")
    except Exception as e:
        print(f"💥 错误: {description} - {e}")


def mock_fn() -> MockFunction:
    return MockFunction()


# 完整的测试示例
def run_complete_tests():
    """运行完整的测试套件"""

    def test_string_utils():
        def capitalize(s: str) -> str:
            return s.upper()

        def test_capitalize_basic():
            result = capitalize("hello")
            expect(result).to_equal("HELLO")

        def test_capitalize_empty():
            result = capitalize("")
            expect(result).to_equal("")

        it("应该正确转换字符串为大写", test_capitalize_basic)
        it("应该处理空字符串", test_capitalize_empty)

    def test_async_operations():
        def async_operation(callback: Callable):
            # 模拟异步操作
            import threading
            import time

            def worker():
                time.sleep(0.01)  # 模拟延迟
                callback("success")

            thread = threading.Thread(target=worker)
            thread.start()
            thread.join()

        def test_async_callback():
            result = {"value": None}

            def callback(value):
                result["value"] = value

            async_operation(callback)
            expect(result["value"]).to_equal("success")

        it("应该正确处理异步回调", test_async_callback)

    def test_mock_advanced():
        def test_mock_with_implementation():
            mock_func = mock_fn()
            mock_func.mock_implementation(lambda x: x * 2)

            result = mock_func(5)
            expect(result).to_equal(10)
            expect(mock_func.mock_calls_length()).to_equal(1)

        def test_mock_clearing():
            mock_func = mock_fn()
            mock_func(1)
            mock_func(2)

            expect(mock_func.mock_calls_length()).to_equal(2)
            mock_func.mock_clear()
            expect(mock_func.mock_calls_length()).to_equal(0)

        it("应该支持自定义实现", test_mock_with_implementation)
        it("应该支持清除调用记录", test_mock_clearing)

    describe("字符串工具函数测试", test_string_utils)
    describe("异步操作测试", test_async_operations)
    describe("高级 Mock 测试", test_mock_advanced)


if __name__ == "__main__":
    print("🚀 运行完整 Jest 模拟测试解决方案...")
    run_complete_tests()
    print("🏁 所有测试完成!")