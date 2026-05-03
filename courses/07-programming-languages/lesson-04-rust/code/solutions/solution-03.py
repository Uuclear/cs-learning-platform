#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rust生命周期模拟 - 解决方案3：生命周期和资源管理

本解决方案演示如何在Python中模拟Rust的生命周期概念和资源管理。
"""

import weakref
from typing import Optional, Any, Callable


class LifetimeTracker:
    """生命周期跟踪器"""

    def __init__(self, name: str):
        self.name = name
        self.alive = True
        print(f"🆕 创建对象: {self.name}")

    def __del__(self):
        if self.alive:
            print(f"🧹 销毁对象: {self.name}")
            self.alive = False

    def is_alive(self) -> bool:
        return self.alive


class ScopedReference:
    """作用域引用，模拟Rust生命周期"""

    def __init__(self, obj: LifetimeTracker, scope_name: str):
        self.obj = obj
        self.scope_name = scope_name
        self.valid = True
        print(f"🔗 在作用域 '{scope_name}' 中创建引用到 {obj.name}")

    def get_value(self) -> Optional[LifetimeTracker]:
        """获取引用的对象（如果仍然有效）"""
        if not self.obj.is_alive():
            print(f"❌ 引用失效！对象 {self.obj.name} 已被销毁")
            self.valid = False
            return None
        return self.obj

    def is_valid(self) -> bool:
        return self.valid and self.obj.is_alive()


class ResourceManager:
    """资源管理器，确保资源在正确的时间被清理"""

    def __init__(self):
        self.resources = []
        self.cleanup_callbacks = []

    def add_resource(self, resource: Any, cleanup_func: Callable):
        """添加需要管理的资源"""
        self.resources.append(resource)
        self.cleanup_callbacks.append(cleanup_func)

    def cleanup(self):
        """清理所有资源"""
        print("🔄 清理所有资源...")
        for callback in reversed(self.cleanup_callbacks):
            callback()
        self.resources.clear()
        self.cleanup_callbacks.clear()


def demonstrate_lifetime_scoping():
    """演示生命周期作用域"""
    print("🔄 生命周期作用域演示")

    # 创建资源管理器
    rm = ResourceManager()

    # 创建对象
    data = LifetimeTracker("数据对象")
    rm.add_resource(data, lambda: setattr(data, 'alive', False))

    # 在内部作用域中创建引用
    def inner_scope():
        ref = ScopedReference(data, "inner_scope")
        value = ref.get_value()
        if value:
            print(f"✅ 在内部作用域中访问: {value.name}")
        return ref

    # 获取引用
    reference = inner_scope()

    # 尝试在外部作用域使用引用
    value = reference.get_value()
    if value:
        print(f"✅ 在外部作用域中访问: {value.name}")

    # 清理资源
    rm.cleanup()

    # 尝试访问已清理的资源
    value = reference.get_value()
    if value is None:
        print("❌ 无法访问已清理的资源")


def demonstrate_function_lifetime():
    """演示函数参数生命周期"""
    print("\n🔄 函数参数生命周期演示")

    def process_data(data_ref: ScopedReference) -> str:
        """处理数据引用"""
        data = data_ref.get_value()
        if data:
            return f"处理 {data.name}"
        return "无效引用"

    # 创建数据
    data = LifetimeTracker("函数参数数据")

    # 创建引用并传递给函数
    ref = ScopedReference(data, "function_call")
    result = process_data(ref)
    print(f"函数结果: {result}")

    # 数据仍然有效
    print(f"数据状态: {'存活' if data.is_alive() else '已销毁'}")


def main():
    """主函数"""
    print("🎯 Rust生命周期模拟 - Solution 3: 生命周期和资源管理")
    print("=" * 60)

    demonstrate_lifetime_scoping()
    demonstrate_function_lifetime()

    print("\n💡 关键要点:")
    print("• Rust生命周期确保引用不会超出其指向数据的生存期")
    print("• 作用域决定变量的生命周期")
    print("• 资源管理通过RAII（Resource Acquisition Is Initialization）实现")
    print("• Python通过手动跟踪模拟生命周期概念")
    print("• 弱引用可以避免循环引用问题")


if __name__ == "__main__":
    main()