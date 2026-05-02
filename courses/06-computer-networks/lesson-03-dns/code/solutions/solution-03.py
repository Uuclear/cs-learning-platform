#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答：模拟 DNS 层次查询
"""

import time
from typing import Optional, Dict, List, Tuple

class DNSServer:
    """DNS 服务器基类"""

    def __init__(self, name: str, records: Dict[str, str] = None):
        self.name = name
        self.records = records or {}
        self.authoritative_for = set(self.records.keys())

    def is_authoritative(self, domain: str) -> bool:
        """检查是否对该域名具有权威性"""
        return domain in self.authoritative_for

    def get_record(self, domain: str) -> Optional[str]:
        """获取记录"""
        return self.records.get(domain)

    def get_referral(self, domain: str) -> Optional[str]:
        """获取推荐的下一个服务器（用于迭代查询）"""
        # 简单实现：根据域名后缀返回推荐服务器
        if domain.endswith('.com'):
            return 'tld-com-server'
        elif domain.endswith('.org'):
            return 'tld-org-server'
        elif domain.endswith('.cn'):
            return 'tld-cn-server'
        return None

class RootDNSServer(DNSServer):
    """根 DNS 服务器"""

    def __init__(self):
        super().__init__("Root Server", {
            "com": "tld-com-server",
            "org": "tld-org-server",
            "cn": "tld-cn-server"
        })

class TLDDNSServer(DNSServer):
    """顶级域 DNS 服务器"""

    def __init__(self, tld: str, authoritative_map: Dict[str, str]):
        name = f"{tld.upper()} TLD Server"
        super().__init__(name, authoritative_map)

class AuthoritativeDNSServer(DNSServer):
    """权威 DNS 服务器"""

    def __init__(self, name: str, records: Dict[str, str]):
        super().__init__(name, records)

class HierarchicalDNSResolver:
    """层次化 DNS 解析器"""

    def __init__(self):
        # 初始化服务器层次结构
        self.root_server = RootDNSServer()

        self.tld_servers = {
            "com": TLDDNSServer("com", {
                "google.com": "ns1.google.com",
                "baidu.com": "ns.baidu.com",
                "github.com": "dns1.github.com"
            }),
            "org": TLDDNSServer("org", {
                "wikipedia.org": "ns.wikipedia.org"
            })
        }

        self.authoritative_servers = {
            "ns1.google.com": AuthoritativeDNSServer("Google Auth Server", {
                "google.com": "142.250.185.206"
            }),
            "ns.baidu.com": AuthoritativeDNSServer("Baidu Auth Server", {
                "baidu.com": "220.181.38.148"
            }),
            "dns1.github.com": AuthoritativeDNSServer("GitHub Auth Server", {
                "github.com": "140.82.114.4"
            }),
            "ns.wikipedia.org": AuthoritativeDNSServer("Wikipedia Auth Server", {
                "wikipedia.org": "91.198.174.192"
            })
        }

    def recursive_resolve(self, domain: str) -> Optional[str]:
        """
        递归解析 - 客户端视角
        """
        print(f"[递归查询] 开始解析 {domain}")

        # 步骤1: 查询根服务器
        tld = domain.split('.')[-1]
        tld_server_name = self.root_server.get_record(tld)
        if not tld_server_name:
            print(f"[错误] 根服务器无法找到 {tld} 的 TLD 服务器")
            return None

        print(f"[递归查询] 根服务器指向 {tld_server_name}")

        # 步骤2: 查询 TLD 服务器
        if tld not in self.tld_servers:
            print(f"[错误] 不支持的 TLD: {tld}")
            return None

        auth_server_name = self.tld_servers[tld].get_record(domain)
        if not auth_server_name:
            print(f"[错误] TLD 服务器无法找到 {domain} 的权威服务器")
            return None

        print(f"[递归查询] TLD 服务器指向 {auth_server_name}")

        # 步骤3: 查询权威服务器
        if auth_server_name not in self.authoritative_servers:
            print(f"[错误] 权威服务器 {auth_server_name} 不存在")
            return None

        ip = self.authoritative_servers[auth_server_name].get_record(domain)
        if not ip:
            print(f"[错误] 权威服务器没有 {domain} 的记录")
            return None

        print(f"[递归查询] 获得最终 IP: {ip}")
        return ip

    def iterative_resolve(self, domain: str) -> Optional[str]:
        """
        迭代解析 - 模拟服务器间的真实交互
        """
        print(f"[迭代查询] 开始解析 {domain}")

        current_server = self.root_server
        query_domain = domain
        steps = 0

        while steps < 10:  # 防止无限循环
            steps += 1
            print(f"[迭代查询] 步骤 {steps}: 查询 {current_server.name} 获取 {query_domain}")

            # 检查当前服务器是否有权威记录
            if current_server.is_authoritative(query_domain):
                result = current_server.get_record(query_domain)
                print(f"[迭代查询] 找到权威记录: {result}")
                return result

            # 如果不是权威服务器，获取推荐的下一个服务器
            referral = current_server.get_referral(query_domain)
            if not referral:
                # 对于根服务器，直接查记录
                if isinstance(current_server, RootDNSServer):
                    tld = query_domain.split('.')[-1]
                    referral = current_server.get_record(tld)
                else:
                    print(f"[错误] 无法获取下一步推荐")
                    return None

            print(f"[迭代查询] 推荐查询 {referral}")

            # 找到下一个服务器
            next_server = None
            if referral in self.tld_servers.values():
                # 这里简化处理，实际应该根据 referral 名称查找
                tld = query_domain.split('.')[-1]
                next_server = self.tld_servers.get(tld)
            elif referral in self.authoritative_servers:
                next_server = self.authoritative_servers[referral]
            else:
                # 尝试在 TLD 服务器中查找
                for tld_server in self.tld_servers.values():
                    if tld_server.get_record(query_domain):
                        next_server = tld_server
                        break

                if not next_server:
                    # 尝试在权威服务器中查找
                    for auth_name, auth_server in self.authoritative_servers.items():
                        if auth_server.get_record(query_domain):
                            next_server = auth_server
                            break

            if not next_server:
                print(f"[错误] 无法找到下一个服务器: {referral}")
                return None

            current_server = next_server

        print(f"[错误] 查询步骤超过限制")
        return None

# 测试代码
if __name__ == "__main__":
    resolver = HierarchicalDNSResolver()

    print("=== 递归查询测试 ===")
    result1 = resolver.recursive_resolve("google.com")
    print(f"递归查询结果: {result1}\n")

    print("=== 迭代查询测试 ===")
    result2 = resolver.iterative_resolve("baidu.com")
    print(f"迭代查询结果: {result2}\n")

    print("=== 错误情况测试 ===")
    result3 = resolver.recursive_resolve("nonexistent-domain.xyz")
    print(f"不存在域名结果: {result3}")