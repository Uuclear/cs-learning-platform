#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: 线程数据共享

演示线程间的数据共享以及如何使用锁来避免竞态条件。
"""

import threading
import time

# 共享数据
shared_counter = 0
lock = threading.Lock()  # 用于同步的锁

def increment_worker(worker_id):
    """递增共享计数器的线程函数"""
    global shared_counter
    for _ in range(100000):
        # 使用锁保护临界区
        with lock:
            shared_counter += 1
        # 偶尔释放CPU，增加竞争机会
        if _ % 10000 == 0:
            time.sleep(0.001)

if __name__ == "__main__":
    print(f"初始计数器值: {shared_counter}")

    # 创建两个线程同时递增计数器
    thread1 = threading.Thread(target=increment_worker, args=(1,))
    thread2 = threading.Thread(target=increment_worker, args=(2,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(f"最终计数器值: {shared_counter}")
    print(f"期望值: {200000}")
    print(f"是否正确: {'是' if shared_counter == 200000 else '否'}")