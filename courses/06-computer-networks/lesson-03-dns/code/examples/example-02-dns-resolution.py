#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNS 解析过程模拟 - 演示递归查询和迭代查询的区别
"""

class DNSServer:
    """DNS 服务器模拟"""

    def __init__(self, name: str, records: dict):
        self.name = name
        self.records = records  # 本地记录
        self.authoritative_for = set(records.keys())  # 权威域名

    def has_record(self, domain: str) -> bool:
        """检查是否有该域名的记录"""
        return domain in self.authoritative_for

    def get_record(self, domain: str) -> str:
        """获取域名记录"""
        return self.records.get(domain, None)

class RecursiveDNSResolver:
    """递归 DNS 解析器"""

    def __init__(self):
        # 设置 DNS 服务器层次结构
        self.root_server = DNSServer("根服务器", {
            "com": "tld-com-server",
            "org": "tld-org-server",
            "cn": "tld-cn-server"
        })

        self.tld_com_server = DNSServer("COM顶级域服务器", {
            "google.com": "ns1.google.com",
            "baidu.com": "ns.baidu.com",
            "github.com": "dns1.github.com"
        })

        self.authoritative_servers = {
            "ns1.google.com": DNSServer("Google权威服务器", {"google.com": "142.250.185.206"}),
            "ns.baidu.com": DNSServer("百度权威服务器", {"baidu.com": "220.181.38.148"}),
            "dns1.github.com": DNSServer("GitHub权威服务器", {"github.com": "140.82.114.4"})
        }

    def recursive_resolve(self, domain: str) -> str:
        """
        递归解析域名 - 客户端视角
        客户端只需要问一次，DNS 服务器会负责完成所有查询
        """
        print(f"开始递归解析 {domain}")

        # 第一步：问根服务器
        tld_server_name = self.root_server.get_record(domain.split('.')[-1] + '.')
        print(f"根服务器告诉我去问 {tld_server_name}")

        # 第二步：问 TLD 服务器
        auth_server_name = self.tld_com_server.get_record(domain)
        print(f"TLD服务器告诉我去问 {auth_server_name}")

        # 第三步：问权威服务器
        if auth_server_name in self.authoritative_servers:
            ip = self.authoritative_servers[auth_server_name].get_record(domain)
            print(f"权威服务器返回 IP: {ip}")
            return ip
        else:
            return "解析失败"

# 使用示例
if __name__ == "__main__":
    resolver = RecursiveDNSResolver()
    result = resolver.recursive_resolve("google.com")
    print(f"\n最终结果: {result}")