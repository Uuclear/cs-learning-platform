#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 发送HTTP请求

这个脚本演示如何使用requests库发送HTTP GET请求，
并解析响应的状态码、头部和内容。
"""

import requests


def main():
    """主函数：发送HTTP请求并显示结果"""
    # 发送GET请求获取网页内容
    response = requests.get('https://httpbin.org/get')

    # 打印状态码和响应内容
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"响应内容: {response.json()}")


if __name__ == '__main__':
    main()