#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: SSL/TLS 证书验证演示

本示例展示了：
1. 如何验证SSL/TLS证书的有效性
2. 证书链验证过程
3. 自签名证书的处理
"""

import ssl
import socket
import datetime
from urllib.parse import urlparse


def verify_ssl_certificate(hostname, port=443):
    """验证SSL/TLS证书"""
    print(f"=== 验证 {hostname} 的SSL证书 ===")

    try:
        # 创建SSL上下文
        context = ssl.create_default_context()

        # 连接到服务器并获取证书
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        # 解析证书信息
        print("✅ 证书验证成功！")
        print(f"主题: {cert['subject']}")
        print(f"颁发者: {cert['issuer']}")

        # 检查有效期
        not_before = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
        not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        now = datetime.datetime.now()

        print(f"有效期开始: {not_before}")
        print(f"有效期结束: {not_after}")

        if not_before <= now <= not_after:
            print("✅ 证书在有效期内")
        else:
            print("❌ 证书已过期或未生效")

        # 检查域名匹配
        if 'subjectAltName' in cert:
            san_list = [name[1] for name in cert['subjectAltName'] if name[0] == 'DNS']
            print(f"备用域名: {', '.join(san_list)}")

        return True

    except ssl.SSLCertVerificationError as e:
        print(f"❌ SSL证书验证失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False


def demonstrate_insecure_vs_secure():
    """演示安全与不安全的连接"""
    print("\n=== 安全 vs 不安全连接对比 ===")

    # 安全连接（验证证书）
    print("1. 安全连接 (验证证书):")
    secure_result = verify_ssl_certificate("www.google.com")

    # 不安全连接示例（仅用于演示，实际中不应这样做）
    print("\n2. 不安全连接 (跳过证书验证 - 仅演示用):")
    try:
        context = ssl._create_unverified_context()  # 不推荐！仅用于演示
        with socket.create_connection(("www.google.com", 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname="www.google.com") as ssock:
                print("⚠️  虽然连接成功，但跳过了证书验证！")
                print("⚠️  这可能导致中间人攻击！")
    except Exception as e:
        print(f"连接失败: {e}")


def check_cipher_suite(hostname, port=443):
    """检查使用的加密套件"""
    print(f"\n=== 检查 {hostname} 的加密套件 ===")

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cipher = ssock.cipher()
                protocol = ssock.version()

        print(f"协议版本: {protocol}")
        print(f"加密套件: {cipher[0]}")
        print(f"密钥长度: {cipher[2]} bits")

        # 简单的安全评估
        if protocol in ['TLSv1.2', 'TLSv1.3']:
            print("✅ 使用现代TLS协议")
        else:
            print("⚠️  使用较旧的协议版本")

        if 'AES' in cipher[0] or 'CHACHA20' in cipher[0]:
            print("✅ 使用强加密算法")
        else:
            print("⚠️  加密算法可能不够强")

    except Exception as e:
        print(f"❌ 获取加密套件失败: {e}")


if __name__ == "__main__":
    # 验证几个知名网站的SSL证书
    websites = ["www.google.com", "www.github.com", "www.cloudflare.com"]

    for website in websites:
        verify_ssl_certificate(website)
        check_cipher_suite(website)
        print("-" * 50)

    demonstrate_insecure_vs_secure()