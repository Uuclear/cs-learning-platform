#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LRU 缓存解决方案
"""

from collections import OrderedDict
from typing import Any, Optional

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.eviction_count = 0

    def get(self, key: Any) -> Optional[Any]:
        if key not in self.cache:
            return None

        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
            self.eviction_count += 1

        self.cache[key] = value

    def delete(self, key: Any) -> bool:
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def size(self) -> int:
        return len(self.cache)

    def is_full(self) -> bool:
        return len(self.cache) >= self.capacity

    def get_eviction_count(self) -> int:
        return self.eviction_count