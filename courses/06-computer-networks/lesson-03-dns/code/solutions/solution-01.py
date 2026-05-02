#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答：简单 DNS 缓存实现
"""

import time
from typing import Optional, Dict, Tuple

class SimpleDNSCache:
    """简单的 DNS 缓存实现"""

    def __init__(self):
        self.cache: Dict[str, Tuple[str, float]] = {}

    def get(self, domain: str) -> Optional[str]:
        """获取缓存的 DNS 记录"""
        if domain in self.cache:
            ip, expiry_time = self.cache[domain]
            if time.time() < expiry_time:
                return ip
            else:
                # 缓存过期，删除记录
                del self.cache[domain]
        return None

    def set(self, domain: str, ip: str, ttl: int = 300) -> None:
        """设置 DNS 缓存记录"""
        expiry_time = time.time() + ttl
        self.cache[domain] = (ip, expiry_time)

# 测试代码
if __name__ == "__main__":
    cache = SimpleDNSCache()

    # 设置缓存
    cache.set("example.com", "93.184.216.34", ttl=5)
    print(f"设置缓存: example.com -> 93.184.216.34")

    # 获取缓存（应该成功）
    result = cache.get("example.com")
    print(f"获取缓存: {result}")

    # 等待缓存过期
    time.sleep(6)

    # 再次获取（应该返回 None）
    result = cache.get("example.com")
    print(f"缓存过期后获取: {result}")