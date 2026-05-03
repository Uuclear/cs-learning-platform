#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TypeScript类型系统示例 - 示例3：接口和类型守卫

本示例演示TypeScript接口和类型守卫的使用模式。
"""

from typing import Protocol, runtime_checkable, Union, List


@runtime_checkable
class Animal(Protocol):
    """动物接口"""
    def make_sound(self) -> str:
        ...

    def move(self) -> str:
        ...


class Dog:
    """狗类 - 实现Animal接口"""
    def make_sound(self) -> str:
        return "汪汪！"

    def move(self) -> str:
        return "狗在跑"


class Bird:
    """鸟类 - 实现Animal接口"""
    def make_sound(self) -> str:
        return "啾啾！"

    def move(self) -> str:
        return "鸟在飞"


def is_animal(obj) -> bool:
    """类型守卫：检查是否为Animal"""
    return isinstance(obj, Animal)


def make_animal_sound(animal: Animal) -> str:
    """让动物发出声音"""
    return animal.make_sound()


def process_animals(animals: List[Union[Animal, str]]) -> None:
    """处理动物列表"""
    for item in animals:
        if is_animal(item):
            print(f"🔊 {make_animal_sound(item)}")
            print(f"🏃 {item.move()}")
        else:
            print(f"❓ 未知项目: {item}")


def main():
    """主函数"""
    print("🎯 TypeScript接口和类型守卫示例")
    print("=" * 40)

    # 创建动物实例
    dog = Dog()
    bird = Bird()

    # 测试接口实现
    animals: List[Animal] = [dog, bird]
    for animal in animals:
        print(f"动物声音: {animal.make_sound()}")
        print(f"动物移动: {animal.move()}")

    # 测试类型守卫
    mixed_list = [dog, bird, "不是动物", dog]
    process_animals(mixed_list)

    print("\n📚 学习要点:")
    print("• Protocol可以定义接口契约")
    print("• runtime_checkable允许运行时类型检查")
    print("• 类型守卫帮助处理联合类型")
    print("• 接口支持多态性")
    print("• 结构化类型（鸭子类型）vs 名义类型")


if __name__ == "__main__":
    main()