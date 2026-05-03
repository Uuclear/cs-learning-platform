#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Go并发模式示例 - 示例2：Channel通信

本示例演示Go channel的基本用法和通信模式。
"""

import threading
import queue
import time


def ping_pong_example():
    """Ping-Pong通信示例"""
    print("🏓 Ping-Pong Channel示例")

    # 创建两个channel
    ping_channel = queue.Queue()
    pong_channel = queue.Queue()

    def ping():
        """Ping协程"""
        for i in range(3):
            msg = ping_channel.get()  # 接收ping
            print(f"   接收到: {msg}")
            time.sleep(0.3)
            pong_channel.put(f"Pong-{i+1}")  # 发送pong

    def pong():
        """Pong协程"""
        for i in range(3):
            ping_channel.put(f"Ping-{i+1}")  # 发送ping
            msg = pong_channel.get()  # 接收pong
            print(f"   接收到: {msg}")
            time.sleep(0.3)

    # 启动两个线程
    ping_thread = threading.Thread(target=ping)
    pong_thread = threading.Thread(target=pong)

    ping_thread.start()
    pong_thread.start()

    ping_thread.join()
    pong_thread.join()

    print("✅ Ping-Pong完成！")


def worker_pool_example():
    """工作池示例"""
    print("\n🏭 工作池Channel示例")

    # 创建任务channel和结果channel
    task_channel = queue.Queue()
    result_channel = queue.Queue()

    def worker(worker_id):
        """工作协程"""
        while True:
            try:
                task = task_channel.get(timeout=2)
                if task == "STOP":
                    break
                print(f"   Worker-{worker_id} 处理任务: {task}")
                time.sleep(0.5)  # 模拟工作
                result_channel.put(f"Result-{task}")
                task_channel.task_done()
            except queue.Empty:
                break

    # 启动3个工作线程
    workers = []
    for i in range(3):
        worker_thread = threading.Thread(target=worker, args=(i+1,))
        worker_thread.start()
        workers.append(worker_thread)

    # 发送任务
    tasks = ["Task-A", "Task-B", "Task-C", "Task-D", "Task-E"]
    for task in tasks:
        task_channel.put(task)

    # 等待所有任务完成
    task_channel.join()

    # 停止工作线程
    for _ in workers:
        task_channel.put("STOP")

    # 收集结果
    results = []
    while len(results) < len(tasks):
        try:
            result = result_channel.get(timeout=1)
            results.append(result)
        except queue.Empty:
            break

    print(f"✅ 收到 {len(results)} 个结果: {results}")

    # 等待工作线程结束
    for worker_thread in workers:
        worker_thread.join()


def main():
    """主函数"""
    print("🎯 Channel通信示例")
    print("=" * 30)

    ping_pong_example()
    worker_pool_example()

    print("\n📚 学习要点:")
    print("• Channel用于goroutine之间的通信")
    print("• 可以实现生产者-消费者模式")
    print("• Channel提供同步机制")
    print("• 可以构建复杂的工作流")


if __name__ == "__main__":
    main()