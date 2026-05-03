#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X.509 证书分析示例
演示如何使用 Python 标准库解析和显示 X.509 证书信息
"""

import ssl
import socket
from datetime import datetime


def get_certificate_info(hostname, port=443):
    """
    获取并分析指定主机的 SSL/TLS 证书信息

    Args:
        hostname (str): 主机名
        port (int): 端口号，默认为 443 (HTTPS)

    Returns:
        dict: 包含证书详细信息的字典
    """
    # 创建 SSL 上下文
    context = ssl.create_default_context()

    # 连接到服务器并获取证书
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

    return cert


def display_certificate_info(cert):
    """显示证书的详细信息"""
    print("=== X.509 证书信息分析 ===\n")

    # 主题信息 (Subject)
    print("主题 (Subject):")
    for item in cert.get('subject', []):
        for key, value in item:
            print(f"  {key}: {value}")

    print("\n颁发者 (Issuer):")
    for item in cert.get('issuer', []):
        for key, value in item:
            print(f"  {key}: {value}")

    # 有效期
    not_before = cert.get('notBefore')
    not_after = cert.get('notAfter')
    print(f"\n有效期:")
    print(f"  开始时间: {not_before}")
    print(f"  结束时间: {not_after}")

    # 序列号
    serial_number = cert.get('serialNumber')
    if serial_number:
        print(f"\n序列号: {serial_number}")

    # 版本
    version = cert.get('version')
    if version:
        print(f"版本: v{version}")

    # 扩展信息
    extensions = cert.get('extensions', [])
    if extensions:
        print(f"\n扩展信息 ({len(extensions)} 个):")
        for ext in extensions:
            print(f"  {ext[0]}: {ext[1]}")


def main():
    """主函数 - 分析几个常见网站的证书"""
    websites = ['www.google.com', 'github.com', 'www.python.org']

    for website in websites:
        try:
            print(f"\n{'='*60}")
            print(f"分析网站: {website}")
            print(f"{'='*60}")

            cert = get_certificate_info(website)
            display_certificate_info(cert)

        except Exception as e:
            print(f"获取 {website} 的证书时出错: {e}")


if __name__ == "__main__":
    main()