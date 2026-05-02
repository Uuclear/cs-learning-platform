#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 生产者-消费者模式

实现经典的生产者-消费者模式，使用线程安全的队列进行通信。
"""

import threading
import queue
import random
import time

def producer(producer_id, q, stop_event):
    """生产者函数"""
    while not stop_event.is_set():
        item = random.randint(1, 100)
        q.put(item)
        print(f"生产者 {producer_id} 生产了物品: {item}")
        time.sleep(random.uniform(0.1, 0.5))  # 模拟生产时间

def consumer(consumer_id, q, stop_event):
    """消费者函数"""
    while not stop_event.is_set() or not q.empty():
        try:
            item = q.get(timeout=0.1)
            print(f"消费者 {consumer_id} 消费了物品: {item}")
            q.task_done()
            time.sleep(random.uniform(0.1, 0.3))  # 模拟消费时间
        except queue.Empty:
            continue

if __name__ == "__main__":
    # 创建线程安全的队列
    q = queue.Queue(maxsize=10)
    stop_event = threading.Event()

    # 创建2个生产者和3个消费者
    threads = []

    # 启动生产者
    for i in range(2):
        t = threading.Thread(target=producer, args=(i+1, q, stop_event))
        threads.append(t)
        t.start()

    # 启动消费者
    for i in range(3):
        t = threading.Thread(target=consumer, args=(i+1, q, stop_event))
        threads.append(t)
        t.start()

    # 运行5秒
    time.sleep(5)

    # 设置停止事件
    stop_event.set()

    # 等待所有线程完成
    for t in threads:
        t.join()

    print("生产者-消费者程序结束")