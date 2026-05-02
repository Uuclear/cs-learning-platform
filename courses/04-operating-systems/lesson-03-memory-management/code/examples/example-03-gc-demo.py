#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: Python垃圾回收机制演示
展示Python的引用计数和循环垃圾回收机制。
"""

import gc
import weakref
from typing import Optional, List


class SimpleObject:
    """简单对象，用于演示引用计数"""
    def __init__(self, name: str):
        self.name = name
        print(f"✅ 创建对象: {self.name}")

    def __del__(self):
        print(f"🗑️  销毁对象: {self.name}")


class Node:
    """链表节点，用于演示循环引用"""
    def __init__(self, value: int):
        self.value = value
        self.next: Optional['Node'] = None
        self.prev: Optional['Node'] = None
        print(f"✅ 创建节点: {value}")

    def __del__(self):
        print(f"🗑️  销毁节点: {self.value}")


def demonstrate_reference_counting():
    """演示引用计数"""
    print("🔧 引用计数演示:")
    print("-" * 30)

    # 创建对象
    obj1 = SimpleObject("obj1")
    print(f"   obj1引用计数: {gc.get_referrers(obj1)}")

    # 增加引用
    obj2 = obj1
    print("   创建obj2 = obj1 (增加引用)")

    # 删除一个引用
    del obj1
    print("   删除obj1引用")
    print("   对象仍然存在，因为obj2还在引用它")

    # 删除最后一个引用
    del obj2
    print("   删除obj2引用")
    print("   对象被立即销毁（引用计数为0）")
    print()


def demonstrate_cyclic_references():
    """演示循环引用问题"""
    print("🔧 循环引用演示:")
    print("-" * 30)

    # 创建循环引用
    node1 = Node(1)
    node2 = Node(2)
    node1.next = node2
    node2.prev = node1

    print("   创建了两个相互引用的节点")
    print(f"   node1引用计数: {len(gc.get_referrers(node1))}")
    print(f"   node2引用计数: {len(gc.get_referrers(node2))}")

    # 删除外部引用
    print("   删除外部引用...")
    del node1, node2

    # 检查是否还有对象存活
    collected = gc.collect()
    print(f"   垃圾回收器清理了 {collected} 个对象")

    # 显示当前垃圾回收统计
    stats = gc.get_stats()
    print(f"   GC统计: {stats[0]['collected']} 个对象在第0代被收集")
    print()


def demonstrate_weak_references():
    """演示弱引用解决循环引用"""
    print("🔧 弱引用解决方案:")
    print("-" * 30)

    class Parent:
        def __init__(self, name: str):
            self.name = name
            self.children: List['Child'] = []
            print(f"✅ 创建父对象: {name}")

        def __del__(self):
            print(f"🗑️  销毁父对象: {self.name}")

    class Child:
        def __init__(self, name: str, parent: Parent):
            self.name = name
            # 使用弱引用来避免循环引用
            self.parent = weakref.ref(parent)
            parent.children.append(self)
            print(f"✅ 创建子对象: {name}")

        def __del__(self):
            print(f"🗑️  销毁子对象: {self.name}")

        def get_parent_name(self) -> str:
            parent = self.parent()
            return parent.name if parent else "无父对象"

    # 创建父子关系
    parent = Parent("parent1")
    child1 = Child("child1", parent)
    child2 = Child("child2", parent)

    print(f"   {child1.get_parent_name()} 的子对象: {child1.name}, {child2.name}")

    # 删除所有引用
    print("   删除所有引用...")
    del parent, child1, child2

    # 强制垃圾回收
    collected = gc.collect()
    print(f"   垃圾回收器清理了 {collected} 个对象")
    print()


def main():
    """主函数"""
    print("🚀 Python垃圾回收机制演示")
    print("=" * 50)

    # 启用详细垃圾回收输出
    gc.set_debug(gc.DEBUG_STATS)

    demonstrate_reference_counting()
    demonstrate_cyclic_references()
    demonstrate_weak_references()

    print("\n💡 总结:")
    print("  • Python使用引用计数作为主要GC机制")
    print("  • 循环引用需要专门的循环垃圾回收器处理")
    print("  • 弱引用可以避免不必要的循环引用")
    print("  • 手动调用gc.collect()可以强制垃圾回收")


if __name__ == "__main__":
    main()