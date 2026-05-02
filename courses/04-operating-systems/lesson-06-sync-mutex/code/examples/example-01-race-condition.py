#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 竞态条件演示

这个例子展示了当多个线程同时修改共享变量时，
由于缺乏同步机制导致的竞态条件问题。

运行结果会显示实际值远小于期望值，证明了竞态条件的存在。
"""

import threading
import time

# 共享变量 - 所有线程都能访问
counter = 0
num_threads = 10
increments_per_thread = 100000

def increment_counter():
    """危险的递增函数 - 没有同步保护

    这个函数包含竞态条件！
    counter = counter + 1 不是原子操作，
    它实际上包含三个步骤：
    1. 读取 counter 的当前值
    2. 将值加1
    3. 将新值写回 counter

    如果多个线程同时执行这些步骤，就会互相干扰。
    """
    global counter
    for _ in range(increments_per_thread):
        # 这不是原子操作！存在竞态条件
        counter = counter + 1

def main():
    """主函数 - 创建并运行多个线程"""
    global counter

    # 重置计数器
    counter = 0

    # 创建并启动线程
    threads = []
    start_time = time.time()

    for i in range(num_threads):
        thread = threading.Thread(target=increment_counter, name=f"Thread-{i+1}")
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    end_time = time.time()
    expected_value = num_threads * increments_per_thread

    print("=" * 50)
    print("竞态条件演示结果")
    print("=" * 50)
    print(f"线程数量: {num_threads}")
    print(f"每个线程递增次数: {increments_per_thread:,}")
    print(f"期望值: {expected_value:,}")
    print(f"实际值: {counter:,}")
    print(f"差异: {expected_value - counter:,}")
    print(f"正确率: {counter/expected_value*100:.2f}%")
    print(f"执行时间: {end_time - start_time:.2f}秒")
    print("=" * 50)

if __name__ == "__main__":
    main()