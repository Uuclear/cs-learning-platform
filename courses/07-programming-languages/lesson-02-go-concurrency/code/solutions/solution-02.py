#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Go并发模式模拟 - 解决方案2：Channel模拟

本解决方案演示如何使用Python的queue.Queue来模拟Go的channel。
Channel是Go中用于goroutine之间通信的管道，提供同步和数据传递功能。
"""

import threading
import queue
import time
import random


def producer(channel, name, count):
    """生产者函数，向channel发送数据"""
    print(f"📤 生产者 {name} 开始生产...")
    for i in range(count):
        item = f"{name}-item-{i}"
        channel.put(item)  # 发送数据到channel
        print(f"   生产了: {item}")
        time.sleep(random.uniform(0.1, 0.5))
    print(f"✅ 生产者 {name} 完成生产")


def consumer(channel, name):
    """消费者函数，从channel接收数据"""
    print(f"📥 消费者 {name} 开始消费...")
    while True:
        try:
            # 从channel接收数据，设置超时避免无限阻塞
            item = channel.get(timeout=2)
            print(f"   消费了: {item}")
            channel.task_done()  # 标记任务完成
            time.sleep(random.uniform(0.2, 0.6))
        except queue.Empty:
            # 超时，假设生产已完成
            break
    print(f"✅ 消费者 {name} 完成消费")


def simulate_channels():
    """模拟Go的channel通信模式"""
    print("📡 创建channel并启动生产者/消费者...")

    # 创建一个队列来模拟Go的channel
    channel = queue.Queue()

    # 启动生产者和消费者线程
    producer_thread = threading.Thread(
        target=producer,
        args=(channel, "Producer-A", 5)
    )

    consumer_thread = threading.Thread(
        target=consumer,
        args=(channel, "Consumer-B")
    )

    # 启动线程
    producer_thread.start()
    consumer_thread.start()

    # 等待生产者完成
    producer_thread.join()

    # 等待所有消息被处理完毕
    channel.join()

    # 等待消费者完成（会因为超时而退出）
    consumer_thread.join()

    print("🏁 Channel通信模拟完成！")


def main():
    """主函数"""
    print("🎯 Go并发模式模拟 - Solution 2: Channel")
    print("=" * 50)

    simulate_channels()

    print("\n💡 关键要点:")
    print("• Python的queue.Queue可以模拟Go的channel")
    print("• put()方法相当于Go的 ch <- data")
    print("• get()方法相当于Go的 data := <-ch")
    print("• task_done()和join()提供了类似Go channel的同步机制")
    print("• 注意处理超时和异常情况")


if __name__ == "__main__":
    main()