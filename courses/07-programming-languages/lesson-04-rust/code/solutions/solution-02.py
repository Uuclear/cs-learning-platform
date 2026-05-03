#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rust借用系统模拟 - 解决方案2：借用和引用规则

本解决方案演示如何在Python中模拟Rust的借用规则和引用系统。
"""

from typing import List, Optional


class BorrowChecker:
    """借用检查器，模拟Rust的借用规则"""

    def __init__(self):
        self._mutable_borrowed = False
        self._immutable_borrows = 0

    def borrow_mut(self) -> bool:
        """尝试获取可变借用"""
        if self._mutable_borrowed or self._immutable_borrows > 0:
            return False
        self._mutable_borrowed = True
        return True

    def borrow_immutable(self) -> bool:
        """尝试获取不可变借用"""
        if self._mutable_borrowed:
            return False
        self._immutable_borrows += 1
        return True

    def release_mut(self) -> None:
        """释放可变借用"""
        self._mutable_borrowed = False

    def release_immutable(self) -> None:
        """释放不可变借用"""
        if self._immutable_borrows > 0:
            self._immutable_borrows -= 1

    def can_borrow_mut(self) -> bool:
        """检查是否可以获取可变借用"""
        return not self._mutable_borrowed and self._immutable_borrows == 0

    def can_borrow_immutable(self) -> bool:
        """检查是否可以获取不可变借用"""
        return not self._mutable_borrowed


class SafeContainer:
    """安全容器，实现借用规则"""

    def __init__(self, value: any):
        self._value = value
        self._borrow_checker = BorrowChecker()

    def get_mut(self) -> Optional['MutableRef']:
        """获取可变引用"""
        if self._borrow_checker.borrow_mut():
            return MutableRef(self, self._value)
        return None

    def get_ref(self) -> Optional['ImmutableRef']:
        """获取不可变引用"""
        if self._borrow_checker.borrow_immutable():
            return ImmutableRef(self, self._value)
        return None

    def _release_mut(self) -> None:
        """内部方法：释放可变借用"""
        self._borrow_checker.release_mut()

    def _release_immutable(self) -> None:
        """内部方法：释放不可变借用"""
        self._borrow_checker.release_immutable()


class MutableRef:
    """可变引用包装器"""

    def __init__(self, container: SafeContainer, value: any):
        self._container = container
        self._value = value

    def set_value(self, new_value: any) -> None:
        """设置新值"""
        self._value = new_value

    def get_value(self) -> any:
        """获取值"""
        return self._value

    def __del__(self):
        """析构时释放借用"""
        self._container._release_mut()


class ImmutableRef:
    """不可变引用包装器"""

    def __init__(self, container: SafeContainer, value: any):
        self._container = container
        self._value = value

    def get_value(self) -> any:
        """获取值"""
        return self._value

    def __del__(self):
        """析构时释放借用"""
        self._container._release_immutable()


def demonstrate_borrowing_rules():
    """演示借用规则"""
    print("🔄 借用规则演示")

    container = SafeContainer("初始值")
    print(f"容器初始值: {container._value}")

    # 测试不可变借用
    ref1 = container.get_ref()
    ref2 = container.get_ref()
    if ref1 and ref2:
        print(f"✅ 多个不可变引用: {ref1.get_value()}, {ref2.get_value()}")

    # 尝试获取可变引用（应该失败）
    mut_ref = container.get_mut()
    if mut_ref is None:
        print("❌ 无法获取可变引用（存在不可变引用）")

    # 释放不可变引用
    del ref1, ref2

    # 现在可以获取可变引用
    mut_ref = container.get_mut()
    if mut_ref:
        mut_ref.set_value("修改后的值")
        print(f"✅ 可变引用修改值: {mut_ref.get_value()}")

    # 尝试同时获取不可变和可变引用
    another_ref = container.get_ref()
    if another_ref is None:
        print("❌ 无法获取不可变引用（存在可变引用）")


def main():
    """主函数"""
    print("🎯 Rust借用系统模拟 - Solution 2: 借用和引用规则")
    print("=" * 60)

    demonstrate_borrowing_rules()

    print("\n💡 关键要点:")
    print("• Rust借用规则：要么一个可变引用，要么多个不可变引用")
    print("• 不能同时存在可变和不可变引用")
    print("• 借用检查在编译时进行，保证内存安全")
    print("• Python通过运行时检查模拟这些规则")
    print("• 引用的生命周期必须小于等于被引用对象的生命周期")


if __name__ == "__main__":
    main()