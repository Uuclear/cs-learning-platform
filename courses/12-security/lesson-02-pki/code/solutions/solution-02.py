#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
证书信息分析解决方案
使用 Python 标准库分析终端证书信息
"""

import ssl
import socket


def get_peer_certificate(hostname, port=443):
    """获取服务器的终端证书"""
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

    return cert


def validate_certificate_info(hostname):
    """验证证书的基本属性"""
    print(f"分析 {hostname} 的证书信息...")

    try:
        cert = get_peer_certificate(hostname)

        if not cert:
            print("❌ 无法获取证书")
            return

        print("✅ 获取到终端证书")

        # 验证证书的基本信息
        print(f"\n--- 终端证书 ---")

        subject = dict(x[0] for x in cert.get('subject', []))
        issuer = dict(x[0] for x in cert.get('issuer', []))

        print(f"主题: {subject.get('commonName', 'N/A')}")
        print(f"颁发者: {issuer.get('commonName', 'N/A')}")
        print(f"有效期: {cert.get('notBefore')} 到 {cert.get('notAfter')}")

        # 检查基本约束
        extensions = cert.get('extensions', [])
        is_ca = any('basicConstraints' in ext[0].lower() and 'CA:TRUE' in ext[1]
                   for ext in extensions)

        status = "✅ 正确：终端证书不是CA" if not is_ca else "⚠️  警告：终端证书被标记为CA"
        print(status)

        print("\n💡 注意：Python 标准库无法获取完整的证书链")
        print("   完整的证书链验证需要使用 OpenSSL 或其他工具")

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