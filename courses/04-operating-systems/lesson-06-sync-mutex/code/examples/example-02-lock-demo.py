#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: 锁的使用

这个例子展示了如何使用互斥锁来解决竞态条件问题。
通过在临界区前后加锁和解锁，确保同一时间只有一个线程
能够修改共享变量。

运行结果会显示实际值等于期望值，证明了同步机制的有效性。
"""

import threading
import time

# 共享变量和互斥锁
counter = 0
counter_lock = threading.Lock()  # 创建互斥锁
num_threads = 10
increments_per_thread = 100000

def safe_increment_counter():
    """安全的递增函数 - 使用锁保护

    使用 with 语句自动管理锁的获取和释放，
    即使在临界区内发生异常，锁也会被正确释放。
    """
    global counter
    for _ in range(increments_per_thread):
        # 获取锁 - 进入临界区
        # with 语句确保锁在退出时自动释放
        with counter_lock:
            counter = counter + 1
        # 自动释放锁 - 离开临界区

def main():
    """主函数 - 创建并运行多个线程"""
    global counter

    # 重置计数器
    counter = 0

    # 创建并启动线程
    threads = []
    start_time = time.time()

    for i in range(num_threads):
        thread = threading.Thread(target=safe_increment_counter, name=f"Thread-{i+1}")
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    end_time = time.time()
    expected_value = num_threads * increments_per_thread

    print("=" * 50)
    print("使用互斥锁的结果")
    print("=" * 50)
    print(f"线程数量: {num_threads}")
    print(f"每个线程递增次数: {increments_per_thread:,}")
    print(f"期望值: {expected_value:,}")
    print(f"实际值: {counter:,}")
    print(f"差异: {expected_value - counter:,}")
    print(f"正确率: {counter/expected_value*100:.2f}%")
    print(f"执行时间: {end_time - start_time:.2f}秒")
    print("=" * 50)
    print("✅ 结果完全正确！但注意执行时间比无锁版本长。")

if __name__ == "__main__":
    main()