#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: 进程基本信息获取

获取并显示当前进程的基本信息，包括PID、父进程PID、进程名、启动时间等。
"""

import os
import psutil
import datetime

def get_process_info():
    """获取当前进程的详细信息"""
    # 获取当前进程对象
    current_process = psutil.Process()

    # 获取基本信息
    pid = current_process.pid
    ppid = current_process.ppid()
    name = current_process.name()
    status = current_process.status()

    # 获取启动时间并转换为可读格式
    create_time = datetime.datetime.fromtimestamp(current_process.create_time())

    # 获取内存使用情况
    memory_info = current_process.memory_info()
    memory_mb = memory_info.rss / 1024 / 1024  # 转换为MB

    # 获取CPU使用率（需要调用两次，第一次返回0）
    current_process.cpu_percent()
    time.sleep(0.1)  # 短暂等待
    cpu_percent = current_process.cpu_percent()

    # 打印所有信息
    print("=== 当前进程基本信息 ===")
    print(f"进程ID (PID): {pid}")
    print(f"父进程ID (PPID): {ppid}")
    print(f"进程名称: {name}")
    print(f"进程状态: {status}")
    print(f"启动时间: {create_time}")
    print(f"内存使用: {memory_mb:.2f} MB")
    print(f"CPU使用率: {cpu_percent:.2f}%")

    # 获取工作目录和可执行文件路径
    try:
        cwd = current_process.cwd()
        exe = current_process.exe()
        print(f"工作目录: {cwd}")
        print(f"可执行文件: {exe}")
    except psutil.AccessDenied:
        print("工作目录/可执行文件: 权限不足")

if __name__ == "__main__":
    get_process_info()