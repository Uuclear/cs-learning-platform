#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TypeScript类型系统模拟 - 解决方案3：接口和类型守卫

本解决方案演示如何在Python中模拟TypeScript的接口、类型守卫和高级类型操作。
"""

from typing import Protocol, runtime_checkable, Union, List, Dict, Any, Optional
from abc import ABC, abstractmethod


# 使用Protocol模拟TypeScript接口（结构化类型）
@runtime_checkable
class Drawable(Protocol):
    """可绘制对象接口"""
    def draw(self) -> str:
        ...


@runtime_checkable
class Movable(Protocol):
    """可移动对象接口"""
    def move(self, x: int, y: int) -> str:
        ...


class Circle:
    """圆形类 - 实现Drawable接口"""

    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"绘制圆形，半径: {self.radius}"

    def area(self) -> float:
        return 3.14159 * self.radius ** 2


class Rectangle:
    """矩形类 - 实现Drawable和Movable接口"""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def draw(self) -> str:
        return f"绘制矩形，宽: {self.width}, 高: {self.height}"

    def move(self, x: int, y: int) -> str:
        self.x = x
        self.y = y
        return f"矩形移动到位置 ({x}, {y})"

    def area(self) -> float:
        return self.width * self.height


# 使用抽象基类模拟TypeScript抽象类
class Shape(ABC):
    """抽象形状类"""

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass


class Triangle(Shape):
    """三角形类"""

    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        # 使用海伦公式
        s = (self.a + self.b + self.c) / 2
        return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5

    def perimeter(self) -> float:
        return self.a + self.b + self.c


# 类型守卫函数
def is_drawable(obj: Any) -> bool:
    """检查对象是否实现了Drawable接口"""
    return isinstance(obj, Drawable)


def is_movable(obj: Any) -> bool:
    """检查对象是否实现了Movable接口"""
    return isinstance(obj, Movable)


def is_shape(obj: Any) -> bool:
    """检查对象是否是Shape实例"""
    return isinstance(obj, Shape)


# 条件类型模拟
def process_shape(shape: Union[Drawable, Shape]) -> str:
    """根据类型处理不同形状"""
    if is_drawable(shape):
        return shape.draw()
    elif is_shape(shape):
        return f"抽象形状，面积: {shape.area():.2f}"
    else:
        return "未知形状"


# 映射类型模拟
def create_validator(schema: Dict[str, type]) -> callable:
    """创建基于模式的验证器（模拟TypeScript映射类型）"""
    def validate(data: Dict[str, Any]) -> bool:
        for key, expected_type in schema.items():
            if key not in data or not isinstance(data[key], expected_type):
                return False
        return True
    return validate


def main():
    """主函数"""
    print("🎯 TypeScript类型系统模拟 - Solution 3: 接口和类型守卫")
    print("=" * 60)

    # 测试接口实现
    circle = Circle(5.0)
    rectangle = Rectangle(4.0, 6.0)

    shapes: List[Drawable] = [circle, rectangle]
    for shape in shapes:
        print(f"🎨 {shape.draw()}")

    # 测试多接口实现
    if is_movable(rectangle):
        print(f"🚚 {rectangle.move(10, 20)}")

    # 测试抽象类
    triangle = Triangle(3.0, 4.0, 5.0)
    print(f"🔺 三角形 - 周长: {triangle.perimeter():.2f}, 面积: {triangle.area():.2f}")

    # 测试类型守卫
    test_objects = [circle, rectangle, triangle, "not a shape"]
    for obj in test_objects:
        result = process_shape(obj) if hasattr(obj, 'draw') or isinstance(obj, Shape) else "无法处理"
        print(f"🔍 处理结果: {result}")

    # 测试映射类型验证器
    user_schema = {"name": str, "age": int, "email": str}
    user_validator = create_validator(user_schema)

    valid_user = {"name": "张三", "age": 25, "email": "zhangsan@example.com"}
    invalid_user = {"name": "李四", "age": "twenty-five"}  # age类型错误

    print(f"✅ 有效用户验证: {user_validator(valid_user)}")
    print(f"❌ 无效用户验证: {user_validator(invalid_user)}")

    print("\n💡 关键要点:")
    print("• Python Protocol可以模拟TypeScript接口（鸭子类型）")
    print("• 抽象基类(ABC)可以模拟TypeScript抽象类")
    print("• 类型守卫通过isinstance()和自定义函数实现")
    print("• 联合类型使用Union[T1, T2]表示")
    print("• 可以通过工厂函数模拟TypeScript的映射类型")
    print("• runtime_checkable装饰器允许运行时检查Protocol")


if __name__ == "__main__":
    main()