#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TypeScript类型系统示例 - 示例1：基础类型注解

本示例演示TypeScript基础类型注解的概念和用法。
"""

from typing import List, Dict, Optional


def calculate_area(width: float, height: float) -> float:
    """计算矩形面积"""
    return width * height


def greet_person(name: str, age: Optional[int] = None) -> str:
    """问候某人"""
    if age is not None:
        return f"你好，{name}！你今年{age}岁。"
    else:
        return f"你好，{name}！"


class Student:
    """学生类"""
    def __init__(self, name: str, grades: List[float]):
        self.name = name
        self.grades = grades

    def get_average_grade(self) -> float:
        """获取平均成绩"""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)


def main():
    """主函数"""
    print("🎯 TypeScript基础类型注解示例")
    print("=" * 40)

    # 测试基本类型
    area = calculate_area(5.0, 3.0)
    print(f"矩形面积: {area}")

    # 测试可选参数
    greeting1 = greet_person("张三", 25)
    greeting2 = greet_person("李四")
    print(f"问候1: {greeting1}")
    print(f"问候2: {greeting2}")

    # 测试对象和数组类型
    student = Student("王五", [85.5, 92.0, 78.5, 88.0])
    avg_grade = student.get_average_grade()
    print(f"学生 {student.name} 的平均成绩: {avg_grade:.2f}")

    print("\n📚 学习要点:")
    print("• 函数参数和返回值可以添加类型注解")
    print("• Optional[T] 表示可选类型（可能为None）")
    print("• List[T] 表示类型化的列表")
    print("• 类属性也可以添加类型注解")
    print("• 类型注解提高代码可读性和维护性")


if __name__ == "__main__":
    main()