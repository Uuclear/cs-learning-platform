#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serverless 课程 - 练习题2 解决方案

实现冷启动性能测试和优化策略。
"""

import time
import random


class OptimizedLambdaFunction:
    """优化后的 Lambda 函数，减少冷启动时间"""

    def __init__(self):
        self.is_initialized = False
        self.db_connection = None
        self.config = None

    def initialize(self):
        """延迟初始化，只在需要时才执行"""
        if not self.is_initialized:
            # 只加载必要的依赖
            self.config = self.load_config()
            # 延迟数据库连接，只在真正需要时才建立
            self.is_initialized = True

    def load_config(self):
        """快速加载配置"""
        # 模拟快速配置加载（避免复杂的初始化）
        return {'region': 'us-east-1', 'timeout': 30}

    def get_db_connection(self):
        """按需获取数据库连接"""
        if not self.db_connection:
            # 模拟数据库连接建立（这通常是最耗时的部分）
            time.sleep(0.5)  # 模拟连接时间
            self.db_connection = "db_connection_object"
        return self.db_connection

    def process_request(self, needs_db=False):
        """处理请求"""
        self.initialize()

        start_time = time.time()

        if needs_db:
            conn = self.get_db_connection()
            # 模拟数据库操作
            time.sleep(0.1)

        # 其他业务逻辑
        time.sleep(0.05)

        total_time = time.time() - start_time
        return total_time


def measure_performance():
    """测量性能"""
    func = OptimizedLambdaFunction()

    # 冷启动测试
    cold_start_time = func.process_request(needs_db=True)

    # 热启动测试
    warm_times = []
    for _ in range(3):
        warm_time = func.process_request(needs_db=True)
        warm_times.append(warm_time)

    avg_warm_time = sum(warm_times) / len(warm_times)

    return {
        'cold_start_time': cold_start_time,
        'warm_start_time': avg_warm_time,
        'improvement_ratio': cold_start_time / avg_warm_time if avg_warm_time > 0 else 0
    }