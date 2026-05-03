#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Go并发模式示例 - 示例1：Goroutine基础

本示例演示Go goroutine的基本概念和使用方法。
"""

import threading
import time


def simple_task(name):
    """简单的任务函数"""
    for i in range(3):
        print(f"🧵 {name} 执行第 {i+1} 次")
        time.sleep(0.5)


def main():
    """主函数"""
    print("🎯 Goroutine基础示例")
    print("=" * 30)

    # 创建并启动多个线程（模拟goroutines）
    threads = []
    for i in range(3):
        thread = threading.Thread(
            target=simple_task,
            args=(f"Goroutine-{i+1}",)
        )
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("\n✅ 所有goroutine完成！")

    print("\n📚 学习要点:")
    print("• goroutine是Go的轻量级并发单元")
    print("• 使用 go 关键字启动goroutine")
    print("• 多个goroutine可以并发执行")
    print("• 需要适当的同步机制来协调")


if __name__ == "__main__":
    main()