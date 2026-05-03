#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Go并发模式模拟 - 解决方案3：Select语句模拟

本解决方案演示如何使用Python的queue和条件变量来模拟Go的select语句。
Select允许goroutine在多个channel操作中选择第一个可用的操作。
"""

import threading
import queue
import time
import random


def send_to_channel(channel, name, messages, delay_range=(0.5, 2.0)):
    """向channel发送消息"""
    for msg in messages:
        time.sleep(random.uniform(*delay_range))
        channel.put(f"{name}: {msg}")
    # 发送完成信号
    channel.put(f"{name}: DONE")


def simulate_select():
    """模拟Go的select语句行为"""
    print("🔄 创建多个channels用于select模拟...")

    # 创建两个channel（队列）
    channel1 = queue.Queue()
    channel2 = queue.Queue()

    # 启动两个生产者线程
    producer1 = threading.Thread(
        target=send_to_channel,
        args=(channel1, "Channel1", ["Hello", "World", "From", "Channel1"])
    )

    producer2 = threading.Thread(
        target=send_to_channel,
        args=(channel2, "Channel2", ["Goodbye", "Universe", "From", "Channel2"])
    )

    producer1.start()
    producer2.start()

    print("📡 开始select-like监听...")

    done_count = 0
    while done_count < 2:
        # 模拟select：检查哪个channel有数据可读
        try:
            # 尝试从channel1读取（非阻塞）
            msg1 = channel1.get_nowait()
            print(f"✅ 从 Channel1 接收到: {msg1}")
            if "DONE" in msg1:
                done_count += 1
            continue  # 立即处理下一个消息
        except queue.Empty:
            pass  # channel1没有数据

        try:
            # 尝试从channel2读取（非阻塞）
            msg2 = channel2.get_nowait()
            print(f"✅ 从 Channel2 接收到: {msg2}")
            if "DONE" in msg2:
                done_count += 1
            continue  # 立即处理下一个消息
        except queue.Empty:
            pass  # channel2没有数据

        # 如果两个channel都没有数据，短暂休眠避免忙等待
        time.sleep(0.1)

    print("🏁 Select模拟完成！")


def advanced_select_simulation():
    """更高级的select模拟，包含超时和默认分支"""
    print("\n🎯 高级Select模拟（包含超时）...")

    work_channel = queue.Queue()
    timeout_duration = 3.0
    start_time = time.time()

    # 启动一个可能延迟的工作线程
    def delayed_worker():
        time.sleep(random.uniform(1.0, 5.0))  # 随机延迟
        work_channel.put("工作完成！")

    worker_thread = threading.Thread(target=delayed_worker)
    worker_thread.start()

    while True:
        elapsed = time.time() - start_time

        # 检查是否超时
        if elapsed >= timeout_duration:
            print("⏰ 超时！工作未在预期时间内完成")
            break

        try:
            # 尝试获取工作结果
            result = work_channel.get_nowait()
            print(f"✅ 工作结果: {result}")
            break
        except queue.Empty:
            # 没有结果，显示进度
            print(f"⏳ 等待中... ({elapsed:.1f}秒)")
            time.sleep(0.5)

    worker_thread.join()


def main():
    """主函数"""
    print("🎯 Go并发模式模拟 - Solution 3: Select Statement")
    print("=" * 50)

    simulate_select()
    advanced_select_simulation()

    print("\n💡 关键要点:")
    print("• Python没有内置的select语句，但可以用非阻塞队列操作模拟")
    print("• get_nowait()相当于尝试读取channel而不阻塞")
    print("• 通过循环检查多个channel来实现select的多路复用")
    print("• 可以添加超时逻辑来模拟select的default分支")
    print("• 注意避免忙等待，适当使用sleep()")


if __name__ == "__main__":
    main()