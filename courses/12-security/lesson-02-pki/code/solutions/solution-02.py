#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
证书链验证解决方案
完整实现证书链的获取和验证
"""

import ssl
import socket


def get_certificate_chain(hostname, port=443):
    """获取服务器的完整证书链"""
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert_chain = ssock.getpeercert(chain=True)

    return cert_chain


def validate_certificate_chain(hostname):
    """验证证书链的基本属性"""
    print(f"验证 {hostname} 的证书链...")

    try:
        cert_chain = get_certificate_chain(hostname)

        if not cert_chain:
            print("❌ 无法获取证书链")
            return

        print(f"✅ 获取到 {len(cert_chain)} 个证书")

        # 验证每个证书
        for i, cert in enumerate(cert_chain):
            cert_type = "终端证书" if i == 0 else f"中间CA {i}"
            print(f"\n--- {cert_type} ---")

            subject = dict(x[0] for x in cert.get('subject', []))
            issuer = dict(x[0] for x in cert.get('issuer', []))

            print(f"主题: {subject.get('commonName', 'N/A')}")
            print(f"颁发者: {issuer.get('commonName', 'N/A')}")
            print(f"有效期: {cert.get('notBefore')} 到 {cert.get('notAfter')}")

            # 检查基本约束（简化版）
            extensions = cert.get('extensions', [])
            is_ca = any('basicConstraints' in ext[0].lower() and 'CA:TRUE' in ext[1]
                       for ext in extensions)

            if i == 0:
                status = "✅ 正确：终端证书不是CA" if not is_ca else "⚠️  警告：终端证书被标记为CA"
            else:
                status = "✅ 正确：CA证书具有CA权限" if is_ca else "⚠️  警告：CA证书缺少CA权限"
            print(status)

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

        result = "✅ 证书链验证成功！" if valid_chain else "❌ 证书链验证失败！"
        print(f"\n{result}")

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