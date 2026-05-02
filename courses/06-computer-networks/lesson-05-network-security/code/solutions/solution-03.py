#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答: 实现简单的HTTPS客户端安全检查

要求：
- 检查网站是否支持HTTPS
- 验证SSL证书的有效性
- 检查是否使用安全的加密套件
- 返回安全评分（0-3分）
"""

import ssl
import socket
import datetime
from urllib.parse import urlparse


def check_https_security(url):
    """检查HTTPS安全性"""
    # 解析URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname or parsed_url.path
    port = parsed_url.port or 443

    score = 0
    issues = []

    try:
        # 创建安全的SSL上下文
        context = ssl.create_default_context()

        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                protocol = ssock.version()

        # 检查1: 证书有效性 (1分)
        not_before = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
        not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        now = datetime.datetime.now()

        if not_before <= now <= not_after:
            score += 1
        else:
            issues.append("证书已过期或未生效")

        # 检查2: 使用现代TLS协议 (1分)
        if protocol in ['TLSv1.2', 'TLSv1.3']:
            score += 1
        else:
            issues.append(f"使用较旧的协议: {protocol}")

        # 检查3: 强加密套件 (1分)
        cipher_name = cipher[0].upper()
        if any(weak in cipher_name for weak in ['RC4', 'DES', '3DES', 'MD5', 'SHA1']):
            issues.append(f"使用弱加密算法: {cipher_name}")
        elif 'AES' in cipher_name or 'CHACHA20' in cipher_name:
            score += 1
        else:
            issues.append(f"加密算法安全性未知: {cipher_name}")

        return {
            'score': score,
            'max_score': 3,
            'issues': issues,
            'protocol': protocol,
            'cipher': cipher_name,
            'cert_valid': not_before <= now <= not_after
        }

    except ssl.SSLCertVerificationError:
        issues.append("SSL证书验证失败")
        return {'score': 0, 'max_score': 3, 'issues': issues, 'error': '证书验证失败'}
    except ssl.SSLError as e:
        issues.append(f"SSL错误: {str(e)}")
        return {'score': 0, 'max_score': 3, 'issues': issues, 'error': str(e)}
    except Exception as e:
        issues.append(f"连接错误: {str(e)}")
        return {'score': 0, 'max_score': 3, 'issues': issues, 'error': str(e)}


def get_security_rating(score, max_score):
    """根据分数返回安全评级"""
    percentage = (score / max_score) * 100
    if percentage >= 80:
        return "优秀"
    elif percentage >= 60:
        return "良好"
    elif percentage >= 40:
        return "一般"
    else:
        return "较差"


if __name__ == "__main__":
    test_urls = [
        "google.com",
        "github.com",
        "cloudflare.com",
        "example.com"
    ]

    for url in test_urls:
        print(f"\n=== 检查 {url} ===")
        result = check_https_security(url)

        if 'error' in result:
            print(f"❌ 安全检查失败: {result['error']}")
        else:
            rating = get_security_rating(result['score'], result['max_score'])
            print(f"安全评分: {result['score']}/{result['max_score']} ({rating})")
            print(f"协议版本: {result['protocol']}")
            print(f"加密套件: {result['cipher']}")

            if result['issues']:
                print("发现的问题:")
                for issue in result['issues']:
                    print(f"  - {issue}")
            else:
                print("✅ 未发现安全问题")