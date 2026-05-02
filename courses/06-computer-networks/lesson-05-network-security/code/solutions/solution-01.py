#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: 实现简单的密码强度检查器

要求：
- 检查密码长度是否至少8位
- 检查是否包含大写字母、小写字母、数字和特殊字符
- 返回密码强度评分（0-4分）
"""

import re


def check_password_strength(password):
    """检查密码强度"""
    score = 0

    # 检查长度
    if len(password) >= 8:
        score += 1

    # 检查是否包含大写字母
    if re.search(r'[A-Z]', password):
        score += 1

    # 检查是否包含小写字母
    if re.search(r'[a-z]', password):
        score += 1

    # 检查是否包含数字
    if re.search(r'\d', password):
        score += 1

    # 检查是否包含特殊字符
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1

    return score


def get_strength_label(score):
    """根据分数返回强度标签"""
    if score <= 1:
        return "很弱"
    elif score == 2:
        return "弱"
    elif score == 3:
        return "中等"
    elif score == 4:
        return "强"
    else:
        return "很强"


if __name__ == "__main__":
    test_passwords = [
        "123456",
        "password",
        "Password123",
        "Password123!",
        "MySecureP@ssw0rd2026!"
    ]

    for pwd in test_passwords:
        score = check_password_strength(pwd)
        label = get_strength_label(score)
        print(f"密码: {pwd} -> 强度: {score}/5 ({label})")