#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟 Serverless 冷启动问题 - 冷启动 vs 热启动延迟比较

这个脚本演示了 Serverless 函数的冷启动现象，以及如何通过预热策略来缓解。
"""

import time
import random
from typing import List, Tuple


class LambdaFunctionSimulator:
    """Lambda 函数模拟器，用于演示冷启动和热启动的区别"""

    def __init__(self):
        self.is_warm = False  # 标记函数是否处于热状态
        self.initialization_time = 0.0
        self.execution_time = 0.0

    def cold_start_initialization(self) -> float:
        """
        模拟冷启动时的初始化过程

        Returns:
            初始化所需时间（秒）
        """
        if self.is_warm:
            return 0.0

        # 模拟各种初始化开销：加载依赖、连接数据库、读取配置等
        init_time = random.uniform(0.8, 2.5)  # 冷启动通常需要 0.8-2.5 秒
        time.sleep(init_time)

        self.is_warm = True
        self.initialization_time = init_time
        return init_time

    def warm_execution(self) -> float:
        """
        模拟热启动时的执行过程

        Returns:
            执行所需时间（秒）
        """
        # 热启动执行时间通常很短
        exec_time = random.uniform(0.01, 0.1)
        time.sleep(exec_time)
        self.execution_time = exec_time
        return exec_time

    def invoke_function(self, force_cold_start: bool = False) -> Tuple[float, float, bool]:
        """
        调用函数并返回性能指标

        Args:
            force_cold_start: 是否强制冷启动

        Returns:
            (总时间, 初始化时间, 是否为冷启动)
        """
        if force_cold_start:
            self.is_warm = False

        start_time = time.time()
        init_time = self.cold_start_initialization()
        exec_time = self.warm_execution()
        total_time = time.time() - start_time

        is_cold_start = init_time > 0
        return total_time, init_time, is_cold_start


def simulate_cold_vs_warm_starts():
    """模拟冷启动和热启动的性能差异"""
    print("=== Serverless 冷启动 vs 热启动性能比较 ===\n")

    simulator = LambdaFunctionSimulator()

    # 测试冷启动
    print("1. 冷启动测试（首次调用）:")
    cold_total, cold_init, _ = simulator.invoke_function(force_cold_start=True)
    print(f"   总时间: {cold_total:.3f}秒")
    print(f"   初始化时间: {cold_init:.3f}秒")
    print(f"   执行时间: {cold_total - cold_init:.3f}秒\n")

    # 测试热启动（连续调用）
    print("2. 热启动测试（后续调用）:")
    warm_times = []
    for i in range(5):
        warm_total, warm_init, _ = simulator.invoke_function()
        warm_times.append(warm_total)
        print(f"   调用 {i+1}: {warm_total:.3f}秒 (初始化: {warm_init:.3f}秒)")

    avg_warm_time = sum(warm_times) / len(warm_times)
    print(f"   平均热启动时间: {avg_warm_time:.3f}秒\n")

    # 计算性能差异
    performance_difference = cold_total / avg_warm_time
    print(f"3. 性能对比:")
    print(f"   冷启动比热启动慢 {performance_difference:.1f} 倍")
    print(f"   冷启动额外开销: {cold_init:.3f}秒 ({cold_init/cold_total*100:.1f}%)\n")


def demonstrate_warmup_strategies():
    """演示缓解冷启动的预热策略"""
    print("=== 冷启动缓解策略演示 ===\n")

    # 策略1: 定时预热
    print("1. 定时预热策略:")
    print("   - 每隔一段时间主动调用函数保持热状态")
    print("   - 适用于可预测的流量模式")

    simulator = LambdaFunctionSimulator()
    # 预热调用
    simulator.invoke_function()
    time.sleep(0.1)  # 模拟预热间隔

    # 用户请求（现在是热启动）
    user_request_time, _, is_cold = simulator.invoke_function()
    print(f"   预热后的用户请求时间: {user_request_time:.3f}秒 (冷启动: {is_cold})\n")

    # 策略2: 并发预热
    print("2. 并发预热策略:")
    print("   - 在高流量期间保持多个实例热启动")
    print("   - 适用于突发流量场景")

    instances = [LambdaFunctionSimulator() for _ in range(3)]
    for i, instance in enumerate(instances):
        instance.invoke_function()  # 预热所有实例

    # 模拟并发用户请求
    concurrent_times = []
    for instance in instances:
        req_time, _, _ = instance.invoke_function()
        concurrent_times.append(req_time)

    avg_concurrent = sum(concurrent_times) / len(concurrent_times)
    print(f"   并发请求平均时间: {avg_concurrent:.3f}秒\n")

    # 策略3: 代码优化
    print("3. 代码优化策略:")
    print("   - 减少初始化代码")
    print("   - 延迟加载非必要依赖")
    print("   - 使用更轻量的运行时")


if __name__ == '__main__':
    simulate_cold_vs_warm_starts()
    print("\n" + "="*60 + "\n")
    demonstrate_warmup_strategies()
    print("\n=== 演示完成 ===")