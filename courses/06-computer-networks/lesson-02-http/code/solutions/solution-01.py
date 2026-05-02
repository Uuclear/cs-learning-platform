#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: HTTP状态码识别

根据HTTP状态码返回对应的中文描述。
"""

def get_status_description(status_code):
    """
    根据HTTP状态码返回对应的中文描述

    Args:
        status_code (int): HTTP状态码

    Returns:
        str: 状态码的中文描述
    """
    status_descriptions = {
        200: "请求成功",
        201: "资源创建成功",
        301: "永久重定向",
        302: "临时重定向",
        400: "请求错误",
        401: "未授权",
        403: "禁止访问",
        404: "资源未找到",
        500: "服务器内部错误"
    }

    return status_descriptions.get(status_code, "未知状态码")


def main():
    """测试函数"""
    test_codes = [200, 201, 301, 302, 400, 401, 403, 404, 500, 999]

    for code in test_codes:
        description = get_status_description(code)
        print(f"状态码 {code}: {description}")


if __name__ == '__main__':
    main()