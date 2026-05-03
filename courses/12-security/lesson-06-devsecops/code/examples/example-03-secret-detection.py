#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3: 敏感信息（密钥）检测模拟器

这个脚本模拟了密钥检测工具的功能，
用于在代码、配置文件和日志中检测意外提交的敏感信息。
"""

import re
import base64
from typing import List, Dict, Tuple


def detect_api_keys(content: str) -> List[Tuple[int, str, str]]:
    """
    检测各种API密钥模式

    参数:
        content: 要扫描的文本内容

    返回:
        包含 (行号, 密钥类型, 密钥片段) 的元组列表
    """
    detections = []
    lines = content.split('\n')

    # 常见API密钥模式
    api_key_patterns = {
        'AWS_ACCESS_KEY': r'(?i)(aws_access_key_id|accesskeyid)[\s]*[=:][\s]*[\'"]?([A-Z0-9]{20})[\'"]?',
        'AWS_SECRET_KEY': r'(?i)(aws_secret_access_key|secretaccesskey)[\s]*[=:][\s]*[\'"]?([A-Za-z0-9/+=]{40})[\'"]?',
        'GITHUB_TOKEN': r'(?i)(github_token|github_pat)[\s]*[=:][\s]*[\'"]?([A-Za-z0-9_]{40,255})[\'"]?',
        'STRIPE_KEY': r'(?i)(stripe.*key)[\s]*[=:][\s]*[\'"]?(sk_test_[A-Za-z0-9]{24}|sk_live_[A-Za-z0-9]{24})[\'"]?',
        'SLACK_TOKEN': r'(?i)(xox[baprs]-[A-Za-z0-9-]+)',
        'JWT_TOKEN': r'(?i)(ey[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)',
    }

    for line_num, line in enumerate(lines, 1):
        for key_type, pattern in api_key_patterns.items():
            matches = re.findall(pattern, line)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        # 提取实际的密钥值（通常是第二个组）
                        secret_value = match[1] if len(match) > 1 else match[0]
                    else:
                        secret_value = match

                    # 只显示密钥的前几个和后几个字符，隐藏中间部分
                    if len(secret_value) > 8:
                        masked = secret_value[:4] + "..." + secret_value[-4:]
                    else:
                        masked = secret_value[:2] + "..." + secret_value[-2:] if len(secret_value) > 4 else "..."

                    detections.append((line_num, key_type, masked))

    return detections


def detect_passwords(content: str) -> List[Tuple[int, str]]:
    """
    检测硬编码密码

    参数:
        content: 要扫描的文本内容

    返回:
        包含 (行号, 密码片段) 的元组列表
    """
    detections = []
    lines = content.split('\n')

    password_patterns = [
        r'(?i)password[\s]*[=:][\s]*[\'"]([^\'"]{6,})[\'"]',
        r'(?i)passwd[\s]*[=:][\s]*[\'"]([^\'"]{6,})[\'"]',
        r'(?i)pwd[\s]*[=:][\s]*[\'"]([^\'"]{6,})[\'"]',
    ]

    for line_num, line in enumerate(lines, 1):
        for pattern in password_patterns:
            matches = re.findall(pattern, line)
            if matches:
                for password in matches:
                    # 隐藏大部分密码内容
                    if len(password) > 6:
                        masked = password[:2] + "..." + password[-2:]
                    else:
                        masked = "******"
                    detections.append((line_num, masked))

    return detections


def detect_private_keys(content: str) -> List[Tuple[int, str]]:
    """
    检测私钥文件内容

    参数:
        content: 要扫描的文本内容

    返回:
        包含 (行号, 密钥类型) 的元组列表
    """
    detections = []
    lines = content.split('\n')

    private_key_indicators = [
        '-----BEGIN RSA PRIVATE KEY-----',
        '-----BEGIN PRIVATE KEY-----',
        '-----BEGIN OPENSSH PRIVATE KEY-----',
        '-----BEGIN DSA PRIVATE KEY-----',
        '-----BEGIN EC PRIVATE KEY-----',
    ]

    for line_num, line in enumerate(lines, 1):
        for indicator in private_key_indicators:
            if indicator in line:
                key_type = indicator.replace('-----BEGIN ', '').replace(' PRIVATE KEY-----', '')
                detections.append((line_num, key_type))

    return detections


def scan_file_content(content: str, filename: str = "unknown") -> Dict[str, List]:
    """
    扫描文件内容中的所有敏感信息

    参数:
        content: 文件内容
        filename: 文件名（用于报告）

    返回:
        包含各种检测结果的字典
    """
    results = {
        'api_keys': detect_api_keys(content),
        'passwords': detect_passwords(content),
        'private_keys': detect_private_keys(content)
    }
    return results


def main():
    """主函数：演示密钥检测"""
    print("=== 敏感信息（密钥）检测模拟器 ===")

    # 模拟包含敏感信息的代码片段
    sample_content = '''
# 配置文件示例
DATABASE_URL = "postgresql://user:mysecretpassword123@localhost/mydb"
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# API密钥
GITHUB_TOKEN = "ghp_abcdefghijklmnopqrstuvwxyz1234567890ABCD"
STRIPE_SECRET_KEY = "sk_test_abcdefghijklmnopqrstuvwxyz1234"

# 私钥示例
PRIVATE_KEY_CONTENT = """
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAxyz...
-----END RSA PRIVATE KEY-----
"""

# 环境变量（危险！）
os.environ["SECRET_KEY"] = "super-secret-key-12345"
'''

    print(f"\n正在扫描示例内容...")

    results = scan_file_content(sample_content)

    total_detections = 0
    detection_details = []

    # 处理API密钥
    if results['api_keys']:
        print(f"\n发现 {len(results['api_keys'])} 个API密钥:")
        for line_num, key_type, masked_value in results['api_keys']:
            print(f"  行 {line_num}: {key_type} = {masked_value}")
            detection_details.append(f"API密钥 ({key_type})")
            total_detections += 1

    # 处理密码
    if results['passwords']:
        print(f"\n发现 {len(results['passwords'])} 个硬编码密码:")
        for line_num, masked_password in results['passwords']:
            print(f"  行 {line_num}: 密码 = {masked_password}")
            detection_details.append("硬编码密码")
            total_detections += 1

    # 处理私钥
    if results['private_keys']:
        print(f"\n发现 {len(results['private_keys'])} 个私钥:")
        for line_num, key_type in results['private_keys']:
            print(f"  行 {line_num}: {key_type} 私钥")
            detection_details.append(f"私钥 ({key_type})")
            total_detections += 1

    if total_detections == 0:
        print("\n✅ 未发现敏感信息！")
    else:
        print(f"\n⚠️  发现 {total_detections} 个敏感信息泄露风险")
        print("建议：")
        print("  1. 使用环境变量或密钥管理服务存储敏感信息")
        print("  2. 在CI/CD管道中集成密钥扫描工具")
        print("  3. 将敏感文件添加到.gitignore")
        print("  4. 定期轮换已泄露的密钥")


if __name__ == "__main__":
    main()