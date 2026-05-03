#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CA 签名模拟示例（使用标准库概念演示）
由于 Python 标准库不支持证书生成，此示例演示 CA 签名的概念和流程
"""

import ssl
import socket
from datetime import datetime


def demonstrate_ca_signing_concept():
    """
    演示 CA 签名的概念和流程
    注意：Python 标准库无法生成 X.509 证书，此为概念演示
    """
    print("=== CA 签名流程概念演示 ===\n")

    print("1. 证书签名请求 (CSR) 创建")
    print("   - 实体生成密钥对（私钥 + 公钥）")
    print("   - 实体创建 CSR，包含公钥和身份信息")
    print("   - CSR 使用私钥签名以证明拥有权\n")

    print("2. CA 验证过程")
    print("   - CA 验证申请者的身份")
    print("   - CA 检查 CSR 的签名有效性")
    print("   - CA 确认申请者拥有对应的私钥\n")

    print("3. CA 签名证书")
    print("   - CA 使用自己的私钥对证书进行签名")
    print("   - 证书包含：主题信息、公钥、有效期、扩展等")
    print("   - 签名确保证书内容的完整性和真实性\n")

    print("4. 证书分发和使用")
    print("   - 实体接收签名后的证书")
    print("   - 在 TLS 握手等场景中提供证书")
    print("   - 客户端使用 CA 公钥验证证书签名\n")


def show_real_certificate_structure():
    """展示真实证书的结构信息"""
    print("\n=== 真实 X.509 证书结构 ===\n")

    try:
        # 获取一个真实证书来展示结构
        hostname = "www.python.org"
        context = ssl.create_default_context()

        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        print("证书字段说明：")
        print("- subject: 证书持有者身份信息")
        print("- issuer: 证书颁发者身份信息")
        print("- version: X.509 版本号")
        print("- serialNumber: 证书序列号（唯一标识）")
        print("- notBefore/notAfter: 证书有效期")
        print("- subjectAltName: 主题备用名称（支持多个域名）")
        print("- extensions: 扩展字段（如基本约束、密钥用途等）\n")

        # 显示实际证书信息
        print(f"实际证书示例 ({hostname}):")
        subject = dict(x[0] for x in cert.get('subject', []))
        issuer = dict(x[0] for x in cert.get('issuer', []))

        print(f"  主题: {subject.get('commonName', 'N/A')}")
        print(f"  颁发者: {issuer.get('commonName', 'N/A')}")
        print(f"  序列号: {cert.get('serialNumber', 'N/A')}")
        print(f"  有效期: {cert.get('notBefore')} 到 {cert.get('notAfter')}")

    except Exception as e:
        print(f"获取真实证书信息时出错: {e}")


def explain_trust_chain():
    """解释信任链的工作原理"""
    print("\n=== 信任链工作原理 ===\n")

    print("信任链建立过程：")
    print("1. 浏览器/操作系统内置受信任的根 CA 证书")
    print("2. 根 CA 可以直接签发终端证书，或签发中间 CA")
    print("3. 中间 CA 可以签发更多的中间 CA 或终端证书")
    print("4. 验证时从终端证书向上追溯到受信任的根 CA\n")

    print("证书路径验证步骤：")
    print("✓ 验证每个证书的签名（使用上级证书的公钥）")
    print("✓ 检查所有证书是否在有效期内")
    print("✓ 验证基本约束（CA 证书必须有 CA 权限）")
    print("✓ 检查密钥用途是否符合预期")
    print("✓ 确认根证书在受信任的根存储中\n")


def main():
    """主函数"""
    demonstrate_ca_signing_concept()
    show_real_certificate_structure()
    explain_trust_chain()

    print("\n💡 注意：完整的证书生成需要使用专门的库如 OpenSSL 或 cryptography")
    print("   Python 标准库主要用于证书验证和 TLS 通信")


if __name__ == "__main__":
    main()