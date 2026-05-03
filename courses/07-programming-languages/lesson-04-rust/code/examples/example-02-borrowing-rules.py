#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rust概念示例 - 示例2：借用规则

本示例演示Rust借用系统的基本规则。
"""

class BorrowRulesDemo:
    """借用规则演示类"""

    def __init__(self):
        self.data = "原始数据"
        self.mutable_borrowed = False
        self.immutable_borrows = 0

    def borrow_mut(self):
        """获取可变借用"""
        if self.mutable_borrowed or self.immutable_borrows > 0:
            return None
        self.mutable_borrowed = True
        return MutableBorrow(self)

    def borrow_immutable(self):
        """获取不可变借用"""
        if self.mutable_borrowed:
            return None
        self.immutable_borrows += 1
        return ImmutableBorrow(self)

    def _release_mut(self):
        self.mutable_borrowed = False

    def _release_immutable(self):
        self.immutable_borrows -= 1


class MutableBorrow:
    def __init__(self, owner):
        self.owner = owner

    def modify(self, new_data):
        self.owner.data = new_data

    def __del__(self):
        self.owner._release_mut()


class ImmutableBorrow:
    def __init__(self, owner):
        self.owner = owner

    def read(self):
        return self.owner.data

    def __del__(self):
        self.owner._release_immutable()


def main():
    demo = BorrowRulesDemo()

    # 测试不可变借用
    ref1 = demo.borrow_immutable()
    ref2 = demo.borrow_immutable()
    print(f"✅ 多个不可变引用: {ref1.read()}, {ref2.read()}")

    # 测试可变借用（应该失败）
    mut_ref = demo.borrow_mut()
    if mut_ref is None:
        print("❌ 无法获取可变引用（存在不可变引用）")

    del ref1, ref2

    # 现在可以获取可变引用
    mut_ref = demo.borrow_mut()
    if mut_ref:
        mut_ref.modify("修改后的数据")
        print(f"✅ 可变引用修改: {mut_ref.owner.data}")

    print("\n📚 学习要点:")
    print("• 要么一个可变引用，要么多个不可变引用")
    print("• 借用检查防止数据竞争")
    print("• 引用生命周期管理")


if __name__ == "__main__":
    main()