#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 生产者-消费者问题

这是一个经典的同步问题，展示了如何使用线程安全的队列
来协调生产者和消费者线程。

生产者生成数据项并放入缓冲区，消费者从缓冲区取出数据项。
Python的Queue类内部已经实现了必要的同步机制。
"""

import threading
import time
import random
from queue import Queue

# 配置参数
buffer = Queue(maxsize=5)  # 有界缓冲区，最多5个元素
producer_count = 3          # 生产者线程数量
consumer_count = 2          # 消费者线程数量
items_to_produce = 20       # 总共要生产的物品数量

def producer(producer_id):
    """生产者线程函数

    生产者生成物品并放入缓冲区。
    如果缓冲区已满，put()方法会自动阻塞直到有空间。
    """
    items_produced = 0
    max_items_per_producer = items_to_produce // producer_count

    for i in range(max_items_per_producer):
        item = f"物品-{producer_id}-{i}"
        buffer.put(item)  # 阻塞直到缓冲区有空间
        print(f"✅ 生产者 {producer_id} 生产了 {item}")
        items_produced += 1

        # 模拟生产时间的随机性
        time.sleep(random.uniform(0.1, 0.3))

    print(f"🏭 生产者 {producer_id} 完成了生产任务 ({items_produced} 个物品)")

def consumer(consumer_id):
    """消费者线程函数

    消费者从缓冲区取出物品进行消费。
    如果缓冲区为空，get()方法会自动阻塞直到有物品。
    """
    items_consumed = 0

    while True:
        try:
            # timeout=2秒，如果2秒内没有物品就认为生产已完成
            item = buffer.get(timeout=2)
            print(f"🛒 消费者 {consumer_id} 消费了 {item}")
            buffer.task_done()  # 标记任务完成
            items_consumed += 1

            # 模拟消费时间的随机性
            time.sleep(random.uniform(0.2, 0.5))

        except:
            # 超时异常，假设生产已完成
            break

    print(f"🍽️  消费者 {consumer_id} 完成了消费任务 ({items_consumed} 个物品)")

def main():
    """主函数 - 启动生产者和消费者线程"""
    print("=" * 60)
    print("生产者-消费者问题演示")
    print("=" * 60)
    print(f"缓冲区大小: {buffer.maxsize}")
    print(f"生产者数量: {producer_count}")
    print(f"消费者数量: {consumer_count}")
    print(f"总生产量: {items_to_produce}")
    print("-" * 60)

    # 创建并启动生产者线程
    producer_threads = []
    for i in range(producer_count):
        thread = threading.Thread(
            target=producer,
            args=(i+1,),
            name=f"Producer-{i+1}"
        )
        producer_threads.append(thread)
        thread.start()

    # 创建并启动消费者线程
    consumer_threads = []
    for i in range(consumer_count):
        thread = threading.Thread(
            target=consumer,
            args=(i+1,),
            name=f"Consumer-{i+1}"
        )
        consumer_threads.append(thread)
        thread.start()

    # 等待所有生产者完成
    for thread in producer_threads:
        thread.join()

    print("\n🔄 所有生产者已完成，等待消费者清空缓冲区...")

    # 等待缓冲区中所有任务完成
    buffer.join()

    print("\n🎉 所有生产和消费任务完成！")

if __name__ == "__main__":
    main()