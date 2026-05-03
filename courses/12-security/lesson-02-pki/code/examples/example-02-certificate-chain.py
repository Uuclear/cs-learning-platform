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


def validate_certificate_chain(hostname):
    """
    验证证书链的基本属性

    Args:
        hostname (str): 要验证的主机名
    """
    print(f"验证 {hostname} 的证书链...")

    try:
        cert_chain = get_certificate_chain(hostname)

        if not cert_chain:
            print("❌ 无法获取证书链")
            return

        print(f"✅ 获取到 {len(cert_chain)} 个证书")

        # 验证每个证书的基本信息
        for i, cert in enumerate(cert_chain):
            cert_type = "终端证书" if i == 0 else f"中间CA {i}"
            print(f"\n--- {cert_type} ---")

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

            if i == 0:  # 终端证书
                if not is_ca:
                    print("✅ 正确：终端证书不是CA")
                else:
                    print("⚠️  警告：终端证书被标记为CA")
            else:  # CA证书
                if is_ca:
                    print("✅ 正确：CA证书具有CA权限")
                else:
                    print("⚠️  警告：CA证书缺少CA权限")

        # 验证证书链链接
        print(f"\n--- 证书链链接验证 ---")
        valid_chain = True

        for i in range(len(cert_chain) - 1):
            current_cert = cert_chain[i]
            next_cert = cert_chain[i + 1]

            current_issuer = dict(x[0] for x in current_cert.get('issuer', []))
            next_subject = dict(x[0] for x in next_cert.get('subject', []))

            current_issuer_cn = current_issuer.get('commonName', '')
            next_subject_cn = next_subject.get('commonName', '')

            if current_issuer_cn == next_subject_cn:
                print(f"✅ 证书 {i} -> 证书 {i+1}: {current_issuer_cn}")
            else:
                print(f"❌ 证书链断裂: {current_issuer_cn} != {next_subject_cn}")
                valid_chain = False

        if valid_chain:
            print("\n✅ 证书链验证成功！")
        else:
            print("\n❌ 证书链验证失败！")

    except Exception as e:
        print(f"❌ 验证过程中出错: {e}")


def main():
    """主函数"""
    websites = ['www.google.com', 'github.com']

    for website in websites:
        print(f"\n{'='*60}")
        validate_certificate_chain(website)
        print(f"{'='*60}")


if __name__ == "__main__":
    main()