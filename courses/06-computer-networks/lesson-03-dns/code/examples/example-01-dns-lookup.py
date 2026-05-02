#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNS 查询模拟器 - 演示基本的域名解析过程
"""

class SimpleDNSResolver:
    """简单的 DNS 解析器模拟"""

    def __init__(self):
        # 模拟的 DNS 记录数据库
        self.dns_records = {
            "google.com": "142.250.185.206",
            "baidu.com": "220.181.38.148",
            "github.com": "140.82.114.4",
            "taobao.com": "110.75.128.22",
            "www.example.com": "93.184.216.34"
        }

    def resolve(self, domain: str) -> str:
        """
        解析域名到 IP 地址

        Args:
            domain (str): 要解析的域名

        Returns:
            str: 对应的 IP 地址，如果找不到则返回错误信息
        """
        if domain in self.dns_records:
            return self.dns_records[domain]
        else:
            return f"错误: 无法找到域名 {domain} 的记录"

# 使用示例
if __name__ == "__main__":
    resolver = SimpleDNSResolver()

    domains = ["google.com", "baidu.com", "unknown-site.com"]

    print("=== DNS 查询模拟 ===")
    for domain in domains:
        ip = resolver.resolve(domain)
        print(f"{domain} -> {ip}")