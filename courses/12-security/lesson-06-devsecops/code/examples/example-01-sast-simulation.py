#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1: 静态应用安全测试 (SAST) 模拟器

这个脚本模拟了静态应用安全测试工具的基本功能，
用于在不运行代码的情况下分析源代码中的安全漏洞。
"""

import re
import sys
from typing import List, Dict, Tuple


def detect_sql_injection(code_lines: List[str]) -> List[Tuple[int, str]]:
    """
    检测 SQL 注入漏洞

    参数:
        code_lines: 源代码行列表

    返回:
        包含漏洞信息的元组列表 (行号, 描述)
    """
    vulnerabilities = []
    sql_patterns = [
        r"SELECT.*FROM.*WHERE.*\+.*",  # 字符串拼接的SQL查询
        r"execute\([^)]*\+\s*[^\)]*\)",  # execute方法中的字符串拼接
        r"query\([^)]*\+\s*[^\)]*\)",   # query方法中的字符串拼接
    ]

    for line_num, line in enumerate(code_lines, 1):
        for pattern in sql_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                vulnerabilities.append((line_num, "发现潜在的SQL注入漏洞：使用字符串拼接构建SQL查询"))
                break

    return vulnerabilities


def detect_xss(code_lines: List[str]) -> List[Tuple[int, str]]:
    """
    检测跨站脚本 (XSS) 漏洞

    参数:
        code_lines: 源代码行列表

    返回:
        包含漏洞信息的元组列表 (行号, 描述)
    """
    vulnerabilities = []
    xss_patterns = [
        r"innerHTML\s*=\s*[^;]*",  # 直接设置innerHTML
        r"outerHTML\s*=\s*[^;]*",  # 直接设置outerHTML
        r"eval\([^)]*\)",  # 使用eval函数
    ]

    for line_num, line in enumerate(code_lines, 1):
        for pattern in xss_patterns:
            if re.search(pattern, line):
                vulnerabilities.append((line_num, "发现潜在的XSS漏洞：直接输出用户输入到HTML中"))
                break

    return vulnerabilities


def detect_hardcoded_secrets(code_lines: List[str]) -> List[Tuple[int, str]]:
    """
    检测硬编码的敏感信息

    参数:
        code_lines: 源代码行列表

    返回:
        包含漏洞信息的元组列表 (行号, 描述)
    """
    vulnerabilities = []
    secret_patterns = [
        r"password\s*=\s*[\"'][^\"']{4,}[\"']",  # 硬编码密码
        r"api_key\s*=\s*[\"'][A-Za-z0-9_\-]{20,}[\"']",  # API密钥
        r"secret\s*=\s*[\"'][^\"']{10,}[\"']",  # 通用密钥
    ]

    for line_num, line in enumerate(code_lines, 1):
        for pattern in secret_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                vulnerabilities.append((line_num, "发现硬编码的敏感信息：不应在代码中存储凭证"))
                break

    return vulnerabilities


def analyze_code(file_content: str) -> Dict[str, List[Tuple[int, str]]]:
    """
    分析代码并返回所有检测到的漏洞

    参数:
        file_content: 文件内容字符串

    返回:
        按漏洞类型分类的漏洞字典
    """
    code_lines = file_content.split('\n')

    results = {
        'sql_injection': detect_sql_injection(code_lines),
        'xss': detect_xss(code_lines),
        'hardcoded_secrets': detect_hardcoded_secrets(code_lines)
    }

    return results


def main():
    """主函数：演示SAST模拟器的使用"""
    # 示例代码片段
    sample_code = '''
def get_user_data(user_id):
    # 危险：SQL注入漏洞
    query = "SELECT * FROM users WHERE id = " + user_id
    result = db.execute(query)
    return result

def display_message(msg):
    # 危险：XSS漏洞
    element.innerHTML = msg

def connect_to_api():
    # 危险：硬编码密钥
    api_key = "sk-1234567890abcdef1234567890abcdef"
    return api_client.connect(api_key)
'''

    print("=== 静态应用安全测试 (SAST) 模拟器 ===")
    print("\n正在分析示例代码...")

    results = analyze_code(sample_code)

    total_vulnerabilities = 0
    for vuln_type, vulnerabilities in results.items():
        if vulnerabilities:
            print(f"\n{vuln_type} 漏洞 ({len(vulnerabilities)} 个):")
            for line_num, description in vulnerabilities:
                print(f"  行 {line_num}: {description}")
                total_vulnerabilities += 1

    if total_vulnerabilities == 0:
        print("\n✅ 未发现安全漏洞！")
    else:
        print(f"\n⚠️  发现 {total_vulnerabilities} 个潜在安全漏洞")
        print("建议：在CI/CD管道中集成SAST工具进行自动化安全扫描")


if __name__ == "__main__":
    main()