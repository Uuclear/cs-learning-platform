#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于 Redis 数据结构的令牌桶限流器实现
使用字典模拟 Redis 的有序集合（Sorted Set）来存储令牌
"""

import time
from typing import Dict, List, Tuple

class RedisLikeRateLimiter:
    """
    使用 Redis-like 数据结构的令牌桶限流器
    模拟使用 Redis 的 Sorted Set 来实现滑动窗口限流
    """

    def __init__(self):
        # 使用字典模拟 Redis 的 key-value 存储
        # key: 限流键名, value: 有序的请求时间戳列表
        self.storage: Dict[str, List[float]] = {}
        self.window_size = 60.0  # 滑动窗口大小（秒）
        self.max_requests = 10   # 窗口内最大请求数

    def is_allowed(self, key: str) -> bool:
        """
        检查是否允许请求通过

        使用滑动窗口算法：
        1. 获取当前时间
        2. 清理过期的请求记录
        3. 检查当前窗口内的请求数是否超过限制

        Args:
            key: 限流的键（如用户ID、IP地址等）

        Returns:
            True 表示允许请求，False 表示拒绝请求
        """
        current_time = time.time()

        # 如果键不存在，初始化为空列表
        if key not in self.storage:
            self.storage[key] = []

        # 清理过期的请求记录（保留窗口内的记录）
        window_start = current_time - self.window_size
        self.storage[key] = [timestamp for timestamp in self.storage[key]
                            if timestamp >= window_start]

        # 检查当前窗口内的请求数
        current_count = len(self.storage[key])

        if current_count < self.max_requests:
            # 允许请求，添加当前时间戳
            self.storage[key].append(current_time)
            return True
        else:
            # 拒绝请求
            return False

    def set_rate_limit(self, max_requests: int, window_size: float) -> None:
        """
        设置限流参数

        Args:
            max_requests: 窗口内最大请求数
            window_size: 窗口大小（秒）
        """
        self.max_requests = max_requests
        self.window_size = window_size

    def get_remaining_requests(self, key: str) -> int:
        """
        获取剩余可请求次数

        Args:
            key: 限流的键

        Returns:
            剩余可请求次数
        """
        current_time = time.time()
        window_start = current_time - self.window_size

        if key not in self.storage:
            return self.max_requests

        # 清理过期记录
        self.storage[key] = [timestamp for timestamp in self.storage[key]
                            if timestamp >= window_start]

        current_count = len(self.storage[key])
        return max(0, self.max_requests - current_count)

    def reset_key(self, key: str) -> None:
        """重置指定键的限流计数"""
        if key in self.storage:
            del self.storage[key]

class TokenBucketRateLimiter:
    """
    传统的令牌桶限流器实现
    更接近实际的令牌桶算法
    """

    def __init__(self, capacity: int, refill_rate: float):
        """
        初始化令牌桶

        Args:
            capacity: 令牌桶容量
            refill_rate: 令牌填充速率（每秒填充的令牌数）
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity  # 当前令牌数
        self.last_refill = time.time()

    def _refill_tokens(self) -> None:
        """填充令牌"""
        current_time = time.time()
        elapsed = current_time - self.last_refill

        # 计算应该填充的令牌数
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = current_time

    def is_allowed(self) -> bool:
        """
        检查是否允许请求

        Returns:
            True 表示允许请求，False 表示拒绝请求
        """
        self._refill_tokens()

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        else:
            return False

    def get_tokens(self) -> float:
        """获取当前令牌数"""
        self._refill_tokens()
        return self.tokens

def simulate_rate_limiting():
    """模拟限流器使用"""
    print("=== 限流器模拟 ===")

    # 测试滑动窗口限流器
    print("\n1. 滑动窗口限流器 (10次/60秒):")
    sliding_limiter = RedisLikeRateLimiter()
    sliding_limiter.set_rate_limit(10, 60.0)

    user_key = "user:123"
    allowed_count = 0

    # 模拟连续请求
    for i in range(15):
        if sliding_limiter.is_allowed(user_key):
            allowed_count += 1
            print(f"  请求 {i+1}: 允许")
        else:
            print(f"  请求 {i+1}: 拒绝")

    print(f"总共允许 {allowed_count} 次请求")
    print(f"剩余可请求次数: {sliding_limiter.get_remaining_requests(user_key)}")

    # 测试令牌桶限流器
    print("\n2. 令牌桶限流器 (容量5, 填充速率2个/秒):")
    token_limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2.0)

    for i in range(8):
        if token_limiter.is_allowed():
            print(f"  请求 {i+1}: 允许 (剩余令牌: {token_limiter.get_tokens():.1f})")
        else:
            print(f"  请求 {i+1}: 拒绝 (剩余令牌: {token_limiter.get_tokens():.1f})")
        time.sleep(0.5)  # 等待一段时间让令牌填充

def main():
    """主函数"""
    simulate_rate_limiting()
    print("\n=== 模拟完成 ===")

if __name__ == "__main__":
    main()