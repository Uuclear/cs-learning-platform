#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 线程创建

演示如何在Python中创建和启动线程，展示多线程的并发执行特性。
"""

import threading
import time

def worker(name):
    """工作线程函数"""
    print(f"线程 {name} 开始工作")
    for i in range(3):
        print(f"线程 {name} 正在处理第 {i+1} 项任务")
        time.sleep(1)  # 模拟耗时操作
    print(f"线程 {name} 工作完成")

if __name__ == "__main__":
    # 创建两个线程
    thread1 = threading.Thread(target=worker, args=("Worker-1",))
    thread2 = threading.Thread(target=worker, args=("Worker-2",))

    # 启动线程
    thread1.start()
    thread2.start()

    # 等待线程完成
    thread1.join()
    thread2.join()

    print("所有线程工作完成！")