#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: 线程安全的计数器

实现一个线程安全的计数器类，支持递增、递减和获取当前值操作。
"""

import threading

class ThreadSafeCounter:
    """线程安全的计数器类"""

    def __init__(self, initial_value=0):
        """初始化计数器

        Args:
            initial_value: 初始值，默认为0
        """
        self._value = initial_value
        self._lock = threading.Lock()

    def increment(self):
        """递增计数器"""
        with self._lock:
            self._value += 1

    def decrement(self):
        """递减计数器"""
        with self._lock:
            self._value -= 1

    def get_value(self):
        """获取当前值

        Returns:
            当前计数器的值
        """
        with self._lock:
            return self._value

    def set_value(self, value):
        """设置计数器的值

        Args:
            value: 要设置的新值
        """
        with self._lock:
            self._value = value

# 测试代码
if __name__ == "__main__":
    import threading
    import time

    # 创建计数器实例
    counter = ThreadSafeCounter(0)

    def worker_increment():
        """工作线程 - 递增操作"""
        for _ in range(10000):
            counter.increment()

    def worker_decrement():
        """工作线程 - 递减操作"""
        for _ in range(5000):
            counter.decrement()

    # 创建并启动线程
    threads = []

    # 2个递增线程
    for i in range(2):
        thread = threading.Thread(target=worker_increment)
        threads.append(thread)
        thread.start()

    # 1个递减线程
    thread = threading.Thread(target=worker_decrement)
    threads.append(thread)
    thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 验证结果
    expected = 2 * 10000 - 5000  # 15000
    actual = counter.get_value()

    print(f"期望值: {expected}")
    print(f"实际值: {actual}")
    print(f"结果正确: {expected == actual}")