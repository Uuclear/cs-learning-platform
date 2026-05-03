#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案：HMR 实现

这是 example-03-hmr-simulation.py 的完整解决方案，
包含了更真实的文件监听和模块热替换逻辑。
"""

import os
import time
import threading
import hashlib
from typing import Dict, Callable, Set, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class HMRModule:
    """HMR 模块信息"""
    file_path: str
    content_hash: str
    content: str
    accept_handlers: list
    is_accepted: bool = False


class AdvancedHMRServer:
    """高级 HMR 服务器实现"""

    def __init__(self, watch_directory: str = "."):
        self.watch_directory = Path(watch_directory)
        self.modules: Dict[str, HMRModule] = {}
        self.file_watcher: Optional[threading.Thread] = None
        self.is_watching = False
        self.file_hashes: Dict[str, str] = {}
        self.callbacks: Dict[str, Set[Callable]] = {}

    def accept(self, module_id: str, callback: Callable = None):
        """接受模块热更新"""
        if module_id not in self.modules:
            self.modules[module_id] = HMRModule(
                file_path=module_id,
                content_hash="",
                content="",
                accept_handlers=[]
            )

        self.modules[module_id].is_accepted = True
        if callback:
            self.modules[module_id].accept_handlers.append(callback)

    def register_callback(self, event_type: str, callback: Callable):
        """注册全局回调"""
        if event_type not in self.callbacks:
            self.callbacks[event_type] = set()
        self.callbacks[event_type].add(callback)

    def _get_file_hash(self, file_path: str) -> str:
        """获取文件哈希值"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except FileNotFoundError:
            return ""

    def _check_file_changes(self):
        """检查文件变化"""
        while self.is_watching:
            time.sleep(0.5)  # 检查间隔

            for module_id, module in self.modules.items():
                if not os.path.exists(module.file_path):
                    continue

                current_hash = self._get_file_hash(module.file_path)
                if current_hash != module.content_hash:
                    # 文件已更改
                    self._handle_module_update(module_id, current_hash)

    def _handle_module_update(self, module_id: str, new_hash: str):
        """处理模块更新"""
        try:
            with open(self.modules[module_id].file_path, 'r', encoding='utf-8') as f:
                new_content = f.read()

            old_module = self.modules[module_id]
            self.modules[module_id] = HMRModule(
                file_path=module_id,
                content_hash=new_hash,
                content=new_content,
                accept_handlers=old_module.accept_handlers.copy(),
                is_accepted=old_module.is_accepted
            )

            print(f"🔄 HMR: 检测到 {module_id} 更新")

            # 执行接受的回调
            if old_module.is_accepted:
                for handler in old_module.accept_handlers:
                    try:
                        handler(new_content)
                        print(f"✅ HMR: 回调执行成功")
                    except Exception as e:
                        print(f"❌ HMR: 回调执行失败 - {e}")
            else:
                print("⚠ HMR: 模块未被接受，将进行完整重载")

            # 触发全局更新事件
            if 'update' in self.callbacks:
                for callback in self.callbacks['update']:
                    callback(module_id)

        except Exception as e:
            print(f"❌ HMR: 更新失败 - {e}")

    def start_watching(self):
        """开始监听文件变化"""
        if self.is_watching:
            return

        self.is_watching = True
        self.file_watcher = threading.Thread(target=self._check_file_changes, daemon=True)
        self.file_watcher.start()
        print("👀 HMR: 开始监听文件变化")

    def stop_watching(self):
        """停止监听"""
        self.is_watching = False
        if self.file_watcher:
            self.file_watcher.join(timeout=1.0)
        print("⏹ HMR: 停止监听")


def create_temp_module_file(content: str, filename: str = "temp_module.js") -> str:
    """创建临时模块文件用于测试"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename


def solution_main():
    """解决方案主函数"""
    print("=== 高级 HMR 解决方案演示 ===\n")

    # 创建临时模块文件
    initial_content = '''
export const counter = {
    value: 0,
    increment() {
        this.value++;
        return this.value;
    }
};

export function greet(name) {
    return `Hello, ${name}! (v1)`;
}
'''
    module_file = create_temp_module_file(initial_content, "counter.js")

    # 初始化 HMR 服务器
    hmr = AdvancedHMRServer()

    # 应用状态（应该在 HMR 中保留）
    app_state = {'counter_value': 5, 'user': '开发者'}

    def on_counter_update(new_content):
        """计数器模块更新回调"""
        print("🔄 正在热更新计数器模块...")
        # 在真实应用中，这里会重新初始化模块但保留状态
        print(f"✅ 状态保留: counter_value = {app_state['counter_value']}")

    # 接受模块更新
    hmr.accept(module_file, on_counter_update)

    # 开始监听
    hmr.start_watching()

    print(f"初始状态: {app_state}")
    print("等待 2 秒后模拟文件更新...")

    # 模拟文件更新
    time.sleep(2)
    updated_content = initial_content.replace("(v1)", "(v2 - HOT UPDATED!)")
    with open(module_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    # 等待 HMR 处理
    time.sleep(1)

    print(f"\n最终状态: {app_state}")
    print("✅ HMR 成功保留了应用状态！")

    # 清理
    hmr.stop_watching()
    os.remove(module_file)


if __name__ == "__main__":
    solution_main()