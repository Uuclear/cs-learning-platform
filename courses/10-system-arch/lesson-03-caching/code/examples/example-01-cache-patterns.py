#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存模式示例：演示三种常见的缓存模式
1. Cache-Aside (旁路缓存)
2. Read-Through (读穿透)
3. Write-Through (写穿透)
"""

import time
from typing import Optional, Dict, Any

class Database:
    """模拟数据库"""
    def __init__(self):
        self.data = {"user:1": "Alice", "user:2": "Bob", "user:3": "Charlie"}
        self.read_count = 0
        self.write_count = 0

    def get(self, key: str) -> Optional[str]:
        """从数据库读取数据"""
        self.read_count += 1
        # 模拟数据库延迟
        time.sleep(0.01)
        return self.data.get(key)

    def set(self, key: str, value: str) -> None:
        """向数据库写入数据"""
        self.write_count += 1
        # 模拟数据库延迟
        time.sleep(0.01)
        self.data[key] = value

class SimpleCache:
    """简单的内存缓存"""
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.hit_count = 0
        self.miss_count = 0

    def get(self, key: str) -> Optional[Any]:
        """从缓存获取数据"""
        if key in self.cache:
            self.hit_count += 1
            return self.cache[key]
        else:
            self.miss_count += 1
            return None

    def set(self, key: str, value: Any) -> None:
        """设置缓存数据"""
        self.cache[key] = value

    def delete(self, key: str) -> None:
        """删除缓存数据"""
        if key in self.cache:
            del self.cache[key]

# === Cache-Aside 模式 (旁路缓存) ===
def cache_aside_get(cache: SimpleCache, db: Database, key: str) -> Optional[str]:
    """
    Cache-Aside 模式读取数据：
    1. 先查缓存
    2. 如果缓存命中，直接返回
    3. 如果缓存未命中，查数据库并将结果写入缓存
    """
    value = cache.get(key)
    if value is not None:
        return value

    # 缓存未命中，查询数据库
    value = db.get(key)
    if value is not None:
        cache.set(key, value)

    return value

def cache_aside_set(cache: SimpleCache, db: Database, key: str, value: str) -> None:
    """
    Cache-Aside 模式写入数据：
    1. 直接写入数据库
    2. 删除对应的缓存（让下次读取时重新加载）
    """
    db.set(key, value)
    cache.delete(key)

# === Read-Through 模式 (读穿透) ===
class ReadThroughCache:
    """Read-Through 缓存封装"""
    def __init__(self, cache: SimpleCache, db: Database):
        self.cache = cache
        self.db = db

    def get(self, key: str) -> Optional[str]:
        """
        Read-Through 模式：
        对应用透明，缓存层自动处理缓存未命中的情况
        """
        value = self.cache.get(key)
        if value is not None:
            return value

        # 自动从数据库加载并缓存
        value = self.db.get(key)
        if value is not None:
            self.cache.set(key, value)

        return value

# === Write-Through 模式 (写穿透) ===
class WriteThroughCache:
    """Write-Through 缓存封装"""
    def __init__(self, cache: SimpleCache, db: Database):
        self.cache = cache
        self.db = db

    def get(self, key: str) -> Optional[str]:
        """读取操作与 Read-Through 相同"""
        value = self.cache.get(key)
        if value is not None:
            return value

        value = self.db.get(key)
        if value is not None:
            self.cache.set(key, value)

        return value

    def set(self, key: str, value: str) -> None:
        """
        Write-Through 模式：
        写入时同时更新缓存和数据库
        """
        self.db.set(key, value)
        self.cache.set(key, value)

def main():
    """演示三种缓存模式"""
    print("=== 缓存模式演示 ===\n")

    # 初始化数据库和缓存
    db = Database()
    cache = SimpleCache()

    # === 测试 Cache-Aside 模式 ===
    print("1. Cache-Aside 模式:")
    cache_aside_set(cache, db, "user:4", "David")
    result1 = cache_aside_get(cache, db, "user:4")  # 第一次读取
    result2 = cache_aside_get(cache, db, "user:4")  # 第二次读取（缓存命中）
    print(f"   数据库读取次数: {db.read_count}, 缓存命中: {cache.hit_count}, 未命中: {cache.miss_count}")

    # 重置计数器
    db.read_count = 0
    cache.hit_count = 0
    cache.miss_count = 0

    # === 测试 Read-Through 模式 ===
    print("\n2. Read-Through 模式:")
    read_through = ReadThroughCache(cache, db)
    result3 = read_through.get("user:1")  # 第一次读取
    result4 = read_through.get("user:1")  # 第二次读取（缓存命中）
    print(f"   数据库读取次数: {db.read_count}, 缓存命中: {cache.hit_count}, 未命中: {cache.miss_count}")

    # 重置计数器
    db.read_count = 0
    cache.hit_count = 0
    cache.miss_count = 0

    # === 测试 Write-Through 模式 ===
    print("\n3. Write-Through 模式:")
    write_through = WriteThroughCache(cache, db)
    write_through.set("user:5", "Eve")
    result5 = write_through.get("user:5")  # 应该直接从缓存读取
    print(f"   数据库读取次数: {db.read_count}, 数据库写入次数: {db.write_count}")
    print(f"   缓存命中: {cache.hit_count}, 未命中: {cache.miss_count}")

    print("\n=== 演示完成 ===")

if __name__ == "__main__":
    main()