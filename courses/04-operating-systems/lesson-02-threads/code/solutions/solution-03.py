#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答: 线程池计算

使用线程池计算大列表中所有数字的平方和，比较单线程和多线程性能。
"""

import threading
from concurrent.futures import ThreadPoolExecutor
import time
import random

def calculate_square_sum(numbers):
    """计算数字列表的平方和"""
    return sum(x * x for x in numbers)

def single_threaded_calculation(numbers):
    """单线程计算"""
    start_time = time.perf_counter()
    result = calculate_square_sum(numbers)
    end_time = time.perf_counter()
    return result, end_time - start_time

def multi_threaded_calculation(numbers, num_threads=4):
    """多线程计算"""
    # 将列表分成num_threads个部分
    chunk_size = len(numbers) // num_threads
    chunks = []
    for i in range(num_threads):
        if i == num_threads - 1:
            # 最后一个chunk包含剩余的所有元素
            chunk = numbers[i * chunk_size:]
        else:
            chunk = numbers[i * chunk_size:(i + 1) * chunk_size]
        chunks.append(chunk)

    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(calculate_square_sum, chunk) for chunk in chunks]
        partial_results = [future.result() for future in futures]

    total_result = sum(partial_results)
    end_time = time.perf_counter()
    return total_result, end_time - start_time

if __name__ == "__main__":
    # 创建包含100万个随机整数的列表
    print("生成100万个随机整数...")
    numbers = [random.randint(1, 1000) for _ in range(1000000)]

    print("开始单线程计算...")
    single_result, single_time = single_threaded_calculation(numbers)
    print(f"单线程结果: {single_result}")
    print(f"单线程耗时: {single_time:.4f} 秒")

    print("\n开始多线程计算...")
    multi_result, multi_time = multi_threaded_calculation(numbers, num_threads=4)
    print(f"多线程结果: {multi_result}")
    print(f"多线程耗时: {multi_time:.4f} 秒")

    print(f"\n结果一致: {single_result == multi_result}")
    print(f"性能提升: {single_time / multi_time:.2f}x" if multi_time > 0 else "无法计算性能提升")

    print("\n注意：由于Python的GIL限制，CPU密集型任务的多线程性能可能不如预期。")
    print("对于真正的并行计算，建议使用multiprocessing模块或C扩展。")