#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2: React 渲染优化模拟

这个文件演示了 React 的渲染优化技术：
1. React.memo - 防止不必要的重新渲染
2. useMemo - 缓存昂贵的计算结果
3. useCallback - 缓存函数引用
"""

import time
from typing import List, Callable, Any
from functools import wraps


def expensive_calculation(n: int) -> int:
    """模拟昂贵的计算操作"""
    time.sleep(0.1)  # 模拟耗时操作
    return sum(i * i for i in range(n))


class Component:
    """模拟 React 组件"""
    def __init__(self, name: str):
        self.name = name
        self.render_count = 0

    def render(self, props: dict = None):
        """模拟组件渲染"""
        self.render_count += 1
        props_str = f" {props}" if props else ""
        print(f"🔄 {self.name} 组件渲染第 {self.render_count} 次{props_str}")


# ========== React.memo 模拟 ==========
def react_memo(component_class):
    """模拟 React.memo 高阶组件"""
    class MemoizedComponent:
        def __init__(self, *args, **kwargs):
            self.component = component_class(*args, **kwargs)
            self.last_props = None

        def render(self, props: dict):
            # 只有当 props 发生变化时才重新渲染
            if props != self.last_props:
                self.component.render(props)
                self.last_props = props.copy()
            else:
                print(f"⏭️  {self.component.name} 组件跳过渲染 (props 未变)")

    return MemoizedComponent


# ========== useMemo 模拟 ==========
class UseMemoCache:
    """模拟 useMemo 钩子"""
    def __init__(self):
        self.cache = {}

    def memo(self, calculation_func: Callable, dependencies: tuple):
        """缓存计算结果"""
        cache_key = str(dependencies)
        if cache_key not in self.cache:
            print(f"   💡 执行新的计算: {calculation_func.__name__}")
            self.cache[cache_key] = calculation_func()
        else:
            print(f"   📦 使用缓存结果: {calculation_func.__name__}")
        return self.cache[cache_key]

    def clear_cache(self):
        """清除缓存"""
        self.cache.clear()


# ========== useCallback 模拟 ==========
def use_callback(func: Callable, dependencies: tuple):
    """模拟 useCallback 钩子"""
    # 在实际 React 中，这会返回相同的函数引用如果依赖没有变化
    # 这里我们简单地返回原函数，但记录依赖信息
    func._dependencies = dependencies
    return func


@react_memo
class UserList(Component):
    """用户列表组件 - 使用 React.memo 优化"""
    def __init__(self):
        super().__init__("用户列表")


@react_memo
class UserProfile(Component):
    """用户个人资料组件 - 使用 React.memo 优化"""
    def __init__(self):
        super().__init__("用户资料")


def main():
    """主函数：演示渲染优化技术"""
    print("🎯 React 渲染优化演示")
    print("=" * 50)

    # ========== 1. React.memo 演示 ==========
    print("\n1️⃣ React.memo - 防止不必要的重新渲染:")

    user_list = UserList()
    user_profile = UserProfile()

    # 第一次渲染
    user_list.render({"users": ["张三", "李四"], "filter": "all"})
    user_profile.render({"user": "张三", "theme": "light"})

    # 相同的 props - 应该跳过渲染
    print("   → 使用相同的 props 再次渲染:")
    user_list.render({"users": ["张三", "李四"], "filter": "all"})
    user_profile.render({"user": "张三", "theme": "light"})

    # 不同的 props - 应该重新渲染
    print("   → 使用不同的 props 渲染:")
    user_list.render({"users": ["张三", "李四", "王五"], "filter": "active"})
    user_profile.render({"user": "李四", "theme": "dark"})

    # ========== 2. useMemo 演示 ==========
    print("\n2️⃣ useMemo - 缓存昂贵的计算:")

    memo_cache = UseMemoCache()

    def calculate_squares():
        return expensive_calculation(100)

    def calculate_cubes():
        return expensive_calculation(50)

    # 第一次计算
    result1 = memo_cache.memo(calculate_squares, (100,))
    print(f"   结果: {result1}")

    # 相同依赖 - 使用缓存
    result2 = memo_cache.memo(calculate_squares, (100,))
    print(f"   结果: {result2}")

    # 不同依赖 - 新的计算
    result3 = memo_cache.memo(calculate_cubes, (50,))
    print(f"   结果: {result3}")

    # ========== 3. useCallback 演示 ==========
    print("\n3️⃣ useCallback - 缓存函数引用:")

    def handle_click(user_id: str):
        print(f"   🔘 点击用户: {user_id}")

    def handle_save(data: dict):
        print(f"   💾 保存数据: {data}")

    # 创建缓存的回调函数
    click_handler = use_callback(handle_click, ("user-list",))
    save_handler = use_callback(handle_save, ("profile-form",))

    print(f"   点击处理器依赖: {click_handler._dependencies}")
    print(f"   保存处理器依赖: {save_handler._dependencies}")

    # 调用回调函数
    click_handler("user-123")
    save_handler({"name": "张三", "email": "zhang@example.com"})


if __name__ == "__main__":
    main()