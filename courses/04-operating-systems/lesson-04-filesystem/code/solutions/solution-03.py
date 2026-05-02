#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答: 简单的文件系统监控
监控指定目录的变化（文件创建、修改、删除）
注意：这个解决方案使用简单的轮询方法，不依赖第三方库
"""

import os
import time
import sys
from datetime import datetime

class SimpleFileSystemMonitor:
    """简单的文件系统监控器（基于轮询）"""

    def __init__(self, directory_path):
        """
        初始化监控器

        Args:
            directory_path (str): 要监控的目录路径
        """
        self.directory_path = os.path.abspath(directory_path)
        self.file_states = {}  # 文件路径 -> 修改时间的映射
        self.running = False

        if not os.path.exists(self.directory_path):
            raise FileNotFoundError(f"目录不存在: {self.directory_path}")

        if not os.path.isdir(self.directory_path):
            raise NotADirectoryError(f"路径不是目录: {self.directory_path}")

        print(f"🔍 初始化监控器: {self.directory_path}")

    def scan_directory(self):
        """
        扫描目录并返回当前文件状态

        Returns:
            dict: 文件路径 -> 修改时间的映射
        """
        current_states = {}

        try:
            for root, dirs, files in os.walk(self.directory_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    try:
                        mtime = os.path.getmtime(file_path)
                        current_states[file_path] = mtime
                    except (OSError, PermissionError):
                        # 跳过无法访问的文件
                        continue
        except PermissionError:
            print(f"⚠️  权限不足，无法扫描目录: {self.directory_path}")

        return current_states

    def detect_changes(self, current_states):
        """
        检测文件系统变化

        Args:
            current_states (dict): 当前文件状态

        Returns:
            list: 变化事件列表
        """
        events = []

        # 检查新文件和修改的文件
        for file_path, current_mtime in current_states.items():
            if file_path not in self.file_states:
                # 新文件
                events.append({
                    'type': 'created',
                    'path': file_path,
                    'time': datetime.now()
                })
            elif self.file_states[file_path] != current_mtime:
                # 修改的文件
                events.append({
                    'type': 'modified',
                    'path': file_path,
                    'time': datetime.now()
                })

        # 检查删除的文件
        for file_path in self.file_states:
            if file_path not in current_states:
                events.append({
                    'type': 'deleted',
                    'path': file_path,
                    'time': datetime.now()
                })

        return events

    def handle_events(self, events):
        """
        处理检测到的事件

        Args:
            events (list): 事件列表
        """
        event_emojis = {
            'created': '🆕',
            'modified': '✏️',
            'deleted': '🗑️'
        }

        for event in events:
            emoji = event_emojis.get(event['type'], '❓')
            relative_path = os.path.relpath(event['path'], self.directory_path)
            timestamp = event['time'].strftime('%H:%M:%S')
            print(f"{emoji} [{timestamp}] {event['type'].upper()}: {relative_path}")

    def start_monitoring(self, interval=1.0):
        """
        开始监控

        Args:
            interval (float): 扫描间隔（秒）
        """
        print(f"🚀 开始监控目录: {self.directory_path}")
        print(f"⏱️  扫描间隔: {interval} 秒")
        print("按 Ctrl+C 停止监控\n")

        # 初始化文件状态
        self.file_states = self.scan_directory()
        print(f"✅ 初始扫描完成，发现 {len(self.file_states)} 个文件")
        print("-" * 60)

        self.running = True
        try:
            while self.running:
                current_states = self.scan_directory()
                events = self.detect_changes(current_states)

                if events:
                    self.handle_events(events)

                self.file_states = current_states
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n🛑 监控已停止")
            self.running = False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python solution-3.py <目录路径> [扫描间隔]")
        print("示例: python solution-3.py /tmp/mydir")
        print("      python solution-3.py /tmp/mydir 2.0")
        return

    directory_path = sys.argv[1]
    interval = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0

    try:
        monitor = SimpleFileSystemMonitor(directory_path)
        monitor.start_monitoring(interval)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()