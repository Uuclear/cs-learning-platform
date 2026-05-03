#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存模式解决方案
"""

import time
from typing import Optional, Dict, Any

class Database:
    def __init__(self):
        self.data = {"user:1": "Alice", "user:2": "Bob", "user:3": "Charlie"}
        self.read_count = 0
        self.write_count = 0

    def get(self, key: str) -> Optional[str]:
        self.read_count += 1
        time.sleep(0.01)
        return self.data.get(key)

    def set(self, key: str, value: str) -> None:
        self.write_count += 1
        time.sleep(0.01)
        self.data[key] = value

class SimpleCache:
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.hit_count = 0
        self.miss_count = 0

    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            self.hit_count += 1
            return self.cache[key]
        else:
            self.miss_count += 1
            return None

    def set(self, key: str, value: Any) -> None:
        self.cache[key] = value

    def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]

def cache_aside_get(cache: SimpleCache, db: Database, key: str) -> Optional[str]:
    value = cache.get(key)
    if value is not None:
        return value

    value = db.get(key)
    if value is not None:
        cache.set(key, value)

    return value

def cache_aside_set(cache: SimpleCache, db: Database, key: str, value: str) -> None:
    db.set(key, value)
    cache.delete(key)

class ReadThroughCache:
    def __init__(self, cache: SimpleCache, db: Database):
        self.cache = cache
        self.db = db

    def get(self, key: str) -> Optional[str]:
        value = self.cache.get(key)
        if value is not None:
            return value

        value = self.db.get(key)
        if value is not None:
            self.cache.set(key, value)

        return value

class WriteThroughCache:
    def __init__(self, cache: SimpleCache, db: Database):
        self.cache = cache
        self.db = db

    def get(self, key: str) -> Optional[str]:
        value = self.cache.get(key)
        if value is not None:
            return value

        value = self.db.get(key)
        if value is not None:
            self.cache.set(key, value)

        return value

    def set(self, key: str, value: str) -> None:
        self.db.set(key, value)
        self.cache.set(key, value)