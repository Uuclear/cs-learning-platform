#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1: React 状态管理模式模拟

这个文件演示了不同的 React 状态管理模式：
1. useState - 简单的状态管理
2. Context API - 跨组件状态共享
3. 全局状态库 (类似 Zustand/Redux) - 集中式状态管理
"""

import json
from typing import Dict, Any, Callable, List


class Component:
    """模拟 React 组件基类"""
    def __init__(self, name: str):
        self.name = name
        self.render_count = 0

    def render(self):
        """模拟组件渲染"""
        self.render_count += 1
        print(f"🔄 {self.name} 组件渲染第 {self.render_count} 次")


# ========== 1. useState 模式 ==========
class UseStateExample:
    """模拟 useState 钩子"""

    def __init__(self, initial_value: Any):
        self.state = initial_value
        self.listeners: List[Callable] = []

    def set_state(self, new_value: Any):
        """更新状态并通知监听器"""
        self.state = new_value
        for listener in self.listeners:
            listener()

    def subscribe(self, callback: Callable):
        """订阅状态变化"""
        self.listeners.append(callback)


# ========== 2. Context API 模式 ==========
class ReactContext:
    """模拟 React Context API"""

    def __init__(self, default_value: Any):
        self.value = default_value
        self.consumers: List[Component] = []

    def provide(self, new_value: Any):
        """提供新的上下文值"""
        self.value = new_value
        # 通知所有消费者重新渲染
        for consumer in self.consumers:
            consumer.render()

    def consume(self, component: Component):
        """消费上下文的组件"""
        self.consumers.append(component)
        return self.value


# ========== 3. 全局状态库模式 ==========
class GlobalStore:
    """模拟全局状态管理库 (如 Zustand/Redux)"""

    def __init__(self, initial_state: Dict[str, Any]):
        self.state = initial_state.copy()
        self.subscribers: Dict[str, List[Callable]] = {}
        self.all_subscribers: List[Callable] = []

    def get_state(self, key: str = None):
        """获取状态"""
        if key is None:
            return self.state
        return self.state.get(key)

    def set_state(self, updates: Dict[str, Any], specific_key: str = None):
        """更新状态"""
        old_state = self.state.copy()

        if specific_key:
            # 只更新特定键
            self.state[specific_key] = updates
            changed_keys = [specific_key]
        else:
            # 批量更新
            self.state.update(updates)
            changed_keys = list(updates.keys())

        # 通知特定键的订阅者
        for key in changed_keys:
            if key in self.subscribers:
                for subscriber in self.subscribers[key]:
                    subscriber(self.state[key])

        # 通知所有订阅者
        for subscriber in self.all_subscribers:
            subscriber(self.state, old_state)

    def subscribe(self, callback: Callable, key: str = None):
        """订阅状态变化"""
        if key:
            if key not in self.subscribers:
                self.subscribers[key] = []
            self.subscribers[key].append(callback)
        else:
            self.all_subscribers.append(callback)


def main():
    """主函数：演示三种状态管理模式"""
    print("🎯 React 状态管理模式演示")
    print("=" * 50)

    # 1. useState 示例
    print("\n1️⃣ useState 模式:")
    counter = UseStateExample(0)
    button_component = Component("计数器按钮")

    def on_counter_change():
        button_component.render()

    counter.subscribe(on_counter_change)
    counter.set_state(1)
    counter.set_state(2)

    # 2. Context API 示例
    print("\n2️⃣ Context API 模式:")
    theme_context = ReactContext("light")
    header = Component("头部")
    sidebar = Component("侧边栏")

    theme_context.consume(header)
    theme_context.consume(sidebar)
    theme_context.provide("dark")

    # 3. 全局状态库示例
    print("\n3️⃣ 全局状态库模式:")
    store = GlobalStore({
        "user": {"name": "张三", "role": "user"},
        "theme": "light",
        "notifications": []
    })

    user_display = Component("用户信息显示")
    theme_switcher = Component("主题切换器")

    def on_user_change(new_user):
        user_display.render()

    def on_theme_change(new_theme):
        theme_switcher.render()

    def on_any_change(new_state, old_state):
        print(f"   📦 全局状态变更: {json.dumps(new_state, ensure_ascii=False)}")

    store.subscribe(on_user_change, "user")
    store.subscribe(on_theme_change, "theme")
    store.subscribe(on_any_change)

    store.set_state({"name": "李四", "role": "admin"}, "user")
    store.set_state("dark", "theme")


if __name__ == "__main__":
    main()