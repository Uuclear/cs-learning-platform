#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
断路器模式实现

断路器模式用于防止系统在依赖服务失败时持续尝试调用，
避免资源耗尽和级联故障。它有三种状态：
- 关闭状态（Closed）：正常调用，记录失败次数
- 打开状态（Open）：直接拒绝调用，快速失败
- 半开状态（Half-Open）：允许少量调用测试服务是否恢复
"""

import time
import random
from enum import Enum
from typing import Callable, Any


class CircuitBreakerState(Enum):
    """断路器状态枚举"""
    CLOSED = "closed"      # 关闭状态：正常调用
    OPEN = "open"          # 打开状态：拒绝调用
    HALF_OPEN = "half_open"  # 半开状态：试探性调用


class CircuitBreaker:
    """断路器实现类"""

    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        """
        初始化断路器

        Args:
            failure_threshold: 失败阈值，超过此值则打开断路器
            timeout: 超时时间（秒），打开状态持续的时间
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0

    def call(self, func: Callable[[], Any]) -> Any:
        """
        通过断路器调用函数

        Args:
            func: 要调用的函数

        Returns:
            函数的返回值

        Raises:
            Exception: 如果断路器处于打开状态或函数执行失败
        """
        if self.state == CircuitBreakerState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitBreakerState.HALF_OPEN
                self.failure_count = 0
            else:
                raise Exception("断路器处于打开状态，拒绝调用")

        try:
            result = func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """处理调用成功的情况"""
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED

    def _on_failure(self):
        """处理调用失败的情况"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def _should_attempt_reset(self) -> bool:
        """检查是否应该尝试重置（从打开状态转为半开状态）"""
        return time.time() - self.last_failure_time >= self.timeout


def simulate_unreliable_service() -> str:
    """
    模拟一个不可靠的服务

    这个服务有70%的概率失败，用于测试断路器的效果
    """
    if random.random() < 0.7:  # 70% 失败概率
        raise Exception("服务暂时不可用")
    return "服务调用成功"


def main():
    """主函数：演示断路器的使用"""
    print("=== 断路器模式演示 ===\n")

    # 创建断路器实例
    cb = CircuitBreaker(failure_threshold=3, timeout=10.0)

    # 模拟连续调用不可靠服务
    for i in range(10):
        try:
            result = cb.call(simulate_unreliable_service)
            print(f"调用 {i+1}: {result} (状态: {cb.state.value})")
        except Exception as e:
            print(f"调用 {i+1}: 失败 - {e} (状态: {cb.state.value})")

        time.sleep(1)

    print("\n等待超时后再次尝试...")
    time.sleep(12)  # 等待超过超时时间

    # 尝试恢复调用
    try:
        result = cb.call(simulate_unreliable_service)
        print(f"恢复调用: {result} (状态: {cb.state.value})")
    except Exception as e:
        print(f"恢复调用: 失败 - {e} (状态: {cb.state.value})")


if __name__ == "__main__":
    main()