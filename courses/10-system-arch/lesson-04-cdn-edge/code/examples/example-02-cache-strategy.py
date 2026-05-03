#!/usr/bin/env python3
"""
CDN缓存策略模拟：演示缓存命中、未命中、TTL和失效机制

这个示例展示了CDN缓存的核心概念，包括缓存命中率、
TTL（生存时间）管理和缓存失效策略。
"""

import time
import random
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class CacheItem:
    """缓存项数据结构"""
    content: str
    timestamp: float  # 缓存创建时间戳
    ttl: int  # 生存时间（秒）

class CDNCache:
    """CDN缓存模拟器"""

    def __init__(self, capacity: int = 100):
        self.cache: Dict[str, CacheItem] = {}  # 缓存存储 {key: CacheItem}
        self.capacity = capacity  # 缓存容量
        self.hits = 0  # 缓存命中次数
        self.misses = 0  # 缓存未命中次数

    def get(self, key: str) -> Optional[str]:
        """
        从缓存中获取内容

        Args:
            key: 缓存键

        Returns:
            缓存内容，如果未命中或已过期则返回None
        """
        if key not in self.cache:
            self.misses += 1
            return None

        item = self.cache[key]
        current_time = time.time()

        # 检查是否过期
        if current_time - item.timestamp > item.ttl:
            # 缓存已过期，删除并返回未命中
            del self.cache[key]
            self.misses += 1
            return None

        self.hits += 1
        return item.content

    def put(self, key: str, content: str, ttl: int = 3600):
        """
        将内容存入缓存

        Args:
            key: 缓存键
            content: 缓存内容
            ttl: 生存时间（秒），默认1小时
        """
        # 如果缓存已满，删除最旧的项（简单LRU策略）
        if len(self.cache) >= self.capacity:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k].timestamp)
            del self.cache[oldest_key]

        self.cache[key] = CacheItem(
            content=content,
            timestamp=time.time(),
            ttl=ttl
        )

    def invalidate(self, key: str):
        """使指定缓存项失效"""
        if key in self.cache:
            del self.cache[key]
            print(f"缓存项 '{key}' 已失效")

    def get_hit_rate(self) -> float:
        """计算缓存命中率"""
        total_requests = self.hits + self.misses
        if total_requests == 0:
            return 0.0
        return self.hits / total_requests

def simulate_cache_operations():
    """模拟CDN缓存操作"""
    print("=== CDN缓存策略模拟 ===\n")

    cache = CDNCache(capacity=5)

    # 模拟热门内容
    popular_content = {
        "/index.html": "<html>首页内容</html>",
        "/style.css": "body { color: black; }",
        "/script.js": "console.log('脚本');",
        "/image.jpg": "binary_image_data...",
        "/api/data.json": '{"data": "API响应"}'
    }

    print("阶段1: 首次请求（全部缓存未命中）")
    for path, content in popular_content.items():
        result = cache.get(path)
        if result is None:
            print(f"  {path}: 缓存未命中 → 从源站获取")
            # 模拟从源站获取并缓存
            cache.put(path, content, ttl=3600)  # 缓存1小时

    print(f"\n当前缓存命中率: {cache.get_hit_rate():.2%}")

    print("\n阶段2: 重复请求（应该大部分命中）")
    test_paths = ["/index.html", "/style.css", "/nonexistent.html", "/script.js"]
    for path in test_paths:
        result = cache.get(path)
        status = "命中" if result else "未命中"
        print(f"  {path}: 缓存{status}")

    print(f"\n更新后缓存命中率: {cache.get_hit_rate():.2%}")

    print("\n阶段3: 缓存失效测试")
    cache.invalidate("/index.html")
    result = cache.get("/index.html")
    print(f"  /index.html 失效后: {'命中' if result else '未命中'}")

    # 模拟TTL过期
    print("\n阶段4: TTL过期测试")
    # 手动设置一个即将过期的缓存项
    cache.put("/temp.html", "<html>临时内容</html>", ttl=1)
    time.sleep(1.1)  # 等待超过TTL
    result = cache.get("/temp.html")
    print(f"  /temp.html TTL过期后: {'命中' if result else '未命中'}")

if __name__ == "__main__":
    simulate_cache_operations()