#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rust概念示例 - 示例3：生命周期管理

本示例演示Rust生命周期的基本概念。
"""

class LifetimeDemo:
    """生命周期演示类"""

    def __init__(self, name):
        self.name = name
        self.alive = True
        print(f"🆕 创建: {self.name}")

    def __del__(self):
        if self.alive:
            print(f"🧹 销毁: {self.name}")
            self.alive = False

    def is_valid(self):
        return self.alive


def create_reference(obj, scope):
    """创建引用"""
    print(f"🔗 在 {scope} 中引用 {obj.name}")
    return obj


def main():
    print("🎯 Rust生命周期示例")
    print("=" * 30)

    # 创建对象
    data = LifetimeDemo("数据")

    # 在函数中使用引用
    ref = create_reference(data, "main")
    print(f"✅ 引用有效: {ref.name}")

    # 对象仍然存活
    print(f"状态: {'存活' if data.is_valid() else '已销毁'}")

    print("\n📚 学习要点:")
    print("• 生命周期确保引用不会超出数据生存期")
    print("• RAII自动管理资源")
    print("• 编译时检查防止悬垂指针")


if __name__ == "__main__":
    main()