#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 进程树查看

递归遍历并显示进程树结构，展示进程间的父子关系。
"""

import os
import psutil

def print_process_tree(pid=None, indent=0):
    """
    递归打印进程树

    参数:
        pid: 要开始打印的进程PID，None表示当前进程
        indent: 缩进级别，用于显示树状结构
    """
    if pid is None:
        pid = os.getpid()  # 默认使用当前进程PID

    try:
        # 获取进程对象
        process = psutil.Process(pid)
        name = process.name()
        status = process.status()

        # 打印当前进程信息（带缩进）
        prefix = "  " * indent
        print(f"{prefix}PID {pid}: {name} [{status}]")

        # 获取所有子进程并递归打印
        children = process.children()
        for child in children:
            print_process_tree(child.pid, indent + 1)

    except psutil.NoSuchProcess:
        # 处理进程已经终止的情况
        print(f"{'  ' * indent}PID {pid}: 已终止")

def show_system_processes():
    """显示系统中的部分进程信息"""
    print("=== 系统进程树示例 ===")

    # 尝试显示根进程（PID 1）的信息
    try:
        init_process = psutil.Process(1)
        print(f"根进程 (PID 1): {init_process.name()}")
        # 获取直接子进程（不递归）
        children = init_process.children(recursive=False)
        print(f"直接子进程数量: {len(children)}")

        # 显示前5个子进程作为示例
        for i, child in enumerate(children[:5]):
            try:
                print(f"  ├── PID {child.pid}: {child.name()}")
            except psutil.NoSuchProcess:
                continue

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        # 在某些系统上可能无法访问PID 1的信息
        print("无法访问根进程信息（需要管理员权限）")

    print("\n=== 当前进程树 ===")
    print_process_tree()

if __name__ == "__main__":
    show_system_processes()