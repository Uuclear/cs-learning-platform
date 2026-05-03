#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
断路器模式解决方案

这是一个完整的断路器实现，包含所有要求的功能。
"""

import time
import random
from enum import Enum
from typing import Callable, Any


class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0

    def call(self, func: Callable[[], Any]) -> Any:
        if self.state == CircuitBreakerState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitBreakerState.HALF_OPEN
                self.failure_count = 0
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN

    def _should_attempt_reset(self) -> bool:
        return time.time() - self.last_failure_time >= self.timeout


# 测试函数
def test_circuit_breaker():
    cb = CircuitBreaker(failure_threshold=3, timeout=5.0)

    # 模拟总是失败的函数
    def failing_func():
        raise Exception("Always fails")

    # 测试断路器打开
    try:
        for _ in range(3):
            cb.call(failing_func)
    except Exception:
        pass

    assert cb.state == CircuitBreakerState.OPEN

    # 等待超时
    time.sleep(6)

    # 现在应该处于半开状态
    assert cb.state == CircuitBreakerState.HALF_OPEN

    print("断路器测试通过！")


if __name__ == "__main__":
    test_circuit_breaker()