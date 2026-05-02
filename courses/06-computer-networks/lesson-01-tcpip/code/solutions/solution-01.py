#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: 网络信息查询工具

查询指定域名的IP地址，并显示本地主机的基本网络信息。
"""

import socket
import sys

def get_local_info():
    """获取本地主机信息"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return hostname, local_ip
    except socket.error as e:
        return "未知", "无法获取本地IP"

def get_domain_ip(domain):
    """查询域名的IP地址"""
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return f"错误：无法解析域名 '{domain}'"

def main():
    # 获取本地信息
    hostname, local_ip = get_local_info()
    print(f"=== 本地主机信息 ===")
    print(f"主机名: {hostname}")
    print(f"IP地址: {local_ip}")
    print()

    # 查询域名（如果没有提供命令行参数，则使用默认域名）
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = "google.com"

    print(f"=== 域名查询: {domain} ===")
    ip_result = get_domain_ip(domain)
    print(f"IP地址: {ip_result}")

if __name__ == "__main__":
    main()