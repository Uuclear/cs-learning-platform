#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
限流器解决方案
"""

import time
from typing import Dict, List

class RedisLikeRateLimiter:
    def __init__(self):
        self.storage: Dict[str, List[float]] = {}
        self.window_size = 60.0
        self.max_requests = 10

    def is_allowed(self, key: str) -> bool:
        current_time = time.time()

        if key not in self.storage:
            self.storage[key] = []

        window_start = current_time - self.window_size
        self.storage[key] = [timestamp for timestamp in self.storage[key]
                            if timestamp >= window_start]

        current_count = len(self.storage[key])

        if current_count < self.max_requests:
            self.storage[key].append(current_time)
            return True
        else:
            return False

    def set_rate_limit(self, max_requests: int, window_size: float) -> None:
        self.max_requests = max_requests
        self.window_size = window_size

    def get_remaining_requests(self, key: str) -> int:
        current_time = time.time()
        window_start = current_time - self.window_size

        if key not in self.storage:
            return self.max_requests

        self.storage[key] = [timestamp for timestamp in self.storage[key]
                            if timestamp >= window_start]

        current_count = len(self.storage[key])
        return max(0, self.max_requests - current_count)

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def _refill_tokens(self) -> None:
        current_time = time.time()
        elapsed = current_time - self.last_refill
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = current_time

    def is_allowed(self) -> bool:
        self._refill_tokens()

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        else:
            return False

    def get_tokens(self) -> float:
        self._refill_tokens()
        return self.tokens