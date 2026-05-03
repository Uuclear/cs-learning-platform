#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Go并发模式模拟 - 解决方案1：Goroutine模拟

本解决方案演示如何使用Python的threading模块来模拟Go的goroutine。
Goroutine是Go语言中的轻量级线程，可以并发执行函数。
"""

import threading
import time
import random


def worker(name, duration):
    """模拟工作函数，类似于Go中的goroutine函数"""
    print(f"🔄 Goroutine {name} 开始工作 (预计耗时 {duration}秒)")
    time.sleep(duration)
    print(f"✅ Goroutine {name} 完成工作")


def simulate_goroutines():
    """模拟多个goroutine并发执行"""
    print("🚀 启动多个goroutine模拟...")

    # 创建多个线程来模拟goroutines
    threads = []
    durations = [2, 3, 1, 4]  # 不同的工作持续时间

    for i, duration in enumerate(durations):
        thread = threading.Thread(
            target=worker,
            args=(f"Worker-{i+1}", duration)
        )
        threads.append(thread)
        thread.start()  # 立即启动，模拟goroutine的非阻塞特性

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("🏁 所有goroutine模拟完成！")


def main():
    """主函数"""
    print("🎯 Go并发模式模拟 - Solution 1: Goroutine")
    print("=" * 50)

    simulate_goroutines()

    print("\n💡 关键要点:")
    print("• Python的threading.Thread类似于Go的goroutine")
    print("• start()方法立即返回，不阻塞主线程")
    print("• join()方法等待线程完成，类似于Go中的sync.WaitGroup")
    print("• 注意：Python的GIL限制了真正的并行，但并发仍然有效")


if __name__ == "__main__":
    main()