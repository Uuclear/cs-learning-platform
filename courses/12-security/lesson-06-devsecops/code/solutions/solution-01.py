#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1: 改进的SAST模拟器

这个脚本展示了如何修复示例中的安全漏洞，
并提供更安全的代码实现。
"""

import re
from typing import List, Dict, Tuple


def detect_sql_injection_safe(code_lines: List[str]) -> List[Tuple[int, str]]:
    """
    使用参数化查询的安全SQL实现检测
    """
    vulnerabilities = []
    # 检测不安全的字符串拼接
    unsafe_patterns = [
        r"SELECT.*FROM.*WHERE.*\+.*",
        r"execute\([^)]*\+\s*[^\)]*\)",
    ]

    for line_num, line in enumerate(code_lines, 1):
        for pattern in unsafe_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                vulnerabilities.append((line_num, "应使用参数化查询代替字符串拼接"))
                break

    return vulnerabilities


def suggest_fixes(vulnerabilities: List[Tuple[int, str]]) -> Dict[int, str]:
    """
    为检测到的漏洞提供修复建议
    """
    fixes = {}
    for line_num, description in vulnerabilities:
        if "SQL注入" in description:
            fixes[line_num] = "使用参数化查询：cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"
        elif "XSS" in description:
            fixes[line_num] = "使用textContent或HTML转义：element.textContent = msg"
        elif "硬编码" in description:
            fixes[line_num] = "使用环境变量：api_key = os.environ.get('API_KEY')"

    return fixes


# 安全的示例代码
SAFE_CODE_EXAMPLE = '''
def get_user_data_safe(user_id):
    # 安全：使用参数化查询
    query = "SELECT * FROM users WHERE id = %s"
    result = db.execute(query, (user_id,))
    return result

def display_message_safe(msg):
    # 安全：使用textContent
    element.textContent = msg

def connect_to_api_safe():
    # 安全：从环境变量获取密钥
    import os
    api_key = os.environ.get("API_KEY")
    return api_client.connect(api_key)
'''