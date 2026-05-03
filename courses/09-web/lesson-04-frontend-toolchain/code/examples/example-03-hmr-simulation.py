#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟 Hot Module Replacement (HMR) - 热模块替换

这个脚本演示了现代前端开发工具（如 Webpack、Vite）中的 HMR 功能：
1. 监听文件变化
2. 只更新修改的模块，而不刷新整个页面
3. 保持应用状态

HMR 大大提高了开发体验，避免了完整的页面重载。
"""

import time
import threading
from typing import Dict, Callable, Any
from dataclasses import dataclass


@dataclass
class Module:
    """模块数据结构"""
    name: str
    content: str
    last_modified: float
    accept_callbacks: list = None

    def __post_init__(self):
        if self.accept_callbacks is None:
            self.accept_callbacks = []


class HMRServer:
    """HMR 服务器模拟器"""

    def __init__(self):
        self.modules: Dict[str, Module] = {}
        self.is_watching = False
        self.watch_thread = None

    def add_module(self, name: str, content: str):
        """添加模块到 HMR 系统"""
        self.modules[name] = Module(
            name=name,
            content=content,
            last_modified=time.time()
        )
        print(f"✓ 模块已加载: {name}")

    def accept(self, module_name: str, callback: Callable[[Any], None]):
        """注册模块接受回调（当模块更新时调用）"""
        if module_name in self.modules:
            self.modules[module_name].accept_callbacks.append(callback)
            print(f"✓ 注册 HMR 回调: {module_name}")

    def update_module(self, module_name: str, new_content: str):
        """更新模块内容（模拟文件变化）"""
        if module_name not in self.modules:
            print(f"⚠ 模块不存在: {module_name}")
            return

        old_module = self.modules[module_name]
        self.modules[module_name] = Module(
            name=module_name,
            content=new_content,
            last_modified=time.time(),
            accept_callbacks=old_module.accept_callbacks.copy()
        )

        print(f"\n🔄 检测到模块更新: {module_name}")
        print("执行 HMR 更新（不刷新页面）...")

        # 执行所有注册的回调
        for callback in self.modules[module_name].accept_callbacks:
            try:
                callback(new_content)
                print(f"✓ HMR 回调执行成功: {callback.__name__}")
            except Exception as e:
                print(f"✗ HMR 回调执行失败: {e}")

        print("✅ HMR 更新完成！应用状态已保留\n")

    def simulate_file_change(self, module_name: str, delay: float = 2.0):
        """模拟文件变化（用于演示）"""
        def change_file():
            time.sleep(delay)
            if module_name in self.modules:
                old_content = self.modules[module_name].content
                # 创建修改后的内容
                new_content = old_content.replace("原始", "更新后").replace("original", "updated")
                if old_content == new_content:
                    new_content += "\n// 这是新增的内容"
                self.update_module(module_name, new_content)

        threading.Thread(target=change_file, daemon=True).start()

    def start_watching(self):
        """开始监听文件变化（简化版）"""
        if self.is_watching:
            return

        self.is_watching = True
        print("👀 开始监听文件变化...")

    def stop_watching(self):
        """停止监听"""
        self.is_watching = False
        print("⏹ 停止监听文件变化")


def main():
    """主函数：演示 HMR 工作流程"""
    print("=== Hot Module Replacement (HMR) 模拟演示 ===\n")

    # 创建 HMR 服务器
    hmr_server = HMRServer()

    # 模拟初始应用状态
    app_state = {
        'user': '开发者',
        'count': 42,
        'theme': 'dark'
    }

    print(f"应用查看状态: {app_state}")
    print("当前计数器值:", app_state['count'])

    # 添加初始模块
    initial_component = '''
// 用户组件 - 原始版本
export function UserProfile({ user, count }) {
    return `<div class="profile">
        <h2>欢迎, ${user}!</h2>
        <p>当前计数: ${count}</p>
        <p>状态: 正常运行</p>
    </div>`;
}
'''

    hmr_server.add_module('UserProfile.js', initial_component)

    # 定义 HMR 接受回调
    def on_user_profile_update(new_content):
        """当 UserProfile 组件更新时的回调"""
        print("🔄 正在更新用户界面...")
        # 在真实应用中，这里会重新渲染组件
        # 但应用状态（如计数器）会被保留

        # 模拟状态保留
        nonlocal app_state
        app_state['count'] += 1  # 实际上状态应该不变，这里只是为了显示效果
        print(f"✅ 界面已更新，状态保留: 计数器 = {app_state['count']}")

    # 注册 HMR 回调
    hmr_server.accept('UserProfile.js', on_user_profile_update)

    # 开始监听
    hmr_server.start_watching()

    print("\n⏳ 等待 3 秒钟模拟开发过程...")
    print("开发者正在编辑 UserProfile.js 文件...\n")

    # 模拟文件变化
    hmr_server.simulate_file_change('UserProfile.js', delay=3.0)

    # 等待 HMR 完成
    time.sleep(5)

    print(f"\n最终应用查看状态: {app_state}")
    print("注意：应用状态被保留，只有 UI 组件被更新！")
    print("\n=== HMR 演示完成 ===")
    print("在真实开发中，这避免了完整的页面刷新，大大提升了开发体验")


if __name__ == "__main__":
    main()