#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 线程池

演示如何使用线程池来高效管理多个工作线程，避免频繁创建和销毁线程的开销。
"""

import threading
from concurrent.futures import ThreadPoolExecutor
import time
import random

def task(task_id):
    """模拟任务执行"""
    sleep_time = random.uniform(0.5, 2.0)
    print(f"任务 {task_id} 开始执行，预计耗时 {sleep_time:.2f} 秒")
    time.sleep(sleep_time)
    result = task_id * 2
    print(f"任务 {task_id} 执行完成，结果: {result}")
    return result

if __name__ == "__main__":
    # 创建线程池，最多4个工作线程
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 提交10个任务
        futures = [executor.submit(task, i) for i in range(10)]

        # 获取所有任务的结果
        results = [future.result() for future in futures]

    print(f"所有任务完成，结果: {results}")