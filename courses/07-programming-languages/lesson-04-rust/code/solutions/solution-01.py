#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rust所有权系统模拟 - 解决方案1：所有权和移动语义

本解决方案演示如何在Python中模拟Rust的所有权和移动语义概念。
通过引用计数和显式所有权转移来模拟Rust的内存安全保证。
"""

import weakref
from typing import Optional, Any


class OwnedValue:
    """模拟Rust所有权的值包装器"""

    def __init__(self, value: Any):
        self._value = value
        self._owner = True  # 标记是否拥有所有权
        self._reference_count = 1

    def take_ownership(self) -> 'OwnedValue':
        """转移所有权（模拟Rust的move语义）"""
        if not self._owner:
            raise RuntimeError("Cannot take ownership: value has already been moved")

        # 创建新的所有权实例，原实例失去所有权
        new_owner = OwnedValue(self._value)
        self._owner = False
        self._value = None
        return new_owner

    def get_value(self) -> Any:
        """获取值（只能在拥有所有权时）"""
        if not self._owner:
            raise RuntimeError("Cannot access value: ownership has been moved")
        return self._value

    def is_valid(self) -> bool:
        """检查是否仍然有效（拥有所有权）"""
        return self._owner

    def __str__(self) -> str:
        if self._owner:
            return f"OwnedValue({self._value})"
        else:
            return "OwnedValue(MOVED)"


class ReferenceCounter:
    """引用计数器，用于跟踪值的使用情况"""

    def __init__(self, value: Any):
        self._value = value
        self._strong_refs = 1
        self._weak_refs = []

    def add_strong_ref(self) -> 'ReferenceCounter':
        """增加强引用计数"""
        self._strong_refs += 1
        return self

    def add_weak_ref(self) -> weakref.ref:
        """创建弱引用"""
        ref = weakref.ref(self)
        self._weak_refs.append(ref)
        return ref

    def release_strong_ref(self) -> None:
        """释放强引用"""
        self._strong_refs -= 1
        if self._strong_refs == 0:
            self._cleanup()

    def _cleanup(self) -> None:
        """清理资源"""
        print(f"🧹 清理资源: {self._value}")
        self._value = None

    def get_value(self) -> Optional[Any]:
        """获取值（如果还存在）"""
        return self._value if self._strong_refs > 0 else None

    def __str__(self) -> str:
        return f"ReferenceCounter(value={self._value}, strong_refs={self._strong_refs})"


def demonstrate_ownership():
    """演示所有权转移"""
    print("🔄 所有权转移演示")

    # 创建一个拥有所有权的值
    original = OwnedValue("Hello, Rust!")
    print(f"原始值: {original}")

    # 转移所有权
    moved = original.take_ownership()
    print(f"转移后 - 原始: {original}")
    print(f"转移后 - 新所有者: {moved}")

    # 尝试访问已转移的值（会失败）
    try:
        original.get_value()
    except RuntimeError as e:
        print(f"❌ 访问已转移值失败: {e}")

    # 正常访问新所有者的值
    print(f"✅ 新所有者值: {moved.get_value()}")


def demonstrate_reference_counting():
    """演示引用计数"""
    print("\n📊 引用计数演示")

    # 创建引用计数对象
    rc = ReferenceCounter("Shared Data")
    print(f"初始状态: {rc}")

    # 创建强引用
    strong_ref1 = rc.add_strong_ref()
    strong_ref2 = rc.add_strong_ref()
    print(f"添加两个强引用: {rc}")

    # 创建弱引用
    weak_ref = rc.add_weak_ref()
    print(f"添加弱引用: {rc}")

    # 释放一个强引用
    rc.release_strong_ref()
    print(f"释放一个强引用: {rc}")

    # 检查弱引用
    if weak_ref() is not None:
        print(f"弱引用仍然有效: {weak_ref().get_value()}")

    # 释放剩余的强引用
    rc.release_strong_ref()
    rc.release_strong_ref()
    print("所有强引用已释放")


def main():
    """主函数"""
    print("🎯 Rust所有权系统模拟 - Solution 1: 所有权和移动语义")
    print("=" * 60)

    demonstrate_ownership()
    demonstrate_reference_counting()

    print("\n💡 关键要点:")
    print("• Rust的所有权确保每个值只有一个所有者")
    print("• 移动语义防止了浅拷贝导致的双重释放问题")
    print("• 引用计数允许多个所有者共享数据（Arc/Rc）")
    print("• 弱引用避免循环引用导致的内存泄漏")
    print("• Python通过手动管理模拟这些概念，但Rust在编译时保证安全")


if __name__ == "__main__":
    main()