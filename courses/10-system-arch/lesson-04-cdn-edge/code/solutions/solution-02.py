#!/usr/bin/env python3
"""
解决方案2: 高级缓存策略

这个解决方案实现了更复杂的CDN缓存策略，
包括LRU淘汰、智能TTL和预热机制。
"""

import time
import heapq
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass, field

@dataclass
class CacheItem:
    key: str
    content: str
    timestamp: float
    ttl: int
    access_count: int = 0
    last_access: float = field(default_factory=time.time)

class AdvancedCDNCache:
    def __init__(self, capacity: int = 100):
        self.cache: Dict[str, CacheItem] = {}
        self.capacity = capacity
        self.hits = 0
        self.misses = 0
        # 用于LRU的访问时间堆
        self.access_heap: List[Tuple[float, str]] = []

    def get(self, key: str) -> Optional[str]:
        if key not in self.cache:
            self.misses += 1
            return None

        item = self.cache[key]
        current_time = time.time()

        if current_time - item.timestamp > item.ttl:
            del self.cache[key]
            self.misses += 1
            return None

        # 更新访问统计
        item.access_count += 1
        item.last_access = current_time
        heapq.heappush(self.access_heap, (current_time, key))

        self.hits += 1
        return item.content

    def put(self, key: str, content: str, ttl: int = 3600, priority: str = "normal"):
        # 根据优先级调整TTL
        if priority == "high":
            ttl = max(ttl, 7200)  # 高优先级至少2小时
        elif priority == "low":
            ttl = min(ttl, 1800)  # 低优先级最多30分钟

        # 清理过期项
        self._cleanup_expired()

        # 如果缓存已满，使用改进的LRU策略
        if len(self.cache) >= self.capacity:
            self._evict_items()

        self.cache[key] = CacheItem(
            key=key,
            content=content,
            timestamp=time.time(),
            ttl=ttl
        )

    def _cleanup_expired(self):
        current_time = time.time()
        expired_keys = []
        for key, item in self.cache.items():
            if current_time - item.timestamp > item.ttl:
                expired_keys.append(key)

        for key in expired_keys:
            del self.cache[key]

    def _evict_items(self):
        # 基于访问频率和时间的混合策略
        items_to_evict = sorted(
            self.cache.items(),
            key=lambda x: (x[1].access_count, x[1].last_access)
        )[:max(1, self.capacity // 10)]

        for key, _ in items_to_evict:
            del self.cache[key]

    def get_hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def warm_up_cache(self, items: List[Tuple[str, str, int]]):
        """预热缓存"""
        for key, content, ttl in items:
            self.put(key, content, ttl, priority="high")

def main():
    cache = AdvancedCDNCache(capacity=5)

    # 预热热门内容
    hot_content = [
        ("/index.html", "<html>首页</html>", 7200),
        ("/style.css", "body { color: black; }", 3600),
        ("/api/popular.json", '{"popular": true}', 1800),
    ]
    cache.warm_up_cache(hot_content)

    # 测试缓存操作
    test_keys = ["/index.html", "/about.html", "/contact.html"]
    for key in test_keys:
        result = cache.get(key)
        status = "命中" if result else "未命中"
        print(f"{key}: {status}")

    print(f"缓存命中率: {cache.get_hit_rate():.2%}")

if __name__ == "__main__":
    main()