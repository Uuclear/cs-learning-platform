#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Go并发模式示例 - 示例3：Select语句

本示例演示Go select语句的使用场景和模式。
"""

import threading
import queue
import time
import random


def timeout_pattern():
    """超时模式示例"""
    print("⏰ 超时模式示例")

    response_channel = queue.Queue()

    def slow_service():
        """模拟慢速服务"""
        time.sleep(random.uniform(1.0, 4.0))
        response_channel.put("服务响应")

    # 启动服务
    service_thread = threading.Thread(target=slow_service)
    service_thread.start()

    # 使用select-like逻辑处理超时
    start_time = time.time()
    timeout = 2.5

    while True:
        elapsed = time.time() - start_time

        if elapsed >= timeout:
            print("   ❌ 请求超时！")
            break

        try:
            response = response_channel.get_nowait()
            print(f"   ✅ 收到响应: {response} (耗时: {elapsed:.1f}秒)")
            break
        except queue.Empty:
            print(f"   ⏳ 等待中... ({elapsed:.1f}秒)")
            time.sleep(0.3)

    service_thread.join()


def fan_in_pattern():
    """Fan-in模式示例（多个输入，一个输出）"""
    print("\n🔀 Fan-in模式示例")

    input_channels = [queue.Queue() for _ in range(3)]
    output_channel = queue.Queue()

    def input_generator(channel_id, channel):
        """输入生成器"""
        for i in range(3):
            msg = f"Input-{channel_id}-{i}"
            time.sleep(random.uniform(0.2, 0.8))
            channel.put(msg)

    def fan_in_merger():
        """Fan-in合并器"""
        received = 0
        total_expected = 9  # 3 channels × 3 messages each

        while received < total_expected:
            for i, channel in enumerate(input_channels):
                try:
                    msg = channel.get_nowait()
                    output_channel.put(f"Merged: {msg}")
                    received += 1
                except queue.Empty:
                    continue
            time.sleep(0.1)

    # 启动输入生成器
    generators = []
    for i, channel in enumerate(input_channels):
        gen_thread = threading.Thread(
            target=input_generator,
            args=(i+1, channel)
        )
        gen_thread.start()
        generators.append(gen_thread)

    # 启动合并器
    merger_thread = threading.Thread(target=fan_in_merger)
    merger_thread.start()

    # 收集输出
    outputs = []
    while len(outputs) < 9:
        try:
            output = output_channel.get(timeout=3)
            outputs.append(output)
            print(f"   📥 {output}")
        except queue.Empty:
            break

    # 等待所有线程完成
    for gen_thread in generators:
        gen_thread.join()
    merger_thread.join()

    print(f"✅ Fan-in完成，收到 {len(outputs)} 条消息")


def main():
    """主函数"""
    print("🎯 Select语句示例")
    print("=" * 30)

    timeout_pattern()
    fan_in_pattern()

    print("\n📚 学习要点:")
    print("• Select允许在多个channel操作中选择")
    print("• 可以实现超时控制")
    print("• 支持复杂的通信模式如Fan-in/Fan-out")
    print("• 提供非阻塞的channel操作")


if __name__ == "__main__":
    main()