#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rust概念示例 - 示例1：所有权基础

本示例演示Rust所有权系统的基本概念。
"""

class SimpleOwner:
    """简单所有者类"""

    def __init__(self, value):
        self.value = value
        self.owned = True

    def transfer_ownership(self):
        """转移所有权"""
        if not self.owned:
            raise ValueError("Already transferred!")
        new_owner = SimpleOwner(self.value)
        self.owned = False
        self.value = None
        return new_owner

    def __str__(self):
        if self.owned:
            return f"Owner({self.value})"
        else:
            return "Owner(TRANSFERRED)"


def main():
    """主函数"""
    print("🎯 Rust所有权基础示例")
    print("=" * 30)

    # 创建所有者
    owner1 = SimpleOwner("Hello")
    print(f"初始所有者: {owner1}")

    # 转移所有权
    owner2 = owner1.transfer_ownership()
    print(f"转移后 - 所有者1: {owner1}")
    print(f"转移后 - 所有者2: {owner2}")

    # 尝试再次转移（会失败）
    try:
        owner1.transfer_ownership()
    except ValueError as e:
        print(f"❌ 转移失败: {e}")

    print("\n📚 学习要点:")
    print("• 每个值都有唯一的所有者")
    print("• 所有权可以转移（move）")
    print("• 原所有者失去访问权限")
    print("• 防止双重释放和悬垂指针")


if __name__ == "__main__":
    main()