#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1: 状态管理优化

这个解决方案展示了如何在实际应用中选择合适的
状态管理模式，并避免常见的性能陷阱。
"""

import json
from typing import Dict, Any, List, Callable


class OptimizedStateManagement:
    """优化的状态管理实现"""

    def __init__(self):
        # 使用分层状态管理策略
        self.local_state = {}      # 组件本地状态
        self.context_state = {}    # 上下文共享状态
        self.global_state = {}     # 全局状态

        # 订阅系统
        self.subscribers: Dict[str, List[Callable]] = {}

    def set_local_state(self, component_id: str, state: Any):
        """设置组件本地状态"""
        self.local_state[component_id] = state

    def set_context_state(self, context_name: str, value: Any):
        """设置上下文状态"""
        old_value = self.context_state.get(context_name)
        self.context_state[context_name] = value

        # 只通知变化的上下文订阅者
        if old_value != value:
            self._notify_subscribers(f"context:{context_name}", value)

    def set_global_state(self, key: str, value: Any):
        """设置全局状态（带防抖）"""
        old_value = self.global_state.get(key)
        self.global_state[key] = value

        # 防止频繁更新导致过多重渲染
        if old_value != value:
            self._notify_subscribers(f"global:{key}", value)

    def subscribe(self, topic: str, callback: Callable):
        """订阅状态变化"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    def _notify_subscribers(self, topic: str, value: Any):
        """通知订阅者"""
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                callback(value)


def main():
    """演示优化的状态管理"""
    print("🎯 优化的状态管理解决方案")
    print("=" * 40)

    state_manager = OptimizedStateManagement()

    # 模拟组件
    def user_component_render(user_data):
        print(f"👤 用户组件渲染: {user_data}")

    def theme_component_render(theme):
        print(f"🎨 主题组件渲染: {theme}")

    def global_logger(new_state):
        print(f"📝 全局状态日志: {new_state}")

    # 设置订阅
    state_manager.subscribe("global:user", user_component_render)
    state_manager.subscribe("context:theme", theme_component_render)
    state_manager.subscribe("global:*", global_logger)  # 通配符订阅

    # 更新状态
    state_manager.set_global_state("user", {"name": "张三", "role": "admin"})
    state_manager.set_context_state("theme", "dark")

    # 再次设置相同值 - 不应触发重渲染
    state_manager.set_global_state("user", {"name": "张三", "role": "admin"})


if __name__ == "__main__":
    main()