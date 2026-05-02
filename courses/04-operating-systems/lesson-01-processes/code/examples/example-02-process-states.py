#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: 进程状态监控

使用psutil库监控进程状态的变化，展示进程在不同活动下的状态转换。
"""

import os
import time
import psutil

def monitor_process_states():
    """监控当前进程的状态变化"""
    # 获取当前进程的PID
    current_pid = os.getpid()
    print(f"当前进程PID: {current_pid}")

    # 创建psutil.Process对象来访问进程信息
    process = psutil.Process(current_pid)

    # 显示进程的初始状态信息
    print(f"初始状态: {process.status()}")
    print(f"CPU使用率: {process.cpu_percent()}%")
    print(f"内存使用: {process.memory_info().rss / 1024 / 1024:.2f} MB")

    # 模拟CPU密集型工作（运行状态）
    print("\n正在进行计算工作...")
    start_time = time.time()
    # 执行空循环2秒来模拟CPU使用
    while time.time() - start_time < 2:
        pass  # 空操作，占用CPU

    # 检查工作后的状态
    print(f"工作后状态: {process.status()}")

    # 模拟I/O等待（阻塞状态）
    print("\n模拟I/O等待（睡眠2秒）...")
    time.sleep(2)  # 进程会进入睡眠/阻塞状态
    print(f"睡眠后状态: {process.status()}")

if __name__ == "__main__":
    monitor_process_states()