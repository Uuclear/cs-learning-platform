#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TypeScript类型系统示例 - 示例2：泛型和联合类型

本示例演示TypeScript泛型和联合类型的使用场景。
"""

from typing import TypeVar, Generic, List, Union, Optional


T = TypeVar('T')


class Box(Generic[T]):
    """泛型盒子类"""
    def __init__(self, content: T):
        self.content = content

    def get_content(self) -> T:
        return self.content

    def set_content(self, content: T) -> None:
        self.content = content


def find_first_match(items: List[T], predicate: callable) -> Optional[T]:
    """查找第一个匹配的元素（泛型函数）"""
    for item in items:
        if predicate(item):
            return item
    return None


NumberOrString = Union[int, str]


def process_value(value: NumberOrString) -> str:
    """处理数字或字符串（联合类型）"""
    if isinstance(value, int):
        return f"数字: {value}"
    else:
        return f"字符串: {value}"


def main():
    """主函数"""
    print("🎯 TypeScript泛型和联合类型示例")
    print("=" * 40)

    # 测试泛型类
    string_box = Box("Hello TypeScript")
    number_box = Box(42)

    print(f"字符串盒子内容: {string_box.get_content()}")
    print(f"数字盒子内容: {number_box.get_content()}")

    # 测试泛型函数
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    first_even = find_first_match(numbers, lambda x: x % 2 == 0)
    print(f"第一个偶数: {first_even}")

    words = ["apple", "banana", "cherry", "date"]
    first_long_word = find_first_match(words, lambda x: len(x) > 5)
    print(f"第一个长单词: {first_long_word}")

    # 测试联合类型
    mixed_values: List[NumberOrString] = [1, "hello", 42, "world", 100]
    for value in mixed_values:
        print(f"  {process_value(value)}")

    print("\n📚 学习要点:")
    print("• 泛型允许创建可重用的类型安全组件")
    print("• Union类型表示值可以是多种类型之一")
    print("• 泛型函数可以处理任何类型的参数")
    print("• 联合类型需要运行时类型检查来处理不同情况")
    print("• Python的typing模块提供了丰富的泛型支持")


if __name__ == "__main__":
    main()