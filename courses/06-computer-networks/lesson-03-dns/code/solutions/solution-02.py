#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答：DNS 记录类型解析器
"""

from typing import Dict, Optional, Any

class DNSRecordType:
    """DNS 记录类型常量"""
    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    MX = "MX"
    TXT = "TXT"
    NS = "NS"

class AdvancedDNSResolver:
    """支持多种记录类型的 DNS 解析器"""

    def __init__(self):
        # 使用 (domain, record_type) 作为键
        self.records: Dict[tuple, Any] = {
            ("google.com", DNSRecordType.A): "142.250.185.206",
            ("google.com", DNSRecordType.AAAA): "2a00:1450:4001:830::200e",
            ("www.google.com", DNSRecordType.CNAME): "google.com",
            ("gmail.com", DNSRecordType.MX): "gmail-smtp-in.l.google.com",
            ("example.com", DNSRecordType.TXT): "v=spf1 include:_spf.google.com ~all",
            ("example.com", DNSRecordType.NS): "ns1.example.com"
        }

    def resolve(self, domain: str, record_type: str = DNSRecordType.A) -> Optional[str]:
        """
        解析指定类型的 DNS 记录

        Args:
            domain (str): 域名
            record_type (str): 记录类型，默认为 A 记录

        Returns:
            str or None: 解析结果或 None（如果未找到）
        """
        key = (domain, record_type)
        return self.records.get(key, None)

    def get_all_records(self, domain: str) -> Dict[str, str]:
        """获取域名的所有记录类型"""
        result = {}
        for (d, rtype), value in self.records.items():
            if d == domain:
                result[rtype] = value
        return result

# 测试代码
if __name__ == "__main__":
    resolver = AdvancedDNSResolver()

    # 测试不同记录类型
    print("=== A 记录查询 ===")
    print(f"google.com A: {resolver.resolve('google.com', DNSRecordType.A)}")

    print("\n=== CNAME 记录查询 ===")
    print(f"www.google.com CNAME: {resolver.resolve('www.google.com', DNSRecordType.CNAME)}")

    print("\n=== MX 记录查询 ===")
    print(f"gmail.com MX: {resolver.resolve('gmail.com', DNSRecordType.MX)}")

    print("\n=== 所有记录查询 ===")
    all_records = resolver.get_all_records("google.com")
    for rtype, value in all_records.items():
        print(f"google.com {rtype}: {value}")

    print("\n=== 查询不存在的记录 ===")
    result = resolver.resolve("nonexistent.com", DNSRecordType.A)
    print(f"nonexistent.com A: {result}")