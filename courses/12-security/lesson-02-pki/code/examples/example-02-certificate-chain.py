#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
证书链验证示例（使用标准库）
演示如何使用 Python 标准库验证证书链
"""

import ssl
import socket
from urllib.parse import urlparse


def get_peer_certificate(hostname, port=443):
    """
    获取服务器的终端证书（标准库限制：无法获取完整证书链）

    Args:
        hostname (str): 主机名
        port (int): 端口号

    Returns:
        dict: 终端证书信息
    """
    context = ssl.create_default_context()

    # 获取终端证书
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

    return cert


def validate_certificate_info(hostname):
    """
    验证证书的基本属性（由于标准库限制，只能验证终端证书）

    Args:
        hostname (str): 要验证的主机名
    """
    print(f"分析 {hostname} 的证书信息...")

    try:
        cert = get_peer_certificate(hostname)

        if not cert:
            print("❌ 无法获取证书")
            return

        print("✅ 获取到终端证书")

        # 验证证书的基本信息
        print(f"\n--- 终端证书 ---")

        # 获取主题信息
        subject = dict(x[0] for x in cert.get('subject', []))
        issuer = dict(x[0] for x in cert.get('issuer', []))

        print(f"主题: {subject.get('commonName', 'N/A')}")
        print(f"颁发者: {issuer.get('commonName', 'N/A')}")

        # 检查有效期
        not_before = cert.get('notBefore')
        not_after = cert.get('notAfter')
        print(f"有效期: {not_before} 到 {not_after}")

        # 检查是否为CA证书（通过基本约束扩展）
        extensions = cert.get('extensions', [])
        is_ca = False
        for ext_name, ext_value in extensions:
            if 'basicConstraints' in ext_name.lower() and 'CA:TRUE' in ext_value:
                is_ca = True
                break

        if not is_ca:
            print("✅ 正确：终端证书不是CA")
        else:
            print("⚠️  警告：终端证书被标记为CA")

        # 注意：标准库无法获取完整证书链，因此无法验证链的完整性
        print("\n💡 注意：Python 标准库无法获取完整的证书链")
        print("   完整的证书链验证需要使用 OpenSSL 或其他工具")
        print("   实际应用中，Web 服务器应配置完整的证书链")

    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")


def main():
    """主函数"""
    websites = ['github.com', 'www.python.org']

    for website in websites:
        print(f"\n{'='*60}")
        validate_certificate_info(website)
        print(f"{'='*60}")


if __name__ == "__main__":
    main()