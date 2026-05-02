#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: 简单的多线程计数器

创建3个线程，每个线程将共享计数器递增1000次，使用锁确保结果正确。
"""

import threading

# 共享计数器
counter = 0
lock = threading.Lock()

def increment_counter():
    """递增计数器1000次"""
    global counter
    for _ in range(1000):
        with lock:
            counter += 1

if __name__ == "__main__":
    # 创建3个线程
    threads = []
    for i in range(3):
        thread = threading.Thread(target=increment_counter)
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print(f"最终计数器值: {counter}")
    print(f"期望值: 3000")
    print(f"结果正确: {counter == 3000}")