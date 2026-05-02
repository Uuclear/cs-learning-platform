#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: Socket基础操作

演示如何使用Python socket库获取基本网络信息，
包括主机名、IP地址和常用服务端口号。
"""

import socket

def main():
    # 创建一个TCP socket (AF_INET = IPv4, SOCK_STREAM = TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 获取本地主机名
        hostname = socket.gethostname()
        print(f"本机主机名: {hostname}")

        # 获取本机IP地址（通过主机名解析）
        local_ip = socket.gethostbyname(hostname)
        print(f"本机IP地址: {local_ip}")

        # 获取常用网络服务的标准端口号
        services = ['http', 'https', 'ssh', 'ftp', 'smtp']
        for service in services:
            try:
                port = socket.getservbyname(service)
                print(f"{service.upper()}服务标准端口: {port}")
            except OSError:
                print(f"{service.upper()}服务端口信息不可用")

    finally:
        # 确保socket被正确关闭
        sock.close()

if __name__ == "__main__":
    main()