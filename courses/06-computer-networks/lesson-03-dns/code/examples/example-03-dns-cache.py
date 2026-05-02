#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNS 缓存实现 - 演示如何通过缓存提高 DNS 查询效率
"""

import time
from typing import Optional, Dict, Tuple

class DNSCache:
    """DNS 缓存实现"""

    def __init__(self, ttl: int = 300):
        """
        初始化 DNS 缓存

        Args:
            ttl (int): 缓存过期时间（秒），默认 5 分钟
        """
        self.cache: Dict[str, Tuple[str, float]] = {}  # 域名 -> (IP, 过期时间)
        self.ttl = ttl

    def get(self, domain: str) -> Optional[str]:
        """
        从缓存获取域名解析结果

        Args:
            domain (str): 要查询的域名

        Returns:
            str or None: 如果缓存有效则返回 IP，否则返回 None
        """
        if domain in self.cache:
            ip, expiry_time = self.cache[domain]
            if time.time() < expiry_time:
                print(f"缓存命中: {domain} -> {ip}")
                return ip
            else:
                # 缓存过期，删除它
                del self.cache[domain]
                print(f"缓存过期: {domain}")
        return None

    def set(self, domain: str, ip: str) -> None:
        """
        设置缓存记录

        Args:
            domain (str): 域名
            ip (str): IP 地址
        """
        expiry_time = time.time() + self.ttl
        self.cache[domain] = (ip, expiry_time)
        print(f"缓存设置: {domain} -> {ip} (过期时间: {self.ttl}秒)")

# 模拟真实的 DNS 查询函数
def real_dns_lookup(domain: str) -> str:
    """模拟真实的 DNS 查询（耗时操作）"""
    print(f"执行真实 DNS 查询: {domain}")
    # 模拟网络延迟
    time.sleep(0.1)

    # 简单的域名到 IP 映射
    dns_map = {
        "google.com": "142.250.185.206",
        "baidu.com": "220.181.38.148",
        "github.com": "140.82.114.4"
    }
    return dns_map.get(domain, "未知域名")

def smart_dns_resolve(domain: str, cache: DNSCache) -> str:
    """智能 DNS 解析（带缓存）"""
    # 先查缓存
    cached_ip = cache.get(domain)
    if cached_ip:
        return cached_ip

    # 缓存未命中，执行真实查询
    ip = real_dns_lookup(domain)
    cache.set(domain, ip)
    return ip

# 使用示例
if __name__ == "__main__":
    cache = DNSCache(ttl=10)  # 10秒缓存

    print("=== 第一次查询（缓存未命中）===")
    ip1 = smart_dns_resolve("google.com", cache)
    print(f"结果: {ip1}\n")

    print("=== 第二次查询（缓存命中）===")
    ip2 = smart_dns_resolve("google.com", cache)
    print(f"结果: {ip2}\n")

    print("=== 等待缓存过期 ===")
    time.sleep(11)  # 等待超过 TTL

    print("=== 第三次查询（缓存已过期）===")
    ip3 = smart_dns_resolve("google.com", cache)
    print(f"结果: {ip3}")