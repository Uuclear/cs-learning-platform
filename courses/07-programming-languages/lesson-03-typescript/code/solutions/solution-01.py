#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TypeScript类型系统模拟 - 解决方案1：基础类型注解

本解决方案演示如何在Python中模拟TypeScript的基础类型注解系统。
使用Python的typing模块来提供类似TypeScript的类型安全。
"""

from typing import Union, Optional, List, Dict, Any


def greet_user(name: str, age: int) -> str:
    """模拟TypeScript函数类型注解"""
    return f"你好，{name}！你今年{age}岁。"


def process_numbers(numbers: List[int]) -> Dict[str, Union[int, float]]:
    """处理数字列表并返回统计信息"""
    if not numbers:
        return {"count": 0, "sum": 0, "average": 0.0}

    total = sum(numbers)
    count = len(numbers)
    average = total / count

    return {
        "count": count,
        "sum": total,
        "average": average
    }


class User:
    """模拟TypeScript接口"""
    def __init__(self, name: str, email: str, age: Optional[int] = None):
        self.name = name
        self.email = email
        self.age = age

    def __str__(self) -> str:
        age_info = f", 年龄: {self.age}" if self.age else ""
        return f"用户: {self.name}, 邮箱: {self.email}{age_info}"


def validate_user_data(data: Dict[str, Any]) -> bool:
    """验证用户数据结构（模拟TypeScript类型守卫）"""
    required_fields = ["name", "email"]

    # 检查必需字段
    for field in required_fields:
        if field not in data or not isinstance(data[field], str):
            return False

    # 检查可选字段
    if "age" in data and not isinstance(data["age"], int):
        return False

    return True


def main():
    """主函数"""
    print("🎯 TypeScript类型系统模拟 - Solution 1: 基础类型注解")
    print("=" * 60)

    # 测试函数类型注解
    message = greet_user("张三", 25)
    print(f"💬 {message}")

    # 测试数组和对象类型
    stats = process_numbers([1, 2, 3, 4, 5])
    print(f"📊 统计信息: {stats}")

    # 测试类和可选属性
    user1 = User("李四", "lisi@example.com", 30)
    user2 = User("王五", "wangwu@example.com")  # 年龄可选
    print(f"👤 {user1}")
    print(f"👤 {user2}")

    # 测试类型守卫
    valid_data = {"name": "赵六", "email": "zhaoliu@example.com", "age": 28}
    invalid_data = {"name": "钱七", "phone": "123456789"}  # 缺少email

    print(f"✅ 有效数据验证: {validate_user_data(valid_data)}")
    print(f"❌ 无效数据验证: {validate_user_data(invalid_data)}")

    print("\n💡 关键要点:")
    print("• Python的typing模块提供了类似TypeScript的类型注解")
    print("• Union类型对应TypeScript的联合类型 (string | number)")
    print("• Optional[T]对应TypeScript的可选属性 (property?)")
    print("• 类型注解在运行时不会强制执行，但可以用于静态分析")
    print("• 可以通过手动验证实现类似TypeScript类型守卫的功能")


if __name__ == "__main__":
    main()