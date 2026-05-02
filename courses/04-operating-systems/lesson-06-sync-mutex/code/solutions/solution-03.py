#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答: 读者-写者问题（读者优先）

实现读者-写者问题的解决方案，允许多个读者同时读取，
但写者必须独占访问。采用读者优先策略。
"""

import threading
import time
import random

class ReaderWriterLock:
    """读者-写者锁（读者优先）"""

    def __init__(self):
        """初始化读者-写者锁"""
        self._readers_count = 0          # 当前读者数量
        self._readers_lock = threading.Lock()   # 保护读者计数器的锁
        self._writers_lock = threading.Lock()   # 写者独占锁

    def reader_acquire(self):
        """读者获取锁"""
        with self._readers_lock:
            self._readers_count += 1
            # 第一个读者需要获取写者锁
            if self._readers_count == 1:
                self._writers_lock.acquire()

    def reader_release(self):
        """读者释放锁"""
        with self._readers_lock:
            self._readers_count -= 1
            # 最后一个读者释放写者锁
            if self._readers_count == 0:
                self._writers_lock.release()

    def writer_acquire(self):
        """写者获取锁"""
        self._writers_lock.acquire()

    def writer_release(self):
        """写者释放锁"""
        self._writers_lock.release()

class SharedResource:
    """共享资源类"""

    def __init__(self):
        """初始化共享资源"""
        self._data = "初始数据"
        self._lock = ReaderWriterLock()

    def read_data(self, reader_id):
        """读取数据

        Args:
            reader_id: 读者ID
        """
        self._lock.reader_acquire()
        try:
            # 模拟读取操作
            print(f"📖 读者 {reader_id} 正在读取: {self._data}")
            time.sleep(random.uniform(0.1, 0.3))  # 模拟读取时间
            return self._data
        finally:
            self._lock.reader_release()

    def write_data(self, writer_id, new_data):
        """写入数据

        Args:
            writer_id: 写者ID
            new_data: 新数据
        """
        self._lock.writer_acquire()
        try:
            print(f"✍️  写者 {writer_id} 正在写入: {new_data}")
            self._data = new_data
            time.sleep(random.uniform(0.2, 0.4))  # 模拟写入时间
        finally:
            self._lock.writer_release()

def reader_task(resource, reader_id):
    """读者任务函数

    Args:
        resource: 共享资源
        reader_id: 读者ID
    """
    for i in range(5):  # 每个读者读取5次
        data = resource.read_data(reader_id)
        print(f"✅ 读者 {reader_id} 完成第{i+1}次读取")
        time.sleep(random.uniform(0.1, 0.2))

def writer_task(resource, writer_id):
    """写者任务函数

    Args:
        resource: 共享资源
        writer_id: 写者ID
    """
    for i in range(3):  # 每个写者写入3次
        new_data = f"数据-{writer_id}-{i}"
        resource.write_data(writer_id, new_data)
        print(f"✅ 写者 {writer_id} 完成第{i+1}次写入")
        time.sleep(random.uniform(0.3, 0.5))

def main():
    """主函数 - 测试读者-写者锁"""
    resource = SharedResource()

    # 创建读者和写者线程
    threads = []

    # 创建3个读者线程
    for i in range(3):
        thread = threading.Thread(
            target=reader_task,
            args=(resource, i+1),
            name=f"Reader-{i+1}"
        )
        threads.append(thread)

    # 创建2个写者线程
    for i in range(2):
        thread = threading.Thread(
            target=writer_task,
            args=(resource, i+1),
            name=f"Writer-{i+1}"
        )
        threads.append(thread)

    # 启动所有线程
    print("启动读者和写者线程...")
    for thread in threads:
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("\n✅ 所有读者和写者任务完成！")

if __name__ == "__main__":
    main()