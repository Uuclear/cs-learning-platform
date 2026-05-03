#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TypeScript类型系统模拟 - 解决方案2：泛型和高级类型

本解决方案演示如何在Python中模拟TypeScript的泛型和高级类型特性。
"""

from typing import TypeVar, Generic, List, Dict, Optional, Union, Callable


# 定义泛型类型变量
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


class Stack(Generic[T]):
    """模拟TypeScript泛型类 - 栈数据结构"""

    def __init__(self):
        self._items: List[T] = []

    def push(self, item: T) -> None:
        """压入元素"""
        self._items.append(item)

    def pop(self) -> Optional[T]:
        """弹出元素"""
        if self._items:
            return self._items.pop()
        return None

    def peek(self) -> Optional[T]:
        """查看栈顶元素"""
        if self._items:
            return self._items[-1]
        return None

    def is_empty(self) -> bool:
        """检查是否为空"""
        return len(self._items) == 0

    def size(self) -> int:
        """获取栈大小"""
        return len(self._items)


def identity(value: T) -> T:
    """泛型恒等函数"""
    return value


def map_list(func: Callable[[T], V], items: List[T]) -> List[V]:
    """泛型映射函数"""
    return [func(item) for item in items]


# 联合类型和交叉类型模拟
NumberOrString = Union[int, str]
UserDict = Dict[str, Union[str, int, bool]]


def process_mixed_data(data: NumberOrString) -> str:
    """处理联合类型数据"""
    if isinstance(data, int):
        return f"数字: {data}"
    else:
        return f"字符串: {data}"


class ApiResponse(Generic[T]):
    """模拟API响应泛型类"""

    def __init__(self, success: bool, data: Optional[T] = None, error: Optional[str] = None):
        self.success = success
        self.data = data
        self.error = error

    def __str__(self) -> str:
        if self.success:
            return f"成功: {self.data}"
        else:
            return f"错误: {self.error}"


def fetch_user(user_id: int) -> ApiResponse[Dict[str, str]]:
    """模拟获取用户数据的API调用"""
    if user_id > 0:
        user_data = {"id": str(user_id), "name": f"用户{user_id}", "email": f"user{user_id}@example.com"}
        return ApiResponse(True, user_data)
    else:
        return ApiResponse(False, error="无效的用户ID")


def main():
    """主函数"""
    print("🎯 TypeScript类型系统模拟 - Solution 2: 泛型和高级类型")
    print("=" * 60)

    # 测试泛型栈
    string_stack = Stack[str]()
    string_stack.push("Hello")
    string_stack.push("World")
    print(f"字符串栈: {string_stack.pop()}, {string_stack.pop()}")

    number_stack = Stack[int]()
    number_stack.push(1)
    number_stack.push(2)
    number_stack.push(3)
    print(f"数字栈大小: {number_stack.size()}")
    print(f"栈顶元素: {number_stack.peek()}")

    # 测试泛型函数
    numbers = [1, 2, 3, 4, 5]
    doubled = map_list(lambda x: x * 2, numbers)
    print(f"原数组: {numbers}")
    print(f"翻倍后: {doubled}")

    # 测试联合类型
    mixed_values: List[NumberOrString] = [42, "hello", 100, "world"]
    for value in mixed_values:
        print(f"  {process_mixed_data(value)}")

    # 测试泛型API响应
    success_response = fetch_user(123)
    error_response = fetch_user(-1)
    print(f"成功响应: {success_response}")
    print(f"错误响应: {error_response}")

    print("\n💡 关键要点:")
    print("• Python的Generic和TypeVar可以模拟TypeScript泛型")
    print("• Union类型对应TypeScript联合类型 (A | B)")
    print("• 可以创建泛型类、函数和类型别名")
    print("• 泛型提供类型安全的同时保持代码可重用性")
    print("• 运行时仍需要手动类型检查，但开发时有类型提示")


if __name__ == "__main__":
    main()